/* Vertex Charts — chart-theme-obsidian-copper.js (§35-36)
   Thème graphique unique OBSIDIAN COPPER DEEP, aligné sur tokens.css :
   série principale = orange cuivré · benchmark = gris clair · série
   secondaire = ambre/beige · positif = vert atténué · négatif = rouge
   corail · options = violet sombre limité. AUCUNE série principale bleue,
   aucune palette arc-en-ciel automatique. Chargé AVANT chart-core.js. */
(function () {
  'use strict';
  window.VXChartTheme = {
    colors: {
      brand: '#cf6128',       /* série principale : orange cuivré */
      copper: '#914b2b',
      copperLight: '#b9683d',
      amber: '#ce8a29',       /* série secondaire */
      beige: '#c8ad8d',
      info: '#b9683d',        /* information = cuivre clair */
      blue: '#b9683d',        /* alias legacy — plus jamais bleu */
      cyan: '#c8ad8d',        /* alias legacy → beige */
      violet: '#85609f',      /* options & IA (limité) */
      positive: '#38b879',
      negative: '#dc5f52',
      warning: '#ce8a29',
      neutral: '#8f8a83',     /* benchmark */
      text: '#b7b3ad',
      muted: '#817d77',
      grid: 'rgba(255,255,255,.05)',
      /* Ordre des séries : référence cuivrée, beige, gris benchmark,
         violet options, ambre, cuivre sombre. */
      series: ['#cf6128', '#c8ad8d', '#8f8a83', '#85609f', '#ce8a29', '#914b2b'],
    },
    tooltip: {
      backgroundColor: '#151719',
      borderColor: 'rgba(255,255,255,.15)',
      titleColor: '#f3f1ed',
      bodyColor: '#b7b3ad',
    },
  };
})();
