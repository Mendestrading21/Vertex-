/* regime-aura.js — REGIME AURA (widget officiel W01, réalisé en live).
   Le régime de marché comme une atmosphère : halo coloré par l'état, arc de
   confiance (orange Ember), grammaire boursière (SPX vs MM200 · breadth · VIX)
   et conclusion « risque neuf autorisé / bloqué » + invalidation.
   L'UI ne calcule rien : elle trace ce que renvoient les moteurs (régime,
   confiance, new_risk_allowed, invalidation). Donnée absente → état honnête. */
(function () {
  'use strict';
  const VX = window.VX;
  const C = window.VXCharts = window.VXCharts || {};

  /* Tonalité dérivée UNIQUEMENT des données moteur (aucune couleur décorative). */
  function toneOf(o) {
    if (o.newRisk === true) return 'go';
    if (o.newRisk === false) return 'risk';
    return 'wait';
  }
  const TONE_COLOR = { go: 'var(--vx-positive)', risk: 'var(--vx-negative)', wait: 'var(--vx-warning)' };

  function arc(cx, cy, r, d0, d1) {
    const a0 = d0 * Math.PI / 180, a1 = d1 * Math.PI / 180;
    const x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0);
    const x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
    const large = Math.abs(d1 - d0) > 180 ? 1 : 0;
    return `M${x0.toFixed(1)},${y0.toFixed(1)} A${r},${r} 0 ${large} 1 ${x1.toFixed(1)},${y1.toFixed(1)}`;
  }

  C.regimeAura = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};

    /* État honnête : régime indéterminé → pas d'objet, message assumé. */
    if (o.state === 'empty' || !o.regime) {
      el.innerHTML = VX.states.empty(o.stateMessage || 'Régime indéterminé — Vertex ne tranche pas.');
      return null;
    }
    if (o.state === 'error') {
      el.innerHTML = VX.states.error(o.stateMessage || 'Régime indisponible.');
      return null;
    }

    const tone = toneOf(o);
    const col = TONE_COLOR[tone];
    const conf = (o.confidence == null || isNaN(o.confidence)) ? null : Math.max(0, Math.min(100, o.confidence));
    const uid = 'ra' + Math.round((o.confidence || 0) + (o.regime || '').length * 7);
    const W = 320, H = 150, cx = W / 2, cy = 96;
    /* GRAMMAIRE TV (lot 192) : arc de confiance ENTIER en dégradé continu de la
       tonalité (fondu gauche→droite), POINTEUR blanc court posé sur l'arc à la
       position de la confiance — même langage que C.gauge (lot 189). */
    const track = arc(cx, cy, 62, 152, 388);
    const aConf = (152 + (conf == null ? 0 : conf / 100 * 236)) * Math.PI / 180;
    const raPt = (rr) => [cx + rr * Math.cos(aConf), cy + rr * Math.sin(aConf)];
    let pointer = '';
    if (conf != null) {
      const [px0, py0] = raPt(50), [px1, py1] = raPt(60), [phx, phy] = raPt(62);
      pointer = `<circle cx="${phx.toFixed(1)}" cy="${phy.toFixed(1)}" r="7" fill="${col}" fill-opacity=".3"/>`
        + `<line x1="${px0.toFixed(1)}" y1="${py0.toFixed(1)}" x2="${px1.toFixed(1)}" y2="${py1.toFixed(1)}" stroke="var(--vx-text,#F8F5F3)" stroke-width="3" stroke-linecap="round"/>`
        + `<circle cx="${px0.toFixed(1)}" cy="${py0.toFixed(1)}" r="2.2" fill="var(--vx-text,#F8F5F3)"/>`;
    }
    const g = o.grammar || {};
    const chip = (label, value) =>
      `<span class="vx-ra-chip"><span class="k">${label}</span><span class="v">${value}</span></span>`;
    const chips = [];
    if (g.roro) chips.push(chip('Marché', g.roro));
    if (g.breadth != null) chips.push(chip('Breadth &gt;MM200', VX.fmt.nd(g.breadth) + ' %'));
    if (g.vix != null) chips.push(chip('VIX', VX.fmt.nd(g.vix)));

    const confTxt = conf == null ? 'confiance n/d' : Math.round(conf) + ' % confiance';
    const verdict = o.newRisk === true ? 'Risque neuf autorisé'
      : o.newRisk === false ? 'Risque neuf BLOQUÉ' : 'Régime à confirmer';
    const inval = o.invalidation ? (' · ' + o.invalidation) : '';
    const aria = `Régime ${o.regime}, ${confTxt}. ${verdict}${inval}`;

    el.innerHTML =
      `<div class="vx-regime-aura" role="img" aria-label="${String(aria).replace(/"/g, '&quot;')}">
        <svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px;display:block;margin:0 auto">
          <defs>
            <radialGradient id="${uid}h" cx="50%" cy="34%" r="66%">
              <stop offset="0" stop-color="${col}" stop-opacity=".42"/>
              <stop offset="46%" stop-color="${col}" stop-opacity=".10"/>
              <stop offset="100%" stop-color="${col}" stop-opacity="0"/></radialGradient>
            <linearGradient id="${uid}z" x1="0" x2="1">
              <stop offset="0" stop-color="${col}" stop-opacity="0"/>
              <stop offset=".5" stop-color="${col}" stop-opacity=".5"/>
              <stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient>
            <linearGradient id="${uid}a" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stop-color="${col}" stop-opacity=".18"/>
              <stop offset=".55" stop-color="${col}" stop-opacity=".55"/>
              <stop offset="1" stop-color="${col}" stop-opacity=".95"/></linearGradient>
            <filter id="${uid}b"><feGaussianBlur stdDeviation="6"/></filter></defs>
          <rect x="0" y="0" width="${W}" height="${H}" fill="url(#${uid}h)"/>
          <ellipse cx="${cx}" cy="${cy - 52}" rx="128" ry="26" fill="${col}" opacity=".16" filter="url(#${uid}b)"/>
          <ellipse cx="${cx}" cy="${cy - 36}" rx="92" ry="14" fill="${col}" opacity=".20" filter="url(#${uid}b)"/>
          <line x1="30" y1="${cy}" x2="${W - 30}" y2="${cy}" stroke="url(#${uid}z)" stroke-width="1.3"/>
          <path d="${track}" fill="none" stroke="url(#${uid}a)" stroke-opacity="${conf == null ? '.3' : '.95'}" stroke-width="5" stroke-linecap="round"/>
          ${pointer}
          <text x="${cx}" y="${cy - 10}" text-anchor="middle" fill="var(--vx-text,#F8F5F3)" font-size="17" font-weight="800">${o.regime}</text>
          <text x="${cx}" y="${cy + 8}" text-anchor="middle" fill="${conf == null ? 'var(--vx-text-muted,#8A8284)' : col}" font-size="10.5" font-weight="${conf == null ? '400' : '800'}">${confTxt}</text>
        </svg>
        ${chips.length ? `<div class="vx-ra-grammar">${chips.join('')}</div>` : ''}
        <div class="vx-ra-verdict" data-tone="${tone}">▸ ${verdict}${inval}</div>
      </div>` +
      `<div class="vx-chart-foot">${VX.updateIndicator(o.timestamp, o.source || 'Moteur de régimes', o.mode || 'delayed')}</div>`;
    return el;
  };
})();
