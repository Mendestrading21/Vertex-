# Vertex — Bibliothèque graphique (V3)

Moteur unique : **Chart.js** (`static/chart.umd.min.js`) — aucune librairie
concurrente. Thème unique : `charts/chart-theme.js` (tokens V3) consommé
par `charts/chart-core.js` (gardien `test_chart_theme_is_single`).

## Contrat de carte graphique (§16)

`VXCharts.card(host, opts)` impose : **Titre · Question · Conclusion ·
Contrôles · Graphique · Légende · Source · Timestamp · Mode ·
Limites · bouton « Comprendre ce graphique »** (drawer : ce que montre /
pourquoi cela compte / ce qui confirmerait / ce qui invaliderait).
Gardiens : `test_every_chart_has_title/source/timestamp`.

Style commun : fond intégré, grille α .055, axes discrets, tooltip premium
(fond `#151c27`, rayon 8), chiffres tabulaires, animations 250 ms
(coupées en reduced-motion), registre anti-canvas-orphelins (`C.mount`).

## Modules (24)

| Module | Usage |
|---|---|
| chart-theme.js | thème couleurs/tooltip V3 |
| chart-core.js | contrat de carte, axes, mount, primitives (sparkline/area/bars/donut/multiLine), plugins niveaux & événements |
| sparkline.js | mini-courbes des KPI |
| line-area-chart.js | séries de référence (aire dégradée) |
| candlestick-chart.js | chandeliers (si OHLC fourni — repli clôtures honnête) |
| price-chart.js | graphique titre + niveaux entrée/stop/TP + marqueurs earnings |
| bar-chart.js | barres verticales/horizontales ± sémantiques |
| donut-chart.js | allocations (≤ 5 catégories) |
| heatmap.js | grilles HTML accessibles (secteurs, P&L mensuel, scénarios) |
| sector-chart.js | rotation sectorielle cliquable (drill-down) |
| breadth-chart.js | participation |
| equity-chart.js / drawdown-chart.js | courbe d'équité déclarée & drawdown dérivé |
| timeline-chart.js | calendriers (macro, earnings, catalyseurs) |
| correlation-matrix.js | matrice de corrélation |
| vol-surface.js | surface IV (strike × échéance) |
| option-payoff.js | payoff à l'échéance |
| option-scenarios.js | matrice spot × temps (moteur scenario_pricer) |
| option-theta.js | décomposition temps |
| option-iv-sensitivity.js | sensibilité IV ±20 % |
| factor-chart.js / geographic-exposure.js | expositions |
| annotations.js | alerte depuis un niveau (double-clic graphe) |

## Sémantique couleur (thème unique)

orange `#f68a3c` = série de référence & niveaux d'action · bleu `#4ca6ff` =
information · cyan `#2cc9d8` = données/live · violet `#8b6df6` = options/IA ·
vert `#2acb7f` = positif · rouge corail `#f05d55` = négatif · ambre
`#f3a93b` = attention · gris `#738096` = benchmark. Séries multiples :
`colors.series` (référence orange puis hues distinctes).

## Règles

1. L'UI ne recalcule **aucun** indicateur — elle trace ce que les moteurs
   fournissent (transformations d'affichage seules : rebasage %,
   normalisation d'échelle).
2. Donnée absente → carte en état vide honnête, jamais un graphique
   décoratif.
3. Un graphique = une fonction (aucun remplissage décoratif).
