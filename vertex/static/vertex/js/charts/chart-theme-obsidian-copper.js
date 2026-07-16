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
      brand: '#c9cdd4',       /* série principale : ARGENT neutre (plus de vert identité) */
      copper: '#3a3f47',
      copperLight: '#84aa31', /* (hex marque conservé pour cohérence registre) */
      amber: '#dda23b',       /* série secondaire */
      beige: '#c0b79f',
      info: '#c9cdd4',        /* information = argent neutre */
      blue: '#84aa31',        /* alias legacy — plus jamais bleu */
      cyan: '#c0b79f',        /* alias legacy → beige */
      violet: '#9c79d0',      /* options & IA (limité) */
      option: '#9c79d0',
      teal: '#53b9ad',        /* macro / cross-asset / liquidité */
      plum: '#8f698c',        /* série secondaire distincte */
      sand: '#c0b79f',
      steel: '#909b94',
      stone: '#6d746e',
      positive: '#36c889',
      negative: '#ed655c',
      warning: '#dda23b',
      neutral: '#8f8a83',     /* benchmark */
      text: '#b7b3ad',
      muted: '#817d77',
      grid: 'rgba(255,255,255,.05)',
      /* Ordre des séries : argent (primaire neutre), gris benchmark, beige,
         violet options, ambre, gris pierre. Aucune série verte/bleue. */
      series: ['#c9cdd4', '#8f8a83', '#c0b79f', '#9c79d0', '#dda23b', '#6d746e'],
    },
    tooltip: {
      backgroundColor: '#151719',
      borderColor: 'rgba(255,255,255,.15)',
      titleColor: '#f3f1ed',
      bodyColor: '#b7b3ad',
    },
  };
})();
