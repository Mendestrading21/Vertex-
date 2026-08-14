/* Vertex Charts — thème Signal OS.
   Miroir strict de `vertex/visualization/palette.py` :
   violet = identité / série principale ; violet profond = options ;
   émeraude = positif ; corail = négatif ; jaune = attente ;
   cyan = comparaison technique ; gris = benchmark neutre.
   Chargé avant chart-core.js. */
(function () {
  'use strict';
  window.VXChartTheme = {
    colors: {
      brand: '#9B7BFF',
      copper: '#8A8284',
      copperLight: '#EEF1F5',
      amber: '#D9BE3C',
      beige: '#c8bfae',
      info: '#45D6E8',
      blue: '#45D6E8',       /* alias legacy → comparaison technique */
      cyan: '#45D6E8',
      violet: '#7F5DF0',     /* options / volatilité */
      positive: '#2BBE90',
      negative: '#E9555F',
      warning: '#D9BE3C',
      neutral: '#BABABA',
      text: '#BABABA',
      muted: '#8A8284',
      grid: 'rgba(255,255,255,.05)',
      series: ['#9B7BFF', '#45D6E8', '#c8bfae', '#EEF1F5', '#D9BE3C', '#8A8284'],
    },
    tooltip: {
      backgroundColor: '#121214',
      borderColor: 'rgba(255,255,255,.12)',
      titleColor: '#F8F5F3',
      bodyColor: '#BABABA',
    },
  };
})();
