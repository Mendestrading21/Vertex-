/* Vertex Charts — chart-theme-obsidian-copper.js (§35-36)
   Thème graphique unique VERTEX (identité BLANC/GRIS neutre), MIROIR de la source
   de vérité Python `vertex/visualization/palette.py` (test durci
   test_js_theme_matches_python_palette compare la série entière) :
   série principale = blanc-gris (identité/référence, PAS « hausse ») · benchmark =
   gris chaud · série secondaire = sable/ambre · positif = émeraude · négatif =
   rouge corail · options = violet contrôlé · comparaison technique = cyan. Plus
   aucun bleu ni orange identitaire ; aucune palette arc-en-ciel automatique.
   Chargé AVANT chart-core.js. */
(function () {
  'use strict';
  window.VXChartTheme = {
    colors: {
      brand: '#DBE1E8',       /* série principale : blanc-gris neutre (identité) */
      copper: '#8A8284',      /* série neutre acier (palette.COPPER) */
      copperLight: '#EEF1F5', /* blanc-gris clair (palette.COPPER_LIGHT) */
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
      muted: '#8A8284',
      grid: 'rgba(255,255,255,.05)',
      /* Ordre des séries = palette.SERIES : marque, sable, neutre, violet
         options, ambre, acier. Toute divergence casse le test de cohérence. */
      series: ['#DBE1E8', '#45D6E8', '#c8bfae', '#9B7BFF', '#D9BE3C', '#8A8284'],
    },
    tooltip: {
      backgroundColor: '#1D1819',
      borderColor: 'rgba(90,69,64,.55)',
      titleColor: '#F8F5F3',
      bodyColor: '#BABABA',
    },
  };
})();
