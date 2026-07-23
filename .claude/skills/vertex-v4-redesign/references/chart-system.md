# Chart system Vertex V4

Bibliothèque canonique : `vertex/static/vertex/js/charts/chart-core.js`, exposée
par `window.VXCharts` (`C`). Chart.js sert les canvas ; quelques primitives SVG
gèrent jauges, radars et visualisations spécialisées.

Contrat obligatoire : `docs/canonical/CHART_CONTRACT.md`.

## Contrat d'une carte graphique

Chaque graphique affiche ou rend accessible :

- question métier ;
- source et timestamp/fraîcheur ;
- période, fuseau et unité ;
- tooltip utile ;
- conclusion courte ;
- état vide honnête via les primitives communes.

Palette par tokens : prism pour la série principale neutre, gris pour le
benchmark, vert/rouge/ambre pour leur sémantique stricte et bleu seulement pour
une comparaison secondaire. Aucune courbe n'est fabriquée en cas d'absence.

## Primitives existantes

`C.card`, `C.area`, `C.bars`, `C.donut`, `C.multiLine`, `C.gauge`, `C.radar`,
`C.treemap`, `C.waterfall`, `C.flow`, `C.rings`, `C.funnel`, `C.sparkbars`,
`C.mount`, `C.axes`, `C.colors`, `C.rgba`, `C.optionChainGrid`,
`C.volSurfaceCard`.

Avant de créer une primitive, rechercher un équivalent et vérifier qu'une table
ou un KPI ne répond pas mieux à la question.

## Migration V4

Le fichier `chart-theme-obsidian-copper.js` reste temporairement chargé. Le lot
04 migre ses exports vers `chart-theme-v4.js`, met à jour les imports et ne
supprime l'ancien fichier qu'après tests et contrôle visuel complet.
