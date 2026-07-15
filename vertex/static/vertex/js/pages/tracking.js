/* tracking.js — espace Suivis (§17). Lit /api/tracking + performance par suivi.
   Tout gain est étiqueté HYPOTHÉTIQUE. Lecture seule. */
(function () {
  'use strict';
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var VXf = (window.VX && VX.fmt) || { nd: function (v) { return v == null ? '—' : v; }, num: function (v, d) { return v == null ? '—' : Number(v).toFixed(d || 2); } };

  function get(url) { return (window.VX && VX.fetch) ? VX.fetch(url, { ttl: 10000 }) : fetch(url).then(function (r) { return r.json(); }); }
  function pct(v) {
    if (v == null) return '<span class="vx-muted">—</span>';
    var cls = v >= 0 ? 'vx-pos' : 'vx-neg';
    return '<span class="' + cls + '">' + (v >= 0 ? '+' : '') + VXf.num(v, 2) + ' %</span>';
  }
  function absDate(iso) {
    if (!iso) return '—';
    try { var d = new Date(iso); return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' }); }
    catch (e) { return esc(iso); }
  }

  function summaryHtml(s) {
    function stat(l, v) { return '<div class="vx-stat"><span class="vx-stat-label">' + l + '</span><span class="vx-stat-value">' + v + '</span></div>'; }
    return '<div class="vx-stats-row" style="display:flex;flex-wrap:wrap;gap:1.4rem">' +
      stat('Actifs', VXf.nd(s.active)) + stat('Actions', VXf.nd(s.stocks)) +
      stat('Options', VXf.nd(s.options)) + stat('Clôturés', VXf.nd(s.stopped)) +
      stat('Réf. manquante', VXf.nd(s.data_required)) + '</div>';
  }

  function activeRow(t, p) {
    var ref = t.reference_price;
    return '<tr>' +
      '<td><b>' + esc(t.symbol) + '</b>' + (t.entity_type === 'OPTION' ? ' <span class="vx-muted">OPT</span>' : '') + '</td>' +
      '<td>' + absDate(t.started_at) + '</td>' +
      '<td>' + (ref != null ? VXf.num(ref, 2) : '<span class="vx-muted">réf. requise</span>') +
      (t.reference_price_type ? ' <span class="vx-muted">(' + esc(t.reference_price_type) + ')</span>' : '') + '</td>' +
      '<td>' + (p && p.current_price != null ? VXf.num(p.current_price, 2) : '—') + '</td>' +
      '<td>' + pct(p && p.return_pct) + '</td>' +
      '<td>' + pct(p && p.benchmark_return_pct) + '</td>' +
      '<td>' + pct(p && p.alpha_pct) + '</td>' +
      '<td>' + pct(p && p.mfe_pct) + ' / ' + pct(p && p.mae_pct) + '</td>' +
      '<td>' + esc(t.strategy_decision_at_start || '—') + '</td>' +
      '</tr>';
  }

  function table(head, bodyRows) {
    return '<div class="vx-table-wrap"><table class="vx-table"><thead><tr>' +
      head.map(function (h) { return '<th>' + h + '</th>'; }).join('') +
      '</tr></thead><tbody>' + bodyRows + '</tbody></table></div>';
  }

  // Graphique interactif : rendement hypothétique vs SPY par suivi actif.
  function renderPerfChart(rows) {
    var host = document.getElementById('vx-trk-chart');
    var VC = window.VXCharts;
    if (!host || !VC || !window.Chart) return;
    var pts = rows.filter(function (r) { return r.p && r.p.return_pct != null; });
    if (!pts.length) { host.innerHTML = ''; return; }
    var brand = (VC.colors && VC.colors.brand) || '#84aa31';
    var neutral = (VC.colors && VC.colors.neutral) || '#8f8a83';
    var labels = pts.map(function (r) { return r.t.symbol; });
    var self = pts.map(function (r) { return +r.p.return_pct.toFixed(2); });
    var spy = pts.map(function (r) { return r.p.benchmark_return_pct != null ? +r.p.benchmark_return_pct.toFixed(2) : null; });
    VC.card('vx-trk-chart', {
      title: 'Performance hypothétique depuis le suivi',
      question: 'Chaque idée suivie bat-elle SPY depuis que je l\'ai marquée ?',
      conclusion: pts.length + ' suivi(s) actif(s) — rendements 100 % hypothétiques',
      height: 240, source: 'SCAN', timestamp: Date.now(), mode: 'delayed',
      limits: 'rendement prix hors frais/dividendes · aucune position réelle',
      legend: [{ label: 'Idée suivie', color: brand }, { label: 'SPY', color: neutral }],
      explain: {
        shows: 'Le rendement de chaque idée suivie et celui de SPY sur la même fenêtre.',
        why: 'Vertex vise à battre SPY : un alpha positif valide la sélection.',
        confirm: 'Barres oranges au-dessus des grises (alpha positif).',
        invalidate: 'Sous-performance persistante vs SPY.'
      },
      render: function (cv) {
        return VC.mount(cv, {
          type: 'bar',
          data: {
            labels: labels, datasets: [
              { label: 'Idée suivie', data: self, backgroundColor: brand, borderRadius: 3, maxBarThickness: 26 },
              { label: 'SPY', data: spy, backgroundColor: neutral + 'cc', borderRadius: 3, maxBarThickness: 26 }
            ]
          },
          options: {
            interaction: { mode: 'index', intersect: false },
            plugins: { tooltip: { callbacks: { label: function (ctx) { return ctx.dataset.label + ' : ' + (ctx.parsed.y == null ? '—' : (ctx.parsed.y >= 0 ? '+' : '') + ctx.parsed.y + ' %'); } } } },
            scales: { y: { suggestedMin: -1, suggestedMax: 1, ticks: { callback: function (v) { return v + ' %'; } } } }
          }
        });
      }
    });
  }

  function loadActive() {
    var sEl = document.getElementById('vx-trk-summary-body');
    var aEl = document.getElementById('vx-trk-active-body');
    var xEl = document.getElementById('vx-trk-stopped-body');
    get('/api/tracking').then(function (d) {
      var items = (d && d.trackings) || [];
      if (sEl) sEl.innerHTML = summaryHtml((d && d.summary) || {});
      var active = items.filter(function (t) { return t.status === 'ACTIVE' || t.status === 'DATA_REQUIRED'; });
      var stopped = items.filter(function (t) { return t.status === 'STOPPED'; });
      if (!active.length) {
        aEl.innerHTML = (window.VX && VX.states) ? VX.states.empty('Aucun suivi actif. Marque une idée « Suivre » depuis Opportunités ou une analyse.') : 'Aucun suivi.';
      } else {
        // charge la performance de chaque suivi (séquentiel léger)
        Promise.all(active.map(function (t) {
          return get('/api/tracking/' + encodeURIComponent(t.tracking_id) + '/performance')
            .then(function (p) { return { t: t, p: p }; }).catch(function () { return { t: t, p: null }; });
        })).then(function (rows) {
          aEl.innerHTML = table(['Titre', 'Depuis le', 'Référence', 'Actuel', 'Rdt hypo.', 'SPY', 'Alpha', 'MFE / MAE', 'Décision init.'],
            rows.map(function (r) { return activeRow(r.t, r.p); }).join(''));
          renderPerfChart(rows);
        });
      }
      if (stopped.length) {
        xEl.innerHTML = table(['Titre', 'Ouvert', 'Clôturé', 'Rdt final hypo.', 'MFE', 'MAE', 'Décision'],
          stopped.map(function (t) {
            var f = t.final || {};
            return '<tr><td><b>' + esc(t.symbol) + '</b></td><td>' + absDate(t.started_at) + '</td><td>' + absDate(t.stopped_at) +
              '</td><td>' + pct(f.return_pct) + '</td><td>' + pct(f.mfe_pct) + '</td><td>' + pct(f.mae_pct) +
              '</td><td>' + esc(f.final_decision || '—') + '</td></tr>';
          }).join(''));
      } else if (xEl) { xEl.innerHTML = '<div class="vx-empty">Aucun suivi clôturé.</div>'; }
    }).catch(function (e) {
      if (aEl) aEl.innerHTML = '<div class="vx-error-banner">⚠ ' + esc(e.message) + '</div>';
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', loadActive);
  else loadActive();
})();
