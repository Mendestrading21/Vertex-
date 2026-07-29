/* options-gex.js — vue « Positionnement dealer (GEX) » de l'espace Options.
   Récupère /api/options/gex/<sym> (profil GEX + flux notable + thèse, données
   réelles du board) et rend : thèse (analyste), tuiles de synthèse, barres GEX
   par strike (SVG inline), flux notable. Honnête : vue fenêtrée signalée, « n/d »
   si donnée absente, jamais de chiffre inventé. Lecture seule, aucun ordre. */
(function () {
  'use strict';
  if (!document.getElementById('vx-gx-thesis')) return;   // pas sur cette vue
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[<>&"']/g, function (c) {
    return { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var f = function (x, d) { return (typeof x === 'number' && isFinite(x)) ? x.toLocaleString('fr-FR', { maximumFractionDigits: d == null ? 2 : d }) : 'n/d'; };
  var money = function (x) {
    if (typeof x !== 'number' || !isFinite(x)) return 'n/d';
    var a = Math.abs(x), s = x < 0 ? '−' : '';
    if (a >= 1e9) return s + (a / 1e9).toFixed(2) + ' Md$';
    if (a >= 1e6) return s + (a / 1e6).toFixed(2) + ' M$';
    if (a >= 1e3) return s + (a / 1e3).toFixed(1) + ' k$';
    return s + a.toFixed(0) + ' $';
  };

  function toneBias(b) { return b === 'haussier' ? 'pos' : b === 'baissier' ? 'neg' : 'neutral'; }

  function renderThesis(d) {
    var s = d.synthesis || {}, host = $('vx-gx-thesis');
    if (!host) return;
    if (s.empty) {
      host.innerHTML = '<section class="vx-card"><div class="vx-empty"><b>Aucune donnée</b><br>'
        + esc((s.reason || 'positionnement indisponible') + '.') + '</div></section>';
      return;
    }
    var demo = d.demo ? '<span class="vx-demo-tag">DÉMO</span> ' : '';
    var chips = [];
    (s.evidence || []).forEach(function (e) { chips.push('<li>' + esc(e) + '</li>'); });
    host.innerHTML =
      '<section class="vx-card" aria-label="Thèse positionnement">'
      + '<div class="vx-verdict">' + demo
      + '<div class="vx-flex" style="gap:.5rem;align-items:center;flex-wrap:wrap">'
      + '<span class="vx-badge" data-tone="' + toneBias(s.bias) + '">' + esc(s.headline || '—') + '</span>'
      + (s.earnings_risk ? '<span class="vx-badge" data-tone="neg">Risque événementiel : ' + esc(s.earnings_risk) + '</span>' : '')
      + '</div>'
      + '<p class="vx-lead">' + esc(s.narrative || '') + '</p>'
      + (chips.length ? '<ul class="vx-muted" style="margin:.4rem 0 .2rem;padding-left:1.1rem">' + chips.join('') + '</ul>' : '')
      + '<div class="vx-muted">Vue ' + esc(d.coverage || '') + ' · thèse déterministe · lecture seule — aucun ordre.</div>'
      + '</div></section>';
  }

  function tile(label, value, sub) {
    return '<div class="vx-stat"><span class="vx-stat-label">' + esc(label) + '</span>'
      + '<span class="vx-stat-value">' + value + '</span>'
      + (sub ? '<span class="vx-muted">' + esc(sub) + '</span>' : '') + '</div>';
  }

  function renderTiles(d) {
    var g = d.gex || {}, host = $('vx-gx-tiles');
    if (!host) return;
    if (g.empty) { host.innerHTML = ''; return; }
    var reg = g.regime === 'stabilisant' ? 'Stabilisant (pinning)'
      : g.regime === 'accelerateur' ? 'Accélérateur' : 'Neutre';
    host.innerHTML = '<section class="vx-card"><div class="vx-stats-row">'
      + tile('Spot', f(g.spot), null)
      + tile('Net GEX', money(g.net_gex_total), g.net_gex_total > 0 ? 'dealers longs gamma' : g.net_gex_total < 0 ? 'dealers courts gamma' : '')
      + tile('Régime', '<span class="vx-badge" data-tone="' + (g.net_gex_total > 0 ? 'pos' : g.net_gex_total < 0 ? 'neg' : 'neutral') + '">' + reg + '</span>', null)
      + tile('Bascule 0-γ', f(g.zero_gamma), 'zero-gamma flip')
      + tile('Mur call', f(g.call_wall), 'aimant haussier')
      + tile('Mur put', f(g.put_wall), 'support')
      + '</div></section>';
  }

  /* Barres GEX par strike — SVG inline (call vert vers la droite, put rouge vers la gauche). */
  function renderBars(d) {
    var g = d.gex || {}, host = $('vx-gx-bars');
    if (!host) return;
    if (g.empty || !(g.strikes || []).length) {
      host.innerHTML = '<div class="vx-empty">Aucun strike exploitable (OI + gamma réels absents).</div>';
      return;
    }
    var rows = g.strikes.slice().sort(function (a, b) { return b.strike - a.strike; });   // strikes hauts en haut
    var maxAbs = 0;
    rows.forEach(function (r) { maxAbs = Math.max(maxAbs, Math.abs(r.call_gex || 0), Math.abs(r.put_gex || 0)); });
    maxAbs = maxAbs || 1;
    var W = 520, mid = W / 2, rowH = 20, H = rows.length * rowH + 28, scale = (W / 2 - 60) / maxAbs;
    var pos = 'var(--vx-positive,#38b879)', neg = 'var(--vx-negative,#dc5f52)';
    var spotY = null;
    var svg = ['<svg viewBox="0 0 ' + W + ' ' + H + '" width="100%" role="img" aria-label="GEX par strike">'];
    svg.push('<line x1="' + mid + '" y1="6" x2="' + mid + '" y2="' + (H - 16) + '" stroke="var(--vx-border,#3a332c)"/>');
    rows.forEach(function (r, i) {
      var y = 10 + i * rowH;
      if (spotY === null && g.spot != null && r.strike <= g.spot) spotY = y - 2;   // 1er strike ≤ spot
      var cw = Math.abs(r.call_gex || 0) * scale, pw = Math.abs(r.put_gex || 0) * scale;
      if (cw > 0.5) svg.push('<rect x="' + mid + '" y="' + y + '" width="' + cw + '" height="' + (rowH - 6) + '" fill="' + pos + '" opacity=".85"/>');
      if (pw > 0.5) svg.push('<rect x="' + (mid - pw) + '" y="' + y + '" width="' + pw + '" height="' + (rowH - 6) + '" fill="' + neg + '" opacity=".85"/>');
      svg.push('<text x="' + (mid + 4) + '" y="' + (y + rowH - 9) + '" font-size="9.5" fill="var(--vx-text-dim,#8a837a)">' + f(r.strike, 0) + '</text>');
    });
    if (spotY != null) svg.push('<line x1="10" y1="' + spotY + '" x2="' + (W - 10) + '" y2="' + spotY + '" stroke="var(--vx-orange-500,#cf6128)" stroke-dasharray="3 3"/>');
    svg.push('</svg>');
    host.innerHTML = svg.join('')
      + '<div class="vx-muted" style="margin-top:.3rem">Vert = call GEX (+) · rouge = put GEX (−) · pointillé orange = spot ' + f(g.spot) + '. '
      + esc(d.coverage || '') + '.</div>';
  }

  function renderFlow(d) {
    var fl = d.flow || {}, host = $('vx-gx-flow');
    if (!host) return;
    if (fl.empty || !(fl.contracts || []).length) {
      host.innerHTML = '<div class="vx-empty">' + esc((fl.reason || 'aucun flux notable exploitable') + '.') + '</div>';
      return;
    }
    var rows = fl.contracts.map(function (c) {
      return '<tr><td><span class="vx-badge" data-tone="' + (c.type === 'CALL' ? 'pos' : 'neg') + '">' + esc(c.type) + '</span> ' + f(c.strike, 0)
        + (c.exp ? ' <span class="vx-muted">' + esc(c.exp) + '</span>' : '') + '</td>'
        + '<td class="vx-num">' + f(c.vol, 0) + '</td>'
        + '<td class="vx-num">' + (c.vol_oi != null ? f(c.vol_oi, 2) + (c.fresh ? ' ⚡' : '') : 'n/d') + '</td>'
        + '<td class="vx-num">' + money(c.premium) + '</td></tr>';
    }).join('');
    var skew = fl.skew ? '<div class="vx-muted" style="margin-bottom:.3rem">Skew premium : <b>' + esc(fl.skew) + '</b> (' + f(fl.call_pct, 0) + ' % calls)</div>' : '';
    host.innerHTML = skew
      + '<div class="vx-table-wrap"><table class="vx-table"><thead><tr><th>Contrat</th><th class="vx-num">Vol</th><th class="vx-num">Vol/OI</th><th class="vx-num">Premium</th></tr></thead>'
      + '<tbody>' + rows + '</tbody></table></div>'
      + '<div class="vx-muted" style="margin-top:.3rem">' + esc(fl.basis || '') + '. ⚡ = volume &gt; OI (positionnement frais).</div>';
  }

  function load(sym) {
    sym = (sym || '').trim().toUpperCase();
    if (!/^[A-Z.\-]{1,12}$/.test(sym)) { VX.toast && VX.toast('Ticker invalide', 'error'); return; }
    $('vx-gx-thesis').innerHTML = '<section class="vx-card"><div class="vx-empty">Analyse du positionnement de ' + esc(sym) + '…</div></section>';
    VX.fetch('/api/options/gex/' + encodeURIComponent(sym), { ttl: 120000 }).then(function (d) {
      renderThesis(d); renderTiles(d); renderBars(d); renderFlow(d);
      try { VX.context && VX.context.save && VX.context.save({ selectedSymbol: sym }); } catch (e) {}
    }).catch(function (e) {
      $('vx-gx-thesis').innerHTML = '<section class="vx-card"><div class="vx-error-banner">Chargement impossible : ' + esc(e.message) + '</div></section>';
    });
  }

  var go = $('vx-gx-go'), inp = $('vx-gx-sym');
  if (go && inp) {
    go.addEventListener('click', function () { load(inp.value); });
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') load(inp.value); });
  }
  /* pré-remplissage : ticker actif du store, sinon un contrat du board via chips */
  var pre = '';
  try { pre = (VX.store && VX.store.get && VX.store.get('active_ticker')) || ''; } catch (e) {}
  if (pre && inp) { inp.value = pre; load(pre); }
})();
