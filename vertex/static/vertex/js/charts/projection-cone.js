/* Vertex Charts — projection-cone.js (TOURNÉE TV, lot 190)
   CÔNE DE PROJECTION du plan de trade — la signature « prix cible »
   TradingView, nourrie par les niveaux RÉELS du moteur (entrée/stop/TP1-3),
   JAMAIS un consensus inventé : sans plan complet → état vide honnête.

   VXCharts.projectionCone(host, {
     spot,                // prix actuel RÉEL (requis)
     stop, tp1, tp2, tp3, // niveaux du plan moteur (stop + tp1 requis)
     history,             // clôtures réelles récentes (optionnel — trait « réel »)
     horizonLabel,        // ex. « horizon du plan » (texte, jamais une date inventée)
     note                 // pied honnête optionnel
   })
   Zone future HACHURÉE (tvHatch = estimation), chips de bord (tvEdgeChip) :
   TP3/TP2/TP1 (+x %), Actuel, Stop (−x %). Tokens C.colors uniquement. */
(function () {
  'use strict';
  const C = window.VXCharts = window.VXCharts || {};

  C.projectionCone = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    const num = (x) => (x === null || x === undefined || isNaN(x)) ? null : +x;
    const spot = num(o.spot), stop = num(o.stop), tp1 = num(o.tp1);
    const tp2 = num(o.tp2), tp3 = num(o.tp3);
    if (spot === null || stop === null || tp1 === null) {
      el.innerHTML = (window.VX && VX.states && VX.states.empty)
        ? VX.states.empty('Pas de plan moteur complet pour ce titre — le cône de projection n’invente jamais de niveaux.')
        : '';
      return el;
    }
    const top = Math.max.apply(null, [tp3, tp2, tp1, spot].filter(v => v !== null));
    const hist = Array.isArray(o.history) ? o.history.filter(v => v !== null && !isNaN(v)).slice(-60) : [];
    const lo = Math.min.apply(null, [stop, spot].concat(hist));
    const hi = Math.max.apply(null, [top].concat(hist));
    const pad = (hi - lo) * 0.08 || 1;
    const yMin = lo - pad, yMax = hi + pad;

    const W = 560, H = 240, mL = 8, mR = 118, mT = 18, mB = 14;
    const x0 = mL + (W - mL - mR) * 0.34;          // frontière réel → projection
    const x1 = W - mR;
    const Y = (v) => mT + (H - mT - mB) * (1 - (v - yMin) / (yMax - yMin));
    const pct = (v) => {
      const p = (v / spot - 1) * 100;
      return (p >= 0 ? '+' : '−') + Math.abs(p).toFixed(1).replace('.', ',') + ' %';
    };
    const fmt = (v) => (window.VX && VX.fmt && VX.fmt.price) ? VX.fmt.price(v)
      : (Math.abs(v) >= 100 ? v.toFixed(0) : v.toFixed(2));

    const gid = 'vxCone-' + ((el.id || 'c').replace(/[^\w-]/g, ''));
    const defs = '<defs>' + C.tvHatch(gid + '-hp', C.colors.positive)
      + C.tvHatch(gid + '-hn', C.colors.negative) + '</defs>';

    /* trait RÉEL : clôtures récentes jusqu'au spot */
    let real = '';
    if (hist.length > 1) {
      const pts = hist.map((v, i) => (mL + (x0 - mL) * i / (hist.length - 1)).toFixed(1) + ',' + Y(v).toFixed(1)).join(' ');
      real = '<polyline points="' + pts + '" fill="none" stroke="var(--vx-text-primary,#F8F5F3)" stroke-width="2" stroke-opacity=".9"/>';
    }
    const ySpot = Y(spot);
    const dot = '<circle cx="' + x0.toFixed(1) + '" cy="' + ySpot.toFixed(1) + '" r="4" fill="var(--vx-text-primary,#F8F5F3)"/>'
      + '<circle cx="' + x0.toFixed(1) + '" cy="' + ySpot.toFixed(1) + '" r="8" fill="var(--vx-text-primary,#F8F5F3)" fill-opacity=".18"/>';

    /* faisceau HAUSSIER (TP1→TP3) hachuré + faisceau de RISQUE (→ stop) */
    const upTop = tp3 !== null ? tp3 : tp1;
    const wedgeUp = '<polygon points="' + x0.toFixed(1) + ',' + ySpot.toFixed(1)
      + ' ' + x1 + ',' + Y(upTop).toFixed(1) + ' ' + x1 + ',' + Y(tp1).toFixed(1) + '"'
      + ' fill="' + C.colors.positive + '" fill-opacity=".14"/>'
      + '<polygon points="' + x0.toFixed(1) + ',' + ySpot.toFixed(1)
      + ' ' + x1 + ',' + Y(upTop).toFixed(1) + ' ' + x1 + ',' + Y(tp1).toFixed(1) + '"'
      + ' fill="url(#' + gid + '-hp)"/>'
      + '<line x1="' + x0.toFixed(1) + '" y1="' + ySpot.toFixed(1) + '" x2="' + x1 + '" y2="' + Y(upTop).toFixed(1) + '" stroke="' + C.colors.positive + '" stroke-width="1.6" stroke-opacity=".85"/>'
      + '<line x1="' + x0.toFixed(1) + '" y1="' + ySpot.toFixed(1) + '" x2="' + x1 + '" y2="' + Y(tp1).toFixed(1) + '" stroke="' + C.colors.positive + '" stroke-width="1.2" stroke-opacity=".55" stroke-dasharray="2 3"/>';
    const wedgeDn = '<polygon points="' + x0.toFixed(1) + ',' + ySpot.toFixed(1)
      + ' ' + x1 + ',' + ySpot.toFixed(1) + ' ' + x1 + ',' + Y(stop).toFixed(1) + '"'
      + ' fill="' + C.colors.negative + '" fill-opacity=".12"/>'
      + '<polygon points="' + x0.toFixed(1) + ',' + ySpot.toFixed(1)
      + ' ' + x1 + ',' + ySpot.toFixed(1) + ' ' + x1 + ',' + Y(stop).toFixed(1) + '"'
      + ' fill="url(#' + gid + '-hn)"/>'
      + '<line x1="' + x0.toFixed(1) + '" y1="' + ySpot.toFixed(1) + '" x2="' + x1 + '" y2="' + Y(stop).toFixed(1) + '" stroke="' + C.colors.negative + '" stroke-width="1.6" stroke-opacity=".8"/>';
    const median = tp2 !== null
      ? '<line x1="' + x0.toFixed(1) + '" y1="' + ySpot.toFixed(1) + '" x2="' + x1 + '" y2="' + Y(tp2).toFixed(1) + '" stroke="' + C.colors.brand + '" stroke-width="1.6" stroke-dasharray="5 4" stroke-opacity=".9"/>'
      : '';

    /* frontière aujourd'hui + libellé de zone */
    const nowLine = '<line x1="' + x0.toFixed(1) + '" y1="' + mT + '" x2="' + x0.toFixed(1) + '" y2="' + (H - mB) + '" stroke="var(--vx-text-muted,#8A8284)" stroke-width="1" stroke-dasharray="2 4" stroke-opacity=".6"/>'
      + '<text x="' + (x0 + 6).toFixed(1) + '" y="' + (mT + 8) + '" fill="var(--vx-text-muted,#8A8284)" font-size="8.5" letter-spacing=".6">PROJECTION — ' + (o.horizonLabel || 'plan moteur') + '</text>';

    /* chips de bord (grammaire tvEdgeChip, lot 189) */
    let chips = '';
    const chip = (v, label, color) => {
      if (v === null) return;
      chips += C.tvEdgeChip(x1 + 4, Y(v), label + ' ' + fmt(v), color, { align: 'left', fontSize: 9 });
    };
    chip(tp3, 'TP3 ' + pct(tp3), C.colors.positive);
    chip(tp2, 'TP2', C.colors.positive);
    chip(tp1, 'TP1', C.colors.positive);
    chip(spot, 'Actuel', C.colors.neutral);
    chip(stop, 'Stop ' + pct(stop), C.colors.negative);

    const aria = 'Cône de projection du plan : actuel ' + fmt(spot)
      + ', stop ' + fmt(stop) + ' (' + pct(stop) + ')'
      + (tp3 !== null ? ', TP3 ' + fmt(tp3) + ' (' + pct(tp3) + ')' : '');
    el.innerHTML = '<div class="vx-cone" role="img" aria-label="' + aria.replace(/"/g, '&quot;') + '">'
      + '<svg viewBox="0 0 ' + W + ' ' + H + '" width="100%" style="display:block">'
      + defs + wedgeUp + wedgeDn + median + nowLine + real + dot + chips + '</svg>'
      + '<div class="vx-meta" style="margin-top:2px">' + (o.note || 'Niveaux du plan moteur — une carte de risque, pas une prévision de marché.') + '</div></div>';
    return el;
  };
})();
