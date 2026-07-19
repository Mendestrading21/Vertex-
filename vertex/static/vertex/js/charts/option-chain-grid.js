/* option-chain-grid.js — GRILLE de chaîne d'options RÉELLE (strikes × échéances).
 *
 * C.optionChainGrid(host, {expiries, spot, symbol, source, timestamp, mode, greeks_source})
 *   Vraie grille institutionnelle : PUTS ← Strike → CALLS, une échéance à la fois
 *   (sélecteur). Colonnes par côté : Bid · Ask · IV · Δ · Θ · V · OI (Γ en info-bulle).
 *   Ombrage ITM (teinte argent neutre — jamais vert/rouge), repère spot inséré
 *   entre les strikes, strike ATM surligné. Greeks = COURTIER IBKR en live
 *   (greeks_source='broker') ; « — » honnête si un champ manque. Lecture seule.
 *
 *   Complète (ne remplace pas) optionChainTable, la shortlist des meilleurs
 *   contrats (greeks modèle Black-Scholes).
 */
(function () {
  var C = window.VXCharts, VX = window.VX;
  function esc(s) { return String(s == null ? '' : s).replace(/[<>&"]/g, function (c) { return { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]; }); }
  function nd(v, d) { return (v == null || v === '' || (typeof v === 'number' && !isFinite(v))) ? '—' : VX.fmt.num(+v, d == null ? 2 : d); }
  function pct(v) { return (v == null || !isFinite(v)) ? '—' : VX.fmt.num(v * 100, 1) + '%'; }
  function fmtExp(e) {                                   // 20260902 → 02 sep 26
    var m = /^(\d{4})(\d{2})(\d{2})/.exec(String(e).replace(/-/g, ''));
    if (!m) return esc(e);
    var mo = ['jan', 'fév', 'mar', 'avr', 'mai', 'juin', 'juil', 'aoû', 'sep', 'oct', 'nov', 'déc'][(+m[2]) - 1] || m[2];
    return m[3] + ' ' + mo + ' ' + m[1].slice(2);
  }

  // Sous-colonnes d'un côté (ordre commun calls & puts).
  var SUB = [
    { k: 'bid', label: 'Bid', d: 2 },
    { k: 'ask', label: 'Ask', d: 2 },
    { k: 'iv', label: 'IV', iv: true },
    { k: 'delta', label: 'Δ', d: 2 },
    { k: 'theta', label: 'Θ', d: 2 },
    { k: 'vega', label: 'V', d: 2 },
    { k: 'oi', label: 'OI', d: 0 },
  ];

  function sideCells(side, itm) {
    var cls = 'vx-num vx-mono' + (itm ? ' vx-ocg-itm' : '');
    var gamma = side && side.gamma != null ? ' title="Γ ' + nd(side.gamma, 3) + (side.vol != null ? ' · vol ' + side.vol : '') + '"' : '';
    return SUB.map(function (c) {
      var v = side ? side[c.k] : null;
      var txt = c.iv ? pct(v) : nd(v, c.d);
      return '<td class="' + cls + '"' + (c.k === 'iv' ? gamma : '') + '>' + txt + '</td>';
    }).join('');
  }

  C.optionChainGrid = function (host, opts) {
    var el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return;
    var o = opts || {};
    var exps = (o.expiries || []).filter(function (e) { return e && e.strikes && e.strikes.length; });
    el.classList.add('vx-card');
    var title = 'Chaîne d\'options — strikes × échéances' + (o.symbol ? ' · ' + esc(o.symbol) : '');
    var question = 'À quel strike et quelle échéance la convexité et la liquidité sont-elles les meilleures ?';
    if (!exps.length) {
      el.innerHTML = '<div class="vx-card-header"><span class="vx-card-title">' + title + '</span>'
        + '<span class="vx-chart-question">' + question + '</span></div>'
        + VX.states.empty('Chaîne large indisponible pour ' + esc(o.symbol || '') + ' — TWS fermé, hors séance, ou titre pas encore chargé (aucune donnée inventée).');
      return;
    }
    var spot = +o.spot || 0;
    var greeksBroker = o.greeks_source === 'broker';
    var srcLabel = greeksBroker ? 'courtier IBKR (greeks réels)' : (o.source || 'chaîne large');
    var COLSPAN = SUB.length * 2 + 1;
    var state = { i: 0 };

    function paint() {
      var ex = exps[state.i] || exps[0];
      var rows = (ex.strikes || []).slice().sort(function (a, b) { return b.strike - a.strike; });  // strike décroissant
      var subHead = SUB.map(function (c) { return '<th class="vx-num">' + c.label + '</th>'; }).join('');
      var head = '<tr><th colspan="' + SUB.length + '" class="vx-ocg-side">PUTS</th>'
        + '<th class="vx-ocg-strike">Strike</th>'
        + '<th colspan="' + SUB.length + '" class="vx-ocg-side">CALLS</th></tr>'
        + '<tr>' + subHead + '<th class="vx-ocg-strike"></th>' + subHead + '</tr>';
      var body = '', spotDrawn = false;
      rows.forEach(function (r) {
        var K = r.strike;
        if (!spotDrawn && spot > 0 && K < spot) {
          body += '<tr class="vx-ocg-spot"><td colspan="' + COLSPAN + '"><span>◄ spot ' + VX.fmt.num(spot, 2) + '</span></td></tr>';
          spotDrawn = true;
        }
        var putItm = spot > 0 && K > spot;               // put ITM si strike > spot
        var callItm = spot > 0 && K < spot;              // call ITM si strike < spot
        var atm = spot > 0 && Math.abs(K - spot) <= (spot * 0.006);
        body += '<tr' + (atm ? ' class="vx-ocg-atm"' : '') + '>'
          + sideCells(r.put, putItm)
          + '<td class="vx-ocg-strike vx-mono">' + VX.fmt.num(K, 2) + '</td>'
          + sideCells(r.call, callItm) + '</tr>';
      });
      var expSel = '<select class="vx-select" data-ocg-exp style="width:auto">'
        + exps.map(function (e, i) {
          return '<option value="' + i + '"' + (i === state.i ? ' selected' : '') + '>'
            + fmtExp(e.exp) + (e.dte != null ? ' · ' + e.dte + ' j' : '') + '</option>';
        }).join('') + '</select>';
      el.querySelector('[data-ocg-body]').innerHTML =
        '<div class="vx-ocg-bar vx-flex" style="gap:.5rem;align-items:center;flex-wrap:wrap;margin-bottom:8px">'
        + '<span class="vx-meta">Échéance</span>' + expSel
        + '<span class="vx-meta">Spot ' + (spot > 0 ? VX.fmt.num(spot, 2) : '—') + ' · ' + rows.length + ' strikes · '
        + (greeksBroker ? 'greeks courtier' : 'greeks ' + esc(o.greeks_source || 'n/d')) + '</span></div>'
        + '<div class="vx-datagrid vx-ocg-wrap" style="overflow-x:auto"><table class="vx-table vx-ocg"><thead>'
        + head + '</thead><tbody>' + body + '</tbody></table></div>';
      var es = el.querySelector('[data-ocg-exp]');
      if (es) es.addEventListener('change', function () { state.i = +this.value || 0; paint(); });
    }

    el.innerHTML =
      '<div class="vx-card-header"><span class="vx-card-title">' + title + '</span>'
      + '<span class="vx-chart-question">' + question + '</span></div>'
      + '<div data-ocg-body></div>'
      + '<div class="vx-chart-foot">' + VX.updateIndicator(o.timestamp, srcLabel, o.mode || 'delayed')
      + '<span class="vx-meta">Grille strikes × échéances · '
      + (greeksBroker ? 'greeks & IV courtier IBKR' : 'greeks ' + esc(o.greeks_source || 'n/d'))
      + ' · bid/ask temps différé · ombrage ITM · lecture seule.</span></div>';
    paint();
  };
})();
