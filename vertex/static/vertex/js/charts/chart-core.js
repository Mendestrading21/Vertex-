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
    brand: '#DBE1E8', blue: '#45D6E8', cyan: '#45D6E8', violet: '#9B7BFF',
    positive: '#2BBE90', negative: '#E9555F', warning: '#D9BE3C',
    info: '#45D6E8', neutral: '#BABABA',
    text: '#BABABA', muted: '#989092', grid: 'rgba(255,255,255,.05)',
    /* lot 56 : séries réordonnées pour un contraste réel entre courbes
       comparées (marque, cyan, sable, violet, jaune, gris) — les trois
       premiers étaient des blancs-gris indistinguables. Palette inchangée. */
    series: ['#DBE1E8', '#45D6E8', '#c8bfae', '#9B7BFF', '#D9BE3C', '#8A8284'],
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
  /* Détruit UNE instance sur un canvas donné (registre + registre interne Chart.js). */
  function destroyOn(canvas) {
    if (!canvas) return;
    try {
      const c = registry.get(canvas) || (window.Chart && Chart.getChart && Chart.getChart(canvas));
      if (c) c.destroy();
    } catch (e) {}
    registry.delete(canvas);
  }
  /* Détruit TOUS les graphiques Chart.js montés (appelé au teardown de page — anti-fuite
     sur navigation SPA : les canvas de la page sortante seraient sinon orphelins). */
  C.destroyAll = function () {
    try {
      document.querySelectorAll('canvas').forEach(function (cv) {
        const c = window.Chart && Chart.getChart && Chart.getChart(cv);
        if (c) { try { c.destroy(); } catch (e) {} }
      });
    } catch (e) {}
    registry.clear();
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

  /* Badge de fraîcheur canonique — langage visuel unique de l'honnêteté.
     freshness ∈ live | delayed | stale | demo | offline | missing. */
  C.freshnessBadge = function (freshness) {
    if (!freshness) return '';
    const f = String(freshness).toLowerCase();
    const map = {
      live: ['live', 'Live'], delayed: ['delayed', 'Différé'],
      stale: ['frozen', 'Périmé'], demo: ['fallback', 'Démo'],
      offline: ['offline', 'Hors ligne'], missing: ['offline', 'Indisponible'],
    };
    const m = map[f] || ['fallback', freshness];
    return `<span class="vx-freshness" data-live="${m[0]}" title="Fraîcheur : ${m[1]}">` +
      `<span class="vx-live-dot"></span>${m[1]}</span>`;
  };

  /* Corps d'état honnête du Chart Shell : loading / empty / stale / error. */
  C._stateBody = function (state, opts) {
    const h = opts.height || 200;
    const msg = opts.stateMessage;
    if (state === 'loading')
      return `<div class="vx-chart-body" style="height:${h}px" aria-busy="true">${VX.states.loading(3)}</div>`;
    if (state === 'stale')
      return `<div class="vx-stale-banner">⏱ Données périmées — ${msg || 'dernière valeur connue affichée.'}</div>` +
        `<div class="vx-chart-body" style="height:${h}px"><div class="vx-state" data-state="stale"><div class="vx-state-icon">⏱</div><div><b>Périmé</b><br>${msg || 'Rafraîchir pour actualiser.'}</div></div></div>`;
    if (state === 'error')
      return `<div class="vx-chart-body" style="height:${h}px"><div class="vx-state" data-tone="error" data-state="error"><div class="vx-state-icon">!</div><div><b>Erreur</b><br>${msg || 'Impossible de charger ce graphique.'}</div></div></div>`;
    /* empty (défaut) — assumé, jamais un rectangle vide */
    return `<div class="vx-chart-body" style="height:${h}px"><div class="vx-state" data-state="empty"><div class="vx-state-icon">—</div><div><b>Donnée indisponible</b><br>${msg || opts.question || 'Aucune donnée à afficher.'}</div></div></div>`;
  };

  /* Raccourci : rendre un Chart Shell dans un état donné (sans canvas). */
  C.cardState = function (host, opts) {
    return C.card(host, Object.assign({}, opts, { state: (opts && opts.state) || 'empty' }));
  };

  C.card = function (host, opts) {
    /* CHART SHELL CANONIQUE (§34). opts:
       {title, question, conclusion, timeframe, unit, freshness, summary,
        controlsHtml, height, source, timestamp, mode, limits,
        explain:{shows,why,confirm,invalidate}, legend:[{label,color}],
        state:'loading'|'empty'|'stale'|'error', stateMessage,
        render(canvas)->Chart}
       Contrat : titre · question · conclusion · période · unité · source ·
       fraîcheur · légende · aide · résumé accessible · skeleton/vide/périmé/erreur. */
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    destroyOn(el.querySelector('canvas'));   // anti-fuite : détruit le graphique du rendu précédent
    const id = 'vxch-' + (++uid);
    const legend = (opts.legend || []).map(l =>
      `<span><span class="vx-swatch" style="background:${l.color}"></span>${l.label}</span>`).join('');
    el.classList.add('vx-card', 'vx-chart-card');
    const head = `
      <div class="vx-chart-head">
        <span class="vx-chart-title">${opts.title || ''}</span>
        ${opts.timeframe ? `<span class="vx-badge">${opts.timeframe}</span>` : ''}
        ${opts.unit ? `<span class="vx-badge vx-badge-unit">${opts.unit}</span>` : ''}
        ${C.freshnessBadge(opts.freshness)}
        <span class="vx-chart-controls">${opts.controlsHtml || ''}</span>
        ${opts.question ? `<span class="vx-chart-question">${opts.question}</span>` : ''}
        ${opts.conclusion ? `<span class="vx-chart-conclusion">${opts.conclusion}</span>` : ''}
      </div>`;

    /* États honnêtes : pas de canvas, on rend l'état et on sort. */
    if (opts.state && opts.state !== 'ready') {
      el.innerHTML = head + C._stateBody(opts.state, opts);
      return null;
    }

    const summary = opts.summary || opts.conclusion || opts.title || 'graphique';
    el.innerHTML = head +
      `<div class="vx-chart-body" style="height:${opts.height || 200}px"><canvas id="${id}" role="img" aria-label="${summary}"></canvas></div>` +
      (opts.summary ? `<p class="vx-sr-only">${opts.summary}</p>` : '') +
      (legend ? `<div class="vx-chart-legend">${legend}</div>` : '') +
      `<div class="vx-chart-foot">
        ${VX.updateIndicator(opts.timestamp, opts.source, opts.mode)}
        ${opts.unit ? `<span class="vx-meta">Unité : ${opts.unit}</span>` : ''}
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
        <div class="vx-meta">Source : ${opts.source || 'n/d'}${opts.unit ? ' · Unité : ' + opts.unit : ''} · ${VX.fmt.ago(opts.timestamp)}${opts.limits ? ' · ' + opts.limits : ''}</div>`);
    });
    return chart;
  };

  /* ── Primitives réutilisées par tous les modules ─────────────────── */
  C.sparkline = function (canvas, values, { color, positiveIsGood = true, fill = true } = {}) {
    if (!canvas || !values || values.length < 2) return null;
    const up = values[values.length - 1] >= values[0];
    const col = color || (up === positiveIsGood ? C.colors.positive : C.colors.negative);
    /* signature 2026 (lot 53) : lissage monotone + mini-aire en dégradé —
       le rendu watchlist des apps de courtage, muet (aucune interaction). */
    return C.mount(canvas, {
      type: 'line',
      data: { labels: values.map((_, i) => i), datasets: [{ data: values, borderColor: col, borderWidth: 1.6, pointRadius: 0, cubicInterpolationMode: 'monotone', tension: .35, fill,
        backgroundColor: (ctx) => {
          const g = ctx.chart.ctx.createLinearGradient(0, 0, 0, ctx.chart.height || 60);
          g.addColorStop(0, col + '33'); g.addColorStop(1, col + '00'); return g;
        } }] },
      options: { scales: { x: { display: false }, y: { display: false } }, plugins: { tooltip: { enabled: false } }, events: [] },
    });
  };
  /* ── Signature visuelle 2026 (LOT 51) — appliquée CENTRALEMENT à C.area ──
     Courbe LISSE monotone (jamais de dépassement au-delà des données réelles),
     dégradé riche 3 arrêts, glow subtil de la ligne, pastille de dernier prix
     façon app de courtage. Palette : C.colors + suffixes alpha sur la couleur
     reçue (même idiome que l'existant — aucun littéral nouveau). */
  C.glowPlugin = function (color) {
    return {
      id: 'vxGlow',
      beforeDatasetDraw(chart, args) {
        if (args.index !== 0) return;
        const ctx = chart.ctx;
        ctx.save(); ctx.shadowColor = color + '59'; ctx.shadowBlur = 7;
        ctx.shadowOffsetY = 1;
      },
      afterDatasetDraw(chart, args) {
        if (args.index !== 0) return;
        chart.ctx.restore();
      },
    };
  };
  C.crosshairPlugin = function (color) {
    /* ligne de visée verticale au survol (type app de courtage) — suit le
       point ACTIF du tooltip (mode index) + point surligné ; jamais
       dessinée hors survol. */
    return {
      id: 'vxCrosshair',
      afterDatasetsDraw(chart) {
        const tt = chart.tooltip;
        if (!tt || !tt.getActiveElements) return;
        const active = tt.getActiveElements();
        if (!active.length || tt.opacity === 0) return;
        const el = active[0].element, area = chart.chartArea, ctx = chart.ctx;
        ctx.save();
        ctx.strokeStyle = color + '59';
        ctx.setLineDash([3, 3]); ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(el.x, area.top); ctx.lineTo(el.x, area.bottom); ctx.stroke();
        ctx.setLineDash([]);
        ctx.beginPath(); ctx.arc(el.x, el.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = color; ctx.fill();
        ctx.restore();
      },
    };
  };
  C.lastDotPlugin = function (color, yFmt) {
    /* pastille + halo sur le DERNIER point réel + pilule de prix au bord
       droit (lastValueLabel) — la donnée affichée est la vraie dernière
       valeur de la série, jamais interpolée. */
    return {
      id: 'vxLastDot',
      afterDatasetsDraw(chart) {
        const meta = chart.getDatasetMeta(0);
        const data = (chart.data.datasets[0] || {}).data || [];
        if (!meta || !meta.data || !meta.data.length || !data.length) return;
        let i = data.length - 1;
        while (i >= 0 && (data[i] === null || data[i] === undefined)) i--;
        if (i < 0 || !meta.data[i]) return;
        const pt = meta.data[i], ctx = chart.ctx, area = chart.chartArea;
        ctx.save();
        ctx.beginPath(); ctx.arc(pt.x, pt.y, 7, 0, Math.PI * 2);
        ctx.fillStyle = color + '22'; ctx.fill();               /* halo */
        ctx.beginPath(); ctx.arc(pt.x, pt.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = color; ctx.fill();                      /* point */
        const raw = data[i];
        const txt = (typeof yFmt === 'function') ? yFmt(raw)
          : (window.VX && VX.fmt && VX.fmt.price ? VX.fmt.price(raw) : String(raw));
        ctx.font = '600 10px ' + ((window.Chart && Chart.defaults.font.family) || 'Inter,sans-serif');
        const w = ctx.measureText(txt).width + 12, h = 16, r = 8;
        let x = Math.min(pt.x + 10, area.right - w), y = pt.y - h / 2;
        y = Math.max(area.top, Math.min(y, area.bottom - h));
        ctx.beginPath(); ctx.roundRect(x, y, w, h, r);
        ctx.fillStyle = color; ctx.fill();
        const tt = (window.VXChartTheme && VXChartTheme.tooltip) || {};
        ctx.fillStyle = tt.backgroundColor || '#151719';        /* texte sur pilule */
        ctx.textBaseline = 'middle';
        ctx.fillText(txt, x + 6, y + h / 2 + 0.5);              /* lastValueLabel */
        ctx.restore();
      },
    };
  };
  /* GRAMMAIRE TV (lot 197) : motif hachuré 45° réutilisable — équivalent
     CANVAS du tvHatch SVG (teinte faible + rayures fines) : la texture qui
     dit « estimation/projection, pas un réel » sur les remplissages. */
  C.hatchPattern = function (color) {
    const t = document.createElement('canvas'); t.width = 8; t.height = 8;
    const g = t.getContext('2d');
    g.globalAlpha = .08; g.fillStyle = color; g.fillRect(0, 0, 8, 8);
    g.globalAlpha = .38; g.strokeStyle = color; g.lineWidth = 1.4;
    g.beginPath();
    g.moveTo(-2, 10); g.lineTo(10, -2);
    g.moveTo(-2, 2); g.lineTo(2, -2);
    g.moveTo(6, 10); g.lineTo(10, 6);
    g.stroke();
    return g.createPattern(t, 'repeat');
  };
  /* GRAMMAIRE TV (lot 195) : chips Max/Min posés sur les extrêmes RÉELS de la
     série — équivalent canvas du tvEdgeChip SVG (fond plein, texte sombre).
     which : undefined = les deux · 'max' | 'min' = un seul. */
  C.tvExtremesPlugin = function (color, yFmt, which) {
    const lbl = (v) => (typeof yFmt === 'function') ? yFmt(v)
      : (window.VX && VX.fmt && VX.fmt.price ? VX.fmt.price(v) : String(v));
    return {
      id: 'vxTvExtremes',
      afterDatasetsDraw(chart) {
        const meta = chart.getDatasetMeta(0);
        const data = (chart.data.datasets[0] || {}).data || [];
        if (!meta || !meta.data || !meta.data.length || !data.length) return;
        let iMax = -1, iMin = -1;
        data.forEach((v, i) => {
          if (v === null || v === undefined || isNaN(v)) return;
          if (iMax < 0 || v > data[iMax]) iMax = i;
          if (iMin < 0 || v < data[iMin]) iMin = i;
        });
        if (iMax < 0 || iMax === iMin) return;
        const ctx = chart.ctx, area = chart.chartArea;
        const tt = (window.VXChartTheme && VXChartTheme.tooltip) || {};
        const chip = (i, tag) => {
          const pt = meta.data[i]; if (!pt) return;
          const txt = tag + ' ' + lbl(data[i]);
          ctx.save();
          ctx.font = '700 9px ' + ((window.Chart && Chart.defaults.font.family) || 'Inter,sans-serif');
          const w = ctx.measureText(txt).width + 10, h = 14;
          const x = Math.max(area.left, Math.min(pt.x - w / 2, area.right - w));
          let y = tag === 'Max' ? pt.y - h - 6 : pt.y + 6;
          y = Math.max(area.top, Math.min(y, area.bottom - h));
          ctx.beginPath(); ctx.roundRect(x, y, w, h, 7);
          ctx.fillStyle = color; ctx.fill();
          ctx.fillStyle = tt.backgroundColor || '#151719';
          ctx.textBaseline = 'middle';
          ctx.fillText(txt, x + 5, y + h / 2 + 0.5);
          ctx.restore();
        };
        if (which !== 'min') chip(iMax, 'Max');
        if (which !== 'max') chip(iMin, 'Min');
      },
    };
  };
  C.area = function (canvas, labels, values, { color = C.colors.blue, yFmt, fill = true, extraDatasets = [], last = true, glow = true, crosshair = true, extremes = false, hatch = false } = {}) {
    const plugins = [];
    if (glow) plugins.push(C.glowPlugin(color));
    if (crosshair) plugins.push(C.crosshairPlugin(color));
    if (last) plugins.push(C.lastDotPlugin(color, yFmt));
    if (extremes) plugins.push(C.tvExtremesPlugin(color, yFmt, extremes === true ? undefined : extremes));
    return C.mount(canvas, {
      type: 'line',
      data: { labels, datasets: [{ data: values, borderColor: color, borderWidth: 1.8, pointRadius: 0,
        cubicInterpolationMode: 'monotone', tension: .35, fill,
        /* LOT 120 : dégradé vertical à 4 arrêts — descente plus douce
           (jamais un aplat), fin totalement transparente.
           LOT 197 (tournée TV) : hatch=true → remplissage HACHURÉ
           (C.hatchPattern) = la texture « estimation/projection ». */
        backgroundColor: hatch ? C.hatchPattern(color) : (ctx) => {
          const g = ctx.chart.ctx.createLinearGradient(0, 0, 0, ctx.chart.height || 200);
          g.addColorStop(0, color + '59'); g.addColorStop(.3, color + '2E');
          g.addColorStop(.62, color + '12'); g.addColorStop(1, color + '00');
          return g;
        } }, ...extraDatasets] },
      options: { scales: C.axes({ yFmt }), interaction: { mode: 'index', intersect: false } },
      plugins,
    });
  };
  C.bars = function (canvas, labels, values, { colors, horizontal = false, yFmt } = {}) {
    const cols = colors || values.map(v => v >= 0 ? C.colors.positive : C.colors.negative);
    /* signature 2026 (lot 53) + LOT 125 : matière VERRE — chaque barre est un
       dégradé de sa PROPRE couleur, dense à l'extrémité de la valeur et doux
       vers la base (même grammaire que le treemap/l'aire), liseré fin de la
       couleur, PLEINE au survol. L'alpha n'est appliqué qu'aux hex 6 digits —
       toute autre couleur passe inchangée, jamais corrompue. */
    const isHex = (c) => typeof c === 'string' && /^#[0-9A-Fa-f]{6}$/.test(c);
    const glass = (ctx) => {
      const c = cols[ctx.dataIndex % cols.length];
      if (!isHex(c)) return c;
      const area = ctx.chart.chartArea;
      if (!area) return c + 'D9';
      const neg = Number(ctx.raw) < 0;
      const g = horizontal
        ? ctx.chart.ctx.createLinearGradient(area.left, 0, area.right, 0)
        : ctx.chart.ctx.createLinearGradient(0, area.top, 0, area.bottom);
      /* extrémité de la valeur = dense (E0), base = douce (55) */
      if (horizontal ? neg : !neg) { g.addColorStop(0, c + 'E0'); g.addColorStop(1, c + '55'); }
      else { g.addColorStop(0, c + '55'); g.addColorStop(1, c + 'E0'); }
      return g;
    };
    /* GRAMMAIRE TV (lot 199) : la barre DOMINANTE (|valeur| max, si ≥ 2
       barres) porte un liseré appuyé + sa VALEUR en chip pleine couleur
       (texte sombre) au bout de la barre — même langage que la barre
       dominante du consensus (191) et la cellule dominante de la heatmap
       (194). Les autres barres gardent leur matière verre inchangée. */
    const domI = values.length >= 2
      ? values.reduce((b, v, i) => Math.abs(Number(v) || 0) > Math.abs(Number(values[b]) || 0) ? i : b, 0)
      : -1;
    const domPlugin = {
      id: 'vxBarDominant',
      afterDatasetsDraw(chart) {
        if (domI < 0) return;
        const meta = chart.getDatasetMeta(0);
        const pt = meta && meta.data && meta.data[domI]; if (!pt) return;
        const v = Number(values[domI]); if (!isFinite(v)) return;
        const col = cols[domI % cols.length];
        const txt = (typeof yFmt === 'function') ? yFmt(v) : String(v);
        const ctx = chart.ctx, area = chart.chartArea;
        ctx.save();
        ctx.font = '700 9px ' + ((window.Chart && Chart.defaults.font.family) || 'Inter,sans-serif');
        const w = ctx.measureText(txt).width + 10, h = 14;
        let x, y;
        if (horizontal) { x = v >= 0 ? pt.x + 4 : pt.x - w - 4; y = pt.y - h / 2; }
        else { x = pt.x - w / 2; y = v >= 0 ? pt.y - h - 4 : pt.y + 4; }
        x = Math.max(area.left, Math.min(x, area.right - w));
        y = Math.max(area.top, Math.min(y, area.bottom - h));
        ctx.beginPath(); ctx.roundRect(x, y, w, h, 7);
        ctx.fillStyle = (typeof col === 'string') ? col : C.colors.neutral; ctx.fill();
        const tt = (window.VXChartTheme && VXChartTheme.tooltip) || {};
        ctx.fillStyle = tt.backgroundColor || '#151719'; ctx.textBaseline = 'middle';
        ctx.fillText(txt, x + 5, y + h / 2 + 0.5);
        ctx.restore();
      },
    };
    return C.mount(canvas, {
      type: 'bar',
      data: { labels, datasets: [{ data: values, backgroundColor: glass, hoverBackgroundColor: cols,
        borderColor: cols.map((c, i) => isHex(c) ? (i === domI ? c : c + '80') : c),
        borderWidth: values.map((_, i) => i === domI ? 1.6 : 1),
        borderRadius: 5, borderSkipped: false, maxBarThickness: 26 }] },
      options: { indexAxis: horizontal ? 'y' : 'x', scales: C.axes({ yFmt }) },
      plugins: [domPlugin],
    });
  };
  C.donut = function (canvas, labels, values, { colors } = {}) {
    /* §33 : un donut ≤ ~5 catégories · signature 2026 (lot 53) : arcs
       arrondis espacés + léger décalage au survol.
       LOT 128 : LE chiffre éducatif du donut — la catégorie DOMINANTE et sa
       part (%) affichées au CENTRE de l'anneau, dans la couleur de son arc.
       L'œil lit la conclusion sans additionner de tête. Rien si total nul. */
    const l = labels.slice(0, 5), v = values.slice(0, 5);
    const center = {
      id: 'vxDonutCenter',
      afterDatasetsDraw(chart) {
        const total = v.reduce((a, b) => a + (Number(b) || 0), 0);
        if (!(total > 0)) return;
        let bi = 0; v.forEach((x, i) => { if (Number(x) > Number(v[bi])) bi = i; });
        const meta = chart.getDatasetMeta(0);
        if (!meta || !meta.data || !meta.data[0]) return;
        const { x, y } = meta.data[0];
        const cols = chart.data.datasets[0].backgroundColor || C.colors.series;
        const { ctx } = chart;
        ctx.save();
        ctx.textAlign = 'center';
        ctx.fillStyle = cols[bi] || C.colors.brand;
        ctx.font = '800 19px sans-serif';
        ctx.fillText(Math.round(Number(v[bi]) / total * 100) + ' %', x, y - 2);
        ctx.fillStyle = C.colors.muted;
        ctx.font = '10px sans-serif';
        ctx.fillText(String(l[bi] == null ? '' : l[bi]).slice(0, 14), x, y + 13);
        ctx.restore();
      },
    };
    return C.mount(canvas, {
      type: 'doughnut',
      data: { labels: l, datasets: [{ data: v, backgroundColor: colors || C.colors.series, borderWidth: 0, borderRadius: 4, spacing: 2, hoverOffset: 6 }] },
      options: { cutout: '70%', plugins: { legend: { display: true, position: 'right', labels: { boxWidth: 10, font: { size: 10 } } } } },
      plugins: [center],
    });
  };
  /* LOT 120 — finition « ultra propre » des lignes multiples : chaque série
     se termine par un POINT NET dans sa couleur (halo léger) et son NOM court
     collé au bout de la ligne — l'œil suit une courbe jusqu'à son identité,
     sans aller-retour avec la légende. Aucun littéral couleur nouveau. */
  C.endDotsPlugin = function (withLabels) {
    return {
      id: 'vxEndDots',
      afterDatasetsDraw(chart) {
        const { ctx } = chart;
        /* LOT 129 : anti-collision des noms de série — deux lignes qui
           finissent à la même hauteur (ex. courbe des taux « Actuelle » /
           « Séance préc. ») écartent leurs étiquettes d'au moins 11 px au
           lieu de s'écrire l'une sur l'autre. */
        const placed = [];
        const labelY = (y) => {
          let yy = y;
          for (let g = 0; g < 8; g++) {
            const hit = placed.find(p => Math.abs(p - yy) < 11);
            if (!hit) break;
            yy = hit + 11;
          }
          placed.push(yy);
          return yy;
        };
        chart.data.datasets.forEach((d, i) => {
          const meta = chart.getDatasetMeta(i);
          if (!meta || meta.hidden || !meta.data || !meta.data.length) return;
          const pt = meta.data[meta.data.length - 1];
          if (!pt || pt.x == null) return;
          const col = (typeof d.borderColor === 'string' && d.borderColor) || C.colors.series[i % 6];
          ctx.save();
          ctx.fillStyle = col;
          ctx.globalAlpha = .22;
          ctx.beginPath(); ctx.arc(pt.x, pt.y, 6, 0, Math.PI * 2); ctx.fill();   /* halo */
          ctx.globalAlpha = 1;
          ctx.beginPath(); ctx.arc(pt.x, pt.y, 2.6, 0, Math.PI * 2); ctx.fill(); /* point net */
          if (withLabels && d.label) {
            ctx.font = '600 9px ' + ((window.Chart && Chart.defaults.font.family) || 'Inter,sans-serif');
            ctx.textBaseline = 'middle';
            ctx.fillText(String(d.label).slice(0, 11), pt.x + 8, labelY(pt.y));
          }
          ctx.restore();
        });
      },
    };
  };
  /* Halo néon très doux sous chaque trait — la matière Neon Glass sans bruit. */
  C.softGlowPlugin = function () {
    return {
      id: 'vxSoftGlow',
      beforeDatasetDraw(chart, args) {
        const d = chart.data.datasets[args.index] || {};
        chart.ctx.save();
        if (typeof d.borderColor === 'string') {
          chart.ctx.shadowColor = d.borderColor;
          chart.ctx.shadowBlur = 4;
        }
      },
      afterDatasetDraw(chart) { chart.ctx.restore(); },
    };
  };
  C.multiLine = function (canvas, labels, datasets, { yFmt, crosshair = true } = {}) {
    /* signature 2026 affinée (lot 120) : traits FINS (1.6), halo néon doux,
       point terminal net + nom de série en bout de ligne. Lissage monotone
       conservé (jamais de faux extrêmes). */
    return C.mount(canvas, {
      type: 'line',
      data: { labels, datasets: datasets.map((d, i) => Object.assign({ borderColor: C.colors.series[i % 6], borderWidth: 1.6, pointRadius: 0, cubicInterpolationMode: 'monotone', tension: .35, fill: false }, d)) },
      options: { scales: C.axes({ yFmt }), interaction: { mode: 'index', intersect: false },
        layout: { padding: { right: 54 } },
        plugins: { legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } } },
      plugins: [...(crosshair ? [C.crosshairPlugin(C.colors.brand)] : []),
                C.softGlowPlugin(), C.endDotsPlugin(true)],
    });
  };
  /* Annotations de niveaux (entrée/stop/TP…) — plugin ligne horizontale. */
  C.levelLines = function (levels) {
    /* levels: [{value,label,kind:'entry'|'stop'|'tp'|'support'|'resistance'}]
       GRAMMAIRE TV (lot 202) : chaque niveau du PLAN porte son étiquette en
       CHIP pleine couleur au BORD DROIT (texte sombre) — comme les étiquettes
       de l'échelle de prix TradingView — avec anti-collision verticale
       (empilement) et bornage à la zone de tracé. Ligne pointillée inchangée. */
    const colByKind = { entry: C.colors.info, stop: C.colors.negative, tp: C.colors.positive,
      support: C.colors.cyan, resistance: C.colors.warning };
    return {
      id: 'vxLevels',
      afterDatasetsDraw(chart) {
        const { ctx, chartArea, scales } = chart;
        if (!scales.y) return;
        const drawn = [];
        const tt = (window.VXChartTheme && VXChartTheme.tooltip) || {};
        (levels || []).forEach(lv => {
          if (lv.value === null || lv.value === undefined) return;
          const y = scales.y.getPixelForValue(lv.value);
          if (y < chartArea.top || y > chartArea.bottom) return;
          const col = colByKind[lv.kind] || C.colors.muted;
          ctx.save();
          ctx.strokeStyle = col;
          ctx.setLineDash([4, 4]); ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(chartArea.left, y); ctx.lineTo(chartArea.right, y); ctx.stroke();
          ctx.setLineDash([]);
          const txt = `${lv.label || lv.kind} ${VX.fmt.price(lv.value)}`;
          ctx.font = '700 9px ' + ((window.Chart && Chart.defaults.font.family) || 'monospace');
          const w = ctx.measureText(txt).width + 10, h = 14;
          let cy = y;
          while (drawn.some(d => Math.abs(d - cy) < h + 2)) cy += h + 2;
          cy = Math.max(chartArea.top + h / 2, Math.min(cy, chartArea.bottom - h / 2));
          drawn.push(cy);
          const x = chartArea.right - w - 2;
          ctx.beginPath(); ctx.roundRect(x, cy - h / 2, w, h, 7);
          ctx.fillStyle = col; ctx.fill();
          ctx.fillStyle = tt.backgroundColor || '#151719';
          ctx.textBaseline = 'middle';
          ctx.fillText(txt, x + 5, cy + 0.5);
          ctx.restore();
        });
      },
    };
  };
  /* ── GRAMMAIRE TV (tournée graphique, lot 189) ─────────────────────────────
     Helpers partagés par les builders refaits au style TradingView :
     hachures d'ESTIMATION (zones prévisionnelles) et chip d'ÉTIQUETTE DE BORD
     (Max/Moy/Min collés au bord droit, comme le cône de prix cible TV). */
  C.tvHatch = function (id, color) {
    // <defs> réutilisable : rayures diagonales fines = « estimation, pas un réel »
    return `<pattern id="${id}" width="6" height="6" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="${color}" fill-opacity=".08"/>
      <line x1="0" y1="0" x2="0" y2="6" stroke="${color}" stroke-opacity=".38" stroke-width="1.6"/></pattern>`;
  };
  C.tvEdgeChip = function (x, y, text, color, opts) {
    // chip SVG valeur/étiquette collée au bord (fond plein couleur, texte sombre)
    const o = opts || {}; const fs = o.fontSize || 10;
    const w = o.width || (text.length * fs * 0.62 + 12), h = fs + 8;
    const anchor = o.align === 'left' ? x : x - w;
    return `<g role="presentation"><rect x="${anchor.toFixed(1)}" y="${(y - h / 2).toFixed(1)}" width="${w.toFixed(1)}" height="${h}" rx="3" fill="${color}"/>
      <text x="${(anchor + w / 2).toFixed(1)}" y="${(y + fs * 0.36).toFixed(1)}" text-anchor="middle" fill="var(--vx-graphite-850,#121214)" font-size="${fs}" font-weight="800" style="font-variant-numeric:tabular-nums">${text}</text></g>`;
  };

  /* ── Jauge TV (SVG, sans Chart.js) — régime, risk score, VIX, options env ──
     STYLE TRADINGVIEW (lot 189) : arc UNIQUE en dégradé continu construit sur
     les couleurs des bandes (rouge→jaune→vert…), AIGUILLE blanche depuis le
     pivot, libellés de zones au fil de l'arc, état (reading) affiché
     en évidence dans la couleur de la zone courante.
     opts: {value, min=0, max=100, unit, label, reading,
            bands:[{to, color, label?}]}  // zones gauche→droite (ordre croissant)
     Accessible : role=img + aria-label chiffré. Aucune animation permanente. */
  C.gauge = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    const min = o.min != null ? o.min : 0, max = o.max != null ? o.max : 100;
    const v = (o.value == null || isNaN(o.value)) ? null : Math.max(min, Math.min(max, o.value));
    const W = 220, H = 132, cx = 110, cy = 112, r = 86;
    const ang = (t) => Math.PI * (1 - (Math.max(min, Math.min(max, t)) - min) / (max - min)); // 180°→0°
    const pt = (a, rr = r) => [cx + rr * Math.cos(a), cy - rr * Math.sin(a)];
    const arc = (a0, a1, rr = r) => {
      const [x0, y0] = pt(a0, rr), [x1, y1] = pt(a1, rr);
      const large = Math.abs(a0 - a1) > Math.PI ? 1 : 0;
      return `M ${x0.toFixed(1)} ${y0.toFixed(1)} A ${rr} ${rr} 0 ${large} 1 ${x1.toFixed(1)} ${y1.toFixed(1)}`;
    };
    const bands = o.bands && o.bands.length ? o.bands : [{ to: max, color: C.colors.neutral }];
    const gid = 'vxGg-' + ((el.id || 'g').replace(/[^\w-]/g, ''));
    // Dégradé CONTINU le long de l'axe des valeurs : un stop au début et à la
    // fin de chaque bande (les couleurs fondent à la frontière, comme TV).
    const span = max - min;
    let stops = '', prev = min;
    bands.forEach((b, i) => {
      const p0 = ((prev - min) / span), p1 = ((Math.min(b.to, max) - min) / span);
      stops += `<stop offset="${(p0 + 0.04).toFixed(3)}" stop-color="${b.color}"/>`
        + `<stop offset="${Math.max(p0, p1 - 0.04).toFixed(3)}" stop-color="${b.color}"/>`;
      prev = b.to;
    });
    const defs = `<defs><linearGradient id="${gid}" x1="0" y1="0" x2="1" y2="0">${stops}</linearGradient>${C.tvHatch(gid + '-h', C.colors.muted)}</defs>`;
    // piste : l'arc ENTIER en dégradé (léger si pas de valeur, franc sinon)
    const track = `<path d="${arc(ang(min), ang(max))}" stroke="url(#${gid})" stroke-opacity="${v == null ? '.28' : '.9'}" stroke-width="10" fill="none" stroke-linecap="round"/>`;
    // libellés de zones (si fournis) au milieu de chaque bande, hors de l'arc
    let zoneLabels = ''; prev = min;
    bands.forEach(b => {
      if (b.label) {
        const [zx, zy] = pt(ang((prev + Math.min(b.to, max)) / 2), r + 14);
        zoneLabels += `<text x="${zx.toFixed(1)}" y="${zy.toFixed(1)}" text-anchor="middle" fill="var(--vx-text-muted,#989092)" font-size="9" letter-spacing=".4">${b.label}</text>`;
      }
      prev = b.to;
    });
    let needle = '', valColor = C.colors.neutral;
    if (v != null) {
      for (const b of bands) { if (v <= b.to) { valColor = b.color; break; } valColor = b.color; }
      // AIGUILLE TV : pointeur blanc COURT posé sur l'arc (jamais sur le texte
      // central) + halo de la couleur de zone au bout.
      const a = ang(v);
      const [x1, y1] = pt(a, r - 24), [x2, y2] = pt(a, r - 2);
      const [hx, hy] = pt(a, r);
      needle = `<circle cx="${hx.toFixed(1)}" cy="${hy.toFixed(1)}" r="8" fill="${valColor}" fill-opacity=".3"/>`
        + `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="var(--vx-text-primary,#F8F5F3)" stroke-width="3.5" stroke-linecap="round"/>`
        + `<circle cx="${x1.toFixed(1)}" cy="${y1.toFixed(1)}" r="2.4" fill="var(--vx-text-primary,#F8F5F3)"/>`;
    }
    const disp = v == null ? '—' : (Number.isInteger(v) ? v : (+v).toFixed(1));
    const aria = `${o.label || 'jauge'} : ${v == null ? 'donnée indisponible' : disp + (o.unit || '')}${o.reading ? ' — ' + o.reading : ''}`;
    el.innerHTML = `
      <div class="vx-gauge" role="img" aria-label="${aria.replace(/"/g, '&quot;')}">
        <svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:250px;display:block;margin:0 auto">
          ${defs}${track}${zoneLabels}${needle}
          <text x="${cx}" y="${cy - 34}" text-anchor="middle" fill="var(--vx-text-primary,#F8F5F3)" font-size="26" font-weight="800" style="font-variant-numeric:tabular-nums">${disp}<tspan font-size="12" font-weight="600" fill="var(--vx-text-muted,#989092)">${o.unit || ''}</tspan></text>
          <text x="${cx}" y="${cy - 18}" text-anchor="middle" fill="var(--vx-text-muted,#989092)" font-size="9.5" letter-spacing=".5">${o.label || ''}</text>
        </svg>
        ${o.reading ? `<div style="text-align:center;margin-top:2px;font-size:14px;font-weight:800;color:${valColor}">${o.reading}</div>` : ''}
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
    /* LOT 123 — matière VERRE : chaque tuile est un dégradé diagonal de sa
       propre couleur (dense en haut-gauche → doux en bas-droit), liseré fin
       de la couleur elle-même, part du total affichée en haut-droit sur les
       grandes tuiles (LE chiffre éducatif du treemap). Aucun littéral
       couleur nouveau — les couleurs viennent des données. */
    const tid = 'vxTm-' + String(el.id || 't').replace(/[^a-zA-Z0-9_-]/g, '');
    const tdefs = '<defs>' + rects.map((r, i) => {
      const col = r.d.color || C.colors.neutral;
      return `<linearGradient id="${tid}-${i}" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="${col}" stop-opacity=".9"/>
        <stop offset="1" stop-color="${col}" stop-opacity=".45"/>
      </linearGradient>`;
    }).join('') + '</defs>';
    const svg = rects.map((r, i) => {
      const col = r.d.color || C.colors.neutral;
      const small = r.w < 54 || r.h < 30;
      const lbl = String(r.d.label || '');
      const share = Math.round(r.d.value / total * 100);
      const aria = `${lbl} : ${fmt(r.d.value)}${r.d.sub ? ' ' + r.d.sub : ''} (${share} %)`;
      return `<g role="img" aria-label="${aria.replace(/"/g, '&quot;')}">
        <rect x="${r.x.toFixed(1)}" y="${r.y.toFixed(1)}" width="${Math.max(0, r.w - 2).toFixed(1)}" height="${Math.max(0, r.h - 2).toFixed(1)}"
          rx="5" fill="url(#${tid}-${i})" stroke="${col}" stroke-opacity=".5" stroke-width="1"/>
        ${small ? '' : `<text x="${(r.x + 7).toFixed(1)}" y="${(r.y + 17).toFixed(1)}" fill="var(--vx-text-primary,#F8F5F3)" font-size="11" font-weight="700">${lbl.slice(0, Math.floor(r.w / 7))}</text>
        <text x="${(r.x + 7).toFixed(1)}" y="${(r.y + 31).toFixed(1)}" fill="rgba(255,255,255,.82)" font-size="10" style="font-variant-numeric:tabular-nums">${fmt(r.d.value)}${r.d.sub ? ' · ' + r.d.sub : ''}</text>
        ${r.w > 90 ? C.tvEdgeChip(r.x + r.w - 7, r.y + 15, share + ' %', col, { fontSize: 9 }) : ''}`}
      </g>`;
    }).join('');
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="100%" preserveAspectRatio="none" style="display:block">${tdefs}${svg}</svg>`;
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
      svg += `<text x="${(x + bw / 2).toFixed(1)}" y="${(yTop - 4).toFixed(1)}" text-anchor="middle" font-size="10" fill="var(--vx-text-secondary,#BABABA)" style="font-variant-numeric:tabular-nums">${(b.val >= 0 && !b.total ? '+' : '') + fmt(b.val)}</text>`;
      svg += `<text x="${(x + bw / 2).toFixed(1)}" y="${(H - 9).toFixed(1)}" text-anchor="middle" font-size="9" fill="var(--vx-text-muted,#989092)">${String(b.label).slice(0, Math.floor(bw / 6) + 2)}</text>`;
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
    /* LOT 122 — grille en opacité DÉGRESSIVE (l'anneau extérieur guide,
       l'intérieur murmure) : la profondeur se lit sans bruit. */
    let grid = '';
    [[0.25, .035], [0.5, .05], [0.75, .065], [1, .09]].forEach(([f, op]) => {
      grid += `<polygon points="${axes.map((_, i) => pt(i, R * f).map(n => n.toFixed(1)).join(',')).join(' ')}" fill="none" stroke="rgba(255,255,255,${op})" stroke-width="1"/>`;
    });
    let spokes = '', labels = '';
    axes.forEach((a, i) => {
      const [ex, ey] = pt(i, R);
      spokes += `<line x1="${cx}" y1="${cy}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}" stroke="rgba(255,255,255,.06)"/>`;
      const [lx, ly] = pt(i, R + 13);
      const anchor = Math.abs(lx - cx) < 6 ? 'middle' : (lx > cx ? 'start' : 'end');
      labels += `<text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" text-anchor="${anchor}" dominant-baseline="middle" font-size="9.5" fill="var(--vx-text-muted,#989092)">${a.label}</text>`;
    });
    const clamp = (v) => Math.max(0, Math.min(1, (v || 0) / max));
    const vpts = axes.map((a, i) => pt(i, R * clamp(a.value)).map(n => n.toFixed(1)).join(',')).join(' ');
    const col = o.color || C.colors.brand;
    /* LOT 122 — remplissage en dégradé RADIAL (centre transparent → bord
       coloré) : la surface respire au lieu d'être un aplat. Points sommets
       nets avec halo léger. Aucun littéral couleur nouveau. */
    const rid = 'vxRad-' + String(el.id || 'r').replace(/[^a-zA-Z0-9_-]/g, '');
    const rdefs = `<defs><radialGradient id="${rid}" cx="50%" cy="50%" r="65%">
      <stop offset="0" stop-color="${col}" stop-opacity=".04"/>
      <stop offset="1" stop-color="${col}" stop-opacity=".30"/>
    </radialGradient></defs>`;
    const dots = axes.map((a, i) => {
      const [px, py] = pt(i, R * clamp(a.value));
      return `<circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="5" fill="${col}" fill-opacity=".18"/>
        <circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="2.4" fill="${col}"/>`;
    }).join('');
    /* GRAMMAIRE TV (lot 201) : le SOMMET DOMINANT (valeur max réelle) porte
       un anneau de focus + sa valeur en chip pleine couleur (tvEdgeChip),
       posé vers le centre pour ne pas gêner les libellés d'axes. */
    let domMark = '';
    let domI = -1;
    axes.forEach((a, i) => {
      if (a.value != null && !isNaN(a.value) && (domI < 0 || Number(a.value) > Number(axes[domI].value))) domI = i;
    });
    if (domI >= 0 && C.tvEdgeChip) {
      const [dx, dy] = pt(domI, R * clamp(axes[domI].value));
      const [ix, iy] = pt(domI, Math.max(R * clamp(axes[domI].value) - 20, 14));
      const txt = String(Math.round(axes[domI].value || 0));
      domMark = `<circle cx="${dx.toFixed(1)}" cy="${dy.toFixed(1)}" r="6.5" fill="none" stroke="${col}" stroke-opacity=".55" stroke-width="1.5"/>`
        + C.tvEdgeChip(ix - (txt.length * 9 * 0.62 + 12) / 2, iy, txt, col, { align: 'left', fontSize: 9 });
    }
    const aria = (o.ariaLabel || 'radar') + ' : ' + axes.map(a => a.label + ' ' + Math.round(a.value || 0)).join(', ');
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px;display:block;margin:0 auto" role="img" aria-label="${aria.replace(/"/g, '&quot;')}">
      ${rdefs}${grid}${spokes}<polygon points="${vpts}" fill="url(#${rid})" stroke="${col}" stroke-width="1.6" stroke-linejoin="round"/>${dots}${domMark}${labels}</svg>`;
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
        const bg = active ? 'rgba(57,184,120,.09)' : 'var(--vx-surface-2,#121214)';
        const arrow = i < nodes.length - 1 ? '<span aria-hidden="true" style="align-self:center;color:var(--vx-text-muted,#989092);padding:0 5px;font-size:13px">→</span>' : '';
        return '<div style="flex:0 0 auto;min-width:76px;text-align:center;padding:8px 10px;border-radius:9px;background:' + bg + ';border:1px solid ' + col + '55">'
          + '<div style="font-size:10.5px;color:var(--vx-text-secondary,#BABABA);text-transform:capitalize;white-space:nowrap">' + String(n.label) + '</div>'
          + (n.count != null ? '<div style="font-size:15px;font-weight:800;color:' + col + ';font-variant-numeric:tabular-nums">' + n.count + '</div>' : '')
          + (n.sub ? '<div style="font-size:9px;letter-spacing:.04em;text-transform:uppercase;color:var(--vx-text-muted,#989092)">' + n.sub + '</div>' : '')
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
        <span class="vx-grow vx-truncate" style="color:var(--vx-text-secondary,#BABABA)">${String(d.label)}</span>
        <b class="vx-mono" style="color:${col}">${Number.isInteger(d.value) ? d.value : (+d.value).toFixed(1)}${o.unit || ' %'}</b></div>`;
    });
    const center = (o.centerValue != null)
      ? `<text x="${cx}" y="${cy - 2}" text-anchor="middle" font-size="26" font-weight="800" fill="var(--vx-text-primary,#F8F5F3)" style="font-variant-numeric:tabular-nums">${o.centerValue}</text>
         ${o.centerLabel ? `<text x="${cx}" y="${cy + 16}" text-anchor="middle" font-size="9.5" fill="var(--vx-text-muted,#989092)">${o.centerLabel}</text>` : ''}`
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
    /* LOT 121 — entonnoir « ultra propre » : UN SEUL ton de marque en dégradé
       vertical, opacité qui décroît avec la profondeur (la matière raconte la
       déperdition), UN chiffre par étage, la plus forte perte marquée d'un
       −N discret. Fini l'arc-en-ciel et les pourcentages doublés. */
    const gid = 'vxFnl-' + String(el.id || 'f').replace(/[^a-zA-Z0-9_-]/g, '');
    const defs = `<defs><linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${C.colors.brand}"/>
      <stop offset="1" stop-color="${C.colors.cyan}"/>
    </linearGradient></defs>`;
    let worstDrop = 0, worstIdx = -1;
    stages.forEach((s, i) => {
      const next = stages[i + 1];
      if (next && (s.value - next.value) > worstDrop) { worstDrop = s.value - next.value; worstIdx = i; }
    });
    let rows = '';
    stages.forEach((s, i) => {
      const w0 = minW + (W - minW) * (Math.max(0, s.value) / top);
      const next = stages[i + 1];
      const w1 = next ? minW + (W - minW) * (Math.max(0, next.value) / top) : w0 * 0.86;
      const y = i * (rowH + gap);
      const depth = stages.length > 1 ? i / (stages.length - 1) : 0;
      const op = (0.88 - depth * 0.55).toFixed(2);
      rows += `<polygon points="${(cx - w0 / 2).toFixed(1)},${y} ${(cx + w0 / 2).toFixed(1)},${y} ${(cx + w1 / 2).toFixed(1)},${y + rowH} ${(cx - w1 / 2).toFixed(1)},${y + rowH}"
        fill="url(#${gid})" fill-opacity="${op}" stroke="${C.colors.brand}" stroke-opacity=".25" stroke-width="1"/>
        <text x="${cx}" y="${y + rowH / 2 - 1}" text-anchor="middle" dominant-baseline="middle" font-size="12.5" font-weight="800" fill="var(--vx-text,#F8F5F3)" style="font-variant-numeric:tabular-nums">${fmt(s.value)}</text>`;
      rows += `<text x="8" y="${y + rowH / 2}" dominant-baseline="middle" font-size="10.5" fill="var(--vx-text-secondary,#BABABA)">${String(s.label)}</text>`;
      if (i === worstIdx && worstDrop > 0) {
        rows += `<text x="${W - 6}" y="${y + rowH + gap / 2 + 3}" text-anchor="end" font-size="9.5" font-weight="700"
          fill="${C.colors.negative}" fill-opacity=".85" style="font-variant-numeric:tabular-nums">−${fmt(worstDrop)}</text>`;
      }
    });
    const aria = (o.ariaLabel || 'entonnoir') + ' : ' + stages.map(s => s.label + ' ' + fmt(s.value)).join(' → ');
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="display:block" role="img" aria-label="${aria.replace(/"/g, '&quot;')}">${defs}${rows}</svg>`;
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
