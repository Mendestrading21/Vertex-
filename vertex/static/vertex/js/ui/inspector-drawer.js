/* inspector-drawer.js — INSPECTEUR LATÉRAL GLOBAL réutilisable (§29).
 * VX.inspect(sym) ouvre un aperçu riche d'un titre SANS quitter la page :
 * identité, cours, décision, scores moteur, mini-courbe, plan de trade, thèse,
 * et navigation. Données RÉELLES via /api/ticker/<sym> — aucun chiffre inventé,
 * « — » honnête si absent. Délégué sur [data-inspect] partout dans l'app.
 * Lecture seule : aucune action n'exécute d'ordre. */
(function () {
  'use strict';
  var VX = window.VX; if (!VX) return;
  function esc(s) { return String(s == null ? '' : s).replace(/[<>&"]/g, function (c) { return { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]; }); }

  /* Mini-courbe SVG (clôtures réelles) — teinte selon la direction. */
  function spark(closes) {
    var v = (closes || []).filter(function (x) { return x != null && isFinite(x); }).slice(-60);
    if (v.length < 8) return '';
    var w = 260, h = 54, mn = Math.min.apply(null, v), mx = Math.max.apply(null, v), rng = (mx - mn) || 1;
    var pts = v.map(function (x, i) { return (i / (v.length - 1) * w).toFixed(1) + ',' + (h - 2 - ((x - mn) / rng) * (h - 4)).toFixed(1); }).join(' ');
    var up = v[v.length - 1] >= v[0];
    var col = up ? 'var(--vx-positive)' : 'var(--vx-negative)';
    return '<svg viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" width="100%" height="54" style="display:block;margin:8px 0" aria-hidden="true">'
      + '<polyline points="' + pts + '" fill="none" stroke="' + col + '" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>';
  }

  /* Barre de niveaux du plan (stop · cours · objectif). */
  function levels(plan, price) {
    if (!plan || plan.entry == null || plan.stop == null) return '';
    var tp = plan.tp3 || plan.tp2 || plan.tp1; if (tp == null) return '';
    var lo = Math.min(plan.stop, plan.entry, price || plan.entry), hi = Math.max(tp, plan.entry, price || plan.entry), rng = (hi - lo) || 1;
    var pc = function (x) { return Math.max(0, Math.min(100, (x - lo) / rng * 100)); };
    var zStop = pc(plan.stop), zEntry = pc(plan.entry);
    return '<div style="margin-top:8px">'
      + '<div class="vx-flex" style="justify-content:space-between;font-size:10px;color:var(--vx-text-dim)">'
      + '<span style="color:var(--vx-negative)">stop ' + VX.fmt.price(plan.stop) + '</span>'
      + '<span>entrée ' + VX.fmt.price(plan.entry) + '</span>'
      + '<span style="color:var(--vx-positive)">objectif ' + VX.fmt.price(tp) + '</span></div>'
      + '<div style="position:relative;height:7px;border-radius:99px;margin-top:4px;overflow:hidden;'
      + 'background:linear-gradient(90deg,rgba(239,103,93,.35) 0%,rgba(239,103,93,.14) ' + zStop + '%,var(--vx-surface-0) ' + zStop + '%,var(--vx-surface-0) ' + zEntry + '%,rgba(53,201,135,.14) ' + zEntry + '%,rgba(53,201,135,.4) 100%)">'
      + (price != null ? '<i style="position:absolute;left:' + pc(price) + '%;top:-3px;width:10px;height:10px;margin-left:-5px;border-radius:99px;background:var(--vx-text-primary);box-shadow:0 0 0 2px var(--vx-surface-0)"></i>' : '')
      + '</div></div>';
  }

  function kv(k, v, cls) { return '<div class="vx-kv"><span class="k">' + k + '</span><span class="v vx-mono ' + (cls || '') + '">' + (v == null ? '—' : v) + '</span></div>'; }
  function bar(label, val, good, mid) {
    if (val == null || isNaN(val)) return '';
    var v = Math.max(0, Math.min(100, val));
    var col = good != null ? (val >= good ? 'var(--vx-positive)' : val >= (mid || 0) ? 'var(--vx-warning)' : 'var(--vx-negative)') : 'var(--vx-brand)';
    return '<div class="vx-flex" style="gap:8px;align-items:center;padding:2px 0">'
      + '<span style="flex:0 0 92px;font-size:11px;color:var(--vx-text-muted)">' + label + '</span>'
      + '<span style="flex:1;height:6px;border-radius:99px;background:var(--vx-surface-0);overflow:hidden"><i style="display:block;height:100%;width:' + v + '%;background:' + col + ';border-radius:99px"></i></span>'
      + '<b class="vx-mono" style="flex:0 0 28px;text-align:right;font-size:11px">' + Math.round(val) + '</b></div>';
  }

  var VERD = { BUY: 'ACHAT', WATCH: 'SURVEILLER', WAIT: 'ATTENDRE', AVOID: 'ÉVITER', ACHETER: 'ACHAT', RENFORCER: 'RENFORCER' };

  VX.inspect = function (sym) {
    sym = String(sym || '').toUpperCase();
    if (!sym) return;
    VX.shell.openDrawer(sym, '<div class="vx-skeleton vx-skeleton-line" style="width:70%;margin-bottom:10px"></div>'
      + '<div class="vx-skeleton vx-skeleton-chart" style="height:60px;margin-bottom:12px"></div>'
      + '<div class="vx-skeleton vx-skeleton-line" style="margin-bottom:6px"></div><div class="vx-skeleton vx-skeleton-line" style="width:80%"></div>');
    var body = document.getElementById('vx-drawer-body');
    VX.fetch('/api/ticker/' + encodeURIComponent(sym), { ttl: 60000 }).then(function (t) {
      if (!body) return;
      var d = (t && t.detail) || {};
      var co = (t && t.company) || {};
      var name = co.name || co.shortName || '';
      var verd = d.verdict || '';
      var chg = d.change;
      var plan = d.plan || {};
      var series = d.series || {};
      var pwin = d.vx_pwin != null ? Math.round(d.vx_pwin * 100) : null;
      var badges = window.VXEntities && VXEntities.badges ? VXEntities.badges(sym) : '';
      body.innerHTML =
        '<div class="vx-flex" style="justify-content:space-between;align-items:flex-start;gap:8px">'
        + '<div style="min-width:0"><div class="vx-ticker" style="font-size:19px;font-weight:700">' + esc(sym) + '</div>'
        + (name ? '<div class="vx-meta vx-truncate" style="max-width:230px">' + esc(name) + '</div>' : '') + '</div>'
        + (verd ? '<span class="vx-badge vx-badge-decision" data-decision="' + esc(String(verd).replace('É', 'E')) + '">' + esc(VERD[verd] || verd) + '</span>' : '') + '</div>'
        + '<div class="vx-flex" style="gap:10px;align-items:baseline;margin-top:6px">'
        + '<span class="vx-mono" style="font-size:24px;font-weight:700">' + (d.price != null ? VX.fmt.price(d.price) : '—') + '</span>'
        + '<span class="vx-mono ' + (chg > 0 ? 'vx-pos' : chg < 0 ? 'vx-neg' : 'vx-muted') + '">' + (chg != null ? VX.fmt.pct(chg, 1) : '—') + '</span>'
        + (badges ? '<span class="vx-right">' + badges + '</span>' : '') + '</div>'
        + spark(series.close)
        + '<div class="vx-mt2">'
        + bar('Score', d.score, 72, 56)
        + (pwin != null ? bar('Proba gain', pwin, 60, 45) : '')
        + (d.vx_edge != null ? bar('Avantage', d.vx_edge, 60, 40) : '')
        + '</div>'
        + '<div class="vx-mt2">'
        + kv('Secteur', esc(d.sector || '—'))
        + (d.rr != null ? kv('Gain/risque', VX.fmt.num(d.rr, 1) + '×') : '')
        + (d.vx_ev != null ? kv('Espérance / trade', (d.vx_ev >= 0 ? '+' : '') + VX.fmt.num(d.vx_ev, 1) + ' %', d.vx_ev > 0 ? 'vx-pos' : 'vx-neg') : '')
        + (d.mtf && d.mtf.state ? kv('Multi-horizons', esc(d.mtf.state)) : '')
        + '</div>'
        + levels(plan, d.price)
        + (d.thesis ? '<div class="vx-meta vx-mt3" style="white-space:normal;line-height:1.5"><b>Thèse moteur :</b> ' + esc(d.thesis) + '</div>'
          : (d.chart_read ? '<div class="vx-meta vx-mt3" style="white-space:normal;line-height:1.5"><b>Lecture :</b> ' + esc(d.chart_read) + '</div>' : ''))
        + '<div class="vx-divider vx-mt3"></div>'
        + '<div class="vx-flex vx-wrap" style="gap:.4rem;margin-top:8px">'
        + '<a class="vx-btn vx-btn-sm vx-btn-primary" href="/analysis/' + esc(sym) + '">Analyse complète →</a>'
        + '<a class="vx-btn vx-btn-sm" href="/options/' + esc(sym) + '">Options</a>'
        + '<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\'' + esc(sym) + '\',\'follow\')">Suivre</button>'
        + '<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\'' + esc(sym) + '\',\'alert\')">Alerte</button>'
        + '</div>'
        + '<div class="vx-meta vx-mt2">Aperçu — données du scan · lecture seule, aucun ordre.</div>';
    }).catch(function () {
      if (body) body.innerHTML = VX.states.error('Aperçu indisponible pour ' + esc(sym) + '.');
    });
  };

  /* Délégation globale : tout élément [data-inspect="SYM"] ouvre l'inspecteur. */
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-inspect]');
    if (!el) return;
    e.preventDefault(); e.stopPropagation();
    VX.inspect(el.getAttribute('data-inspect'));
  });
})();
