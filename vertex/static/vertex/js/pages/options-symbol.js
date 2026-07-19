/* options-symbol.js — DOSSIER OPTIONS d'un titre (« machine d'analyse »).
 * Lit /scan (options_board), /api/options/vol-charts/<sym>, /api/options/
 * scenarios/<sym> et /api/options/strategies/<sym>. Chaque section peint dès
 * que sa donnée arrive ; états vides honnêtes — aucun chiffre inventé. */
(function () {
  'use strict';
  var root = document.getElementById('vx-osym-root'); if (!root) return;
  var SYM = root.dataset.sym || '';
  var VXf = (window.VX && VX.fmt) || { nd: function (v) { return v == null ? '—' : v; }, num: function (v, d) { return v == null ? '—' : Number(v).toFixed(d == null ? 2 : d); }, price: function (v) { return v == null ? '—' : Number(v).toFixed(2); }, pct: function (v, d) { return v == null ? '—' : (v > 0 ? '+' : '') + Number(v).toFixed(d == null ? 1 : d) + ' %'; } };

  function esc(s) { return String(s == null ? '' : s).replace(/[<>&"]/g, function (c) { return { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]; }); }
  function body(id, html) { var el = document.querySelector('#' + id + ' [data-body]'); if (el) el.innerHTML = html; }
  function empty(msg) { return (window.VX && VX.states) ? VX.states.empty(msg) : '<div class="vx-empty">' + esc(msg) + '</div>'; }
  function ready(fn) { if (window.VXCharts && window.Chart) return fn(); var n = 0, iv = setInterval(function () { if ((window.VXCharts && window.Chart) || ++n > 80) { clearInterval(iv); if (window.VXCharts && window.Chart) fn(); } }, 100); }
  function get(url) { return (window.VX && VX.fetch) ? VX.fetch(url, { ttl: 60000 }) : fetch(url).then(function (r) { return r.json(); }); }
  function microBar(val, unit, col) {
    if (val == null || isNaN(val)) return '<td>—</td>';
    var w = Math.max(4, Math.min(100, Math.abs(val)));
    return '<td><span style="display:inline-flex;align-items:center;gap:6px">' +
      '<span style="flex:0 0 34px;height:5px;border-radius:99px;background:var(--vx-surface-0);position:relative;overflow:hidden">' +
      '<i style="position:absolute;left:0;top:0;bottom:0;width:' + w + '%;background:' + col + ';border-radius:99px"></i></span>' +
      '<b class="vx-mono" style="font-weight:600">' + Math.round(val) + (unit || '') + '</b></span></td>';
  }
  var VIOLET = 'var(--vx-violet)', BRAND = 'var(--vx-brand)';

  /* ── Scorecard de chaîne (depuis le board réel) ─────────────────── */
  function paintScorecard(board, spot) {
    var host = document.getElementById('vx-osym-scorecard'); if (!host) return;
    var mine = board.filter(function (c) { return c.sym === SYM; });
    var spotEl = document.getElementById('vx-osym-spot');
    if (spotEl && spot != null) spotEl.textContent = '$' + VXf.price(spot);
    if (!mine.length) {
      host.innerHTML = empty('Aucun contrat ' + SYM + ' dans le tableau d’options courant (scan limité ou hors séance).');
      body('vx-osym-chain', empty('Chaîne indisponible pour ' + SYM + '.'));
      return;
    }
    var calls = mine.filter(function (c) { return c.type === 'CALL'; }).length;
    var puts = mine.length - calls;
    var cp = Math.round(calls / mine.length * 100);
    var qmax = Math.max.apply(null, mine.map(function (c) { return c.quality || 0; }));
    var pmax = Math.max.apply(null, mine.map(function (c) { return c.pop || 0; }));
    var ivs = mine.map(function (c) { return c.iv; }).filter(function (x) { return x != null; }).sort(function (a, b) { return a - b; });
    var ivMed = ivs.length ? ivs[Math.floor(ivs.length / 2)] : null;
    var oiTot = mine.reduce(function (s, c) { return s + (c.oi || 0); }, 0);
    var dtes = mine.map(function (c) { return c.dte; }).filter(function (x) { return x != null; });
    var costs = mine.map(function (c) { return c.cost; }).filter(function (x) { return x != null; });
    /* Demande par strike (OI cumulé) & contrats les plus risqués — sur les contrats
       RÉELLEMENT disponibles (honnête : rien si aucun OI publié / hors séance). */
    var oiByStrike = {};
    mine.forEach(function (c) { if (c.oi) oiByStrike[c.strike] = (oiByStrike[c.strike] || 0) + c.oi; });
    var topStrike = Object.keys(oiByStrike).map(function (k) { return [k, oiByStrike[k]]; }).sort(function (a, b) { return b[1] - a[1]; })[0];
    var risky = mine.filter(function (c) { return (c.danger_n != null || c.danger != null); })
      .slice().sort(function (a, b) { return (b.danger_n || b.danger || 0) - (a.danger_n || a.danger || 0); }).slice(0, 3);
    var G = window.VXCharts && VXCharts.scoreGaugeSVG;
    var gauges = G ? ('<div class="vx-gaugecluster">' +
      G(qmax, { label: 'meilleure qualité' }) +
      G(pmax, { label: 'meilleure PoP' }) +
      G(ivMed != null ? Math.min(100, ivMed) : null, { label: 'IV médiane %', invert: true }) +
      '</div>') : '';
    var m = function (k, v, u) { return '<div class="vx-metric"><span class="vx-metric-k">' + k + '</span><span class="vx-metric-v">' + (v == null ? '—' : v) + (u ? '<span class="vx-metric-u">' + u + '</span>' : '') + '</span></div>'; };
    host.innerHTML = '<div class="vx-scorecard" style="grid-template-columns:auto minmax(0,1fr)">' + gauges +
      '<div class="vx-scorecard-side">' +
      '<div class="vx-metricgrid">' +
      m('Contrats', mine.length) + m('CALLS', calls) + m('PUTS', puts) +
      m('Open interest', oiTot ? oiTot.toLocaleString('fr-FR') : null) +
      m('DTE', dtes.length ? (Math.min.apply(null, dtes) + '–' + Math.max.apply(null, dtes)) : null, ' j') +
      m('Coût min', costs.length ? VXf.price(Math.min.apply(null, costs)) : null, ' $') +
      m('Strike le + demandé', topStrike ? ('$' + topStrike[0]) : null, topStrike ? (' · OI ' + Number(topStrike[1]).toLocaleString('fr-FR')) : '') +
      '</div>' +
      '<div class="vx-mt2"><span class="vx-metric-k" style="display:block;margin-bottom:3px">Contrats les plus risqués</span>' +
      (risky.length ? risky.map(function (c) { return '<span class="vx-badge" style="color:var(--vx-warning);margin:2px" title="danger ' + (c.danger_n || c.danger) + '">' + c.type + ' ' + c.strike + (c.exp ? ' · ' + esc(c.exp) : '') + '</span>'; }).join('') : '<span class="vx-meta">— aucun contrat à risque élevé —</span>') +
      '</div>' +
      '<div class="vx-stackbar-legend" style="justify-content:space-between;margin:10px 0 6px">' +
      '<span><i style="background:' + BRAND + '"></i>CALLS ' + calls + ' <b>' + cp + '%</b></span>' +
      '<span><i style="background:' + VIOLET + '"></i>PUTS ' + puts + ' <b>' + (100 - cp) + '%</b></span></div>' +
      '<div class="vx-stackbar"><i style="width:' + cp + '%;background:' + BRAND + '"></i><i style="width:' + (100 - cp) + '%;background:' + VIOLET + '"></i></div>' +
      '</div></div>';
    paintChain(mine);
  }

  /* ── Chaîne complète du titre ───────────────────────────────────── */
  window.__osymFollow = function (btn) {
    var d = btn.dataset, mark = d.cost ? Number(d.cost) / 100 : null;
    if (mark == null || !isFinite(mark)) { if (window.VX && VX.toast) VX.toast('Prime indisponible', 'error'); return; }
    fetch('/api/tracking', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ entity_type: 'OPTION', symbol: SYM, contract_id: d.cid, mark: mark, decision: 'SURVEILLER' }) })
      .then(function () { if (window.VX && VX.toast) VX.toast('Contrat suivi (hypothétique)', 'success'); })
      .catch(function () { if (window.VX && VX.toast) VX.toast('Suivi impossible', 'error'); });
  };
  function paintChain(mine) {
    var meta = document.getElementById('vx-osym-chain-meta');
    if (meta) meta.textContent = mine.length + ' contrat(s) · scan réel';
    var rows = mine.slice().sort(function (a, b) { return (b.quality || 0) - (a.quality || 0); }).map(function (c) {
      var cid = [c.sym, c.exp || '', c.strike != null ? c.strike : '', c.type === 'PUT' ? 'P' : 'C'].join('|');
      return '<tr title="' + esc(c.why || '') + '">' +
        '<td><span class="vx-badge" style="color:' + (c.type === 'PUT' ? VIOLET : 'var(--vx-text-secondary)') + '">' + esc(c.type || '') + '</span></td>' +
        '<td class="vx-num vx-mono">' + VXf.nd(c.strike) + '</td>' +
        '<td class="vx-mono" style="font-size:11.5px">' + esc(String(c.exp || '').slice(0, 10)) + '</td>' +
        '<td class="vx-num vx-mono">' + (c.dte != null ? c.dte + ' j' : '—') + '</td>' +
        '<td class="vx-num vx-mono">' + (c.delta != null ? VXf.num(c.delta, 2) : '—') + '</td>' +
        '<td class="vx-num vx-mono">' + (c.iv != null ? VXf.num(c.iv, 1) + ' %' : '—') + '</td>' +
        '<td class="vx-num vx-mono">' + (c.cost != null ? VXf.price(c.cost) + ' $' : '—') + '</td>' +
        '<td class="vx-num vx-mono">' + (c.oi != null ? c.oi.toLocaleString('fr-FR') : '—') + '</td>' +
        '<td class="vx-num vx-mono' + (c.spread_pct > 5 ? ' vx-warn' : '') + '">' + (c.spread_pct != null ? VXf.num(c.spread_pct, 1) + ' %' : '—') + '</td>' +
        microBar(c.pop, '%', BRAND) +
        microBar(c.quality, '', (c.quality >= 66 ? 'var(--vx-positive)' : c.quality >= 45 ? 'var(--vx-warning)' : 'var(--vx-negative)')) +
        '<td><button class="vx-btn vx-btn-sm vx-btn-ghost" data-cid="' + esc(cid) + '" data-cost="' + esc(c.cost) + '" onclick="window.__osymFollow(this)">Suivre</button></td></tr>';
    }).join('');
    body('vx-osym-chain', '<div class="vx-table-wrap"><table class="vx-table"><thead><tr>' +
      '<th>Type</th><th class="vx-num">Strike</th><th>Échéance</th><th class="vx-num">DTE</th><th class="vx-num">Delta</th>' +
      '<th class="vx-num">IV</th><th class="vx-num">Coût</th><th class="vx-num">OI</th><th class="vx-num">Spread</th>' +
      '<th>PoP</th><th>Qualité</th><th></th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
      '<div class="vx-meta vx-mt2">Survole une ligne pour lire le « pourquoi » du moteur · spread ambre = liquidité coûteuse.</div>');
  }

  /* ── Volatilité : 4 graphiques ──────────────────────────────────── */
  function paintVol(d) {
    var it = d.interpretation || {};
    var tone = /élevée|cher|stress/i.test(it.dominant_reading || '') ? 'risk' : 'ai';
    body('vx-osym-verdict',
      (it.dominant_reading ? '<div class="vx-insight" data-tone="' + tone + '"><b>' + esc(it.dominant_reading) + '</b>' +
        (it.action ? ' — ' + esc(it.action) : '') + '</div>' : empty('Interprétation indisponible.')) +
      '<div class="vx-meta vx-mt2">Contrats analysés : ' + VXf.nd(d.contracts) + (it.confidence != null ? ' · confiance ' + Math.round(it.confidence * 100) + ' %' : '') + '</div>');
    var envB = document.getElementById('vx-osym-envbadge');
    if (envB && d.contracts != null) envB.textContent = d.contracts + ' contrat(s) analysés';
    ready(function () {
      var cc = VXCharts.colors;
      var ts = (d.term_structure && d.term_structure.points) || [];
      if (ts.length >= 2) VXCharts.card('vx-osym-term', {
        title: 'Structure par terme de l’IV', question: 'L’IV monte-t-elle ou baisse-t-elle avec l’échéance ?',
        conclusion: (d.term_structure.slope < 0 ? 'Inversée — stress court terme' : 'Normale — prime au temps long'), height: 220,
        source: 'scan', timestamp: Date.now(), mode: 'delayed',
        render: function (cv) { return VXCharts.mount(cv, { type: 'line',
          data: { labels: ts.map(function (p) { return p.dte + ' j'; }), datasets: [{ data: ts.map(function (p) { return p.iv * 100; }), borderColor: cc.brand, backgroundColor: 'rgba(201,205,212,.12)', fill: true, tension: .3, pointRadius: 4, pointBackgroundColor: cc.brand }] },
          options: { scales: { y: { ticks: { callback: function (v) { return v + ' %'; } }, grid: { color: 'rgba(255,255,255,.05)' } }, x: { grid: { display: false } } } } }); } });
      else document.getElementById('vx-osym-term').innerHTML = '';
      var cn = (d.expected_move_cone && d.expected_move_cone.points) || [];
      if (cn.length >= 2) {
        var mk = function (key, col, w, dash) { return { data: cn.map(function (p) { return p[key]; }), borderColor: col, borderWidth: w, borderDash: dash || [], pointRadius: 0, fill: false, tension: .2 }; };
        VXCharts.card('vx-osym-cone', {
          title: 'Cône de mouvement attendu', question: 'Jusqu’où ' + SYM + ' peut-il bouger à 1σ et 2σ ?',
          conclusion: 'Spot ' + VXf.price(d.spot), height: 220, source: 'scan · σ = spot·IV·√(DTE/365)', timestamp: Date.now(), mode: 'delayed',
          legend: [{ label: '1σ', color: cc.brand }, { label: '2σ', color: cc.neutral }],
          render: function (cv) { return VXCharts.mount(cv, { type: 'line',
            data: { labels: cn.map(function (p) { return p.dte + ' j'; }), datasets: [mk('hi2', cc.neutral, 1, [4, 4]), mk('hi1', cc.brand, 1.4), mk('mid', cc.positive, 2), mk('lo1', cc.brand, 1.4), mk('lo2', cc.neutral, 1, [4, 4])] },
            options: { scales: { y: { grid: { color: 'rgba(255,255,255,.05)' } }, x: { grid: { display: false } } } } }); } });
      } else document.getElementById('vx-osym-cone').innerHTML = '';
      var oi = (d.oi_by_strike && d.oi_by_strike.rows) || [];
      if (oi.length) VXCharts.card('vx-osym-oi', {
        title: 'Open interest par strike', question: 'Où se concentrent les positions ouvertes ?',
        conclusion: 'CALL vs PUT · spot ' + VXf.price(d.spot), height: 220, source: 'scan', timestamp: Date.now(), mode: 'delayed',
        legend: [{ label: 'CALL OI', color: '#c9cdd4' }, { label: 'PUT OI', color: '#9c79d0' }],
        render: function (cv) { return VXCharts.mount(cv, { type: 'bar',
          data: { labels: oi.map(function (r) { return r.strike; }), datasets: [
            { label: 'CALL', data: oi.map(function (r) { return r.call; }), backgroundColor: 'rgba(201,205,212,.8)' },
            { label: 'PUT', data: oi.map(function (r) { return r.put; }), backgroundColor: 'rgba(156,121,208,.8)' }] },
          options: { scales: { y: { grid: { color: 'rgba(255,255,255,.05)' } }, x: { grid: { display: false } } } } }); } });
      else document.getElementById('vx-osym-oi').innerHTML = '';
      var sm = d.iv_smile || {}; var smC = sm.calls || [], smP = sm.puts || [];
      if (smC.length + smP.length >= 2) VXCharts.card('vx-osym-smile', {
        title: 'Smile d’IV · ' + (sm.dte != null ? sm.dte + ' j' : ''), question: 'L’IV est-elle plus chère sur les puts (skew) ?',
        conclusion: 'Spot ' + VXf.price(sm.spot), height: 220, source: 'scan', timestamp: Date.now(), mode: 'delayed',
        legend: [{ label: 'CALL IV', color: '#c9cdd4' }, { label: 'PUT IV', color: '#9c79d0' }],
        render: function (cv) { return VXCharts.mount(cv, { type: 'scatter',
          data: { datasets: [
            { data: smC.map(function (p) { return { x: p.strike, y: p.iv * 100 }; }), pointBackgroundColor: '#c9cdd4', pointRadius: 5 },
            { data: smP.map(function (p) { return { x: p.strike, y: p.iv * 100 }; }), pointBackgroundColor: '#9c79d0', pointRadius: 5 }] },
          options: { scales: { y: { ticks: { callback: function (v) { return v + ' %'; } }, grid: { color: 'rgba(255,255,255,.05)' } }, x: { grid: { color: 'rgba(255,255,255,.04)' } } } } }); } });
      else document.getElementById('vx-osym-smile').innerHTML = '<div class="vx-card">' + empty('Smile indisponible (trop peu de strikes cotés).') + '</div>';
    });
  }

  /* ── Scénarios × horizon + décote + sensibilité IV ──────────────── */
  function paintScenarios(d) {
    var sim = d.sim || {}, ct = d.contract || {};
    var meta = document.getElementById('vx-osym-sc-meta');
    if (meta && ct.type) meta.textContent = ct.type + ' ' + ct.strike + ' · ' + (ct.dte != null ? ct.dte + ' j' : '') + ' · IV ' + VXf.num(ct.iv, 1) + ' % · spot ' + VXf.price(ct.spot);
    var rows = [], seen = {};
    var add = function (label, node) { if (node && node.by_time_days && !seen[label]) { seen[label] = 1; rows.push({ label: label, node: node.by_time_days }); } };
    /* sim.scenarios porte souvent déjà tout (STOP/BEAR/FLAT/BASE/TP1-3) — ordre
       lisible du pire au meilleur, puis repli sur les noeuds at_* sans doublon. */
    var sc = sim.scenarios || {};
    ['STOP', 'BEAR', 'FLAT', 'BASE', 'TP1', 'TP2', 'TP3'].forEach(function (k) { add(k, sc[k]); });
    Object.keys(sc).forEach(function (k) { add(k, sc[k]); });
    add('STOP', sim.at_stop); add('TP1', sim.at_tp1); add('TP2', sim.at_tp2); add('TP3', sim.at_tp3);
    if (!rows.length) { body('vx-osym-scenarios', empty('Scénarios indisponibles pour ' + SYM + ' (aucun contrat exploitable).')); return; }
    var days = Object.keys(rows[0].node).map(Number).sort(function (a, b) { return a - b; });
    /* le conteneur DOIT exister avant heatmapCard (ready peut être synchrone) */
    body('vx-osym-scenarios', '<div id="vx-osym-scenarios-hm"></div>' +
      (sim.reward_risk != null ? '<div class="vx-meta vx-mt2">R:R du plan sur le contrat : <b class="vx-mono">' + VXf.num(sim.reward_risk, 2) + '</b>' + (sim.worst_planned_loss_pct != null ? ' · pire perte planifiée ' + VXf.pct(sim.worst_planned_loss_pct, 1) : '') + '</div>' : ''));
    ready(function () {
      VXCharts.heatmapCard('vx-osym-scenarios-hm', {
        title: '', columns: days.map(function (j) { return 'J+' + j; }),
        rows: rows.map(function (r) { return { label: r.label, cells: days.map(function (j) { var c = r.node[String(j)] || {}; return { value: c.pnl_pct, label: c.pnl_pct != null ? Math.round(c.pnl_pct) + ' %' : '—', title: r.label + ' J+' + j + ' : ' + (c.pnl_pct != null ? c.pnl_pct + ' % (valeur ' + c.value + ')' : 'n/d') }; }) }; }),
        min: -80, max: 80, source: 'scenario_pricer (MODEL_ESTIMATE)', timestamp: Date.now(), mode: 'delayed',
        limits: 'estimation modèle Black-Scholes — pas une promesse'
      });
      var td = sim.time_decay || [];
      if (td.length >= 2) VXCharts.card('vx-osym-decay', {
        title: 'Décote temps (theta)', question: 'Combien le temps grignote-t-il la prime, à spot figé ?', height: 200,
        source: 'scenario_pricer', timestamp: Date.now(), mode: 'delayed',
        render: function (cv) { return VXCharts.mount(cv, { type: 'line',
          data: { labels: td.map(function (p) { return 'J+' + p.days; }), datasets: [{ data: td.map(function (p) { return p.value; }), borderColor: VXCharts.colors.warning, backgroundColor: 'rgba(221,162,59,.12)', fill: true, tension: .25, pointRadius: 2 }] },
          options: { scales: { y: { grid: { color: 'rgba(255,255,255,.05)' } }, x: { grid: { display: false } } } } }); } });
      var iv = sim.iv_sensitivity || [];
      if (iv.length >= 2) VXCharts.card('vx-osym-ivsens', {
        title: 'Sensibilité à l’IV', question: 'Quel impact d’une variation d’implicite sur la prime ?', height: 200,
        source: 'scenario_pricer', timestamp: Date.now(), mode: 'delayed',
        render: function (cv) { return VXCharts.mount(cv, { type: 'bar',
          data: { labels: iv.map(function (p) { return (p.iv_shift_pct > 0 ? '+' : '') + p.iv_shift_pct + ' %'; }), datasets: [{ data: iv.map(function (p) { return p.pnl_pct; }), backgroundColor: iv.map(function (p) { return p.pnl_pct >= 0 ? 'rgba(54,200,137,.8)' : 'rgba(237,101,92,.8)'; }) }] },
          options: { scales: { y: { ticks: { callback: function (v) { return v + ' %'; } }, grid: { color: 'rgba(255,255,255,.05)' } }, x: { grid: { display: false } } } } }); } });
    });
  }

  /* ── Stratégies multi-jambes ────────────────────────────────────── */
  function paintStrats(d) {
    var list = (d.strategies || []).filter(function (s) { return s && s.available !== false; });
    if (!list.length) { body('vx-osym-strats', empty(d.reason || 'Aucune stratégie constructible depuis le board pour ' + SYM + '.')); return; }
    var html = '<div class="vx-grid">' + list.slice(0, 4).map(function (s, i) {
      var pop = s.probability_of_profit != null ? Math.round(s.probability_of_profit * (s.probability_of_profit <= 1 ? 100 : 1)) : null;
      return '<div class="vx-card vx-col-6' + (s.recommended ? ' vx-active' : '') + '">' +
        '<div class="vx-card-header"><span class="vx-card-title">' + esc(s.label || s.name || 'Stratégie') + '</span>' +
        (s.recommended ? '<span class="vx-badge" style="color:var(--vx-brand-strong)">★ Recommandée</span>' : '') +
        '<span class="vx-badge" style="color:' + VIOLET + '">' + (s.is_credit ? 'crédit' : 'débit') + ' ' + (s.net_premium != null ? VXf.price(Math.abs(s.net_premium)) + ' $' : '') + '</span></div>' +
        '<div id="vx-osym-strat-pf-' + i + '" style="height:140px"><canvas></canvas></div>' +
        '<div class="vx-metricgrid vx-mt2" style="grid-template-columns:repeat(4,1fr)">' +
        '<div class="vx-metric"><span class="vx-metric-k">PoP</span><span class="vx-metric-v">' + (pop != null ? pop + '<span class="vx-metric-u">%</span>' : '—') + '</span></div>' +
        '<div class="vx-metric" data-tone="pos"><span class="vx-metric-k">Gain max</span><span class="vx-metric-v" style="font-size:15px">' + (s.max_profit_unbounded ? 'illimité' : (s.max_profit != null ? VXf.price(s.max_profit) + ' $' : '—')) + '</span></div>' +
        '<div class="vx-metric" data-tone="neg"><span class="vx-metric-k">Perte max</span><span class="vx-metric-v" style="font-size:15px">' + (s.max_loss != null ? VXf.price(s.max_loss) + ' $' : '—') + '</span></div>' +
        '<div class="vx-metric"><span class="vx-metric-k">Breakeven</span><span class="vx-metric-v" style="font-size:15px">' + ((s.breakevens || []).map(function (b) { return VXf.price(b); }).join(' · ') || '—') + '</span></div></div>' +
        (s.greeks ? '<div class="vx-meta vx-mt1">Δ ' + VXf.num(s.greeks.delta, 2) + ' · Θ ' + VXf.num(s.greeks.theta, 2) + '/j · Vega ' + VXf.num(s.greeks.vega, 1) + '</div>' : '') +
        '</div>';
    }).join('') + '</div>' +
      '<div class="vx-meta vx-mt2">Payoff à l’échéance ; PoP = modèle lognormal risque-neutre — estimation, pas une promesse. <a class="vx-btn vx-btn-sm vx-btn-ghost" href="/options?view=scenarios">Constructeur complet →</a></div>';
    body('vx-osym-strats', html);
    ready(function () {
      list.slice(0, 4).forEach(function (s, i) {
        var pts = s.payoff || []; var host = document.getElementById('vx-osym-strat-pf-' + i);
        if (!host || pts.length < 2) { if (host) host.innerHTML = ''; return; }
        VXCharts.mount(host.querySelector('canvas'), { type: 'line',
          data: { labels: pts.map(function (p) { return p.price; }), datasets: [{ data: pts.map(function (p) { return p.pnl; }), borderColor: VXCharts.colors.neutral, borderWidth: 1.8, pointRadius: 0, fill: false,
            segment: { borderColor: function (ctx) { return ctx.p1.parsed.y >= 0 ? VXCharts.colors.positive : VXCharts.colors.negative; } } }] },
          options: { scales: { y: { grid: { color: 'rgba(255,255,255,.05)' } }, x: { ticks: { maxTicksLimit: 6 }, grid: { display: false } } }, plugins: { tooltip: { callbacks: { label: function (it) { return 'P&L ' + VXf.price(it.parsed.y) + ' $ @ ' + it.label; } } } } } });
      });
    });
  }

  /* ── Max pain / murs d'OI (chaîne LARGE réelle IBKR) ───────────── */
  function fmtOI(v) { return v == null ? '—' : Number(v).toLocaleString('fr-FR'); }
  function dte(exp) { try { var d = Math.round((new Date(exp + 'T00:00:00') - Date.now()) / 864e5); return d >= 0 ? d : null; } catch (e) { return null; } }
  function paintMaxPain(d) {
    if (!d || d.available === false) {
      body('vx-osym-maxpain', empty((d && d.note) || 'Open interest par strike indisponible (TWS fermé, hors séance, ou titre pas encore chargé).'));
      return;
    }
    var exps = (d.expiries || []).filter(function (e) { return e && e.max_pain != null; });
    if (!exps.length) { body('vx-osym-maxpain', empty('Open interest par strike insuffisant pour établir un max pain (chaîne trop courte).')); return; }
    var spot = d.spot || 0;
    var meta = document.getElementById('vx-osym-mp-meta');
    if (meta) meta.textContent = 'chaîne réelle IBKR' + (d.ts ? ' · ' + new Date(d.ts * 1000).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }) : '');
    var pcr = d.pcr, near = exps[0];
    var dist = (spot && near.max_pain) ? ((near.max_pain / spot - 1) * 100) : null;
    var distTxt = dist == null ? '' : (dist >= 0 ? '+' : '') + dist.toFixed(1) + ' %';
    var pcrTone = pcr == null ? 'neu' : (pcr > 1.15 ? 'neg' : (pcr < 0.85 ? 'pos' : 'warn'));
    var pcrRead = pcr == null ? '' : (pcr > 1.1 ? 'puts dominants (couverture / prudence)' : (pcr < 0.9 ? 'calls dominants (appétit haussier)' : 'équilibré'));
    var lead = spot && near.max_pain
      ? 'À l’échéance <b>' + esc(near.exp) + '</b>, la masse d’open interest tire ' + SYM + ' vers <b class="vx-mono">$' + VXf.price(near.max_pain) + '</b>'
        + (dist != null ? ' — soit <b>' + distTxt + '</b> ' + (Math.abs(dist) < 0.5 ? 'quasi sur le prix' : (dist < 0 ? 'sous le prix' : 'au-dessus du prix')) + ' (' + '$' + VXf.price(spot) + ').' : '.')
      : 'Max pain établi sur la chaîne réelle IBKR.';

    // Métriques agrégées
    var head = '<p class="vx-lead" style="margin:0 0 var(--vx-s3)">' + lead + '</p>' +
      '<div class="vx-metricgrid" style="grid-template-columns:repeat(4,1fr)">' +
      '<div class="vx-metric" data-tone="' + (spot && near.max_pain ? (Math.abs(dist) < 0.5 ? 'warn' : (dist < 0 ? 'neg' : 'pos')) : 'neu') + '"><span class="vx-metric-k">Max pain proche</span><span class="vx-metric-v">' + (near.max_pain != null ? '$' + VXf.price(near.max_pain) : '—') + '</span><span class="vx-metric-u">' + (distTxt || 'vs prix') + '</span></div>' +
      '<div class="vx-metric"><span class="vx-metric-k">OI CALL total</span><span class="vx-metric-v" style="color:' + VIOLET + '">' + fmtOI(d.total_call_oi) + '</span></div>' +
      '<div class="vx-metric"><span class="vx-metric-k">OI PUT total</span><span class="vx-metric-v" style="color:var(--vx-silver-2,#9aa0a8)">' + fmtOI(d.total_put_oi) + '</span></div>' +
      '<div class="vx-metric" data-tone="' + pcrTone + '"><span class="vx-metric-k">PCR (OI)</span><span class="vx-metric-v">' + (pcr == null ? '—' : pcr.toFixed(2)) + '</span><span class="vx-metric-u">' + esc(pcrRead) + '</span></div></div>';

    // Tableau par échéance
    var rows = exps.slice(0, 6).map(function (e) {
      var dd = dte(e.exp), di = (spot && e.max_pain) ? ((e.max_pain / spot - 1) * 100) : null;
      var w = (e.walls || [])[0] || {};
      return '<tr>' +
        '<td class="vx-mono">' + esc(e.exp) + (dd != null ? ' <span class="vx-meta">' + dd + 'j</span>' : '') + '</td>' +
        '<td class="vx-mono" style="font-weight:700">$' + VXf.price(e.max_pain) + (di != null ? ' <span class="vx-meta" style="color:' + (di < 0 ? 'var(--vx-negative)' : 'var(--vx-positive)') + '">' + (di >= 0 ? '+' : '') + di.toFixed(1) + '%</span>' : '') + '</td>' +
        '<td class="vx-mono" style="text-align:right;color:' + VIOLET + '">' + fmtOI(e.call_oi) + '</td>' +
        '<td class="vx-mono" style="text-align:right">' + fmtOI(e.put_oi) + '</td>' +
        '<td class="vx-mono" style="text-align:right;color:' + (e.pcr != null && e.pcr > 1.1 ? 'var(--vx-caution)' : (e.pcr != null && e.pcr < 0.9 ? 'var(--vx-positive)' : 'inherit')) + '">' + (e.pcr == null ? '—' : e.pcr.toFixed(2)) + '</td>' +
        '<td class="vx-mono" style="text-align:right">' + (w.strike != null ? '$' + VXf.price(w.strike) + ' <span class="vx-meta">' + fmtOI(w.oi) + '</span>' : '—') + '</td>' +
        '</tr>';
    }).join('');
    var table = '<div class="vx-table-wrap vx-mt3"><table class="vx-table"><thead><tr>' +
      '<th>Échéance</th><th>Max pain</th><th style="text-align:right">OI call</th><th style="text-align:right">OI put</th><th style="text-align:right">PCR</th><th style="text-align:right">Mur d’OI n°1</th>' +
      '</tr></thead><tbody>' + rows + '</tbody></table></div>';

    // Murs d'OI de l'échéance proche : barres call/put par strike (aimant + prix repérés)
    var bs = (near.by_strike || []).slice().sort(function (a, b) { return b.strike - a.strike; });
    var maxOI = bs.reduce(function (m, r) { return Math.max(m, r.call_oi || 0, r.put_oi || 0); }, 1);
    var nearestK = null;                         // strike unique le plus proche du prix (repère ▸)
    if (spot && bs.length) nearestK = bs.reduce(function (a, b) { return Math.abs(b.strike - spot) < Math.abs(a.strike - spot) ? b : a; }).strike;
    var wallsHtml = '';
    if (bs.length) {
      wallsHtml = '<div class="vx-mt4"><div class="vx-meta vx-mb2">Murs d’open interest — échéance ' + esc(near.exp) + ' · <span style="color:' + VIOLET + '">■ calls</span> · <span style="color:var(--vx-silver-2,#9aa0a8)">■ puts</span> · ◆ max pain · ▸ prix</div>' +
        bs.map(function (r) {
          var cw = Math.round((r.call_oi || 0) / maxOI * 100), pw = Math.round((r.put_oi || 0) / maxOI * 100);
          var isMP = near.max_pain != null && Math.abs(r.strike - near.max_pain) < 0.01;
          var isSpot = nearestK != null && Math.abs(r.strike - nearestK) < 0.01;
          return '<div style="display:flex;align-items:center;gap:8px;margin:2px 0' + (isMP ? ';background:rgba(156,121,208,.10);border-radius:6px' : '') + '">' +
            '<span style="flex:0 0 34px;text-align:right"><span style="height:9px;display:inline-block;border-radius:2px;background:var(--vx-silver-2,#9aa0a8);width:' + pw + '%"></span></span>' +
            '<span class="vx-mono" style="flex:0 0 96px;text-align:center;font-weight:' + (isMP ? '700' : '500') + '">' + (isMP ? '◆ ' : '') + '$' + VXf.price(r.strike) + (isSpot ? ' ▸' : '') + '</span>' +
            '<span style="flex:1"><span style="height:9px;display:inline-block;border-radius:2px;background:' + VIOLET + ';width:' + cw + '%"></span></span>' +
            '</div>';
        }).join('') + '</div>';
    }

    body('vx-osym-maxpain', head + table + wallsHtml +
      '<div class="vx-meta vx-mt3">Max pain = strike qui <b>minimise</b> le paiement total aux détenteurs d’options à l’échéance ; l’open interest tend à « aimanter » le cours vers ce niveau à l’approche du règlement. Open interest RÉEL par strike (chaîne large IBKR, 14 strikes/côté). Repère, pas une garantie.</div>');
  }

  /* ── Boot : chaque section peint dès que sa donnée arrive ───────── */
  /* Chaîne dédiée (board ∪ fetch à la demande côté serveur) — un titre pas encore
     couvert par la rotation du board obtient quand même son dossier. */
  get('/api/options/chain/' + encodeURIComponent(SYM)).then(function (d) {
    paintScorecard((d && d.contracts) || [], d && d.spot);
    if (d && d.on_demand) {
      var meta = document.getElementById('vx-osym-chain-meta');
      if (meta) meta.textContent += ' · chaîne chargée à la demande';
    }
  }).catch(function () {
    /* Repli : ancien chemin via /scan si l'endpoint chaîne est indisponible. */
    get('/scan').then(function (scan) {
      var board = (scan && scan.options_board) || [];
      var det = scan && scan.detail && scan.detail[SYM];
      var spot = (det && det.price) != null ? det.price : (board.find(function (c) { return c.sym === SYM; }) || {}).spot;
      paintScorecard(board, spot);
    }).catch(function () { document.getElementById('vx-osym-scorecard').innerHTML = empty('Scan injoignable.'); });
  });
  get('/api/options/vol-charts/' + encodeURIComponent(SYM)).then(paintVol)
    .catch(function () { body('vx-osym-verdict', empty('Volatilité indisponible.')); });
  get('/api/options/scenarios/' + encodeURIComponent(SYM)).then(paintScenarios)
    .catch(function () { body('vx-osym-scenarios', empty('Scénarios indisponibles.')); });
  get('/api/options/strategies/' + encodeURIComponent(SYM)).then(paintStrats)
    .catch(function () { body('vx-osym-strats', empty('Stratégies indisponibles.')); });
  // Grille de chaîne (strikes × échéances) — greeks courtier IBKR (chaîne large réelle)
  ready(function () {
    var g = document.getElementById('vx-osym-grid');
    if (g) g.innerHTML = '<div class="vx-skeleton" style="height:140px"></div>';
    function paintGrid(d) {
      if (!window.VXCharts || !VXCharts.optionChainGrid) return;
      var ok = d && d.available !== false && (d.expiries || []).length;
      VXCharts.optionChainGrid('vx-osym-grid', ok
        ? { expiries: d.expiries, spot: d.spot, symbol: SYM, source: d.source, greeks_source: d.greeks_source, timestamp: d.ts, mode: 'delayed' }
        : { expiries: [], symbol: SYM });
    }
    ((window.VX && VX.fetch) ? VX.fetch('/api/options/chain-grid/' + encodeURIComponent(SYM), { ttl: 300000 })
      : fetch('/api/options/chain-grid/' + encodeURIComponent(SYM)).then(function (r) { return r.json(); }))
      .then(paintGrid).catch(function () { paintGrid(null); });
  });
  // Max pain : le serveur peut tirer la chaîne large en direct (IBKR, ~40-60 s) → état d'attente honnête, TTL long.
  (function () {
    var el = document.querySelector('#vx-osym-maxpain [data-body]');
    if (el) el.innerHTML = '<div style="color:var(--vx-text-muted);padding:var(--vx-s2) 0" aria-busy="true">' +
      '⟳ Lecture de l’open interest réel par strike (chaîne large IBKR, peut prendre ~1 min)…</div>';
    ((window.VX && VX.fetch) ? VX.fetch('/api/options/max-pain/' + encodeURIComponent(SYM), { ttl: 300000 })
      : fetch('/api/options/max-pain/' + encodeURIComponent(SYM)).then(function (r) { return r.json(); }))
      .then(paintMaxPain)
      .catch(function () { body('vx-osym-maxpain', empty('Max pain indisponible (chaîne large injoignable).')); });
  })();
})();
