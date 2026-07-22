/* Vertex Charts — thème graphique unique (§35-36).
   VERTEX V4 OBSIDIAN PRISM (Lot 04) : série principale = violet prism ·
   benchmark = gris · magenta / teal / ambre = séries secondaires distinctes ·
   options = violet · positif = vert · négatif = rouge corail. ZÉRO bleu
   (garde-fous palette : test_no_blue_main_series + test_js_theme_matches_python_palette).
   La série de comparaison bleue optionnelle (§6.2) reste différée. Cohérent avec
   le registre central `vertex/visualization/palette.py`. Aligné sur `--vx-v4-*` ;
   chart-core lit --vx-brand/positive/negative/warning/option au runtime.
   (Nom de fichier historique conservé — rename → chart-theme-v4.js au Lot 15.)
   Chargé AVANT chart-core.js. */
(function () {
  'use strict';
  window.VXChartTheme = {
    colors: {
      brand: '#9a5cff',       /* série principale : VIOLET prism (runtime = --vx-brand) */
      copper: '#3a3f47',      /* surface neutre sombre (legacy) */
      copperLight: '#9a5cff', /* alias marque → violet */
      amber: '#e6a846',       /* série secondaire (attente/ambre) */
      beige: '#858e9f',       /* série secondaire : gris froid */
      info: '#7e8798',        /* information = gris neutre (jamais bleu) */
      blue: '#9a5cff',        /* alias legacy → violet (defaults d'aire = prism, pas bleu) */
      cyan: '#7e8798',        /* alias legacy → gris neutre */
      violet: '#a875ff',      /* options & IA */
      option: '#a875ff',
      teal: '#53b9ad',        /* macro / cross-asset / liquidité */
      plum: '#8f698c',        /* série secondaire distincte */
      sand: '#c0b79f',
      steel: '#7e8798',
      stone: '#6d746e',
      positive: '#35d28b',
      negative: '#ff625f',
      warning: '#e6a846',
      neutral: '#7e8798',     /* benchmark gris */
      text: '#bec5d2',
      muted: '#858e9f',
      grid: 'rgba(255,255,255,.06)',
      /* Ordre des séries : violet prism (primaire), gris benchmark, magenta,
         teal macro, ambre, gris pierre. Aucune série verte ni bleue. */
      series: ['#9a5cff', '#7e8798', '#d86cb7', '#53b9ad', '#e6a846', '#6d746e'],
    },
    tooltip: {
      backgroundColor: '#12161f',
      borderColor: 'rgba(138,82,255,.25)',
      titleColor: '#f5f7fb',
      bodyColor: '#bec5d2',
    },
  };
})();
