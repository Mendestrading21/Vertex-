/* Vertex Charts — thème graphique unique VERTEX (§35-36), MIROIR de la source
   de vérité Python `vertex/visualization/palette.py` (test durci
   test_js_theme_matches_python_palette compare la série entière) :
   série principale = VIOLET (identité/référence, PAS « hausse ») · benchmark =
   gris chaud · série secondaire = sable/ambre · positif = émeraude · négatif =
   rouge corail · comparaison technique = cyan. Plus aucun bleu identitaire ;
   aucune palette arc-en-ciel automatique.

   LE NOM NE PORTE PLUS DE COULEUR, ET C'EST LE POINT. Ce fichier s'est appelé
   `chart-theme-obsidian-copper.js` alors qu'il servait un violet : un nom qui
   encode l'identité du moment ment dès que l'identité change — et elle a changé
   deux fois (Signal Green → Ember/cuivre → violet). Il s'appelle désormais
   `chart-theme.js` : il dit ce qu'il EST, pas de quelle couleur il était.
   La même logique vaut pour les alias `--vx-ember-*` / `--vx-orange-*` de
   tokens.css, dont la rampe canonique s'appelle maintenant `--vx-violet-*`.
   Chargé AVANT chart-core.js. */
(function () {
  'use strict';
  window.VXChartTheme = {
    colors: {
      brand: '#9B7BFF',       /* série principale : violet Vertex (identité) */
      brandHover: '#B9A2FF',  /* violet clair : interaction / survol */
      copper: '#8A8284',      /* série neutre acier (palette.COPPER) */
      copperLight: '#B9A2FF', /* alias historique de palette.COPPER_LIGHT */
      amber: '#D9BE3C',       /* série secondaire / attention */
      beige: '#c8bfae',       /* benchmark clair (sable) */
      info: '#45D6E8',        /* information = cyan comparaison technique */
      blue: '#45D6E8',        /* alias legacy → cyan technique (distinct du bleu marque) */
      cyan: '#45D6E8',        /* comparaison technique */
      violet: '#9B7BFF',      /* options & IA — MÊME valeur que brand (voir palette.py) */
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
      /* Ordre des séries = palette.SERIES : marque, cyan technique, sable,
         ambre, acier. Le violet options en est SORTI — il vaut désormais la
         marque, et deux séries de même couleur ne sont pas deux séries. Toute
         divergence casse le test de cohérence. */
      series: ['#9B7BFF', '#45D6E8', '#c8bfae', '#D9BE3C', '#8A8284'],
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
