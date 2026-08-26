/* radar-chart.js — Radar de valorisation « titre vs médiane sectorielle ».
   Chaque axe est normalisé sur une échelle radiale 0..100 où 50 = médiane du
   secteur ; le polygone du titre se lit d'un coup d'œil contre l'anneau médian.
   DONNÉES RÉELLES uniquement : un axe sans valeur ou sans médiane est écarté
   (jamais de point inventé). Palette Vertex stricte (vert Signal = titre,
   acier = médiane secteur). S'appuie sur Chart.js (RadarController). */
(function () {
  const C = window.VXCharts; if (!C) return;

  /* score radial : 50 = médiane. « high » = plus haut vaut mieux (marge, ROE,
     croissance) ; « low » = plus bas vaut mieux (P/E). Borné [6..100] pour
     rester lisible même sur les écarts extrêmes. */
  function radial(value, median, better) {
    if (value == null || median == null || median === 0) return null;
    const ratio = better === 'low' ? (median / value) : (value / median);
    return Math.max(6, Math.min(100, ratio * 50));
  }

  /* opts: { host, title, question, conclusion, sym, sectorLabel,
             axes:[{label, value, median, better:'high'|'low', fmt(v)->str}],
             source, timestamp, mode } */
  C.valuationRadar = function (host, opts) {
    const axes = (opts.axes || []).filter(a => a.value != null && a.median != null && a.median !== 0);
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    if (axes.length < 3) {
      el.classList.add('vx-card');
      el.innerHTML = '<div class="vx-card-header"><span class="vx-card-title">' +
        (opts.title || 'Valorisation vs secteur') + '</span></div>' +
        (window.VX ? VX.states.empty('Fondamentaux comparables insuffisants pour ce titre.')
                   : '<div class="vx-dim">Données insuffisantes.</div>');
      return null;
    }
    const labels = axes.map(a => a.label);
    const meScore = axes.map(a => radial(a.value, a.median, a.better));
    const medScore = axes.map(() => 50);
    const symName = opts.sym || 'Titre';
    const sectorName = opts.sectorLabel || 'Médiane secteur';
    const fmt = (a, v) => (v == null ? '—' : (a.fmt ? a.fmt(v) : (+v).toFixed(1)));

    return C.card(el, Object.assign({
      height: opts.height || 300,
      legend: [{ label: symName, color: C.colors.brand },
               { label: sectorName, color: C.colors.neutral }],
      render(canvas) {
        if (!window.Chart) return null;
        return C.mount(canvas, {
          type: 'radar',
          data: {
            labels,
            datasets: [
              { label: sectorName, data: medScore,
                borderColor: C.colors.neutral, borderWidth: 1.2, borderDash: [4, 4],
                backgroundColor: 'rgba(143,138,131,.10)',
                pointRadius: 2, pointBackgroundColor: C.colors.neutral, pointBorderWidth: 0 },
              { label: symName, data: meScore,
                borderColor: C.colors.brand, borderWidth: 2,
                backgroundColor: (C.rgba && C.rgba(C.colors.brand, .16)) || 'rgba(201,205,212,.16)',
                pointRadius: 3, pointBackgroundColor: C.colors.brand,
                pointBorderColor: 'rgba(0,0,0,.35)', pointBorderWidth: 1,
                pointHoverRadius: 5 },
            ],
          },
          options: {
            layout: { padding: { top: 10, bottom: 10, left: 30, right: 30 } },
            scales: {
              r: {
                min: 0, max: 100, beginAtZero: true,
                grid: { color: 'rgba(255,255,255,.06)' },
                angleLines: { color: 'rgba(255,255,255,.06)' },
                ticks: { display: false, stepSize: 25 },
                pointLabels: {
                  color: C.colors.text, font: { size: 10.5, weight: '600' },
                  padding: 6,
                },
              },
            },
            plugins: {
              tooltip: {
                callbacks: {
                  title: (items) => labels[items[0].dataIndex],
                  label: (item) => {
                    const a = axes[item.dataIndex];
                    if (item.datasetIndex === 0) return sectorName + ' : ' + fmt(a, a.median);
                    return symName + ' : ' + fmt(a, a.value) +
                      '  (méd. ' + fmt(a, a.median) + ')';
                  },
                },
              },
            },
            elements: { line: { tension: 0 } },
          },
        });
      },
    }, opts));
  };

  /* Mini-jauge radiale de SCORE (0-100) pour un cluster « profil ». Arc coloré par
     niveau (vert haut · ambre moyen · corail bas ; inversé pour le risque), nombre
     au centre + libellé dessous. Autonome (SVG), aucune dépendance. */
  C.scoreGaugeSVG = function (pct, opts) {
    opts = opts || {};
    var size = opts.size || 84, sw = opts.stroke || 7;
    var r = (size - sw) / 2 - 1, cx = size / 2, cy = size / 2;
    var start = 135, sweep = 270;
    var v = (pct == null || isNaN(pct)) ? null : Math.max(0, Math.min(100, +pct));
    var circ = 2 * Math.PI * r, arcLen = circ * (sweep / 360);
    var dash = v == null ? 0 : arcLen * (v / 100);
    // niveau → couleur (invert : haut = risque = corail)
    var lvl = v == null ? 0 : (opts.invert ? 100 - v : v);
    var col = lvl >= 67 ? 'var(--vx-positive)' : lvl >= 40 ? 'var(--vx-warning)' : 'var(--vx-negative)';
    var glow = lvl >= 67 ? 'rgba(54,200,137,.5)' : lvl >= 40 ? 'rgba(221,162,59,.45)' : 'rgba(237,101,92,.45)';
    var rot = 'rotate(' + start + ' ' + cx + ' ' + cy + ')';
    return '<div class="vx-scoregauge" style="--_glow:' + glow + '">' +
      '<svg width="' + size + '" height="' + size + '" viewBox="0 0 ' + size + ' ' + size + '" role="img" aria-label="' + (opts.label || 'score') + ' ' + (v == null ? 'n/d' : Math.round(v)) + '">' +
      '<circle class="vx-cg-track" cx="' + cx + '" cy="' + cy + '" r="' + r + '" stroke-width="' + sw + '" stroke-dasharray="' + arcLen + ' ' + circ + '" transform="' + rot + '"/>' +
      '<circle class="vx-cg-arc" cx="' + cx + '" cy="' + cy + '" r="' + r + '" stroke="' + col + '" stroke-width="' + sw + '" stroke-dasharray="' + dash + ' ' + circ + '" transform="' + rot + '"/>' +
      '<text class="vx-sg-val" x="' + cx + '" y="' + (cy + 5) + '" text-anchor="middle" fill="' + (v == null ? 'var(--vx-text-faint)' : col) + '">' + (v == null ? '—' : Math.round(v)) + '</text>' +
      '</svg><div class="vx-sg-lbl">' + (opts.label || '') + '</div></div>';
  };

  /* Jauge de confiance circulaire (Signals). Renvoie une chaîne SVG autonome :
     arc coloré (émeraude si hausse, corail si baisse, acier si neutre),
     libellé direction + %. `dir` ∈ {'up','down','flat'}. `pct` ∈ [0..100]. */
  C.confidenceGaugeSVG = function (pct, dir, opts) {
    opts = opts || {};
    const size = opts.size || 92, sw = opts.stroke || 8;
    const r = (size - sw) / 2 - 2, cx = size / 2, cy = size / 2;
    const start = 135, sweep = 270;                 // arc ouvert en bas
    const p = Math.max(0, Math.min(100, +pct || 0));
    const circ = 2 * Math.PI * r;
    const arcLen = circ * (sweep / 360);
    const dash = arcLen * (p / 100);
    const col = dir === 'up' ? 'var(--vx-positive)' : dir === 'down' ? 'var(--vx-negative)' : 'var(--vx-steel-3)';
    const glow = dir === 'up' ? 'rgba(54,200,137,.55)' : dir === 'down' ? 'rgba(237,101,92,.5)' : 'rgba(143,138,131,.4)';
    const dirTxt = opts.dirLabel || (dir === 'up' ? 'Rise' : dir === 'down' ? 'Fall' : 'Flat');
    const rot = `rotate(${start} ${cx} ${cy})`;
    return '<div class="vx-confgauge" style="--_glow:' + glow + '">' +
      '<svg width="' + size + '" height="' + size + '" viewBox="0 0 ' + size + ' ' + size + '" role="img" aria-label="Confiance ' + p + '%">' +
      '<circle class="vx-cg-track" cx="' + cx + '" cy="' + cy + '" r="' + r + '" stroke-width="' + sw + '"' +
        ' stroke-dasharray="' + arcLen + ' ' + circ + '" transform="' + rot + '"/>' +
      '<circle class="vx-cg-arc" cx="' + cx + '" cy="' + cy + '" r="' + r + '" stroke="' + col + '" stroke-width="' + sw + '"' +
        ' stroke-dasharray="' + dash + ' ' + circ + '" transform="' + rot + '"/>' +
      '<text class="vx-cg-dir" x="' + cx + '" y="' + (cy - 4) + '" text-anchor="middle" fill="' + col + '">' + dirTxt + '</text>' +
      '<text class="vx-cg-pct" x="' + cx + '" y="' + (cy + 13) + '" text-anchor="middle">' + Math.round(p) + '%</text>' +
      '</svg></div>';
  };
})();
