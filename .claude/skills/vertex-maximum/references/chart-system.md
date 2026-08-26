# Chart system Vertex (`window.VXCharts`)

UNE seule bibliothèque graphique : `vertex/static/vertex/js/charts/chart-core.js` (expose `window.VXCharts`, alias
`C`) + `option-chain-grid.js` (grille de chaîne) + `vol-surface.js` (surface IV) + `bar-chart.js`. Basée sur
Chart.js pour les canvas + SVG sur-mesure (jauges/radars). Cross-ref : `docs/VERTEX_CHART_LIBRARY.md`,
`docs/claude/VERTEX_CHART_CONTRACT.md`. Inventaire réel des primitives : `docs/vertex-audit/06-chart-inventory.md`.

## Contrat de graphique (OBLIGATOIRE pour chaque `VXCharts.*Card(`)
Chaque carte-graphique doit porter : **source · timestamp/fraîcheur · question** (que résout-il ?) **· conclusion**
(lecture en une phrase). État vide **honnête** via `VX.states.empty` (jamais une courbe fabriquée). Palette
**uniquement** `C.colors` (zéro bleu ; violet = options). Test gardien : `tests/test_ui_v3.py` (présence `source`).

## Primitives existantes (extrait — voir l'inventaire pour la liste exacte + signatures)
`C.card` (enveloppe carte+canvas+contrat) · `C.area` · `C.bars` (h/v, signé) · `C.donut` · `C.multiLine` ·
`C.gauge` (SVG, bille blanche) · `C.radar` (SVG) · `C.treemap` · `C.waterfall` · `C.flow` · `C.rings` · `C.funnel` ·
`C.sparkbars` · `C.scoreGaugeSVG` · `C.mount` (Chart.js) · `C.axes` · `C.colors` · `C.rgba` · `C.optionChainGrid` ·
`C.volSurfaceCard`.

## Mapping cible (mission §7) → existant / à combler
| Cible mission | Existant Vertex | Statut |
|---|---|---|
| LineChart / AreaChart | `C.multiLine` / `C.area` | ✅ |
| BarChart / StackedBar | `C.bars` | ✅ (empilé à confirmer) |
| WaterfallChart | `C.waterfall` | ✅ |
| Heatmap / CalendarHeatmap | (perf mensuelle existe) | ⚠️ à généraliser |
| ScatterChart | scatter (opportunités) | ✅ |
| Histogram | distribution rendements | ✅ |
| DonutChart / Treemap | `C.donut` / `C.treemap` | ✅ |
| Gauge / Sparkline | `C.gauge` / `C.sparkbars` | ✅ |
| PayoffChart (options) | swing/scenarios | ⚠️ à formaliser en primitive |
| DrawdownChart | drawdown (perf) | ✅ |
| GreeksChart (radar) | `C.radar` | ✅ |
| ScenarioChart | MC/bootstrap fan | ✅ (fiche analyse) |
| CorrelationMatrix / RiskMatrix | — | ❌ à créer si donnée dispo |
| Candlestick | — | ❌ (prix = area/close aujourd'hui) |

## Grille de décision par graphique (mission §7 — appliquer à chaque graphe existant)
Quelle question ? quelle décision permise ? données exactes ? unités visibles ? période/fuseau clairs ? valeurs
manquantes traitées ? tooltip utile ? lisible sans couleur ? une table serait-elle mieux ? existe-t-il déjà
ailleurs ? décoratif ? perf OK ? petit écran OK ? fraîcheur affichée ? → **Supprimer/remplacer tout graphe qui
n'apporte aucune décision.** Jamais deux couleurs différentes pour une même sémantique selon la page.
