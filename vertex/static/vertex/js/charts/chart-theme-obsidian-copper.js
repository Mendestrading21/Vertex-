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
      brand: '#84aa31',       /* série principale : orange cuivré */
      copper: '#48631b',
      copperLight: '#84aa31',
      amber: '#dda23b',       /* série secondaire */
      beige: '#c0b79f',
      info: '#84aa31',        /* information = cuivre clair */
      blue: '#84aa31',        /* alias legacy — plus jamais bleu */
      cyan: '#c0b79f',        /* alias legacy → beige */
      violet: '#9c79d0',      /* options & IA (limité) */
      positive: '#36c889',
      negative: '#ed655c',
      warning: '#dda23b',
      neutral: '#8f8a83',     /* benchmark */
      text: '#b7b3ad',
      muted: '#817d77',
      grid: 'rgba(255,255,255,.05)',
      /* Ordre des séries : référence cuivrée, beige, gris benchmark,
         violet options, ambre, cuivre sombre. */
      series: ['#84aa31', '#c0b79f', '#8f8a83', '#9c79d0', '#dda23b', '#48631b'],
    },
    tooltip: {
      backgroundColor: '#151719',
      borderColor: 'rgba(255,255,255,.15)',
      titleColor: '#f3f1ed',
      bodyColor: '#b7b3ad',
    },
  };
})();
