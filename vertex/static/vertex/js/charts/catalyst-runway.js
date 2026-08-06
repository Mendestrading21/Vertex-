/* catalyst-runway.js — CATALYST RUNWAY (widget officiel W-CR, réalisé en live).
   Les prochains catalyseurs comme une piste de décollage : chaque événement est
   posé selon son DTE (jours avant l'événement), coloré par impact, le prochain
   étant priorisé. L'UI trace ce que renvoie le calendrier moteur ; aucune
   donnée inventée — calendrier vide → état honnête. */
(function () {
  'use strict';
  const VX = window.VX;
  const C = window.VXCharts = window.VXCharts || {};

  const IMPACT_COLOR = {
    high: 'var(--vx-negative)', haute: 'var(--vx-negative)',
    med: 'var(--vx-warning)', moyenne: 'var(--vx-warning)',
    low: 'var(--vx-text-muted)', basse: 'var(--vx-text-muted)',
  };

  C.catalystRunway = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    el.classList.add('vx-card');

    const head = `<div class="vx-chart-head"><span class="vx-chart-title">${o.title || 'Catalyseurs imminents'}</span>
      ${o.question ? `<span class="vx-chart-question">${o.question}</span>` : ''}</div>`;
    const foot = `<div class="vx-chart-foot">${VX.updateIndicator(o.timestamp, o.source || 'calendrier moteur', o.mode || 'delayed')}</div>`;

    const events = (o.events || [])
      .filter(e => e && e.dte != null && !isNaN(e.dte))
      .sort((a, b) => a.dte - b.dte)
      .slice(0, 6);

    if (!events.length) {
      el.innerHTML = head + VX.states.empty(o.emptyText || 'Aucun catalyseur imminent identifié.') + foot;
      return null;
    }

    const horizon = Math.max(events[events.length - 1].dte, 1);
    const W = 320, H = 120, x0 = 12, x1 = W - 12, axisY = 52;
    /* anti-collision (lot 61) : DEUX rangées d'étiquettes par côté ; chaque
       étiquette prend la première rangée où il reste de la place (calculée
       sur la position BORNÉE au viewBox — la parité d'index posait parfois
       deux étiquettes proches du même côté et le bornage de bord pouvait les
       rapprocher). Déterministe : même calendrier → même dessin. */
    const MIN_GAP = 36;                          // ~largeur d'étiquette (viewBox)
    let lastTop0 = -Infinity, lastBot0 = -Infinity,
        lastTop1 = -Infinity, lastBot1 = -Infinity;
    const marks = events.map((e) => {
      const left = x0 + (e.dte / horizon) * (x1 - x0);
      const col = IMPACT_COLOR[String(e.impact || '').toLowerCase()] || 'var(--vx-text-muted)';
      const lx = Math.min(Math.max(left, x0 + 16), x1 - 16);
      let top, outer;
      if (lx - lastTop0 >= MIN_GAP) { top = true; outer = false; lastTop0 = lx; }
      else if (lx - lastBot0 >= MIN_GAP) { top = false; outer = false; lastBot0 = lx; }
      else if (lx - lastTop1 >= MIN_GAP) { top = true; outer = true; lastTop1 = lx; }
      else { top = false; outer = true; lastBot1 = lx; }
      const stemY2 = top ? axisY - 16 : axisY + 16;
      const lblY = top ? (outer ? 10 : 30) : (outer ? axisY + 50 : axisY + 30);
      const label = (e.label || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      return `<g>
        <line x1="${left.toFixed(1)}" y1="${axisY}" x2="${left.toFixed(1)}" y2="${stemY2}" stroke="${col}" stroke-opacity=".7" stroke-width="1.5"/>
        <circle cx="${left.toFixed(1)}" cy="${axisY}" r="4" fill="${col}"/>
        <text x="${lx.toFixed(1)}" y="${lblY}" text-anchor="middle" fill="var(--vx-text-muted,#8A8284)" font-size="8.5">${label.slice(0, 12)}</text>
        <text x="${lx.toFixed(1)}" y="${lblY + 11}" text-anchor="middle" fill="var(--vx-text,#F8F5F3)" font-size="9" font-weight="700">J-${e.dte}</text>
      </g>`;
    }).join('');

    const nxt = events[0];
    const tone = nxt.dte <= 5 ? 'risk' : 'go';
    const verdict = nxt.dte <= 5
      ? `${nxt.label} dans ${nxt.dte} j — risque événementiel imminent`
      : `${nxt.label} dans ${nxt.dte} j — fenêtre dégagée`;
    const svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px;display:block;margin:2px auto">
      <line x1="${x0}" y1="${axisY}" x2="${x1}" y2="${axisY}" stroke="var(--vx-border-soft,#30292B)" stroke-width="1"/>
      <line x1="${x0}" y1="${axisY - 5}" x2="${x0}" y2="${axisY + 5}" stroke="rgba(255,255,255,.5)" stroke-width="2"/>
      ${marks}</svg>`;

    el.innerHTML = head + svg +
      `<div class="vx-cr-verdict" data-tone="${tone}">▸ ${String(verdict).replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>` + foot;
    return el;
  };
})();
