# VERTEX INSTITUTIONAL EXPERIENCE — BASELINE (Phase 1)

> Branche `feature/vertex-institutional-experience-overhaul` (créée depuis
> `feature/vertex-visual-command-center`, 15 commits visuels préservés).
> Mission **additive & READONLY** : 0 modif source/calcul/stratégie/connexion,
> 0 donnée fictive, aucun chemin d'ordre.

## Point de départ (déjà en place avant cet overhaul)

**Infrastructure graphique mature** : `VXCharts` (ChartCard §34, registry anti-fuite),
Chart.js + 23 charts, thème Obsidian Copper, états (loading/empty/stale/error).

**5 types réutilisables déjà construits** (command-center) : `gauge`, `treemap`, `flow`,
`radar`, `waterfall` + R:R ladder.

**Pages déjà enrichies** (15 commits) : Briefing (jauge régime), Marchés ×5 (régime, VIX,
secteurs treemap, santé waterfall, courbe des taux), Opportunités (classement sous-scores),
Intelligence ×2 (flow, radar), Système (heatmap fraîcheur), Analyse ×2 (R:R ladder, perf
multi-horizons), Portefeuille ×3 (treemap allocation, stress bars, treemap options).

**Routes/pages** : Briefing `/`, Marchés `/markets` (overview/macro/sectors/breadth/
volatility), Opportunités `/opportunities` (radar/stocks/options/anomalies/calendar),
Portefeuille `/portfolio` (team/positions/options/risk/watchlist), Analyse `/analysis`,
**Options Intelligence `/options`** (overview/volatility/radar/scenarios), Performance
`/performance`, Intelligence `/intelligence`, Système `/system`.

## Écarts vs le cahier institutionnel (à traiter)

| Domaine | État | Priorité |
|---|---|---|
| **Options en nav principale** | ✅ FAIT (commit 1) | P0 |
| **Top/Flop Briefing** | ✅ FAIT (commit 2) | P0 |
| Options : sous-pages (chain/greeks/CALL-PUT/optimizer/position workspace) | partiel (overview/vol/radar/scénarios existent) | P1 |
| Opportunités : limiter le rendu (pas 500 points par défaut) | radar limité mais univers table longue | P1 |
| Marchés Breadth / Volatilité : encore légers | partiels | P2 |
| Cross-asset (BTC/pétrole/or/DXY) : diagnostic si absent | KPIs présents, diagnostic partiel | P2 |
| Analyse : graphique dominant plus grand + presets overlays | chart présent, presets à enrichir | P2 |
| Performance : parcours progressif (états) | à renforcer | P2 |
| Intelligence : convergence/sankey/decision waterfall | flow + radar faits, reste sankey | P2 |
| Container large (utilisation de la largeur) | grille 12 col OK, max-width à revoir | P3 |

## Garde-fous (non négociables)
- READONLY intact, aucun bouton/route d'ordre.
- Aucune donnée fictive : absence → état vide premium (jamais 0/n/d silencieux masqué).
- Projections = conditionnelles/distributions (jamais « prix futur certain »).
- Pas de bleu/cyan dominant. SW bumpé à chaque changement de static.
- Chaque page vérifiée navigateur (0 erreur console) + commit isolé.

## Méthode de vérification
Pages de scan → vérifiées directement sur instance sans verrou. Pages à données perso
(positions/journal/options live) → prouvées par **injection de données de test** + états
vides honnêtes ; validation finale sur données réelles **quand l'utilisateur est connecté**.

---
*Baseline vivante — mise à jour au fil des lots. Ce programme (47 phases) est multi-sessions.*
