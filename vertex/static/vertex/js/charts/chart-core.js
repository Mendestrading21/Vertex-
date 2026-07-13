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
    brand: '#cf6128', blue: '#b9683d', cyan: '#c8ad8d', violet: '#85609f',
    positive: '#38b879', negative: '#dc5f52', warning: '#ce8a29',
    info: '#b9683d', neutral: '#8f8a83',
    text: '#b7b3ad', muted: '#817d77', grid: 'rgba(255,255,255,.05)',
    series: ['#cf6128', '#c8ad8d', '#8f8a83', '#85609f', '#ce8a29', '#914b2b'],
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
    d.plugins.tooltip.backgroundColor = tt.backgroundColor || '#151719';
    d.plugins.tooltip.borderColor = tt.borderColor || 'rgba(255,255,255,.15)';
    d.plugins.tooltip.borderWidth = 1;
    d.plugins.tooltip.padding = 10;
    d.plugins.tooltip.cornerRadius = 8;
    d.plugins.tooltip.titleColor = tt.titleColor || '#f3f1ed';
    d.plugins.tooltip.bodyColor = tt.bodyColor || '#b7b3ad';
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
  /* ── Jauge radiale (SVG, sans Chart.js) — régime, risk score, VIX, options env ──
     opts: {value, min=0, max=100, unit, label, reading,
            bands:[{to, color}], // zones colorées de gauche→droite (ordre croissant)
            positiveIsLow=false} // n/u : la couleur vient des bandes
     Accessible : role=img + aria-label chiffré. Aucune animation permanente. */
  C.gauge = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    const min = o.min != null ? o.min : 0, max = o.max != null ? o.max : 100;
    const v = (o.value == null || isNaN(o.value)) ? null : Math.max(min, Math.min(max, o.value));
    const W = 200, H = 118, cx = 100, cy = 104, r = 84;
    const ang = (t) => Math.PI * (1 - (Math.max(min, Math.min(max, t)) - min) / (max - min)); // 180°→0°
    const pt = (a, rr = r) => [cx + rr * Math.cos(a), cy - rr * Math.sin(a)];
    const arc = (a0, a1, rr = r) => {
      const [x0, y0] = pt(a0, rr), [x1, y1] = pt(a1, rr);
      const large = Math.abs(a0 - a1) > Math.PI ? 1 : 0;
      return `M ${x0.toFixed(1)} ${y0.toFixed(1)} A ${rr} ${rr} 0 ${large} 1 ${x1.toFixed(1)} ${y1.toFixed(1)}`;
    };
    const bands = o.bands && o.bands.length ? o.bands : [{ to: max, color: C.colors.neutral }];
    // pistes de fond colorées par bande (contexte), puis arc de valeur par-dessus
    let track = '', prev = min;
    bands.forEach(b => {
      track += `<path d="${arc(ang(prev), ang(b.to))}" stroke="${b.color}" stroke-opacity=".22" stroke-width="9" fill="none" stroke-linecap="butt"/>`;
      prev = b.to;
    });
    let valArc = '', needle = '', valColor = C.colors.neutral;
    if (v != null) {
      for (const b of bands) { if (v <= b.to) { valColor = b.color; break; } valColor = b.color; }
      valArc = `<path d="${arc(ang(min), ang(v))}" stroke="${valColor}" stroke-width="9" fill="none" stroke-linecap="round"/>`;
      const [nx, ny] = pt(ang(v), r - 2);
      needle = `<circle cx="${nx.toFixed(1)}" cy="${ny.toFixed(1)}" r="4.5" fill="${valColor}"/>`;
    }
    const disp = v == null ? '—' : (Number.isInteger(v) ? v : (+v).toFixed(1));
    const aria = `${o.label || 'jauge'} : ${v == null ? 'donnée indisponible' : disp + (o.unit || '')}${o.reading ? ' — ' + o.reading : ''}`;
    el.innerHTML = `
      <div class="vx-gauge" role="img" aria-label="${aria.replace(/"/g, '&quot;')}">
        <svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:230px;display:block;margin:0 auto">
          ${track}${valArc}${needle}
          <text x="${cx}" y="${cy - 20}" text-anchor="middle" fill="${valColor}" font-size="30" font-weight="800" style="font-variant-numeric:tabular-nums">${disp}</text>
          <text x="${cx}" y="${cy - 3}" text-anchor="middle" fill="var(--vx-text-muted,#817d77)" font-size="10" letter-spacing=".5">${(o.unit || '') + (o.label ? ' · ' + o.label : '')}</text>
        </svg>
        ${o.reading ? `<div class="vx-meta" style="text-align:center;margin-top:4px">${o.reading}</div>` : ''}
      </div>`;
    return el;
  };

  /* ── Treemap (SVG squarifié) — poids relatif : portefeuille, segments, secteurs ──
     opts: {items:[{label, value>0, color?, sub?}], width, height, fmt?, emptyHtml?}
     Aspect ratios équilibrés (algorithme squarify). Accessible : chaque tuile role=img. */
  C.treemap = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    let items = (o.items || []).filter(d => d && d.value > 0).sort((a, b) => b.value - a.value);
    if (!items.length) { el.innerHTML = o.emptyHtml || ''; return null; }
    const W = o.width || 640, H = o.height || 300;
    const total = items.reduce((s, d) => s + d.value, 0);
    const nodes = items.map(d => ({ d, area: d.value / total * W * H }));
    const rects = [];
    let fx = 0, fy = 0, fw = W, fh = H;
    const worst = (row, len) => {
      let sum = 0, mx = 0, mn = Infinity;
      row.forEach(r => { sum += r.area; if (r.area > mx) mx = r.area; if (r.area < mn) mn = r.area; });
      const s2 = sum * sum, l2 = len * len;
      return Math.max(l2 * mx / s2, s2 / (l2 * mn));
    };
    const layout = (row) => {
      const sum = row.reduce((a, r) => a + r.area, 0);
      if (fw >= fh) {                       // bande verticale à gauche (largeur rw)
        const rw = sum / fh; let oy = fy;
        row.forEach(r => { const rh = r.area / rw; rects.push({ d: r.d, x: fx, y: oy, w: rw, h: rh }); oy += rh; });
        fx += rw; fw -= rw;
      } else {                              // bande horizontale en haut (hauteur rh)
        const rh = sum / fw; let ox = fx;
        row.forEach(r => { const rw = r.area / rh; rects.push({ d: r.d, x: ox, y: fy, w: rw, h: rh }); ox += rw; });
        fy += rh; fh -= rh;
      }
    };
    let rest = nodes.slice(), row = [];
    while (rest.length) {
      const len = Math.min(fw, fh), next = rest[0];
      if (row.length === 0 || worst(row.concat(next), len) <= worst(row, len)) row.push(rest.shift());
      else { layout(row); row = []; }
    }
    if (row.length) layout(row);
    const fmt = o.fmt || ((v) => v);
    const svg = rects.map(r => {
      const col = r.d.color || C.colors.neutral;
      const small = r.w < 54 || r.h < 30;
      const lbl = String(r.d.label || '');
      const aria = `${lbl} : ${fmt(r.d.value)}${r.d.sub ? ' ' + r.d.sub : ''}`;
      return `<g role="img" aria-label="${aria.replace(/"/g, '&quot;')}">
        <rect x="${r.x.toFixed(1)}" y="${r.y.toFixed(1)}" width="${Math.max(0, r.w - 1.5).toFixed(1)}" height="${Math.max(0, r.h - 1.5).toFixed(1)}"
          rx="3" fill="${col}" fill-opacity=".82" stroke="var(--vx-bg-app,#050505)" stroke-width="1.5"/>
        ${small ? '' : `<text x="${(r.x + 6).toFixed(1)}" y="${(r.y + 16).toFixed(1)}" fill="#f3f1ed" font-size="11" font-weight="700">${lbl.slice(0, Math.floor(r.w / 7))}</text>
        <text x="${(r.x + 6).toFixed(1)}" y="${(r.y + 30).toFixed(1)}" fill="rgba(255,255,255,.82)" font-size="10" style="font-variant-numeric:tabular-nums">${fmt(r.d.value)}${r.d.sub ? ' · ' + r.d.sub : ''}</text>`}
      </g>`;
    }).join('');
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="100%" preserveAspectRatio="none" style="display:block">${svg}</svg>`;
    return el;
  };

  /* ── Flow diagram (chaîne de nœuds connectés) — impacts, pipeline système ──
     opts: {nodes:[{label, count?, sub?, tone?('active'|'idle'|'warn'|'err'), color?}], ariaLabel, emptyHtml}
     Horizontal, scrollable, responsive. Accessible : role=img + résumé. */
  C.flow = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    const nodes = o.nodes || [];
    if (!nodes.length) { el.innerHTML = o.emptyHtml || ''; return null; }
    const toneCol = { active: C.colors.positive, idle: C.colors.neutral, warn: C.colors.warning, err: C.colors.negative };
    const aria = (o.ariaLabel || 'diagramme de flux') + ' : ' + nodes.map(n => n.label + (n.count != null ? ' ' + n.count : '')).join(' → ');
    el.innerHTML = '<div role="img" aria-label="' + aria.replace(/"/g, '&quot;') + '" style="display:flex;align-items:stretch;overflow-x:auto;padding:4px 0">'
      + nodes.map((n, i) => {
        const col = n.color || toneCol[n.tone] || C.colors.neutral;
        const active = n.tone === 'active' || (n.count > 0);
        const bg = active ? 'rgba(57,184,120,.09)' : 'var(--vx-surface-2,#111315)';
        const arrow = i < nodes.length - 1 ? '<span aria-hidden="true" style="align-self:center;color:var(--vx-text-muted,#817d77);padding:0 5px;font-size:13px">→</span>' : '';
        return '<div style="flex:0 0 auto;min-width:76px;text-align:center;padding:8px 10px;border-radius:9px;background:' + bg + ';border:1px solid ' + col + '55">'
          + '<div style="font-size:10.5px;color:var(--vx-text-secondary,#b7b2aa);text-transform:capitalize;white-space:nowrap">' + String(n.label) + '</div>'
          + (n.count != null ? '<div style="font-size:15px;font-weight:800;color:' + col + ';font-variant-numeric:tabular-nums">' + n.count + '</div>' : '')
          + (n.sub ? '<div style="font-size:9px;letter-spacing:.04em;text-transform:uppercase;color:var(--vx-text-muted,#817d77)">' + n.sub + '</div>' : '')
          + '</div>' + arrow;
      }).join('') + '</div>';
    return el;
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
