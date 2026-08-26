# 07 — Inventaire des graphiques (VXCharts)

Bibliothèque **unique** : `window.VXCharts` (`vertex/static/vertex/js/charts/chart-core.js:9`, `const C =
window.VXCharts`), bâtie sur Chart.js (plugins maison `_glowPlugin`/`_leadDotPlugin`/`_crossPlugin`,
`chart-core.js:161`). Chaque module de graphe attache ses fabriques à `C` (ex. `sparkline.js` :
`C.sparklineInto = …`, `C.sparkline = …`).

## Modules (27 fichiers `charts/`)
`chart-core` (cœur + thème `chart-theme-obsidian-copper`) · `price-chart` · `candlestick-chart` · `candlestick-lwc`
· `line-area-chart` · `bar-chart` · `sparkline` · `equity-chart` · `drawdown-chart` · `breadth-chart` ·
`sector-chart` · `radar-chart` · `donut-chart` · `heatmap` · `correlation-matrix` · `factor-chart` ·
`timeline-chart` · `geographic-exposure` · `annotations` · **options** : `option-chain` · `option-chain-grid` ·
`option-payoff` · `option-scenarios` · `option-theta` · `option-iv-sensitivity` · `vol-surface`.

## Contrat de graphique (à faire respecter partout)
Chaque graphe doit porter : **source · timestamp · question posée · conclusion lisible · état vide honnête ·
palette `C.colors`** (jamais deux couleurs pour une même sémantique, jamais un hex moteur brut). Référence :
`references/chart-system.md` + `docs/claude/VERTEX_CHART_CONTRACT.md`.

## Findings
- **CHT-01 (P2) — Redondance de primitives lignes/chandeliers.** `candlestick-chart` **et** `candlestick-lwc`
  (lightweight-charts) coexistent ; `price-chart`/`line-area-chart` se recouvrent. **Action** : documenter quand
  utiliser quoi, ou fusionner. Ne pas casser les pages qui les consomment (auditer les appelants d'abord).
- **CHT-02 (P2) — Uniformité du contrat.** Vérifier module par module que source/timestamp/question/conclusion
  et l'état vide sont réellement rendus (pas de graphe décoratif sans légende de provenance). Prioriser les
  graphes de décision (payoff, scénarios, IV, greeks, MC/bootstrap).
- **CHT-03 (P3) — `Date.now()` en source côté page.** Plusieurs pages passent `timestamp: Date.now()`
  (`opportunities_page.py:486`, `options-symbol.js:195`) — acceptable pour l'horodatage de rendu, mais le
  timestamp de **la donnée** (pas du rendu) doit primer quand il existe. Clarifier dans le contrat.

## Cible (Phase 2)
Contrat unique appliqué à tous les modules ; palette `C.colors` = seule source de couleur sémantique ; violet
réservé aux graphes d'options ; états vide/erreur standardisés.
