/* options-scanner.js — SCANNER PAR UNIVERS (SKYLER LOT 8c).
   TACTICAL / SWING / LEAPS strictement séparés (mandat V2), hors-mandat
   ÉTIQUETÉ (jamais caché), probabilité de doublement ESTIMÉE affichée telle
   quelle (modèle non calibré — dit à l'écran). Lecture seule, aucun ordre. */
(function () {
  'use strict';
  var out = document.getElementById('vx-sc-out');
  if (!out) return;                      // actif uniquement sur la vue LEAPS
  var tabs = document.getElementById('vx-sc-tabs');
  var symIn = document.getElementById('vx-sc-sym');
  var go = document.getElementById('vx-sc-go');
  var universe = 'LEAPS';
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[<>&"']/g, function (c) {
      return { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };
  var num = function (v, d) { return (v == null || isNaN(v)) ? '—' : Number(v).toFixed(d == null ? 2 : d); };

  function mandateCell(c) {
    if (c.mandate == null) return '<span class="vx-muted">n/a</span>';
    if (!c.hors_mandat) return '<span class="vx-badge" data-tone="pos">conforme</span>';
    var why = [];
    if (c.mandate.delta_ok === false) why.push('delta hors 0,70-0,90');
    if (c.mandate.oi_ok === false) why.push('OI insuffisant');
    if (c.mandate.spread_ok === false) why.push('spread trop large');
    return '<span class="vx-badge" data-tone="neg" title="' + esc(why.join(' · ')) + '">HORS MANDAT</span>';
  }

  function render(d) {
    if (!d || d.available === false) {
      out.innerHTML = '<div class="vx-empty">' + esc((d && d.reason) || 'Scan indisponible.') + '</div>';
      return;
    }
    var rows = (d.candidates || []).map(function (c) {
      var dp = c.double_prob;
      var dpTxt = (dp && dp.available)
        ? (num(dp.probability * 100, 1) + ' % <span class="vx-muted">EST.</span>')
        : '<span class="vx-muted">—</span>';
      return '<tr>'
        + '<td data-label="Titre"><b>' + esc(c.sym) + '</b></td>'
        + '<td data-label="Type">' + esc(c.type) + '</td>'
        + '<td data-label="Strike" class="vx-num">' + num(c.strike, 1) + '</td>'
        + '<td data-label="DTE" class="vx-num">' + esc(c.dte) + '</td>'
        + '<td data-label="Delta" class="vx-num">' + num(c.delta, 2) + '</td>'
        + '<td data-label="IV" class="vx-num">' + (c.iv != null ? num(c.iv * 100, 1) + ' %' : '—') + '</td>'
        + '<td data-label="OI" class="vx-num">' + (c.oi != null ? c.oi : '—') + '</td>'
        + '<td data-label="Spread" class="vx-num">' + (c.spread_pct != null ? num(c.spread_pct, 1) + ' %' : '—') + '</td>'
        + '<td data-label="Qualité" class="vx-num">' + (c.quality != null ? c.quality : '—') + '</td>'
        + '<td data-label="Mandat">' + mandateCell(c) + '</td>'
        + '<td data-label="P(doubler)" class="vx-num">' + dpTxt + '</td>'
        + '</tr>';
    }).join('');
    out.innerHTML = '<div class="vx-meta vx-mb1">' + esc(d.universe) + ' · fenêtre ' + esc((d.window || []).join('-'))
      + ' DTE · ' + d.n + ' contrat(s)' + (d.demo ? ' · <span class="vx-badge" data-tone="neutral">DÉMO</span>' : '') + '</div>'
      + '<div class="vx-table-wrap"><table class="vx-table"><thead><tr>'
      + '<th>Titre</th><th>Type</th><th>Strike</th><th>DTE</th><th>Delta</th><th>IV</th><th>OI</th>'
      + '<th>Spread</th><th>Qualité</th><th>Mandat</th><th>P(doubler)</th>'
      + '</tr></thead><tbody>' + rows + '</tbody></table></div>'
      + '<div class="vx-meta" style="margin-top:.3rem">P(doubler) = P(valeur terminale ≥ 2× coût), '
      + 'modèle lognormal non calibré — estimation, pas une promesse · hors-mandat affiché, jamais filtré en silence.</div>';
  }

  function run() {
    var sym = (symIn && symIn.value || '').trim().toUpperCase();
    out.innerHTML = '<div class="vx-empty">Scan ' + esc(universe) + '…</div>';
    VX.fetch('/api/options/scanner/' + encodeURIComponent(universe) + (sym ? ('?sym=' + encodeURIComponent(sym)) : ''),
             { ttl: 120000 })
      .then(render)
      .catch(function (e) { out.innerHTML = '<div class="vx-error-banner">Scanner injoignable : ' + esc(e.message) + '</div>'; });
  }

  if (tabs) {
    tabs.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-universe]');
      if (!b) return;
      universe = b.getAttribute('data-universe');
      Array.prototype.forEach.call(tabs.querySelectorAll('[data-universe]'), function (x) {
        x.classList.toggle('vx-btn-ghost', x !== b);
      });
      run();
    });
  }
  if (go) go.addEventListener('click', run);
  if (symIn) symIn.addEventListener('keydown', function (e) { if (e.key === 'Enter') run(); });
  run();
})();
