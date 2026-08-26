/* option-chain.js — chaîne d'options enrichie réutilisable (§16, foundation).
 *
 * C.optionChainTable(host, {contracts, spot, sym, source, timestamp, mode})
 *   Tableau triable/filtrable des MEILLEURS contrats du board (shortlist, pas la
 *   grille intégrale strikes×échéances). Colonnes RÉELLES : type, strike, DTE,
 *   delta/gamma/theta/vega, IV, prime, break-even, OI, volume, PoP, qualité +
 *   colonnes CALCULÉES honnêtes : risque max (= prime payée) et rendement/risque
 *   (depuis swing_ret réel du moteur). Greeks = MODÈLE Black-Scholes (étiqueté),
 *   pas des greeks broker. « — » honnête si un champ manque. Lecture seule.
 *
 * C.bestContractBubble(host, {contracts, spot, ...})
 *   Nuage prime × DTE, rayon = qualité/PoP : repère le meilleur équilibre
 *   potentiel / échéance / risque. Couleur = CALL vert / PUT violet.
 */
(function () {
  var C = window.VXCharts, VX = window.VX;
  function esc(s) { return String(s == null ? '' : s).replace(/[<>&"]/g, function (c) { return { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]; }); }
  function nd(v, d) { return (v == null || v === '' || (typeof v === 'number' && !isFinite(v))) ? '—' : VX.fmt.num(+v, d == null ? 2 : d); }

  /* Colonnes : [clé, libellé, décimales, formateur?]. Les greeks/IV/prime/BE sont
     RÉELS (ou modèle pour les greeks) ; risque max & R:R sont dérivés du contrat. */
  var COLS = [
    { k: 'type', label: 'Type', cls: '' },
    { k: 'strike', label: 'Strike', num: true, d: 2 },
    { k: 'dte', label: 'DTE', num: true, fmt: function (c) { return c.dte != null ? c.dte + ' j' : '—'; } },
    { k: 'delta', label: 'Δ', num: true, d: 2 },
    { k: 'gamma', label: 'Γ', num: true, d: 3 },
    { k: 'theta', label: 'Θ', num: true, d: 2 },
    { k: 'vega', label: 'V', num: true, d: 2 },
    { k: 'iv', label: 'IV', num: true, fmt: function (c) { return c.iv != null ? VX.fmt.num(c.iv, 0) + ' %' : '—'; } },
    { k: 'mid', label: 'Prime', num: true, fmt: function (c) { var m = c.mid != null ? c.mid : c.premium; return m != null ? VX.fmt.num(m, 2) : '—'; } },
    { k: 'be', label: 'Seuil', num: true, d: 2, title: 'Break-even (seuil de rentabilité à l\'échéance)' },
    { k: 'risk', label: 'Risque max', num: true, fmt: function (c) { return c.cost != null ? VX.fmt.price(c.cost) + ' $' : '—'; }, title: 'Prime payée = perte maximale d\'un achat' },
    { k: 'swing_ret', label: 'Rendt', num: true, fmt: function (c) { return c.swing_ret != null ? '+' + VX.fmt.num(c.swing_ret, 0) + ' %' : '—'; }, title: 'Rendement potentiel du contrat si le sous-jacent atteint la cible (net/prime, moteur swing)' },
    { k: 'oi', label: 'OI', num: true, d: 0 },
    { k: 'vol', label: 'Vol', num: true, d: 0 },
    { k: 'pop', label: 'PoP', num: true, fmt: function (c) { return c.pop != null ? c.pop + ' %' : '—'; }, title: 'Probabilité de profit (modèle lognormal)' },
    { k: 'quality', label: 'Qualité', num: true, d: 0 },
  ];

  C.optionChainTable = function (host, opts) {
    var el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return;
    var all = (opts.contracts || []).filter(function (c) { return c && c.strike != null; });
    el.classList.add('vx-card');
    if (!all.length) {
      el.innerHTML = '<div class="vx-card-header"><span class="vx-card-title">Chaîne — meilleurs contrats</span></div>'
        + VX.states.empty('Aucun contrat exploitable au tableau pour ' + esc(opts.sym || '') + ' (IBKR hors ligne ou titre sans options liquides).');
      return;
    }
    var exps = [];
    all.forEach(function (c) { if (c.exp && exps.indexOf(c.exp) < 0) exps.push(c.exp); });
    exps.sort();
    var state = { type: '', exp: '', sort: 'quality', dir: -1 };

    function paint() {
      var rows = all.filter(function (c) {
        return (!state.type || String(c.type).toUpperCase() === state.type)
          && (!state.exp || c.exp === state.exp);
      });
      rows.sort(function (a, b) {
        var av = a[state.sort], bv = b[state.sort];
        if (av == null) return 1; if (bv == null) return -1;
        return (av - bv) * state.dir;
      });
      var head = COLS.map(function (col) {
        var on = state.sort === col.k;
        return '<th class="' + (col.num ? 'vx-num' : '') + '" data-oc-sort="' + col.k + '" style="cursor:pointer;white-space:nowrap"'
          + (col.title ? ' title="' + esc(col.title) + '"' : '') + '>' + col.label + (on ? (state.dir < 0 ? ' ↓' : ' ↑') : '') + '</th>';
      }).join('');
      var bodyRows = rows.map(function (c) {
        var isPut = String(c.type).toUpperCase() === 'PUT';
        return '<tr>' + COLS.map(function (col) {
          var val;
          if (col.k === 'type') val = '<span class="vx-badge" style="color:var(--vx-' + (isPut ? 'option' : 'positive') + ')">' + esc(c.type || '') + '</span>';
          else if (col.fmt) val = col.fmt(c);
          else val = nd(c[col.k], col.d);
          return '<td class="' + (col.num ? 'vx-num vx-mono' : '') + '">' + val + '</td>';
        }).join('') + '</tr>';
      }).join('');
      el.querySelector('[data-oc-body]').innerHTML =
        '<div class="vx-datagrid" style="max-height:none"><table class="vx-table"><thead><tr>' + head + '</tr></thead><tbody>' + bodyRows + '</tbody></table></div>'
        + '<div class="vx-meta vx-mt1">' + rows.length + ' contrat(s) · ' + (state.type || 'CALL & PUT') + (state.exp ? ' · éch. ' + esc(state.exp) : '') + '</div>';
      el.querySelectorAll('[data-oc-sort]').forEach(function (th) {
        th.addEventListener('click', function () {
          var k = th.getAttribute('data-oc-sort');
          if (state.sort === k) state.dir = -state.dir; else { state.sort = k; state.dir = -1; }
          paint();
        });
      });
    }
    var typeChips = [['', 'Tout'], ['CALL', 'Calls'], ['PUT', 'Puts']].map(function (t) {
      return '<button class="vx-chip" data-oc-type="' + t[0] + '" aria-pressed="' + (state.type === t[0]) + '">' + t[1] + '</button>';
    }).join('');
    var expSel = exps.length > 1 ? '<select class="vx-select" data-oc-exp style="width:auto"><option value="">Toutes échéances</option>'
      + exps.map(function (e) { return '<option value="' + esc(e) + '">' + esc(e) + '</option>'; }).join('') + '</select>' : '';
    el.innerHTML =
      '<div class="vx-card-header"><span class="vx-card-title">Chaîne — meilleurs contrats' + (opts.sym ? ' · ' + esc(opts.sym) : '') + '</span>'
      + '<span class="vx-chart-question">Quels contrats offrent le meilleur équilibre potentiel / échéance / risque ?</span>'
      + '<span class="vx-actions vx-flex" style="gap:.3rem">' + typeChips + expSel + '</span></div>'
      + '<div data-oc-body></div>'
      + '<div class="vx-chart-foot">' + VX.updateIndicator(opts.timestamp, opts.source || 'board options', opts.mode || 'delayed')
      + '<span class="vx-meta">Shortlist des meilleurs contrats (pas la chaîne intégrale) · greeks = modèle Black-Scholes, pas broker · risque max = prime payée · lecture seule.</span></div>';
    el.querySelectorAll('[data-oc-type]').forEach(function (b) {
      b.addEventListener('click', function () {
        state.type = b.getAttribute('data-oc-type');
        el.querySelectorAll('[data-oc-type]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        paint();
      });
    });
    var es = el.querySelector('[data-oc-exp]');
    if (es) es.addEventListener('change', function () { state.exp = this.value; paint(); });
    paint();
  };

  /* Nuage prime × DTE : repère visuellement le meilleur équilibre. */
  C.bestContractBubble = function (host, opts) {
    var el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return;
    var cs = (opts.contracts || []).filter(function (c) {
      return c && c.dte != null && (c.mid != null || c.premium != null);
    });
    if (cs.length < 2) { el.innerHTML = ''; return; }
    var cc = C.colors;
    var pts = cs.map(function (c) {
      var isPut = String(c.type).toUpperCase() === 'PUT';
      var prime = c.mid != null ? c.mid : c.premium;
      return { x: prime, y: c.dte, q: (c.quality != null ? c.quality : (c.pop || 40)),
        sym: (c.type || '') + ' ' + (c.strike != null ? c.strike : ''), put: isPut,
        pop: c.pop, be: c.be };
    });
    C.card(el, {
      title: 'Meilleur équilibre — prime × échéance',
      question: 'Où se situe le contrat au meilleur rapport potentiel / temps / coût ?',
      conclusion: cs.length + ' contrat(s) · rayon = qualité moteur',
      height: opts.height || 240,
      legend: [{ label: 'Call', color: cc.positive }, { label: 'Put', color: cc.option }],
      source: opts.source || 'board options', timestamp: opts.timestamp, mode: opts.mode || 'delayed',
      limits: 'prime par action × jours avant échéance (DTE) · aucun ordre',
      render: function (cv) {
        return C.mount(cv, {
          type: 'bubble',
          data: { datasets: [{ data: pts.map(function (p) { return { x: p.x, y: p.y, r: Math.max(5, Math.min(20, p.q / 5)) }; }),
            backgroundColor: pts.map(function (p) { return C._rgba ? C._rgba(p.put ? cc.option : cc.positive, .5) : (p.put ? cc.option : cc.positive); }),
            borderColor: pts.map(function (p) { return p.put ? cc.option : cc.positive; }), borderWidth: 1.5 }] },
          options: {
            scales: {
              x: { title: { display: true, text: 'Prime ($ / action)' }, grid: { color: cc.grid } },
              y: { title: { display: true, text: 'Jours avant échéance' }, grid: { color: cc.grid } },
            },
            plugins: { tooltip: { callbacks: { label: function (it) { var p = pts[it.dataIndex]; return p.sym + ' — prime ' + VX.fmt.num(p.x, 2) + ', ' + p.y + ' j' + (p.pop != null ? ', PoP ' + p.pop + '%' : '') + (p.be != null ? ', seuil ' + VX.fmt.num(p.be, 2) : ''); } } } },
          },
        });
      },
    });
  };
})();
