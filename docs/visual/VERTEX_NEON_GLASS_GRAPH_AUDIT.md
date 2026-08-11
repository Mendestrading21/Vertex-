# VERTEX NEON GLASS — Audit graphique visuel (Phase 0, issue #14)

> Inventaire read-only de **tous** les graphiques, cartes KPI, jauges, donuts,
> tableaux visuels et sparklines des 8 espaces. **Aucun moteur, aucune donnée,
> aucun calcul modifié.** Base : `84fbdc5` (RC1 stabilisée, 6 graphes morts déjà
> supprimés). Tout le rendu passe par le namespace `VXCharts` (`js/charts/`).

## 1. Totaux par espace

| Espace | Charts VXCharts | jauges | donuts | heatmaps | treemap | funnel | waterfall | timeline | scatter | tuiles KPI |
|---|---|---|---|---|---|---|---|---|---|---|
| Aujourd'hui | 2 | 1 | – | – | – | – | – | 1 | – | 4 |
| Marchés | 13 | 3 | 1 | 1 | – | 1 | 1 | 1 | 1 | ~9 |
| Opportunités | 7 | – | – | – | – | 1 | – | 1 | 1 | 1 |
| Analyse | 2 | – | – | – | – | – | – | – | – | 4 |
| Portefeuille | 8 | 1 | 1 | 1 | 1 | – | – | – | – | ~17 |
| Options | 3 (+N payoff) | 1 | – | – | – | – | – | – | – | chips |
| Journal | 3 | – | – | – | – | – | – | – | – | 4 |
| Système | 3 | 1 | 1 | – | – | – | – | – | – | ~1 |
| **Total (8 espaces)** | **~41** | **7** | **3** | **2** | **1** | **2** | **1** | **3** | **2** | **~40** |

## 2. Matrice avant/après par page (extrait décisionnel)

Recommandation : **K** garder · **M** fusionner/dédupliquer · **R** reconstruire sur primitive neon-glass.

### Aujourd'hui — `briefing.py`
| id | type | question | source | dup ? | reco |
|---|---|---|---|---|---|
| `vx-regime-gauge` | jauge | régime lisible ? | `/api/market/regime` | oui (Marchés) | **M** |
| `vx-calendar` | timeline | catalyseurs ? | `/cal-feed` | oui (Marchés, Opp) | **M** |

### Marchés — `markets_page.py` (page la plus dense : 13 rendus)
`vx-mk-regime-gauge` M · `vx-mk-multi` R(ligne premium) · `vx-mk-spy` R(area) · `vx-mk-yield` K/R · `vx-mk-rotation` (RRG scatter/quadrants) M · `vx-mk-sectors-heat` R(heatmap) · `vx-mk-breadth-gauge` M · `vx-mk-breadth-trend` R · `vx-mk-verdicts` R(ring) · `vx-mk-funnel` M · `vx-mk-health-wf` R(waterfall) · `vx-mk-vix-gauge` M · `vx-mk-macro-cal` M · **custom inline** : `sparkSvg` (KPI), barres roro, histogramme scores, rails → R(mini-sparkline + ticker card).

### Opportunités — `opportunities_page.py`
`op-scatter` (quadrants) M(≈Marchés rotation) · `op-funnel-viz` M · `op-ranking` (barres score custom) R(contribution bars) · `op-payoff` M(≈Options) · `op-scenarios` K/R · `op-theta` K · `op-iv` K · `op-cal` M.

### Analyse — `analysis_page.py`
`an-scorecard-radar` K/R · `an-chart` **K** (candlestick LWC canonique, chaîne de repli LWC→Canvas→ligne = dégradation voulue, pas un doublon).

### Portefeuille — `portfolio_page.py`
`pf-alloc-tree` R(treemap) · `pf-contrib-host` ≡ `pf-perf-contrib` **M (même graphe, 2 vues)** · `pf-perf-equity` R(area) · `pf-perf-drawdown` R(drawdown area) · `pf-perf-monthly` M(heatmap) · `pf-risk-gauge` M · `pf-sector-donut` M(ring) · barres de stress custom R.

### Options — `options_intel_page.py` + `options-structure.js`
`vx-opt-gauge-radial` M · `strat-pf-<i>` (N payoffs bruts) **M** · `vx-os-payoff` **payoff canonique unique** (garder, fusionner les autres dedans) · greeks (`vx-greek`) R(glass KPI).

### Journal — `performance_page.py`
`vx-pf-dist` R(histogramme) · `vx-pf-prog-chart` R · `vx-pf-track-bar` R(contribution bars) · `vx-pf-biais` (barres custom) R · tables `vx-pf-journal`/`vx-pf-track` R(table visuelle canonique).

