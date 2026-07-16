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
    brand: '#84aa31', blue: '#84aa31', cyan: '#c0b79f', violet: '#9c79d0',
    option: '#9c79d0', teal: '#53b9ad', plum: '#8f698c', sand: '#c0b79f',
    steel: '#909b94', stone: '#6d746e',
    positive: '#36c889', negative: '#ed655c', warning: '#dda23b',
    info: '#84aa31', neutral: '#8f8a83',
    text: '#b7b3ad', muted: '#817d77', grid: 'rgba(255,255,255,.05)',
    series: ['#84aa31', '#c0b79f', '#8f8a83', '#9c79d0', '#dda23b', '#48631b'],
    /* Palette macro/cross-asset : teal en tête (jamais confondu avec la marque) */
    macroSeries: ['#53b9ad', '#c0b79f', '#8f698c', '#909b94', '#dda23b', '#6d746e'],
  }, THEME.colors);

  /* ── Rendu MODERNE (global) : dégradés, glow, barres arrondies, crosshair ──
     Un seul endroit → tous les graphiques Chart.js de l'app en profitent. */
  function _rgba(col, a) {
    if (typeof col !== 'string') return null;
    if (col[0] === '#' && col.length >= 7) {
      const r = parseInt(col.slice(1, 3), 16), g = parseInt(col.slice(3, 5), 16), b = parseInt(col.slice(5, 7), 16);
      if ([r, g, b].some(isNaN)) return null;
      return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
    }
    const m = col.match(/rgba?\(([^)]+)\)/);
    if (m) { const p = m[1].split(',').slice(0, 3).map(s => s.trim()); return 'rgba(' + p.join(',') + ',' + a + ')'; }
    return null;
  }
  /* Lueur douce sous chaque ligne (couleur de la série) — désactivée si l'OS
     demande moins d'animations (économie de peinture). */
  const _glowPlugin = {
    id: 'vxglow',
    beforeDatasetDraw(chart, args) {
      if (args.meta.type !== 'line') return;
      const ds = chart.data.datasets[args.index] || {};
      const col = typeof ds.borderColor === 'string' ? _rgba(ds.borderColor, .40) : null;
      const c = chart.ctx; c.save();
      c.shadowColor = col || 'rgba(163,202,66,.25)';
      c.shadowBlur = 6; c.shadowOffsetY = 1;
    },
    afterDatasetDraw(chart, args) { if (args.meta.type === 'line') chart.ctx.restore(); },
  };
  /* Crosshair pointillé vertical au survol (axes cartésiens uniquement). */
  const _crossPlugin = {
    id: 'vxcrosshair',
    afterDraw(chart) {
      if (!chart.scales || !chart.scales.x || !chart.chartArea) return;
      const act = chart.tooltip && chart.tooltip.getActiveElements ? chart.tooltip.getActiveElements() : [];
      if (!act.length) return;
      const x = act[0].element.x, a = chart.chartArea, c = chart.ctx;
      c.save(); c.strokeStyle = 'rgba(237,255,237,.14)'; c.lineWidth = 1; c.setLineDash([3, 3]);
      c.beginPath(); c.moveTo(x, a.top); c.lineTo(x, a.bottom); c.stroke(); c.restore();
    },
  };
  function chartDefaults() {
    if (!window.Chart) return;
    const d = Chart.defaults;
    d.color = C.colors.text;
    d.font.family = getComputedStyle(document.documentElement).getPropertyValue('--vx-font') || 'Inter,sans-serif';
    d.font.size = 11;
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced) d.animation = false;
    else if (d.animation && typeof d.animation === 'object') d.animation.duration = 250;
    d.plugins.legend.display = false;
    d.interaction = { mode: 'nearest', axis: 'xy', intersect: false };
    const tt = (window.VXChartTheme && window.VXChartTheme.tooltip) || {};
    d.plugins.tooltip.backgroundColor = tt.backgroundColor || '#151719';
    d.plugins.tooltip.borderColor = tt.borderColor || 'rgba(255,255,255,.15)';
    d.plugins.tooltip.borderWidth = 1;
    d.plugins.tooltip.padding = 10;
    d.plugins.tooltip.cornerRadius = 8;
    d.plugins.tooltip.titleColor = tt.titleColor || '#f3f1ed';
    d.plugins.tooltip.bodyColor = tt.bodyColor || '#b7b3ad';
    d.maintainAspectRatio = false;
    try { if (!reduced) Chart.register(_glowPlugin); Chart.register(_crossPlugin); } catch (e) { /* déjà enregistrés */ }
  }
  if (window.Chart) chartDefaults(); else document.addEventListener('DOMContentLoaded', chartDefaults);

  /* Modernise une config avant montage : remplissage des lignes en DÉGRADÉ
     vertical (couleur de série → transparent) et barres ARRONDIES. Opt-out
     naturel : une série qui fournit déjà un backgroundColor scriptable ou un
     borderRadius garde son réglage. */
  function _modernize(config) {
    const sets = (config && config.data && config.data.datasets) || [];
    sets.forEach(function (ds) {
      const t = ds.type || config.type;
      if (t === 'line' && ds.fill && typeof (ds.backgroundColor || '') === 'string') {
        const base = (typeof ds.borderColor === 'string' && _rgba(ds.borderColor, 1)) ? ds.borderColor : ds.backgroundColor;
        const top = _rgba(base, .30), bottom = _rgba(base, .02);
        if (top && bottom) ds.backgroundColor = function (c2) {
          const ch = c2.chart, area = ch.chartArea;
          if (!area) return bottom;
          const g = ch.ctx.createLinearGradient(0, area.top, 0, area.bottom);
          g.addColorStop(0, top); g.addColorStop(1, bottom); return g;
        };
      }
      if (t === 'bar') {
        if (ds.borderRadius == null) ds.borderRadius = 5;
        if (ds.maxBarThickness == null) ds.maxBarThickness = 38;
      }
    });
    return config;
  }

  const registry = new Map(); // canvasId -> Chart (évite les canvas orphelins)
  C.mount = function (canvas, config) {
    if (!window.Chart || !canvas) return null;
    const prev = registry.get(canvas);
    if (prev) prev.destroy();
    const chart = new Chart(canvas.getContext('2d'), _modernize(config));
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
    /* Re-rendu d'une carte (filtres, périodes) : détruire l'ancien Chart AVANT
       d'écraser le canvas — sinon les instances s'accumulent à chaque repaint. */
    el.querySelectorAll('canvas').forEach(function (oldCv) {
      const prev = registry.get(oldCv) || (window.Chart && Chart.getChart && Chart.getChart(oldCv));
      if (prev) { try { prev.destroy(); } catch (e) { /* déjà détruit */ } }
      registry.delete(oldCv);
    });
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
        <span class="vx-chart-tools">
          <button class="vx-btn vx-btn-sm vx-btn-ghost vx-chart-tbl" title="Voir les données en tableau" aria-label="Voir les données">Données</button>
          <button class="vx-btn vx-btn-sm vx-btn-ghost vx-chart-fs" title="Agrandir en plein écran" aria-label="Plein écran">⤢ Agrandir</button>
          <button class="vx-btn vx-btn-sm vx-btn-ghost vx-explain-btn" data-explain="${id}">Comprendre</button>
        </span>
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
    /* Plein écran / mode focus (§35) : la carte occupe le viewport, le graphique
       se redimensionne (Chart.js maintainAspectRatio:false). Échap ou clic ferme. */
    el.querySelector('.vx-chart-fs')?.addEventListener('click', () => C.toggleFullscreen(el, chart));
    /* Vue tableau (§8) : les données RÉELLES du graphique en table, depuis
       chart.data — aucune valeur inventée, exactement ce qui est tracé. */
    el.querySelector('.vx-chart-tbl')?.addEventListener('click', () => C.showDataTable(opts.title, chart));
    return chart;
  };

  /* Bascule plein écran d'une carte graphique. */
  C.toggleFullscreen = function (el, chart) {
    const on = el.classList.toggle('vx-chart-fs');
    document.body.classList.toggle('vx-fs-open', on);
    let bd = document.getElementById('vx-chart-fs-backdrop');
    if (on && !bd) {
      bd = document.createElement('div'); bd.id = 'vx-chart-fs-backdrop';
      bd.addEventListener('click', () => C.toggleFullscreen(el, chart));
      document.body.appendChild(bd);
    }
    if (bd) bd.style.display = on ? 'block' : 'none';
    const esc = (e) => { if (e.key === 'Escape') { C.toggleFullscreen(el, chart); document.removeEventListener('keydown', esc); } };
    if (on) document.addEventListener('keydown', esc);
    if (chart && chart.resize) setTimeout(() => { try { chart.resize(); } catch (e) {} }, 60);
  };

  /* Construit une table HTML à partir des données réellement tracées. */
  C.showDataTable = function (title, chart) {
    if (!chart || !chart.data) { VX.toast && VX.toast('Aucune donnée tabulable', 'warning'); return; }
    const labels = chart.data.labels || [];
    const ds = chart.data.datasets || [];
    const fmt = (v) => (v == null || v === '') ? '—'
      : (typeof v === 'object' ? (v.y != null ? VX.fmt.num(v.y, 2) : (v.x != null ? VX.fmt.num(v.x, 2) : '—')) : (isNaN(v) ? String(v) : VX.fmt.num(+v, 2)));
    const n = Math.max(labels.length, ...ds.map(d => (d.data || []).length));
    let head = '<th>#</th>' + ds.map(d => `<th class="vx-num">${(d.label || 'série')}</th>`).join('');
    let body = '';
    for (let i = 0; i < n; i++) {
      body += `<tr><td class="vx-mono">${labels[i] != null ? labels[i] : (i + 1)}</td>`
        + ds.map(d => `<td class="vx-num vx-mono">${fmt((d.data || [])[i])}</td>`).join('') + '</tr>';
    }
    VX.shell.openDrawer((title || 'Graphique') + ' — données',
      `<div class="vx-table-wrap" style="max-height:70vh"><table class="vx-table"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>
       <div class="vx-meta vx-mt2">${n} point(s) — valeurs réellement tracées, aucune estimation.</div>`);
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
    /* Horizontal : les CATÉGORIES vivent sur l'axe y — yFmt ne s'applique qu'aux
       VALEURS (axe x), sinon les noms disparaissent au profit de ticks formatés. */
    const scales = horizontal
      ? { x: { grid: { color: C.colors.grid }, ticks: { maxTicksLimit: 6, callback: yFmt || undefined } },
          y: { grid: { display: false }, ticks: { autoSkip: false } } }
      : C.axes({ yFmt });
    return C.mount(canvas, {
      type: 'bar',
      data: { labels, datasets: [{ data: values, backgroundColor: cols, borderRadius: 3, maxBarThickness: 26 }] },
      options: { indexAxis: horizontal ? 'y' : 'x', scales },
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

  /* ── Waterfall (SVG) — décomposition/contribution : P&L, risque, santé, décision ──
     opts: {items:[{label, value, isTotal?}], fmt?, ariaLabel, width, height, emptyHtml}
     Contributions cumulatives (vert +, rouge −) ; isTotal = barre depuis 0 (brand).
     Accessible : role=img + résumé. */
  C.waterfall = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    const items = (o.items || []).filter(it => it && it.value != null && !isNaN(it.value));
    if (!items.length) { el.innerHTML = o.emptyHtml || ''; return null; }
    const W = o.width || 620, H = o.height || 240, PAD_B = 30, PAD_T = 16;
    let cum = 0; const bars = [];
    items.forEach(it => {
      if (it.isTotal) { bars.push({ label: it.label, from: 0, to: it.value, val: it.value, total: true }); }
      else { const from = cum; cum += it.value; bars.push({ label: it.label, from, to: cum, val: it.value }); }
    });
    const vals = bars.reduce((a, b) => a.concat([b.from, b.to]), [0]);
    const maxV = Math.max.apply(null, vals), minV = Math.min.apply(null, vals);
    const range = (maxV - minV) || 1, plotH = H - PAD_B - PAD_T;
    const y = (v) => PAD_T + (maxV - v) / range * plotH;
    const n = bars.length, gap = 10, bw = Math.max(6, (W - gap * (n + 1)) / n);
    const fmt = o.fmt || ((v) => Math.round(v));
    let svg = '';
    bars.forEach((b, i) => {
      const x = gap + i * (bw + gap);
      const yTop = y(Math.max(b.from, b.to)), yBot = y(Math.min(b.from, b.to));
      const h = Math.max(2, yBot - yTop);
      const col = b.total ? C.colors.brand : (b.val >= 0 ? C.colors.positive : C.colors.negative);
      svg += `<rect x="${x.toFixed(1)}" y="${yTop.toFixed(1)}" width="${bw.toFixed(1)}" height="${h.toFixed(1)}" rx="2" fill="${col}" fill-opacity=".82"/>`;
      if (i < bars.length - 1 && !bars[i + 1].total) {
        const yc = y(b.to), xn = gap + (i + 1) * (bw + gap);
        svg += `<line x1="${(x + bw).toFixed(1)}" y1="${yc.toFixed(1)}" x2="${xn.toFixed(1)}" y2="${yc.toFixed(1)}" stroke="rgba(255,255,255,.18)" stroke-dasharray="2,2"/>`;
      }
      svg += `<text x="${(x + bw / 2).toFixed(1)}" y="${(yTop - 4).toFixed(1)}" text-anchor="middle" font-size="10" fill="var(--vx-text-secondary,#b7b2aa)" style="font-variant-numeric:tabular-nums">${(b.val >= 0 && !b.total ? '+' : '') + fmt(b.val)}</text>`;
      svg += `<text x="${(x + bw / 2).toFixed(1)}" y="${(H - 9).toFixed(1)}" text-anchor="middle" font-size="9" fill="var(--vx-text-muted,#817d77)">${String(b.label).slice(0, Math.floor(bw / 6) + 2)}</text>`;
    });
    const aria = (o.ariaLabel || 'décomposition') + ' : ' + bars.map(b => b.label + ' ' + fmt(b.val)).join(', ');
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="100%" role="img" aria-label="${aria.replace(/"/g, '&quot;')}">${svg}</svg>`;
    return el;
  };

  /* ── Radar (SVG polygonal) — scorecard, greeks, risques d'entreprise ──
     opts: {axes:[{label, value}], max=100, color, ariaLabel, width, height, emptyHtml}
     ≥3 axes requis. Accessible : role=img + résumé chiffré. */
  C.radar = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    const axes = (o.axes || []).filter(a => a && a.label != null);
    if (axes.length < 3) { el.innerHTML = o.emptyHtml || ''; return null; }
    const max = o.max || 100, N = axes.length, W = o.width || 260, H = o.height || 240;
    const cx = W / 2, cy = H / 2, R = Math.min(W, H) / 2 - 26;
    const ang = (i) => -Math.PI / 2 + i * 2 * Math.PI / N;
    const pt = (i, r) => [cx + r * Math.cos(ang(i)), cy + r * Math.sin(ang(i))];
    let grid = '';
    [0.25, 0.5, 0.75, 1].forEach(f => {
      grid += `<polygon points="${axes.map((_, i) => pt(i, R * f).map(n => n.toFixed(1)).join(',')).join(' ')}" fill="none" stroke="rgba(255,255,255,.06)" stroke-width="1"/>`;
    });
    let spokes = '', labels = '';
    axes.forEach((a, i) => {
      const [ex, ey] = pt(i, R);
      spokes += `<line x1="${cx}" y1="${cy}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}" stroke="rgba(255,255,255,.06)"/>`;
      const [lx, ly] = pt(i, R + 13);
      const anchor = Math.abs(lx - cx) < 6 ? 'middle' : (lx > cx ? 'start' : 'end');
      labels += `<text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" text-anchor="${anchor}" dominant-baseline="middle" font-size="9.5" fill="var(--vx-text-muted,#817d77)">${a.label}</text>`;
    });
    const clamp = (v) => Math.max(0, Math.min(1, (v || 0) / max));
    const vpts = axes.map((a, i) => pt(i, R * clamp(a.value)).map(n => n.toFixed(1)).join(',')).join(' ');
    const col = o.color || C.colors.brand;
    const dots = axes.map((a, i) => { const [px, py] = pt(i, R * clamp(a.value)); return `<circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="2.6" fill="${col}"/>`; }).join('');
    const aria = (o.ariaLabel || 'radar') + ' : ' + axes.map(a => a.label + ' ' + Math.round(a.value || 0)).join(', ');
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px;display:block;margin:0 auto" role="img" aria-label="${aria.replace(/"/g, '&quot;')}">
      ${grid}${spokes}<polygon points="${vpts}" fill="${col}" fill-opacity=".18" stroke="${col}" stroke-width="1.8"/>${dots}${labels}</svg>`;
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

  /* ── Anneaux concentriques (multi-métriques en %) — composite, scorecard ──
     opts: {items:[{label, value, max?(=100), color?}], size?, centerLabel?, centerValue?, ariaLabel, emptyHtml}
     Jusqu'à 5 anneaux, extérieur → intérieur. SVG pur, accessible. */
  C.rings = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    const items = (o.items || []).filter(d => d && d.value != null && !isNaN(d.value)).slice(0, 5);
    if (!items.length) { el.innerHTML = o.emptyHtml || ''; return null; }
    const S = o.size || 200, cx = S / 2, cy = S / 2;
    const gap = 4, sw = Math.max(6, (S / 2 - 24) / items.length - gap);
    const TAU = Math.PI * 2;
    let rings = '', legend = '';
    items.forEach((d, i) => {
      const r = (S / 2 - 10) - i * (sw + gap);
      const frac = Math.max(0, Math.min(1, (d.value || 0) / (d.max || 100)));
      const col = d.color || C.colors.series[i % C.colors.series.length];
      const circ = TAU * r;
      // piste + arc de valeur (départ à 12h, sens horaire)
      rings += `<circle cx="${cx}" cy="${cy}" r="${r.toFixed(1)}" fill="none" stroke="${col}" stroke-opacity=".16" stroke-width="${sw.toFixed(1)}"/>`;
      rings += `<circle cx="${cx}" cy="${cy}" r="${r.toFixed(1)}" fill="none" stroke="${col}" stroke-width="${sw.toFixed(1)}" stroke-linecap="round"
        stroke-dasharray="${(circ * frac).toFixed(1)} ${(circ * (1 - frac) + circ).toFixed(1)}"
        transform="rotate(-90 ${cx} ${cy})"/>`;
      legend += `<div class="vx-flex" style="gap:6px;align-items:center;font-size:11px">
        <span style="width:9px;height:9px;border-radius:2px;background:${col};flex:0 0 auto"></span>
        <span class="vx-grow vx-truncate" style="color:var(--vx-text-secondary,#b7b2aa)">${String(d.label)}</span>
        <b class="vx-mono" style="color:${col}">${Number.isInteger(d.value) ? d.value : (+d.value).toFixed(1)}${o.unit || ' %'}</b></div>`;
    });
    const center = (o.centerValue != null)
      ? `<text x="${cx}" y="${cy - 2}" text-anchor="middle" font-size="26" font-weight="800" fill="var(--vx-text-primary,#f3f1ed)" style="font-variant-numeric:tabular-nums">${o.centerValue}</text>
         ${o.centerLabel ? `<text x="${cx}" y="${cy + 16}" text-anchor="middle" font-size="9.5" fill="var(--vx-text-muted,#817d77)">${o.centerLabel}</text>` : ''}`
      : '';
    const aria = (o.ariaLabel || 'anneaux') + ' : ' + items.map(d => d.label + ' ' + Math.round(d.value)).join(', ');
    el.innerHTML = `<div class="vx-flex vx-wrap" style="gap:14px;align-items:center;justify-content:center">
      <svg viewBox="0 0 ${S} ${S}" width="${S}" style="max-width:${S}px;flex:0 0 auto" role="img" aria-label="${aria.replace(/"/g, '&quot;')}">${rings}${center}</svg>
      <div style="flex:1;min-width:140px;display:flex;flex-direction:column;gap:6px">${legend}</div></div>`;
    return el;
  };

  /* ── Entonnoir de conversion (étapes qui se resserrent) — pipeline de sélection ──
     opts: {stages:[{label, value, color?}], ariaLabel, fmt?, emptyHtml}
     Trapèzes centrés, largeur ∝ valeur, % de l'étape initiale affiché. */
  C.funnel = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    const stages = (o.stages || []).filter(s => s && s.value != null && !isNaN(s.value));
    if (stages.length < 2) { el.innerHTML = o.emptyHtml || ''; return null; }
    const fmt = o.fmt || ((v) => v);
    const top = Math.max(...stages.map(s => s.value), 1);
    const W = o.width || 320, rowH = 34, gap = 6, H = stages.length * (rowH + gap);
    const cx = W / 2, minW = 26;
    let rows = '';
    stages.forEach((s, i) => {
      const w0 = minW + (W - minW) * (Math.max(0, s.value) / top);
      const next = stages[i + 1];
      const w1 = next ? minW + (W - minW) * (Math.max(0, next.value) / top) : w0 * 0.86;
      const y = i * (rowH + gap);
      const col = s.color || C.colors.series[i % C.colors.series.length];
      const pct = Math.round(s.value / top * 100);
      rows += `<polygon points="${(cx - w0 / 2).toFixed(1)},${y} ${(cx + w0 / 2).toFixed(1)},${y} ${(cx + w1 / 2).toFixed(1)},${y + rowH} ${(cx - w1 / 2).toFixed(1)},${y + rowH}"
        fill="${col}" fill-opacity=".8"/>
        <text x="${cx}" y="${y + rowH / 2 - 1}" text-anchor="middle" dominant-baseline="middle" font-size="12" font-weight="800" fill="#0b0b0c" style="font-variant-numeric:tabular-nums">${fmt(s.value)}</text>`;
      rows += `<text x="8" y="${y + rowH / 2}" dominant-baseline="middle" font-size="10.5" fill="var(--vx-text-secondary,#b7b2aa)">${String(s.label)}</text>
        <text x="${W - 6}" y="${y + rowH / 2}" text-anchor="end" dominant-baseline="middle" font-size="10" fill="var(--vx-text-muted,#817d77)" style="font-variant-numeric:tabular-nums">${pct}%</text>`;
    });
    const aria = (o.ariaLabel || 'entonnoir') + ' : ' + stages.map(s => s.label + ' ' + fmt(s.value)).join(' → ');
    /* max-width : évite que l'entonnoir ne s'étire grotesquement sur une carte
       large (le viewBox 320px scalé à 100% gonflait tout ×4). Centré. */
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="display:block;max-width:${o.maxWidth || 460}px;margin:0 auto" role="img" aria-label="${aria.replace(/"/g, '&quot;')}">${rows}</svg>`;
    return el;
  };

  /* ── Barres-étincelles (mini bar chart pour tuiles KPI) ──
     C.sparkbars(hostOrEl, values[], {color?, height?, posNeg?}) */
  C.sparkbars = function (host, values, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {}, v = (values || []).filter(x => x != null && !isNaN(x));
    if (v.length < 2) { el.innerHTML = ''; return null; }
    const H = o.height || 30, W = Math.max(40, v.length * 5), max = Math.max(...v.map(Math.abs), 1e-9);
    const bw = W / v.length * 0.7, gap = W / v.length * 0.3;
    const bars = v.map((x, i) => {
      const h = Math.max(1, Math.abs(x) / max * (H - 2));
      const col = o.posNeg ? (x >= 0 ? C.colors.positive : C.colors.negative) : (o.color || C.colors.brand);
      return `<rect x="${(i * (bw + gap)).toFixed(1)}" y="${(H - h).toFixed(1)}" width="${bw.toFixed(1)}" height="${h.toFixed(1)}" rx="1" fill="${col}" opacity=".9"/>`;
    }).join('');
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}" preserveAspectRatio="none" style="display:block" aria-hidden="true">${bars}</svg>`;
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
