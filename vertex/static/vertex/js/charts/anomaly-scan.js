/* anomaly-scan.js — SCANNER D'ANOMALIES : courbe du scan + repères statiques
   sur chaque anomalie détectée (spike |z|≥2, régime de volatilité, séquence,
   extrême). SVG inline, points du scan uniquement — aucune interpolation cachée.
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
    /* La direction globale n'est pas un verdict : la série principale reste
       cuivre, seuls les événements portent la sémantique gain/perte. */
    const line = 'var(--vx-brand,#9B7BFF)';
    const pos = 'var(--vx-positive,#2BBE90)';
    const neg = 'var(--vx-negative,#E9555F)', warn = 'var(--vx-warning,#D9BE3C)';
    const dim = 'var(--vx-text-muted,#989092)';
    const aria = 'Scanner d\'anomalies : ' + n + ' clôtures du scan, minimum '
      + mn.toFixed(2) + ', maximum ' + mx.toFixed(2) + ', dernière ' + Number(cl[n - 1]).toFixed(2);
    const svg = ['<svg viewBox="0 0 ' + W + ' ' + H + '" width="100%" role="img" aria-label="' + aria + '">'];

    // Bande de régime de volatilité (5 derniers points) si détecté.
    const volEv = (d.events || []).find((e) => e.kind === 'vol_shift');
    if (volEv && n > 6) {
      const x0 = px(n - 6);
      svg.push('<rect x="' + x0 + '" y="' + padT + '" width="' + (px(n - 1) - x0)
        + '" height="' + (H - padT - padB) + '" fill="' + warn + '" opacity=".08"/>');
      svg.push('<text x="' + (x0 + 3) + '" y="' + (padT + 10) + '" font-size="8.5" fill="' + warn
        + '">vol ×' + volEv.ratio + '</text>');
    }

    // Aire + ligne de prix (points du scan, sans interpolation).
    const pts = cl.map((v, i) => px(i).toFixed(1) + ',' + py(v).toFixed(1)).join(' ');
    svg.push('<defs><linearGradient id="vxanog" x1="0" y1="0" x2="0" y2="1">'
      + '<stop offset="0" stop-color="' + line + '" stop-opacity=".18"/>'
      + '<stop offset="1" stop-color="' + line + '" stop-opacity="0"/></linearGradient></defs>');
    svg.push('<polygon points="' + pts + ' ' + px(n - 1).toFixed(1) + ',' + (H - padB)
      + ' ' + padL + ',' + (H - padB) + '" fill="url(#vxanog)"/>');
    svg.push('<polyline points="' + pts + '" fill="none" stroke="' + line
      + '" stroke-width="1.8" vector-effect="non-scaling-stroke"/>');

    // Repères statiques sur les spikes : lisibles sans mouvement permanent.
    (d.events || []).filter((e) => e.kind === 'spike').forEach((e) => {
      const x = px(e.i), y = py(cl[e.i]);
      const col = (e.ret_pct >= 0) ? pos : neg;
      svg.push('<circle cx="' + x + '" cy="' + y + '" r="3.2" fill="' + col + '">'
        + '<title>' + esc(e.label) + '</title></circle>');
      svg.push('<circle cx="' + x + '" cy="' + y + '" r="7" fill="none" stroke="' + col
        + '" stroke-width="1.2" opacity=".42"/>');
      svg.push('<text x="' + x + '" y="' + (y - 9) + '" font-size="8.5" text-anchor="middle" fill="' + col
        + '" font-weight="700">' + (e.ret_pct > 0 ? '+' : '') + e.ret_pct + '%</text>');
    });

    // Marqueur d'extrême (dernier point aux bornes de la fenêtre).
    const ext = (d.events || []).find((e) => e.kind === 'extreme');
    if (ext) {
      const y = py(cl[n - 1]);
      svg.push('<text x="' + (W - padR + 4) + '" y="' + (y + 3) + '" font-size="8.5" fill="'
        + (ext.side === 'high' ? pos : neg) + '" font-weight="700">'
        + (ext.side === 'high' ? '▲ plus haut' : '▼ plus bas') + '</text>');
    }
    svg.push('<text x="' + padL + '" y="' + (H - 8) + '" font-size="8.5" fill="' + dim + '">'
      + n + ' clôtures du scan · z-scores exacts</text>');
    svg.push('</svg>');

    const badges = (d.events || []).map((e) => {
      const tone = e.kind === 'spike' ? (e.ret_pct >= 0 ? 'pos' : 'neg')
        : e.kind === 'vol_shift' ? 'neg' : e.kind === 'streak' ? 'neutral'
        : (e.side === 'high' ? 'pos' : 'neg');
      return '<span class="vx-badge" data-tone="' + tone + '" style="margin:.15rem .25rem .15rem 0">' + esc(e.label) + '</span>';
    }).join('');

    const demo = !!(window.__vxStatus && window.__vxStatus.demo);
    const fmt = (v) => Number(v).toLocaleString('fr-FR', { maximumFractionDigits: 2 });
    const source = d.series_source ? String(d.series_source).replace(/^scan\./, 'scan · ') : 'scan';
    host.innerHTML = svg.join('')
      + (badges ? '<div class="vx-mt1">' + badges + '</div>' : '')
      + '<div class="vx-flex vx-wrap vx-mt1"><span class="vx-meta">Min ' + fmt(mn)
      + ' · Max ' + fmt(mx) + ' · Dernier ' + fmt(cl[n - 1]) + ' · Source ' + esc(source) + '</span>'
      + (demo ? '<span class="vx-badge vx-warn">DÉMO</span>' : '') + '</div>'
      + '<div class="vx-muted" style="margin-top:.35rem">' + esc(d.narrative || '') + '</div>';
  };
})();
