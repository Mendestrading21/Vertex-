/* Vertex Charts — consensus-bars.js (TOURNÉE TV, lot 191)
   BARRES DE CONSENSUS — le « Note des analystes » TradingView, nourri par
   des comptes RÉELS (verdicts du comité, jamais un sondage inventé).

   VXCharts.consensusBars(host, {
     items: [{label, count, color}],  // comptes réels, ordre libre
     title,                            // ex. « Répartition des verdicts »
     note                              // pied honnête optionnel
   })
   Style TV : libellé à gauche, barre pleine à bout arrondi (longueur ∝ max),
   compte à droite ; la barre DOMINANTE en pleine intensité, les autres
   adoucies ; total rappelé. items vide → état vide honnête. */
(function () {
  'use strict';
  const C = window.VXCharts = window.VXCharts || {};

  C.consensusBars = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};
    const items = (o.items || []).filter(it => it && typeof it.count === 'number' && it.count >= 0);
    const total = items.reduce((s, it) => s + it.count, 0);
    if (!items.length || !total) {
      el.innerHTML = (window.VX && VX.states && VX.states.empty)
        ? VX.states.empty('Aucun verdict à répartir — le consensus n’est jamais inventé.')
        : '';
      return el;
    }
    const max = Math.max.apply(null, items.map(it => it.count));
    const sorted = items.slice().sort((a, b) => b.count - a.count);
    const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
    const rows = sorted.map(it => {
      const w = Math.max(3, Math.round(it.count / max * 100));
      const dominant = it.count === max;
      const col = it.color || C.colors.neutral;
      return '<div class="vx-consensus-row" style="display:flex;align-items:center;gap:10px;margin:6px 0">'
        + '<span style="width:132px;flex:0 0 auto;font-size:12px;font-weight:' + (dominant ? '800' : '500')
        + ';color:' + (dominant ? col : 'var(--vx-text-secondary,#BABABA)') + '">' + esc(it.label) + '</span>'
        + '<span style="flex:1;height:13px;background:var(--vx-graphite-850,#121214);border-radius:7px;overflow:hidden">'
        + '<span style="display:block;height:100%;width:' + w + '%;border-radius:7px;background:' + col
        + ';opacity:' + (dominant ? '1' : '.45') + '"></span></span>'
        + '<span class="vx-mono" style="width:36px;flex:0 0 auto;text-align:right;font-size:12.5px;font-weight:'
        + (dominant ? '800' : '600') + ';color:' + (dominant ? col : 'var(--vx-text-muted,#989092)') + '">' + it.count + '</span></div>';
    }).join('');
    const aria = (o.title || 'Consensus') + ' : ' + sorted.map(it => it.label + ' ' + it.count).join(', ')
      + ' — total ' + total;
    el.innerHTML = '<div class="vx-consensus" role="img" aria-label="' + esc(aria) + '">'
      + (o.title ? '<div class="vx-kpi-label vx-mb2">' + esc(o.title) + '</div>' : '')
      + rows
      + '<div class="vx-meta" style="margin-top:6px">' + (o.note || (total + ' dossiers passés en revue — comptes réels.')) + '</div></div>';
    return el;
  };
})();
