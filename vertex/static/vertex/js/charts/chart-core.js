/* Vertex Charts — chart-core.js
   Moteur unique : Chart.js (déjà embarqué) + contrat visuel §34.
   Chaque graphique = ChartCard { titre, question, conclusion, corps, pied
   (source/date/mode/limites), bouton « Comprendre ce graphique » }.
   L'UI ne calcule AUCUN indicateur : elle trace ce que les moteurs donnent. */
(function () {
  'use strict';
  const VX = window.VX;
  const C = window.VXCharts = window.VXCharts || {};

  /* Thème V3 unique (chart-theme.js) — repli sur les mêmes valeurs si absent */
  const THEME = window.VXChartTheme || { colors: {}, tooltip: {} };
  C.colors = Object.assign({
    brand: '#f68a3c', blue: '#4ca6ff', cyan: '#2cc9d8', violet: '#8b6df6',
    positive: '#2acb7f', negative: '#f05d55', warning: '#f3a93b',
    info: '#4ca6ff', neutral: '#738096',
    text: '#b3bdca', muted: '#7f8b9d', grid: 'rgba(255,255,255,.055)',
    series: ['#f68a3c', '#4ca6ff', '#2cc9d8', '#8b6df6', '#f5b942', '#738096'],
  }, THEME.colors);

  function chartDefaults() {
    if (!window.Chart) return;
    const d = Chart.defaults;
    d.color = C.colors.text;
    d.font.family = getComputedStyle(document.documentElement).getPropertyValue('--vx-font') || 'Inter,sans-serif';
    d.font.size = 11;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) d.animation = false;
    else if (d.animation && typeof d.animation === 'object') d.animation.duration = 250;
    d.plugins.legend.display = false;
    const tt = (window.VXChartTheme && window.VXChartTheme.tooltip) || {};
    d.plugins.tooltip.backgroundColor = tt.backgroundColor || '#151c27';
    d.plugins.tooltip.borderColor = tt.borderColor || 'rgba(255,255,255,.14)';
    d.plugins.tooltip.borderWidth = 1;
    d.plugins.tooltip.padding = 10;
    d.plugins.tooltip.cornerRadius = 8;
    d.plugins.tooltip.titleColor = tt.titleColor || '#f7f8fa';
    d.plugins.tooltip.bodyColor = tt.bodyColor || '#b3bdca';
    d.maintainAspectRatio = false;
  }
  if (window.Chart) chartDefaults(); else document.addEventListener('DOMContentLoaded', chartDefaults);

  const registry = new Map(); // canvasId -> Chart (évite les canvas orphelins)
  C.mount = function (canvas, config) {
    if (!window.Chart || !canvas) return null;
    const prev = registry.get(canvas);
    if (prev) prev.destroy();
    const chart = new Chart(canvas.getContext('2d'), config);
    registry.set(canvas, chart);
    return chart;
  };
  C.axes = function ({ y = true, x = true, yFmt } = {}) {
    return {
      x: { display: x, grid: { color: C.colors.grid }, ticks: { maxTicksLimit: 8, maxRotation: 0 } },
      y: { display: y, grid: { color: C.colors.grid }, position: 'right',
           ticks: { maxTicksLimit: 6, callback: yFmt || undefined } },
    };
  };

  /* ── ChartCard : contrat visuel §34 ─────────────────────────────── */
  let uid = 0;
  C.card = function (host, opts) {
    /* opts: {title, question, conclusion, timeframe, controlsHtml, height,
              source, timestamp, mode, limits, explain:{shows,why,confirm,invalidate},
              legend:[{label,color}], render(canvas)->Chart} */
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const id = 'vxch-' + (++uid);
    const legend = (opts.legend || []).map(l =>
      `<span><span class="vx-swatch" style="background:${l.color}"></span>${l.label}</span>`).join('');
    el.classList.add('vx-card', 'vx-chart-card');
    el.innerHTML = `
      <div class="vx-chart-head">
        <span class="vx-chart-title">${opts.title || ''}</span>
        ${opts.timeframe ? `<span class="vx-badge">${opts.timeframe}</span>` : ''}
        <span class="vx-chart-controls">${opts.controlsHtml || ''}</span>
        ${opts.question ? `<span class="vx-chart-question">${opts.question}</span>` : ''}
        ${opts.conclusion ? `<span class="vx-chart-conclusion">${opts.conclusion}</span>` : ''}
      </div>
      <div class="vx-chart-body" style="height:${opts.height || 200}px"><canvas id="${id}" role="img" aria-label="${opts.title || 'graphique'}"></canvas></div>
      ${legend ? `<div class="vx-chart-legend">${legend}</div>` : ''}
      <div class="vx-chart-foot">
        ${VX.updateIndicator(opts.timestamp, opts.source, opts.mode)}
        ${opts.limits ? `<span class="vx-meta">${opts.limits}</span>` : ''}
        <button class="vx-btn vx-btn-sm vx-btn-ghost vx-explain-btn" data-explain="${id}">Comprendre ce graphique</button>
      </div>`;
    const canvas = el.querySelector('canvas');
    const chart = opts.render ? opts.render(canvas) : null;
    el.querySelector('[data-explain]')?.addEventListener('click', () => {
      const ex = opts.explain || {};
      VX.shell.openDrawer(opts.title || 'Graphique', `
        <h3 class="vx-mb2">Ce que montre le graphique</h3><p class="vx-dim">${ex.shows || opts.question || '—'}</p>
        <h3 class="vx-mt4 vx-mb2">Pourquoi cela compte</h3><p class="vx-dim">${ex.why || '—'}</p>
        <h3 class="vx-mt4 vx-mb2">Ce qui confirmerait</h3><p class="vx-dim">${ex.confirm || '—'}</p>
        <h3 class="vx-mt4 vx-mb2">Ce qui invaliderait</h3><p class="vx-dim">${ex.invalidate || '—'}</p>
        <div class="vx-divider"></div>
        <div class="vx-meta">Source : ${opts.source || 'n/d'} · ${VX.fmt.ago(opts.timestamp)}${opts.limits ? ' · ' + opts.limits : ''}</div>`);
    });
    return chart;
  };

  /* ── Primitives réutilisées par tous les modules ─────────────────── */
  C.sparkline = function (canvas, values, { color, positiveIsGood = true } = {}) {
    if (!canvas || !values || values.length < 2) return null;
    const up = values[values.length - 1] >= values[0];
    const col = color || (up === positiveIsGood ? C.colors.positive : C.colors.negative);
    return C.mount(canvas, {
      type: 'line',
      data: { labels: values.map((_, i) => i), datasets: [{ data: values, borderColor: col, borderWidth: 1.4, pointRadius: 0, fill: false, tension: .3 }] },
      options: { scales: { x: { display: false }, y: { display: false } }, plugins: { tooltip: { enabled: false } }, events: [] },
    });
  };
  C.area = function (canvas, labels, values, { color = C.colors.blue, yFmt, fill = true, extraDatasets = [] } = {}) {
    return C.mount(canvas, {
      type: 'line',
      data: { labels, datasets: [{ data: values, borderColor: color, borderWidth: 1.6, pointRadius: 0, tension: .25, fill,
        backgroundColor: (ctx) => {
          const g = ctx.chart.ctx.createLinearGradient(0, 0, 0, ctx.chart.height || 200);
          g.addColorStop(0, color + '3D'); g.addColorStop(1, color + '00'); return g;
        } }, ...extraDatasets] },
      options: { scales: C.axes({ yFmt }), interaction: { mode: 'index', intersect: false } },
    });
  };
  C.bars = function (canvas, labels, values, { colors, horizontal = false, yFmt } = {}) {
    const cols = colors || values.map(v => v >= 0 ? C.colors.positive : C.colors.negative);
    return C.mount(canvas, {
      type: 'bar',
      data: { labels, datasets: [{ data: values, backgroundColor: cols, borderRadius: 3, maxBarThickness: 26 }] },
      options: { indexAxis: horizontal ? 'y' : 'x', scales: C.axes({ yFmt }) },
    });
  };
  C.donut = function (canvas, labels, values, { colors } = {}) {
    /* §33 : un donut ≤ ~5 catégories */
    const l = labels.slice(0, 5), v = values.slice(0, 5);
    return C.mount(canvas, {
      type: 'doughnut',
      data: { labels: l, datasets: [{ data: v, backgroundColor: colors || C.colors.series, borderWidth: 0 }] },
      options: { cutout: '68%', plugins: { legend: { display: true, position: 'right', labels: { boxWidth: 10, font: { size: 10 } } } } },
    });
  };
  C.multiLine = function (canvas, labels, datasets, { yFmt } = {}) {
    return C.mount(canvas, {
      type: 'line',
      data: { labels, datasets: datasets.map((d, i) => Object.assign({ borderColor: C.colors.series[i % 6], borderWidth: 1.5, pointRadius: 0, tension: .25, fill: false }, d)) },
      options: { scales: C.axes({ yFmt }), interaction: { mode: 'index', intersect: false },
        plugins: { legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } } },
    });
  };
  /* Annotations de niveaux (entrée/stop/TP…) — plugin ligne horizontale. */
  C.levelLines = function (levels) {
    /* levels: [{value,label,kind:'entry'|'stop'|'tp'|'support'|'resistance'}] */
    const colByKind = { entry: C.colors.info, stop: C.colors.negative, tp: C.colors.positive,
      support: C.colors.cyan, resistance: C.colors.warning };
    return {
      id: 'vxLevels',
      afterDatasetsDraw(chart) {
        const { ctx, chartArea, scales } = chart;
        if (!scales.y) return;
        (levels || []).forEach(lv => {
          if (lv.value === null || lv.value === undefined) return;
          const y = scales.y.getPixelForValue(lv.value);
          if (y < chartArea.top || y > chartArea.bottom) return;
          ctx.save();
          ctx.strokeStyle = colByKind[lv.kind] || C.colors.muted;
          ctx.setLineDash([4, 4]); ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(chartArea.left, y); ctx.lineTo(chartArea.right, y); ctx.stroke();
          ctx.setLineDash([]);
          ctx.fillStyle = colByKind[lv.kind] || C.colors.muted;
          ctx.font = '10px ' + (Chart.defaults.font.family || 'monospace');
          ctx.fillText(`${lv.label || lv.kind} ${VX.fmt.price(lv.value)}`, chartArea.left + 4, y - 3);
          ctx.restore();
        });
      },
    };
  };
  /* Marqueurs verticaux (earnings, événements). */
  C.eventMarkers = function (markers) {
    return {
      id: 'vxEvents',
      afterDatasetsDraw(chart) {
        const { ctx, chartArea, scales } = chart;
        (markers || []).forEach(m => {
          const x = scales.x.getPixelForValue(m.index);
          if (!isFinite(x) || x < chartArea.left || x > chartArea.right) return;
          ctx.save();
          ctx.strokeStyle = C.colors.warning; ctx.setLineDash([2, 3]);
          ctx.beginPath(); ctx.moveTo(x, chartArea.top); ctx.lineTo(x, chartArea.bottom); ctx.stroke();
          ctx.fillStyle = C.colors.warning; ctx.font = '9px sans-serif';
          ctx.fillText(m.label || 'E', x + 2, chartArea.top + 9);
          ctx.restore();
        });
      },
    };
  };
})();
