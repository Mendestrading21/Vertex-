# VERTEX VISUAL COMMAND CENTER — AUDIT (Phase 1)

> Mission **additive** et **READONLY**. Aucune source, aucun calcul, aucune règle de
> stratégie, aucune connexion, aucun contrat d'API métier n'est modifié. On ne touche
> qu'à la **présentation** (templates, CSS, JS front, visualisations). Donnée absente =
> état vide premium, jamais un zéro ni une série fictive.
>
> Branche : `feature/vertex-visual-command-center` (jamais `main`).

## 0. Constat central de l'audit

**Une grande partie de la « bibliothèque graphique » demandée EXISTE DÉJÀ et est de bonne
qualité.** La mission est donc réellement de l'**enrichissement ciblé**, pas une création
from-scratch. Créer une lib parallèle serait une régression (doublons, dette).

### Infrastructure visuelle existante (à réutiliser, pas à recréer)

| Élément demandé (spec §9) | État réel |
|---|---|
| Moteur graphique unique | ✅ **Chart.js** embarqué + `VXCharts` (`chart-core.js`) |
| ChartCard (titre/question/conclusion/source/fraîcheur/drawer) | ✅ `VXCharts.card()` — contrat §34 complet, bouton « Comprendre ce graphique » |
| Registry anti-fuite (destroy avant remount) | ✅ `VXCharts.mount()` (Map canvas→Chart, destroy auto) |
| Thème unifié Obsidian Copper | ✅ `chart-theme-obsidian-copper.js` + `tokens.css` |
| Tooltip premium | ✅ défauts Chart.js stylés (fond obsidienne, bordure fine) |
| reduced-motion | ✅ géré dans `chart-core` + `base.css` |
| Couleurs sémantiques (positif/négatif/warning/neutre/option violet) | ✅ `VXCharts.colors` |
| Primitives | ✅ sparkline, area, bars, donut, multiLine, levelLines, eventMarkers |
| États (loading/empty/error/stale) | ✅ `states.css` + `VX.states.*` |
| Tables premium | 🟡 `tables.css` présent, enrichissement partiel |

### 23 charts déjà présents (`vertex/static/vertex/js/charts/`)

`candlestick-chart`, `price-chart`, `line-area-chart`, `equity-chart`, `drawdown-chart`,
`bar-chart`, `sparkline`, `donut-chart`, `breadth-chart`, `sector-chart`, `timeline-chart`,
`heatmap`, `correlation-matrix`, `factor-chart`, `geographic-exposure`, `annotations`,
`option-payoff`, `option-scenarios`, `option-theta`, `option-iv-sensitivity`, `vol-surface`.

### Types graphiques demandés mais MANQUANTS (vrais gaps à créer)

- **Treemap** (portefeuille, revenus par segment) — absent
- **Waterfall** (contribution P&L/risque, décision) — absent
- **Sankey / flow diagram** (Intelligence, Système) — absent
- **Radar** (greeks, risques entreprise) — absent
- **Gauge / radial** (régime, risk score, options environment) — absent (approché par jauges CSS ?)
- **Calendar** (earnings/macro/expirations) — absent (timeline existe)
- **Scatter/bubble matrix** (Opportunity Matrix, Options Radar) — absent

## 1. État par page (chart count = appels `VXCharts.*`)

| Page | Charts | État | Priorité | Gaps principaux vs spec |
|---|---|---|---|---|
| **Marchés** (overview/macro/secteurs/breadth/vol) | 10 | 🟢 riche | P2 | breadth advance/decline (donnée absente → état vide honnête), heatmap secteurs, term structure VIX |
| **Opportunités** | 8 | 🟢 correct | P2 | Opportunity **Matrix** (scatter/bubble), Funnel visuel, Role Map |
| **Performance** | 6 | 🟢 correct | P3 | monthly heatmap, MAE/MFE scatter, rolling metrics |
| **Briefing** | 5 | 🟡 moyen | **P1** | Hero cockpit éditorial, KPI strip indices (S&P/Nasdaq/VIX/10a/Russell/DXY), Catalyst Radar |
| **Système** | 4 | 🟡 moyen | P3 | data freshness **heatmap**, job timeline, **flow diagrams** IBKR→…→Décision |
| **Analyse action** (fiche) | 3 | 🟡 récemment enrichie (PER, consensus, révisions BPA, surprises, notes 13F/initiés, TTM squeeze) | P2 | workspace chandeliers pro (overlays/presets/panneaux RSI-MACD), RS vs SPY/secteur, scenario cone |
| **Portefeuille** (équipe/positions/options/risque) | 3 | 🔴 **pauvre** | **P1** | **treemap** positions, **risk contribution** waterfall, **correlation matrix**, team balance, stress matrix — nécessite positions IBKR (test sous compte réel) |
| **Intelligence** | 3 | 🔴 **pauvre** | **P1** | **Sankey** impacts, convergence matrix comité, decision waterfall, remplacer JSON brut par cartes |
| **Options Intelligence** (overview/radar/chain/vol/greeks/scénarios/position) | à câbler | 🟡 charts options présents mais pages à monter en cockpit | **P1** | environment gauge, greeks radar/waterfall, chain heatmap, scenario heatmaps |
| **Suivis** | — | 🟡 | P3 | perf hypothétique vs SPY, funnel de conversion |

## 2. Problèmes transverses relevés

1. **Pages pauvres** : Portefeuille, Intelligence, Options n'exploitent pas la lib existante à hauteur du reste.
2. **Types manquants** : treemap, waterfall, sankey, radar, gauge, calendar, bubble-matrix.
3. **Vérifiabilité** : Portefeuille/Options/Risque dépendent des positions IBKR → test sous compte réel (U10360059) ; Marchés/Opportunités/Performance/Briefing/Analyse testables sans IBKR.
4. **Honnêteté données** (déjà bien tenue) : breadth advance/decline, VIX term structure = données non fournies par les moteurs → **états vides premium**, ne rien inventer (règle §2 respectée).

## 3. Plan d'exécution (mappé aux phases spec §47)

Les Phases 2–7 (tokens, chart-core, tooltips, cartes, états, légendes) sont **acquises** →
on capitalise dessus. Ordre de valeur :

- **Lot A (P1) — pages pauvres à fort ROI** : Options Intelligence (cockpit + gauge + greeks radar/waterfall), Portefeuille (treemap + risk contribution + team balance), Intelligence (sankey + convergence + cartes vs JSON), Briefing (hero + KPI strip + catalyst radar).
- **Lot B (P2)** : Opportunités (matrix/funnel/role map), Analyse (workspace chandeliers pro), Marchés (heatmaps/term structure).
- **Lot C (P3)** : Performance, Système (freshness heatmap, flow diagrams), Suivis, Calendriers.
- **Transverse** : nouveaux types (treemap/waterfall/sankey/radar/gauge/calendar/bubble) créés dans `charts/` au fil des besoins, testés, réutilisés.

Après **chaque page** : test navigateur, 0 erreur console, états vérifiés, desktop+mobile, commit stable, capture avant/après.

## 4. Garde-fous (non négociables)

- Aucune modif backend sauf **exposer une donnée déjà calculée** (sans recalcul, sans changer sa valeur).
- Aucun chart de production sur donnée fictive ; absence → état vide premium.
- Pas de bleu/cyan en identité ; violet réservé options ; pas de glow permanent.
- Service worker : bump `td-shell-vN` à chaque changement de shell visible.
- READONLY intégral, aucun bouton d'ordre.

---
*Audit vivant — mis à jour au fil des lots livrés.*
