# Vertex — Bibliothèque graphique (Black Glass Institutional)

> **Vérité runtime = le thème `charts/chart-theme-obsidian-copper.js`** (palette
> Black Glass) consommé par `charts/chart-core.js`. Ce document le RÉSUME ; en
> cas de doute, le JS gagne. _(Correctif DES-01 : la palette orange/bleu
> décrite ici auparavant est ABANDONNÉE — voir `.claude/rules/vertex-design-rules.md`.)_

Moteur unique : **Chart.js** (`static/chart.umd.min.js`) — aucune librairie
concurrente. Thème unique : `charts/chart-theme-obsidian-copper.js` (palette
Black Glass, dérivée des tokens `--vx-*`) consommé par `charts/chart-core.js`
(gardien `test_chart_theme_is_single`).

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

## Sémantique couleur (thème unique — Black Glass)

**Zéro bleu.** argent `#c9cdd4` = série de référence / marque / structure ·
vert `#36c889` = positif · rouge corail `#ed655c` = négatif/risque · ambre
`#dda23b` = attention/série secondaire · violet `#9c79d0` = options/IV/Greeks
(limité) · teal `#53b9ad` = macro/cross-asset/liquidité · gris pierre
`#8f8a83` = benchmark/neutre. **Séries multiples** :
`colors.series = ['#c9cdd4','#8f8a83','#9aa1a9','#9c79d0','#dda23b','#6d746e']`
(argent puis neutres/violet/ambre distincts — aucune série verte ni bleue,
le vert restant réservé à la sémantique `positive`). Une même sémantique =
une même couleur sur toutes les pages et graphiques.

## Règles

1. L'UI ne recalcule **aucun** indicateur — elle trace ce que les moteurs
   fournissent (transformations d'affichage seules : rebasage %,
   normalisation d'échelle).
2. Donnée absente → carte en état vide honnête, jamais un graphique
   décoratif.
3. Un graphique = une fonction (aucun remplissage décoratif).
