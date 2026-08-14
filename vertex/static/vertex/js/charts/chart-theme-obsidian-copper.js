/* Vertex Charts — chart-theme-obsidian-copper.js (§35-36)
   Thème graphique unique VERTEX (identité CUIVRE SOBRE), MIROIR de la source
   de vérité Python `vertex/visualization/palette.py` (test durci
   test_js_theme_matches_python_palette compare la série entière) :
   série principale = cuivre (identité/référence, PAS « hausse ») · benchmark =
   gris chaud · série secondaire = sable/ambre · positif = émeraude · négatif =
   rouge corail · options = violet contrôlé · comparaison technique = cyan. Plus
   aucun bleu identitaire ; aucune palette arc-en-ciel automatique.
   Chargé AVANT chart-core.js. */
(function () {
  'use strict';
  window.VXChartTheme = {
    colors: {
      brand: '#D28A54',       /* série principale : cuivre neutre (identité) */
      brandHover: '#E1A06E',  /* cuivre clair : interaction / survol */
      copper: '#8A8284',      /* série neutre acier (palette.COPPER) */
      copperLight: '#E1A06E', /* alias historique de palette.COPPER_LIGHT */
      amber: '#D9BE3C',       /* série secondaire / attention */
      beige: '#c8bfae',       /* benchmark clair (sable) */
      info: '#45D6E8',        /* information = cyan comparaison technique */
      blue: '#45D6E8',        /* alias legacy → cyan technique (distinct du bleu marque) */
      cyan: '#45D6E8',        /* comparaison technique */
      violet: '#9B7BFF',      /* options & IA (limité) */
      positive: '#2BBE90',
      negative: '#E9555F',
      warning: '#D9BE3C',
      neutral: '#BABABA',     /* benchmark neutre (palette.NEUTRAL) */
      text: '#BABABA',
      muted: '#989092',
      /* Infrastructure graphique : neutres chauds, jamais une nouvelle série. */
      grid: 'rgba(200,194,188,.08)',
      axis: 'rgba(200,194,188,.16)',
      crosshair: 'rgba(200,194,188,.30)',
      /* Ordre des séries = palette.SERIES : marque, sable, neutre, violet
         options, ambre, acier. Toute divergence casse le test de cohérence. */
      series: ['#D28A54', '#45D6E8', '#c8bfae', '#9B7BFF', '#D9BE3C', '#8A8284'],
    },
    tooltip: {
      backgroundColor: '#141619',
      borderColor: 'rgba(200,194,188,.20)',
      titleColor: '#F5F3F0',
      bodyColor: '#C8C2BC',
      footerColor: '#989092',
    },
  };
})();
