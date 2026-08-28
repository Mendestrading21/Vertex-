/* Vertex Charts — thème graphique unique.
   (Renommé au lot 24 : « chart-theme-black-glass » — l'ancien nom
   « obsidian-copper » décrivait une palette abandonnée. La coque et les
   bancs suivent le même commit.)

   Aligné sur « Vertex Black Glass — Signal Light ». UNE COULEUR = UNE
   SIGNIFICATION, y compris dans un graphique :

     argent   série principale, structure, sélection
     gris     benchmark, séries neutres — on distingue par luminance,
              épaisseur, tiret et marqueur AVANT d'ajouter une teinte
     vert     positif RÉEL uniquement — jamais une marque, jamais une série
     rouge    négatif, perte, risque
     ambre    prudence, incertitude, donnée dégradée
     violet   OPTIONS exclusivement
     cyan     crosshair et focus technique — RIEN d'autre

   Les clés historiques (`blue`, `cyan`, `teal`, `plum`, `sand`, `copper`…) sont
   conservées : des appelants les nomment encore. Seules leurs VALEURS changent,
   pour qu'aucune ne puisse plus rendre une couleur qui ment.

   Deux de ces alias mentaient réellement :
     · `blue` rendait #84aa31, le vert de marque abandonné. Une série demandée
       « bleue » sortait VERTE — la couleur que la doctrine réserve au positif.
       C'était la valeur par défaut de `C.area()`, donc de toute aire tracée
       sans couleur explicite.
     · `cyan` rendait un beige chaud, et servait de couleur à la COURBE
       D'ÉQUITÉ ainsi qu'aux niveaux de support.
   Les deux retombent désormais sur l'argent. Le cyan analytique existe sous son
   propre nom, `crosshair`, et n'est atteignable que délibérément.

   Chargé AVANT chart-core.js. Ne change aucune série, valeur, agrégation ni
   source : uniquement le rendu. */
(function () {
  'use strict';
  var ARGENT = '#c9ced8';
  var GRIS = '#8f96a2';
  window.VXChartTheme = {
    colors: {
      brand: ARGENT,          /* série principale */
      neutral: GRIS,          /* benchmark */
      positive: '#36c889',    /* positif RÉEL */
      negative: '#ed655c',    /* négatif, perte, risque */
      warning: '#dda23b',     /* prudence, donnée dégradée */
      amber: '#dda23b',
      violet: '#9c79d0',      /* OPTIONS seulement */
      option: '#9c79d0',
      crosshair: '#65d8e8',   /* cyan analytique — crosshair et focus, rien d'autre */

      /* ── Alias historiques : conservés pour leurs appelants, neutralisés ── */
      copper: '#242932',      /* ancien accent marque → graphite */
      copperLight: ARGENT,    /* rendait le vert de marque abandonné */
      info: ARGENT,
      blue: ARGENT,           /* n'a jamais été bleu, et n'est plus vert */
      cyan: ARGENT,           /* le cyan analytique vit sous `crosshair` */
      teal: '#9aa1ad',
      plum: '#7f8794',
      beige: '#9aa1ad',
      sand: '#9aa1ad',
      steel: GRIS,
      stone: '#7f8794',

      text: '#b8bec8',
      muted: '#9aa1ad',       /* relevé au niveau AA, comme --vx-smoke */
      grid: 'rgba(222,228,238,.055)',

      /* Ordre des séries : argent, gris, gris pierre, violet (options), ambre
         (prudence), acier. Aucune série verte, rouge, bleue ni cyan : une
         couleur sémantique n'apparaît que lorsqu'elle PORTE ce sens. */
      series: [ARGENT, GRIS, '#7f8794', '#9c79d0', '#dda23b', '#9aa1ad'],
    },
    tooltip: {
      backgroundColor: '#131720',
      borderColor: 'rgba(222,228,238,.14)',
      titleColor: '#f5f7fa',
      bodyColor: '#b8bec8',
    },
  };
})();
