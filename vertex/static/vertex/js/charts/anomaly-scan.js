/* anomaly-scan.js — SCANNER D'ANOMALIES : courbe de prix réelle + halos pulsants
   sur chaque anomalie détectée (spike |z|≥2, régime de volatilité, séquence,
   extrême). SVG inline, points réels uniquement — aucune interpolation cachée.
   Vide honnête si la série est trop courte. Lecture seule, aucun ordre. */
(function () {
  'use strict';
  const C = window.VXCharts = window.VXCharts || {};

  C.anomalyScan = function (hostId, d) {
    const host = typeof hostId === 'string' ? document.getElementById(hostId) : hostId;
    if (!host) return;
    const esc = (s) => String(s == null ? '' : s).replace(/[<>&"']/g, (c) => (
      { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;' }[c]));
    if (!d || d.empty || !(d.closes || []).length) {
      host.innerHTML = '<div class="vx-empty">' + esc(((d && d.reason) || 'série indisponible') + '.') + '</div>';
      return;
    }
    const cl = d.closes, n = cl.length;
    const W = 640, H = 220, padL = 8, padR = 54, padT = 16, padB = 26;
    const mn = Math.min.apply(null, cl), mx = Math.max.apply(null, cl), rg = (mx - mn) || 1;
    const px = (i) => padL + i / (n - 1) * (W - padL - padR);
    const py = (v) => padT + (1 - (v - mn) / rg) * (H - padT - padB);
    const up = cl[n - 1] >= cl[0];
    const line = up ? 'var(--vx-positive,#38b879)' : 'var(--vx-negative,#dc5f52)';
    const neg = 'var(--vx-negative,#dc5f52)', warn = 'var(--vx-warning,#e0a458)';
    const dim = 'var(--vx-text-dim,#8a837a)';
    const svg = ['<svg viewBox="0 0 ' + W + ' ' + H + '" width="100%" role="img" aria-label="Scanner d\'anomalies">'];

    // Bande de régime de volatilité (5 derniers points) si détecté.
    const volEv = (d.events || []).find((e) => e.kind === 'vol_shift');
    if (volEv && n > 6) {
      const x0 = px(n - 6);
      svg.push('<rect x="' + x0 + '" y="' + padT + '" width="' + (px(n - 1) - x0)
        + '" height="' + (H - padT - padB) + '" fill="' + warn + '" opacity=".08"/>');
      svg.push('<text x="' + (x0 + 3) + '" y="' + (padT + 10) + '" font-size="8.5" fill="' + warn
        + '">vol ×' + volEv.ratio + '</text>');
    }

    // Aire + ligne de prix (points réels).
    const pts = cl.map((v, i) => px(i).toFixed(1) + ',' + py(v).toFixed(1)).join(' ');
    svg.push('<defs><linearGradient id="vxanog" x1="0" y1="0" x2="0" y2="1">'
      + '<stop offset="0" stop-color="' + line + '" stop-opacity=".18"/>'
      + '<stop offset="1" stop-color="' + line + '" stop-opacity="0"/></linearGradient></defs>');
    svg.push('<polygon points="' + pts + ' ' + px(n - 1).toFixed(1) + ',' + (H - padB)
      + ' ' + padL + ',' + (H - padB) + '" fill="url(#vxanog)"/>');
    svg.push('<polyline points="' + pts + '" fill="none" stroke="' + line
      + '" stroke-width="1.8" vector-effect="non-scaling-stroke"/>');

    // Halos PULSANTS sur les spikes (anomalies statistiques) — SMIL, aucun JS.
    (d.events || []).filter((e) => e.kind === 'spike').forEach((e) => {
      const x = px(e.i), y = py(cl[e.i]);
      const col = (e.ret_pct >= 0) ? line : neg;
      svg.push('<circle cx="' + x + '" cy="' + y + '" r="3.2" fill="' + col + '">'
        + '<title>' + esc(e.label) + '</title></circle>');
      svg.push('<circle cx="' + x + '" cy="' + y + '" r="4" fill="none" stroke="' + col + '" stroke-width="1.4" opacity=".9">'
        + '<animate attributeName="r" values="4;11" dur="1.6s" repeatCount="indefinite"/>'
        + '<animate attributeName="opacity" values=".9;0" dur="1.6s" repeatCount="indefinite"/></circle>');
      svg.push('<text x="' + x + '" y="' + (y - 9) + '" font-size="8.5" text-anchor="middle" fill="' + col
        + '" font-weight="700">' + (e.ret_pct > 0 ? '+' : '') + e.ret_pct + '%</text>');
    });

    // Marqueur d'extrême (dernier point aux bornes de la fenêtre).
    const ext = (d.events || []).find((e) => e.kind === 'extreme');
    if (ext) {
      const y = py(cl[n - 1]);
      svg.push('<text x="' + (W - padR + 4) + '" y="' + (y + 3) + '" font-size="8.5" fill="'
        + (ext.side === 'high' ? line : neg) + '" font-weight="700">'
        + (ext.side === 'high' ? '▲ plus haut' : '▼ plus bas') + '</text>');
    }
    svg.push('<text x="' + padL + '" y="' + (H - 8) + '" font-size="8.5" fill="' + dim + '">'
      + n + ' clôtures réelles · z-scores exacts</text>');
    svg.push('</svg>');

    const badges = (d.events || []).map((e) => {
      const tone = e.kind === 'spike' ? (e.ret_pct >= 0 ? 'pos' : 'neg')
        : e.kind === 'vol_shift' ? 'neg' : e.kind === 'streak' ? 'neutral'
        : (e.side === 'high' ? 'pos' : 'neg');
      return '<span class="vx-badge" data-tone="' + tone + '" style="margin:.15rem .25rem .15rem 0">' + esc(e.label) + '</span>';
    }).join('');

    host.innerHTML = svg.join('')
      + (badges ? '<div class="vx-mt1">' + badges + '</div>' : '')
      + '<div class="vx-muted" style="margin-top:.35rem">' + esc(d.narrative || '') + '</div>';
  };
})();
