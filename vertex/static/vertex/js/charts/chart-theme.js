/* Vertex Charts V3 — chart-theme.js
   Thème graphique unique, aligné sur les design tokens (tokens.css).
   UNE COULEUR = UNE SIGNIFICATION :
   brand/orange = série de référence & niveaux d'action ·
   vert = positif · rouge corail = négatif · ambre = attention ·
   bleu = information/série 1 · cyan = données/live · violet = options & IA ·
   gris = benchmark/neutre. Chargé AVANT chart-core.js. */
(function () {
  'use strict';
  window.VXChartTheme = {
    colors: {
      brand: '#f68a3c',
      amber: '#f5b942',
      copper: '#d9773f',
      blue: '#4ca6ff',      /* information */
      info: '#4ca6ff',
      cyan: '#2cc9d8',
      violet: '#8b6df6',
      positive: '#2acb7f',
      negative: '#f05d55',
      warning: '#f3a93b',
      neutral: '#738096',   /* benchmark / référence */
      text: '#b3bdca',
      muted: '#7f8b9d',
      grid: 'rgba(255,255,255,.055)',
      /* Séries multi-courbes : référence orange puis hues distinctes */
      series: ['#f68a3c', '#4ca6ff', '#2cc9d8', '#8b6df6', '#f5b942', '#738096'],
    },
    tooltip: {
      backgroundColor: '#151c27',
      borderColor: 'rgba(255,255,255,.14)',
      titleColor: '#f7f8fa',
      bodyColor: '#b3bdca',
    },
  };
})();