### Système — `system_page.py`
`vx-sys-gauge` M · `vx-brain-movers` R(contribution bars) · `vx-data-quality-chart` M(ring).

## 3. Points chauds de duplication (à fusionner)

- **Jauge ×7** (même demi-cercle) : `vx-regime-gauge`, `vx-mk-regime/breadth/vix-gauge`, `pf-risk-gauge`, `vx-opt-gauge-radial`, `vx-sys-gauge` → **une seule** `gauge` (API bands déjà existante).
- **Timeline ×3** (`/cal-feed` identique) : `vx-calendar`, `vx-mk-macro-cal`, `op-cal`.
- **Payoff ×3** : `op-payoff`, `strat-pf-*`, `vx-os-payoff` → garder `vx-os-payoff` (moteur `multileg_lab`).
- **Scatter/quadrants ×2** : Marchés `rotation` (RRG) ≈ Opp `op-scatter` (asymétrie).
- **Funnel ×2** : Marchés `funnel` ≈ Opp `op-funnel-viz`.
- **Contribution bars ×3-7** : `pf-contrib-host`≡`pf-perf-contrib`, `vx-pf-track-bar`, `vx-brain-movers`, `op-ranking`, barres de stress, `vx-pf-biais` → **une** primitive barres signées.
- **Sparklines** : `sparkSvg` inline (Marchés KPI) réimplémente `sparkline.js`/`C.sparkline` → consolider.

## 4. Fabriques de graphes survivantes (post-RC1) + points d'entrée `VXCharts.*`

`chart-core.js` : `mount, card, cardState, axes, freshnessBadge, sparkline, area, bars,
donut, multiLine, levelLines, gauge, treemap, waterfall, radar, flow, rings, funnel,
sparkbars, eventMarkers, colors`. Puis : `bar-chart(barCard)`, `donut-chart(donutCard)`,
`line-area-chart(areaCard)`, `equity-chart(equityCard)`, `drawdown-chart(drawdownCard)`,
`heatmap(heatmapCard)`, `sparkline(sparklineInto)`, `timeline-chart(timelineCard)`,
`candlestick-chart(candlestickCard)`, `candlestick-lwc(lwCandlestickCard)`,
`price-chart(priceCard)`, `annotations(alertFromLevel)`, `option-payoff(payoffCard)`,
`option-scenarios(scenarioMatrix)`, `option-theta(thetaCard)`,
`option-iv-sensitivity(ivSensitivityCard)`. Thème unique :
`chart-theme-obsidian-copper.js` → `C.colors`. *(Supprimés en RC1 : correlation-matrix,
factor-chart, geographic-exposure, vol-surface, breadth-chart, sector-chart.)*

## 5. Contrat Chart Shell à préserver — `C.card(host, opts)` (chart-core.js)

Clés d'options : `title, question, conclusion, timeframe, unit, freshness, summary,
controlsHtml, height, source, timestamp, mode, limits, explain{shows,why,confirm,
invalidate}, legend[{label,color}], state('loading'|'empty'|'stale'|'error'),
stateMessage, render(canvas)`. Mobilier fourni pour chaque carte : en-tête
(titre · période · unité · fraîcheur · question · conclusion), `<canvas role="img"
aria-label=summary>`, résumé SR-only, légende, pied `VX.updateIndicator` + unité +
limites + bouton **« Comprendre ce graphique »** (drawer shows/why/confirm/invalidate).
**États honnêtes** : si `state≠ready`, la carte rend l'en-tête + l'état SANS canvas
(aucun faux graphe). **Toute reconstruction neon-glass doit conserver ce contrat.**

## 6. Composants canoniques neon-glass à construire (~15)

Premium **line** (multi/rebased) · premium **area** · **drawdown area** · **contribution
bars** (signées) · **histogramme** · **jauge demi-cercle** · **ring/donut sobre** ·
**heatmap** · **treemap** · **scatter/quadrants** · **payoff** · **timeline** · **radar** ·
**waterfall** · **mini-sparkline** · **glass KPI** · **ticker card** · **table visuelle** ·
**candlestick LWC** (garder, restyler). Bilan : **~41 instances → ~15 primitives**
réutilisables, sans jamais casser le contrat `C.card`.

## 7. Invariants de l'audit

Aucun moteur touché · READONLY intact · aucune donnée inventée · les fabriques
option (bar/heatmap) restent des dépendances dures des cartes options. La migration
se fera **page par page** (ordre imposé), après validation du prototype Aujourd'hui.
