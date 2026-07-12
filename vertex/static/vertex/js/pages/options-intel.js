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
      (asOf ? '<div class="vx-muted" style="margin-top:.5rem">Scan : ' + esc(asOf) + '</div>' : '');
  }

  function radarTable(rows) {
    if (!rows || !rows.length) return '<div class="vx-empty">Aucun contrat de qualité mesurable.</div>';
    var body = rows.map(function (r) {
      return '<tr><td><b>' + esc(r.sym) + '</b></td>' +
        '<td>' + esc(r.type || '') + '</td>' +
        '<td>' + esc(r.bucket || '') + '</td>' +
        '<td>' + VXf.nd(r.strike) + '</td>' +
        '<td>' + (r.dte != null ? r.dte + ' j' : '—') + '</td>' +
        '<td>' + (r.iv != null ? VXf.num(r.iv, 1) + ' %' : '—') + '</td>' +
        '<td>' + (r.quality != null ? VXf.num(r.quality, 0) : '—') + '</td>' +
        '<td>' + (r.pop != null ? VXf.num(r.pop, 0) + ' %' : '—') + '</td></tr>';
    }).join('');
    return '<div class="vx-table-wrap"><table class="vx-table"><thead><tr>' +
      '<th>Titre</th><th>Type</th><th>Échéance</th><th>Strike</th><th>DTE</th>' +
      '<th>IV</th><th>Qualité</th><th>PoP</th></tr></thead><tbody>' + body + '</tbody></table></div>';
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
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
