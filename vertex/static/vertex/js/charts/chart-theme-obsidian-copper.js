/* Vertex Charts — chart-theme-obsidian-copper.js (§35-36)
   Thème graphique unique VERTEX (identité BLEU électrique), MIROIR de la source
   de vérité Python `vertex/visualization/palette.py` (test durci
   test_js_theme_matches_python_palette compare la série entière) :
   série principale = Bleu (identité/référence, PAS « hausse ») · benchmark = gris
   chaud · série secondaire = sable/ambre · positif = émeraude · négatif = rouge
   corail · options = violet contrôlé · comparaison technique = cyan. Le bleu EST
   la marque ; aucune palette arc-en-ciel automatique. Chargé AVANT
   chart-core.js. */
(function () {
  'use strict';
  window.VXChartTheme = {
    colors: {
      brand: '#3B82F6',       /* série principale : Bleu électrique (identité) */
      copper: '#8A8284',      /* série neutre acier (palette.COPPER) */
      copperLight: '#5C9BFF', /* Bleu clair (palette.COPPER_LIGHT) */
      amber: '#FFC857',       /* série secondaire / attention */
      beige: '#c8bfae',       /* benchmark clair (sable) */
      info: '#45D6E8',        /* information = cyan comparaison technique */
      blue: '#45D6E8',        /* alias legacy → cyan technique (distinct du bleu marque) */
      cyan: '#45D6E8',        /* comparaison technique */
      violet: '#9B7BFF',      /* options & IA (limité) */
      positive: '#2ED6A1',
      negative: '#FF5F69',
      warning: '#FFC857',
      neutral: '#BABABA',     /* benchmark neutre (palette.NEUTRAL) */
      text: '#BABABA',
      muted: '#8A8284',
      grid: 'rgba(255,255,255,.05)',
      /* Ordre des séries = palette.SERIES : marque, sable, neutre, violet
         options, ambre, acier. Toute divergence casse le test de cohérence. */
      series: ['#3B82F6', '#c8bfae', '#BABABA', '#9B7BFF', '#FFC857', '#8A8284'],
    },
    tooltip: {
      backgroundColor: '#1D1819',
      borderColor: 'rgba(90,69,64,.55)',
      titleColor: '#F8F5F3',
      bodyColor: '#BABABA',
    },
  };
})();
