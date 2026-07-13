/* options-intel.js — client de l'espace Options Intelligence (§18).
 * Lit /api/options/* (moteurs purs) et rend chaque interprétation canonique
 * avec son verdict, ses preuves et un tiroir « Comprendre ce graphique ».
 * Aucun chiffre inventé : donnée absente → état honnête. Lecture seule.
 */
(function () {
  'use strict';
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };
  var VXf = (window.VX && VX.fmt) || { nd: function (v) { return v == null ? '—' : v; }, num: function (v) { return v == null ? '—' : v; } };

  // Couleur/label du statut canonique (jamais de bleu — thème Obsidian Copper).
  var ST = {
    FAVORABLE: { cls: 'pos', label: 'Favorable' },
    NEUTRE: { cls: 'neutral', label: 'Neutre' },
    DEFAVORABLE: { cls: 'neg', label: 'Défavorable' },
    BLOQUANT: { cls: 'neg', label: 'Bloquant' },
    INCONNU: { cls: 'neutral', label: 'Inconnu' }
  };
  // dernière interprétation par graphique — pour le tiroir « Comprendre »
  var LAST = {};

  function badge(status) {
    var s = ST[status] || ST.INCONNU;
    return '<span class="vx-badge" data-tone="' + s.cls + '">' + esc(s.label) + '</span>';
  }

  function confHtml(c) {
    if (c == null) return '<span class="vx-muted">confiance n/d</span>';
    return '<span class="vx-muted">confiance ' + Math.round(c * 100) + ' %</span>';
  }

  // Carte de verdict compacte + mémorisation pour le tiroir.
  function verdictCard(interp) {
    if (!interp) return '<div class="vx-empty">Interprétation indisponible.</div>';
    LAST[interp.chart_id] = interp;
    var reading = interp.dominant_reading || 'Donnée insuffisante pour un verdict.';
    return '<div class="vx-verdict" data-status="' + esc(interp.status) + '">' +
      '<div class="vx-flex" style="gap:.6rem;align-items:center;margin-bottom:.5rem">' +
      badge(interp.status) + confHtml(interp.confidence) +
      (interp.source ? '<span class="vx-muted">· ' + esc(interp.source) + '</span>' : '') +
      '</div>' +
      '<p class="vx-lead">' + esc(reading) + '</p>' +
      '<p class="vx-sub">' + esc(interp.strategy_impact || '') + '</p>' +
      '</div>';
  }

  // Tiroir « Comprendre ce graphique » — question, preuves, incertitudes, limites.
  function explainDrawer(interp) {
    if (!interp) { if (window.VX && VX.toast) VX.toast('Rien à expliquer pour l’instant', 'info'); return; }
    var li = function (arr) {
      if (!arr || !arr.length) return '<li class="vx-muted">—</li>';
      return arr.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('');
    };
    var html = '<div class="vx-explain">' +
      '<h3>' + esc(interp.question) + '</h3>' +
      '<p class="vx-lead">' + badge(interp.status) + ' ' + esc(interp.dominant_reading || '—') + '</p>' +
      '<div class="vx-grid2">' +
      '<div><h4>Ce qui soutient</h4><ul>' + li(interp.positive_evidence) + '</ul></div>' +
      '<div><h4>Ce qui pèse contre</h4><ul>' + li(interp.negative_evidence) + '</ul></div>' +
      '</div>' +
      '<h4>Incertitudes</h4><ul>' + li(interp.uncertainties) + '</ul>' +
      '<h4>Impact stratégique</h4><p>' + esc(interp.strategy_impact || '—') + '</p>' +
      '<h4>Limites méthodologiques</h4><ul>' + li(interp.limitations) + '</ul>' +
      '<p class="vx-muted">Source : ' + esc(interp.source || 'n/d') +
      ' · Donnée : ' + esc(interp.as_of || 'n/d') + '</p>' +
      '</div>';
    if (window.VX && VX.drawer && VX.drawer.open) { VX.drawer.open('Comprendre ce graphique', html); }
    else { showFallbackModal(html); }
  }

  function showFallbackModal(html) {
    var host = document.getElementById('vx-opt-modal');
    if (!host) {
      host = document.createElement('div'); host.id = 'vx-opt-modal';
      host.style.cssText = 'position:fixed;inset:0;background:rgba(8,8,8,.72);z-index:70;display:flex;align-items:center;justify-content:center;padding:1rem';
      host.addEventListener('click', function (e) { if (e.target === host) host.remove(); });
      document.body.appendChild(host);
    }
    host.innerHTML = '<div class="vx-card" style="max-width:640px;max-height:82vh;overflow:auto;padding:1.2rem">' +
      html + '<div style="margin-top:1rem;text-align:right"><button class="vx-btn vx-btn-sm" id="vx-opt-modal-x">Fermer</button></div></div>';
    var x = document.getElementById('vx-opt-modal-x');
    if (x) x.addEventListener('click', function () { host.remove(); });
  }

  function loading(el) { if (el) el.innerHTML = (window.VX && VX.states) ? VX.states.loading(3) : 'Chargement…'; }
  function fail(el, cause) {
    if (el) el.innerHTML = (window.VX && VX.states)
      ? VX.states.error(cause) : '<div class="vx-error-banner">' + esc(cause) + '</div>';
  }

  function get(url) {
    return (window.VX && VX.fetch) ? VX.fetch(url, { ttl: 15000 })
      : fetch(url).then(function (r) { return r.json(); });
  }

  // Jauge d'environnement + pulses (OPTIONS HERO §14).
  function heroHtml(env, op, vp, demo) {
    if (!env || env.score == null) {
      LAST['options.environment'] = env && env.interpretation;
      return '<div class="vx-empty">Environnement non calculable : aucune dimension mesurable.</div>';
    }
    LAST['options.environment'] = env.interpretation;
    var pct = Math.max(0, Math.min(100, env.score));
    var tone = env.label === 'PORTEUR' ? 'pos' : env.label === 'HOSTILE' ? 'neg' : 'neutral';
    var dims = (env.dimensions || []).map(function (d) {
      var w = d.known ? Math.round(d.score) : null;
      return '<div class="vx-opt-dim"><span class="vx-opt-dim-l">' + esc(d.label) + '</span>' +
        '<span class="vx-opt-dim-bar"><i style="width:' + (w == null ? 0 : w) + '%"></i></span>' +
        '<span class="vx-opt-dim-v">' + (w == null ? 'n/d' : w) + '</span></div>';
    }).join('');
    var pulse = '';
    if (op && !op.empty) {
      pulse += pill('CALLS', op.calls) + pill('PUTS', op.puts) +
        pill('C/P', op.call_put_ratio != null ? VXf.num(op.call_put_ratio, 2) : '—') +
        pill('IV moy', op.avg_iv != null ? VXf.num(op.avg_iv, 1) + ' %' : '—') +
        pill('DTE moy', op.avg_dte != null ? Math.round(op.avg_dte) + ' j' : '—') +
        pill('Theta', op.avg_theta_burn != null ? VXf.num(op.avg_theta_burn, 2) : '—');
    }
    if (vp && !vp.empty) {
      pulse += pill('Vol', vp.state) + pill('IV médiane', vp.median_iv != null ? VXf.num(vp.median_iv, 1) + ' %' : '—') +
        pill('Dispersion', vp.dispersion != null ? VXf.num(vp.dispersion, 1) + ' pts' : '—');
    }
    return (demo ? '<div class="vx-demo-tag">Données de démonstration</div>' : '') +
      '<div class="vx-opt-hero-grid">' +
      '<div class="vx-opt-gauge"><div class="vx-opt-gauge-score" data-tone="' + tone + '">' +
      Math.round(env.score) + '<small>/100</small></div>' +
      badge(env.label === 'PORTEUR' ? 'FAVORABLE' : env.label === 'HOSTILE' ? 'DEFAVORABLE' : 'NEUTRE') +
      '<div class="vx-opt-gauge-track"><i data-tone="' + tone + '" style="width:' + pct + '%"></i></div>' +
      '<div class="vx-muted">' + env.dimensions_known + '/' + env.dimensions_total + ' dimensions mesurées</div></div>' +
      '<div class="vx-opt-dims">' + dims + '</div></div>' +
      (pulse ? '<div class="vx-opt-pulse">' + pulse + '</div>' : '');
  }
  function pill(label, val) {
    return '<span class="vx-opt-chip"><b>' + esc(label) + '</b> ' + esc(val == null ? '—' : val) + '</span>';
  }

  // ── Vue d'ensemble ────────────────────────────────────────────────
  function loadOverview() {
    var hEl = document.getElementById('vx-opt-hero-body');
    var cEl = document.getElementById('vx-opt-counters-body');
    var vEl = document.getElementById('vx-opt-verdict-body');
    var rEl = document.getElementById('vx-opt-radar-lite-body');
    [hEl, cEl, vEl, rEl].forEach(loading);
    get('/api/options/overview').then(function (d) {
      if (!d || d.empty) {
        var msg = (window.VX && VX.states) ? VX.states.empty('Aucun contrat dans le tableau (scan vide ou hors séance).') : 'Aucune donnée.';
        if (hEl) hEl.innerHTML = heroHtml(d && d.environment, d && d.option_pulse, d && d.volatility_pulse, d && d.demo);
        if (cEl) cEl.innerHTML = msg;
        if (vEl) vEl.innerHTML = verdictCard(d && d.interpretation);
        if (rEl) rEl.innerHTML = '';
        return;
      }
      var c = d.counters || {};
      if (hEl) hEl.innerHTML = heroHtml(d.environment, d.option_pulse, d.volatility_pulse, d.demo);
      if (cEl) cEl.innerHTML = countersHtml(c, d.demo, d.as_of);
      if (vEl) vEl.innerHTML = verdictCard(d.interpretation);
      if (rEl) rEl.innerHTML = radarTable((d.radar || []).slice(0, 4));
    }).catch(function (e) { fail(hEl, 'Chargement overview: ' + e.message); if (cEl) cEl.innerHTML = ''; });
  }

  function stat(label, val) {
    return '<div class="vx-stat"><span class="vx-stat-label">' + esc(label) +
      '</span><span class="vx-stat-value">' + val + '</span></div>';
  }

  // Barre de proportion CALL vs PUT (direction dominante du tableau d'options).
  function callPutBar(calls, puts) {
    var t = (calls || 0) + (puts || 0); if (!t) return '';
    var cp = Math.round((calls || 0) / t * 100), pp = 100 - cp;
    return '<div style="margin-top:.8rem" role="img" aria-label="CALLS ' + (calls || 0) + ' contre PUTS ' + (puts || 0) + ', ' + cp + ' % calls">' +
      '<div style="display:flex;justify-content:space-between;font-size:11px;color:var(--vx-text-secondary,#bab4ac);margin-bottom:3px">' +
      '<span>CALLS ' + VXf.nd(calls) + ' (' + cp + ' %)</span><span>PUTS ' + VXf.nd(puts) + ' (' + pp + ' %)</span></div>' +
      '<div style="height:14px;border-radius:5px;overflow:hidden;display:flex;background:var(--vx-surface-3,#17191b)">' +
      '<span style="width:' + cp + '%;background:var(--vx-copper-light,#b47852)"></span>' +
      '<span style="width:' + pp + '%;background:var(--vx-option,#806095)"></span></div>' +
      '<div class="vx-muted" style="font-size:11px;margin-top:4px">Direction dominante : CALLS — la Stratégie Vertex privilégie l’achat de calls ; les puts restent tactiques et rares. Volume/OI ≠ conviction certaine.</div></div>';
  }

  function countersHtml(c, demo, asOf) {
    var band = c.quality_band ? esc(c.quality_band) : '—';
    return (demo ? '<div class="vx-demo-tag">Données de démonstration</div>' : '') +
      '<div class="vx-stats-row">' +
      stat('Contrats', VXf.nd(c.total)) +
      stat('CALLS', VXf.nd(c.calls)) +
      stat('PUTS', VXf.nd(c.puts)) +
      stat('Titres', VXf.nd(c.symbols)) +
      stat('IV moyenne', c.avg_iv != null ? VXf.num(c.avg_iv, 1) + ' %' : '—') +
      stat('Qualité moy.', c.avg_quality != null ? VXf.num(c.avg_quality, 0) + ' (' + band + ')' : '—') +
      stat('Spread moy.', c.avg_spread_pct != null ? VXf.num(c.avg_spread_pct, 1) + ' %' : '—') +
      '</div>' +
      callPutBar(c.calls, c.puts) +
      (asOf ? '<div class="vx-muted" style="margin-top:.5rem">Scan : ' + esc(asOf) + '</div>' : '');
  }

  // Suivi hypothétique d'un contrat : référence = prime par action (cost/100).
  window.__optFollow = function (btn) {
    var d = btn.dataset;
    var mark = d.cost ? Number(d.cost) / 100 : null;
    if (mark == null || !isFinite(mark)) { if (window.VX && VX.toast) VX.toast('Prime indisponible — suivi impossible', 'error'); return; }
    fetch('/api/tracking', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ entity_type: 'OPTION', symbol: d.sym, contract_id: d.cid, mark: mark, decision: 'SURVEILLER' })
    }).then(function () { if (window.VX && VX.toast) VX.toast('Contrat ' + d.sym + ' suivi (hypothétique)', 'success'); setTimeout(function () { location.href = '/tracking'; }, 700); })
      .catch(function () { if (window.VX && VX.toast) VX.toast('Suivi impossible', 'error'); });
  };

  function radarTable(rows) {
    if (!rows || !rows.length) return '<div class="vx-empty">Aucun contrat de qualité mesurable.</div>';
    var body = rows.map(function (r) {
      var cid = [r.sym, r.exp || '', r.strike != null ? r.strike : '', r.type === 'PUT' ? 'P' : 'C'].join('|');
      var follow = r.cost != null ? '<button class="vx-btn vx-btn-sm vx-btn-ghost" data-sym="' + esc(r.sym) +
        '" data-cid="' + esc(cid) + '" data-cost="' + esc(r.cost) + '" onclick="window.__optFollow(this)">Suivre</button>' : '<span class="vx-muted">—</span>';
      return '<tr><td><b>' + esc(r.sym) + '</b></td>' +
        '<td>' + esc(r.type || '') + '</td>' +
        '<td>' + esc(r.bucket || '') + '</td>' +
        '<td>' + VXf.nd(r.strike) + '</td>' +
        '<td>' + (r.dte != null ? r.dte + ' j' : '—') + '</td>' +
        '<td>' + (r.iv != null ? VXf.num(r.iv, 1) + ' %' : '—') + '</td>' +
        '<td>' + (r.quality != null ? VXf.num(r.quality, 0) : '—') + '</td>' +
        '<td>' + (r.pop != null ? VXf.num(r.pop, 0) + ' %' : '—') + '</td>' +
        '<td>' + follow + '</td></tr>';
    }).join('');
    return '<div class="vx-table-wrap"><table class="vx-table"><thead><tr>' +
      '<th>Titre</th><th>Type</th><th>Échéance</th><th>Strike</th><th>DTE</th>' +
      '<th>IV</th><th>Qualité</th><th>PoP</th><th></th></tr></thead><tbody>' + body + '</tbody></table></div>';
  }

  function loadRadar() {
    var el = document.getElementById('vx-opt-radar-body');
    loading(el);
    get('/api/options/overview').then(function (d) {
      if (!d || d.empty) { el.innerHTML = (window.VX && VX.states) ? VX.states.empty('Tableau d’options vide.') : 'Aucune donnée.'; return; }
      el.innerHTML = radarTable(d.radar || []);
    }).catch(function (e) { fail(el, e.message); });
  }

  // ── Volatilité par titre ──────────────────────────────────────────
  function loadVolatility(sym) {
    var el = document.getElementById('vx-opt-vol-out-body');
    if (!sym) { el.innerHTML = '<div class="vx-empty">Saisis un symbole.</div>'; return; }
    loading(el);
    get('/api/options/volatility/' + encodeURIComponent(sym)).then(function (d) {
      var interp = d && d.interpretation;
      el.innerHTML = verdictCard(interp) +
        '<div class="vx-muted" style="margin-top:.6rem">Contrats analysés : ' + VXf.nd(d && d.contracts) +
        (d && d.current_iv != null ? ' · IV médiane ' + VXf.num(d.current_iv * 100, 1) + ' %' : '') + '</div>';
    }).catch(function (e) { fail(el, e.message); });
    renderVolCharts(sym);
  }

  // ── Graphiques interactifs de volatilité (§15) ────────────────────
  function clearChart(id) {
    var el = document.getElementById(id);
    if (el) el.innerHTML = '';
    return el;
  }
  var _charts = [];
  function destroyCharts() { _charts.forEach(function (c) { try { c && c.destroy && c.destroy(); } catch (e) { } }); _charts = []; }

  function renderVolCharts(sym) {
    var VC = window.VXCharts;
    var ids = ['vx-opt-term', 'vx-opt-cone', 'vx-opt-oi', 'vx-opt-smile'];
    ids.forEach(function (id) { var e = clearChart(id); if (e) e.innerHTML = '<div class="vx-skeleton" style="height:240px"></div>'; });
    if (!VC || !window.Chart) { ids.forEach(function (id) { var e = document.getElementById(id); if (e) e.innerHTML = '<div class="vx-empty">Moteur graphique indisponible.</div>'; }); return; }
    destroyCharts();
    get('/api/options/vol-charts/' + encodeURIComponent(sym)).then(function (d) {
      if (!d || d.empty) {
        ids.forEach(function (id) { var e = document.getElementById(id); if (e) e.innerHTML = (window.VX && VX.states) ? VX.states.empty('Aucun contrat pour ' + esc(sym) + ' dans le tableau.') : 'Aucune donnée.'; });
        return;
      }
      chartTerm(VC, d);
      chartCone(VC, d);
      chartOI(VC, d);
      chartSmile(VC, d);
    }).catch(function (e) {
      ids.forEach(function (id) { var el = document.getElementById(id); if (el) el.innerHTML = '<div class="vx-error-banner">⚠ ' + esc(e.message) + '</div>'; });
    });
  }

  function col(VC, name, fallback) { return (VC.colors && VC.colors[name]) || fallback; }

  // Structure par terme de l'IV — line, une série (marque).
  function chartTerm(VC, d) {
    var pts = (d.term_structure && d.term_structure.points) || [];
    if (pts.length < 2) { document.getElementById('vx-opt-term').innerHTML = '<div class="vx-card"><div class="vx-empty">Structure par terme : pas assez d’échéances.</div></div>'; return; }
    var brand = col(VC, 'brand', '#cf6128');
    var slope = d.term_structure.slope;
    var concl = slope == null ? '' : slope > 0.02 ? 'Contango — court terme meilleur marché' : slope < -0.02 ? 'Inversée — stress court terme' : 'Structure plate';
    var c = VC.card('vx-opt-term', {
      title: 'Structure par terme de l’IV', question: 'L’IV monte-t-elle ou baisse-t-elle avec l’échéance ?',
      conclusion: concl, height: 240, source: 'SCAN', timestamp: d.as_of, mode: 'delayed',
      limits: 'IV ATM approximée par le contrat le plus proche du spot',
      explain: { shows: 'IV ATM par échéance (DTE).', why: 'Une structure inversée signale un stress/événement de court terme (crush probable).', confirm: 'Pente positive et régulière.', invalidate: 'Pente fortement négative.' },
      render: function (canvas) {
        return VC.mount(canvas, {
          type: 'line',
          data: { labels: pts.map(function (p) { return p.dte + ' j'; }),
            datasets: [{ label: 'IV ATM', data: pts.map(function (p) { return +(p.iv * 100).toFixed(1); }),
              borderColor: brand, backgroundColor: brand + '22', borderWidth: 2, pointRadius: 3, pointHoverRadius: 6, tension: .2, fill: true }] },
          options: { interaction: { mode: 'index', intersect: false },
            plugins: { tooltip: { callbacks: { label: function (ctx) { return 'IV ' + ctx.parsed.y + ' %'; } } } },
            scales: { y: { ticks: { callback: function (v) { return v + ' %'; } } } } } });
      } });
    _charts.push(c);
  }

  // Cône de mouvement attendu — bandes 1σ/2σ (fill entre datasets).
  function chartCone(VC, d) {
    var pts = (d.expected_move_cone && d.expected_move_cone.points) || [];
    if (pts.length < 2) { document.getElementById('vx-opt-cone').innerHTML = '<div class="vx-card"><div class="vx-empty">Cône : pas assez d’échéances.</div></div>'; return; }
    var brand = col(VC, 'brand', '#cf6128'), copper = col(VC, 'copper', '#914b2b');
    var labels = pts.map(function (p) { return p.dte + ' j'; });
    var ds = function (key, w, fill, bg) {
      return { data: pts.map(function (p) { return p[key]; }), borderColor: w ? copper : 'transparent', borderWidth: w, pointRadius: 0, fill: fill, backgroundColor: bg, tension: .25 };
    };
    var c = VC.card('vx-opt-cone', {
      title: 'Cône de mouvement attendu', question: 'Jusqu’où le sous-jacent peut-il bouger, à 1σ et 2σ ?',
      conclusion: 'Spot ' + VXf.nd(d.spot), height: 240, source: 'SCAN', timestamp: d.as_of, mode: 'delayed',
      limits: 'σ = spot · IV_ATM · √(DTE/365) — estimation lognormale',
      legend: [{ label: '1σ', color: brand }, { label: '2σ', color: copper }],
      explain: { shows: 'Fourchette probable du spot par échéance (±1σ, ±2σ).', why: 'Situe stop et objectifs par rapport au mouvement réellement price.', confirm: 'Cible à l’intérieur de 1σ.', invalidate: 'Cible au-delà de 2σ.' },
      render: function (canvas) {
        return VC.mount(canvas, {
          type: 'line',
          data: { labels: labels, datasets: [
            ds('hi2', 0, false, 'transparent'),
            Object.assign(ds('hi1', 1, '-1', copper + '18'), {}),
            Object.assign(ds('mid', 2, '-1', brand + '20'), { borderColor: brand }),
            Object.assign(ds('lo1', 1, '-1', brand + '20'), {}),
            Object.assign(ds('lo2', 1, '-1', copper + '18'), {}) ] },
          options: { interaction: { mode: 'index', intersect: false },
            plugins: { tooltip: { callbacks: { label: function (ctx) { return ['2σ+', '1σ+', 'médian', '1σ−', '2σ−'][ctx.datasetIndex] + ' : ' + VXf.num(ctx.parsed.y, 2); } } } },
            scales: { y: { ticks: { callback: function (v) { return VXf.num(v, 0); } } } } } });
      } });
    _charts.push(c);
  }

  // Open interest par strike — bar divergente CALL / PUT.
  function chartOI(VC, d) {
    var rows = (d.oi_by_strike && d.oi_by_strike.rows) || [];
    if (!rows.length) { document.getElementById('vx-opt-oi').innerHTML = '<div class="vx-card"><div class="vx-empty">Open interest indisponible.</div></div>'; return; }
    var brand = col(VC, 'brand', '#cf6128'), violet = col(VC, 'violet', '#85609f');
    var c = VC.card('vx-opt-oi', {
      title: 'Open interest par strike', question: 'Où se concentrent les positions ouvertes ?',
      conclusion: 'CALL vs PUT', height: 240, source: 'SCAN', timestamp: d.as_of, mode: 'delayed',
      legend: [{ label: 'CALL OI', color: brand }, { label: 'PUT OI', color: violet }],
      explain: { shows: 'Open interest CALL (haut) et PUT (bas) par strike.', why: 'Les gros strikes agissent souvent comme aimants/paliers.', confirm: 'OI CALL massif au-dessus du spot.', invalidate: 'OI PUT dominant sous le spot.' },
      render: function (canvas) {
        return VC.mount(canvas, {
          type: 'bar',
          data: { labels: rows.map(function (r) { return r.strike; }),
            datasets: [
              { label: 'CALL OI', data: rows.map(function (r) { return r.call; }), backgroundColor: brand + 'cc', borderRadius: 2, maxBarThickness: 22 },
              { label: 'PUT OI', data: rows.map(function (r) { return -r.put; }), backgroundColor: violet + 'cc', borderRadius: 2, maxBarThickness: 22 } ] },
          options: { interaction: { mode: 'index', intersect: false },
            plugins: { tooltip: { callbacks: { label: function (ctx) { return ctx.dataset.label + ' : ' + VXf.num(Math.abs(ctx.parsed.y), 0); } } } },
            scales: { x: { stacked: true }, y: { stacked: true, ticks: { callback: function (v) { return VXf.num(Math.abs(v), 0); } } } } } });
      } });
    _charts.push(c);
  }

  // Smile d'IV — IV par strike (calls + puts) pour une échéance.
  function chartSmile(VC, d) {
    var sm = d.iv_smile || {};
    var calls = sm.calls || [], puts = sm.puts || [];
    if (!calls.length && !puts.length) { document.getElementById('vx-opt-smile').innerHTML = '<div class="vx-card"><div class="vx-empty">Smile indisponible.</div></div>'; return; }
    var brand = col(VC, 'brand', '#cf6128'), beige = col(VC, 'beige', '#c8ad8d');
    var strikes = {};
    calls.concat(puts).forEach(function (r) { strikes[r.strike] = 1; });
    var xs = Object.keys(strikes).map(Number).sort(function (a, b) { return a - b; });
    var mapiv = function (arr) { var m = {}; arr.forEach(function (r) { m[r.strike] = +(r.iv * 100).toFixed(1); }); return xs.map(function (x) { return m[x] != null ? m[x] : null; }); };
    var c = VC.card('vx-opt-smile', {
      title: 'Smile d’IV' + (sm.dte != null ? ' · ' + sm.dte + ' j' : ''), question: 'L’IV est-elle plus chère sur les puts (skew) ?',
      conclusion: 'Spot ' + VXf.nd(sm.spot), height: 240, source: 'SCAN', timestamp: d.as_of, mode: 'delayed',
      legend: [{ label: 'CALL IV', color: brand }, { label: 'PUT IV', color: beige }],
      explain: { shows: 'IV par strike pour une échéance (calls et puts).', why: 'Un skew put marqué révèle une demande de protection (peur).', confirm: 'Smile symétrique et bas.', invalidate: 'Skew put très pentu.' },
      render: function (canvas) {
        return VC.mount(canvas, {
          type: 'line', data: { labels: xs, datasets: [
            { label: 'CALL IV', data: mapiv(calls), borderColor: brand, backgroundColor: brand, borderWidth: 2, pointRadius: 3, pointHoverRadius: 6, spanGaps: true, tension: .2, fill: false },
            { label: 'PUT IV', data: mapiv(puts), borderColor: beige, backgroundColor: beige, borderWidth: 2, pointRadius: 3, pointHoverRadius: 6, spanGaps: true, tension: .2, fill: false } ] },
          options: { interaction: { mode: 'index', intersect: false },
            plugins: { tooltip: { callbacks: { label: function (ctx) { return ctx.dataset.label + ' : ' + (ctx.parsed.y == null ? '—' : ctx.parsed.y + ' %'); } } } },
            scales: { y: { ticks: { callback: function (v) { return v + ' %'; } } } } } });
      } });
    _charts.push(c);
  }

  // ── Scénarios du meilleur contrat (§19) ───────────────────────────
  function loadScenarios(sym) {
    var el = document.getElementById('vx-opt-sc-out-body');
    if (!sym) { el.innerHTML = '<div class="vx-empty">Saisis un symbole.</div>'; return; }
    loading(el);
    get('/api/options/scenarios/' + encodeURIComponent(sym)).then(function (d) {
      if (!d || d.empty) { el.innerHTML = (window.VX && VX.states) ? VX.states.empty(esc((d && d.reason) || 'Indisponible.')) : 'Indisponible.'; return; }
      var c = d.contract || {}, sim = d.sim || {};
      var sc = sim.scenarios || {};
      var order = ['STOP', 'BEAR', 'FLAT', 'BASE', 'TP1', 'TP2', 'TP3'];
      // Chaque scénario porte {spot, by_time_days:{'0':{value,pnl_pct},...}} :
      // on affiche l'immédiat (J+0) et un horizon (J+10) pour montrer le theta.
      var rows = order.filter(function (k) { return sc[k]; }).map(function (k) {
        var s = sc[k]; var bt = s.by_time_days || {};
        var d0 = bt['0'] || {}, d10 = bt['10'] || bt['15'] || {};
        var g = d0.pnl_pct, g10 = d10.pnl_pct;
        var cls = g == null ? '' : (g >= 0 ? 'vx-pos' : 'vx-neg');
        var cls10 = g10 == null ? '' : (g10 >= 0 ? 'vx-pos' : 'vx-neg');
        return '<tr><td><b>' + esc(k) + '</b></td>' +
          '<td>' + (s.spot != null ? VXf.num(s.spot, 2) : '—') + '</td>' +
          '<td>' + (d0.value != null ? VXf.num(d0.value, 2) : '—') + '</td>' +
          '<td class="' + cls + '">' + (g != null ? (g >= 0 ? '+' : '') + VXf.num(g, 0) + ' %' : '—') + '</td>' +
          '<td class="' + cls10 + '">' + (g10 != null ? (g10 >= 0 ? '+' : '') + VXf.num(g10, 0) + ' %' : '—') + '</td></tr>';
      }).join('');
      var lims = (sim.limitations || []).map(function (l) { return '<li>' + esc(l) + '</li>'; }).join('');
      el.innerHTML =
        '<div class="vx-muted" style="margin-bottom:.6rem">Contrat : ' + esc(c.type || '') + ' ' + VXf.nd(c.strike) +
        ' · ' + (c.dte != null ? c.dte + ' j' : '—') + ' · IV ' + (c.iv != null ? VXf.num(c.iv, 1) + ' %' : '—') +
        ' · spot ' + VXf.nd(c.spot) + '</div>' +
        (rows ? '<div class="vx-table-wrap"><table class="vx-table"><thead><tr><th>Scénario</th><th>Spot</th><th>Prime (J+0)</th><th>Gain J+0</th><th>Gain J+10</th></tr></thead><tbody>' + rows + '</tbody></table></div>' : '<div class="vx-empty">Grille de scénarios indisponible.</div>') +
        (sim.reward_risk != null ? '<div class="vx-muted" style="margin-top:.5rem">R:R du plan : <b>' + VXf.num(sim.reward_risk, 2) + '</b> · pire perte planifiée : ' + (sim.worst_planned_loss_pct != null ? VXf.num(sim.worst_planned_loss_pct, 0) + ' %' : '—') + '</div>' : '') +
        '<div class="vx-explain" style="margin-top:.8rem"><h4>Limites (estimation)</h4><ul>' + (lims || '<li class="vx-muted">—</li>') + '</ul>' +
        (sim.model_source ? '<p class="vx-muted">Modèle : ' + esc(sim.model_source) + '</p>' : '') + '</div>';
    }).catch(function (e) { fail(el, e.message); });
  }

  // ── Événements par titre ──────────────────────────────────────────
  function loadEvents(sym) {
    var el = document.getElementById('vx-opt-ev-out-body');
    if (!sym) { el.innerHTML = '<div class="vx-empty">Saisis un symbole.</div>'; return; }
    loading(el);
    get('/api/options/event-risk/' + encodeURIComponent(sym)).then(function (d) {
      el.innerHTML = verdictCard(d && d.interpretation);
    }).catch(function (e) { fail(el, e.message); });
  }

  // ── Câblage ───────────────────────────────────────────────────────
  function view() {
    var lbl = document.querySelector('[data-page-label]');
    var v = lbl ? (lbl.dataset.pageLabel || '') : '';
    var m = v.split(':')[1] || 'overview';
    return m;
  }

  function bindExplain() {
    document.body.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('[data-explain]') : null;
      if (!b) return;
      var map = { overview: 'options.overview_mix', volatility: 'options.volatility', event_risk: 'options.event_risk', environment: 'options.environment' };
      explainDrawer(LAST[map[b.dataset.explain]]);
    });
  }

  function init() {
    bindExplain();
    var v = view();
    if (v === 'overview') loadOverview();
    else if (v === 'radar') loadRadar();
    else if (v === 'volatility') {
      var g = document.getElementById('vx-opt-vol-go');
      var s = document.getElementById('vx-opt-vol-sym');
      if (g) g.addEventListener('click', function () { loadVolatility((s.value || '').trim().toUpperCase()); });
      if (s) s.addEventListener('keydown', function (e) { if (e.key === 'Enter') loadVolatility((s.value || '').trim().toUpperCase()); });
    } else if (v === 'events') {
      var g2 = document.getElementById('vx-opt-ev-go');
      var s2 = document.getElementById('vx-opt-ev-sym');
      if (g2) g2.addEventListener('click', function () { loadEvents((s2.value || '').trim().toUpperCase()); });
      if (s2) s2.addEventListener('keydown', function (e) { if (e.key === 'Enter') loadEvents((s2.value || '').trim().toUpperCase()); });
    } else if (v === 'scenarios') {
      var g3 = document.getElementById('vx-opt-sc-go');
      var s3 = document.getElementById('vx-opt-sc-sym');
      if (g3) g3.addEventListener('click', function () { loadScenarios((s3.value || '').trim().toUpperCase()); });
      if (s3) s3.addEventListener('keydown', function (e) { if (e.key === 'Enter') loadScenarios((s3.value || '').trim().toUpperCase()); });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
