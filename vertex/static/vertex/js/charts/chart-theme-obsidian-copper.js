/* Vertex Charts — chart-theme-obsidian-copper.js (§35-36)
   Thème graphique unique VERTEX OBSIDIAN COPPER, MIROIR de la source de vérité
   Python `vertex/visualization/palette.py` (test durci
   test_js_theme_matches_python_palette compare la série entière) :
   série principale = Vert Signal (identité, PAS « hausse ») · benchmark = gris
   chaud · série secondaire = beige/ambre · positif = émeraude · négatif = rouge
   corail · options = violet contrôlé. AUCUNE série principale bleue, aucune
   palette arc-en-ciel automatique. Chargé AVANT chart-core.js. */
(function () {
  'use strict';
  window.VXChartTheme = {
    colors: {
      brand: '#84aa31',       /* série principale : Vert Signal (identité) */
      copper: '#747d75',      /* série neutre acier (palette.COPPER) */
      copperLight: '#a3ca42', /* Vert Signal clair (palette.COPPER_LIGHT) */
      amber: '#dda23b',       /* série secondaire / attention */
      beige: '#c0b79f',       /* benchmark clair (sable) */
      info: '#84aa31',        /* information = Vert Signal */
      blue: '#84aa31',        /* alias legacy — plus jamais bleu */
      cyan: '#c0b79f',        /* alias legacy → beige */
      violet: '#9c79d0',      /* options & IA (limité) */
      positive: '#36c889',
      negative: '#ed655c',
      warning: '#dda23b',
      neutral: '#9d978e',     /* benchmark neutre (palette.NEUTRAL) */
      text: '#b7b3ad',
      muted: '#817d77',
      grid: 'rgba(255,255,255,.05)',
      /* Ordre des séries = palette.SERIES : marque, beige, neutre, violet
         options, ambre, acier. Toute divergence casse le test de cohérence. */
      series: ['#84aa31', '#c0b79f', '#9d978e', '#9c79d0', '#dda23b', '#747d75'],
    },
    tooltip: {
      backgroundColor: '#151719',
      borderColor: 'rgba(255,255,255,.15)',
      titleColor: '#f3f1ed',
      bodyColor: '#b7b3ad',
    },
  };
})();
