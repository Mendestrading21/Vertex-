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
    const W = 320, H = 132, x0 = 14, x1 = W - 14, axisY = 60;
    const xOf = (dte) => x0 + (dte / horizon) * (x1 - x0);
    /* LOT 119 — piste développée : zone d'imminence (≤ 5 j) teintée,
       graduations hebdomadaires, départ « aujourd'hui » nommé. Tokens
       uniquement — aucun littéral couleur nouveau. */
    const dangerX = xOf(Math.min(5, horizon));
    /* GRAMMAIRE TV (lot 193) : piste en dégradé CONTINU (imminence rouge →
       moyen terme jaune → horizon éteint) + zone ≤ 5 j HACHURÉE (tvHatch =
       risque événementiel estimé) + chip tvEdgeChip sur le PROCHAIN. */
    const gid = 'vxCr-' + ((el.id || 'r').replace(/[^\w-]/g, ''));
    const frac5 = Math.min(5, horizon) / horizon;
    const defs = `<defs><linearGradient id="${gid}" x1="${x0}" y1="0" x2="${x1}" y2="0" gradientUnits="userSpaceOnUse">
        <stop offset="0" stop-color="var(--vx-negative)"/>
        <stop offset="${Math.min(0.96, Math.max(0.04, frac5)).toFixed(3)}" stop-color="var(--vx-warning)"/>
        <stop offset="1" stop-color="var(--vx-border-soft,#30292B)"/></linearGradient>
      ${C.tvHatch ? C.tvHatch(gid + '-h', 'var(--vx-negative)') : ''}</defs>`;
    const zone = `<rect x="${x0}" y="${axisY - 14}" width="${(dangerX - x0).toFixed(1)}" height="28" rx="4"
        fill="var(--vx-negative)" fill-opacity=".08"/>
      ${C.tvHatch ? `<rect x="${x0}" y="${axisY - 14}" width="${(dangerX - x0).toFixed(1)}" height="28" rx="4" fill="url(#${gid}-h)"/>` : ''}
      <text x="${x0 + 2}" y="${axisY + 24}" fill="var(--vx-negative)" fill-opacity=".8" font-size="7.5">zone ≤ 5 j</text>`;
    let ticks = '';
    for (let d = 7; d < horizon; d += 7) {
      const tx = xOf(d);
      ticks += `<line x1="${tx.toFixed(1)}" y1="${axisY - 3}" x2="${tx.toFixed(1)}" y2="${axisY + 3}"
        stroke="var(--vx-border-soft,#30292B)" stroke-width="1"/>
        <text x="${tx.toFixed(1)}" y="${axisY + 13}" text-anchor="middle" fill="var(--vx-text-muted,#989092)" font-size="7" opacity=".7">${d}j</text>`;
    }
    /* anti-collision (lot 61) : DEUX rangées d'étiquettes par côté ; chaque
       étiquette prend la première rangée où il reste de la place (calculée
       sur la position BORNÉE au viewBox — la parité d'index posait parfois
       deux étiquettes proches du même côté et le bornage de bord pouvait les
       rapprocher). Déterministe : même calendrier → même dessin. */
    const MIN_GAP = 36;                          // ~largeur d'étiquette (viewBox)
    let lastTop0 = -Infinity, lastBot0 = -Infinity,
        lastTop1 = -Infinity, lastBot1 = -Infinity;
    const IMPACT_R = { high: 5, haute: 5, med: 4, moyenne: 4 };
    const marks = events.map((e, i) => {
      const left = xOf(e.dte);
      const key = String(e.impact || '').toLowerCase();
      const col = IMPACT_COLOR[key] || 'var(--vx-text-muted)';
      const r = IMPACT_R[key] || 3;
      const lx = Math.min(Math.max(left, x0 + 16), x1 - 16);
      let top, outer;
      if (lx - lastTop0 >= MIN_GAP) { top = true; outer = false; lastTop0 = lx; }
      else if (lx - lastBot0 >= MIN_GAP) { top = false; outer = false; lastBot0 = lx; }
      else if (lx - lastTop1 >= MIN_GAP) { top = true; outer = true; lastTop1 = lx; }
      else { top = false; outer = true; lastBot1 = lx; }
      const stemY2 = top ? axisY - 18 : axisY + 18;
      const lblY = top ? (outer ? 10 : 30) : (outer ? axisY + 52 : axisY + 34);
      const label = (e.label || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      /* le PROCHAIN catalyseur porte un anneau — l'œil sait où regarder */
      const focus = i === 0
        ? `<circle cx="${left.toFixed(1)}" cy="${axisY}" r="${r + 3.5}" fill="none" stroke="${col}" stroke-opacity=".45" stroke-width="1.5"/>`
        : '';
      const halo = (r >= 5)
        ? `<circle cx="${left.toFixed(1)}" cy="${axisY}" r="${r + 6}" fill="${col}" fill-opacity=".12"/>`
        : '';
      /* le PROCHAIN porte son J-x en CHIP pleine couleur (tvEdgeChip, lot 189) */
      const jTxt = 'J-' + e.dte;
      const jLabel = (i === 0 && C.tvEdgeChip)
        ? C.tvEdgeChip(lx - (jTxt.length * 9 * 0.62 + 12) / 2, lblY + 7, jTxt, col, { align: 'left', fontSize: 9 })
        : `<text x="${lx.toFixed(1)}" y="${lblY + 11}" text-anchor="middle" fill="var(--vx-text,#F8F5F3)" font-size="9" font-weight="700">${jTxt}</text>`;
      return `<g>
        ${halo}
        <line x1="${left.toFixed(1)}" y1="${axisY}" x2="${left.toFixed(1)}" y2="${stemY2}" stroke="${col}" stroke-opacity=".7" stroke-width="1.5"/>
        ${focus}
        <circle cx="${left.toFixed(1)}" cy="${axisY}" r="${r}" fill="${col}"/>
        <text x="${lx.toFixed(1)}" y="${lblY}" text-anchor="middle" fill="var(--vx-text-muted,#989092)" font-size="8.5">${label.slice(0, 14)}</text>
        ${jLabel}
      </g>`;
    }).join('');

    const nxt = events[0];
    const tone = nxt.dte <= 5 ? 'risk' : 'go';
    const verdict = nxt.dte <= 5
      ? `${nxt.label} dans ${nxt.dte} j — risque événementiel imminent`
      : `${nxt.label} dans ${nxt.dte} j — fenêtre dégagée`;
    const svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="${String(verdict).replace(/"/g, '&quot;').replace(/</g, '&lt;')}" style="max-width:${W}px;display:block;margin:2px auto">
      ${defs}${zone}
      <line x1="${x0}" y1="${axisY}" x2="${x1}" y2="${axisY}" stroke="url(#${gid})" stroke-width="2.5" stroke-linecap="round" stroke-opacity=".85"/>
      ${ticks}
      <line x1="${x0}" y1="${axisY - 6}" x2="${x0}" y2="${axisY + 6}" stroke="rgba(255,255,255,.5)" stroke-width="2"/>
      <text x="${x0}" y="${H - 4}" fill="var(--vx-text-muted,#989092)" font-size="7.5">aujourd’hui</text>
      <text x="${x1}" y="${H - 4}" text-anchor="end" fill="var(--vx-text-muted,#989092)" font-size="7.5">horizon J-${horizon}</text>
      ${marks}</svg>`;

    el.innerHTML = head + svg +
      `<div class="vx-cr-verdict" data-tone="${tone}">${String(verdict).replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>` + foot;
    return el;
  };
})();
