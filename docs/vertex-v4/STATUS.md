# VERTEX V4 — STATUS

Branche d’intégration : `integration/vertex-v4-clean`

Référence : `docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md`

## Règles de suivi

- Un seul lot actif à la fois.
- Claude Code met ce fichier à jour après chaque audit, commit, capture et validation.
- Une case `Code terminé` ne signifie pas `Lot approuvé`.
- La fusion vers `main` est interdite sans accord explicite.

| Lot | Périmètre | Statut | Branche / commit | Tests | Captures | Revue visuelle | Notes |
|---:|---|---|---|---|---|---|---|
| 00 | Consolidation, baseline et inventaire | **Terminé — à valider** | `integration/vertex-v4-clean` | 981 passés, 2 ignorés | 24 références + manifeste | En attente utilisateur | 8 routes 200, `/markets` 302 attendu, health OK, client-log 0 |
| 01 | Tokens, palette, typo, profondeur | **Terminé — à valider** | `claude/v4-01-foundations` | 981 passés, 2 ignorés | 18 (3 viewports × 6 routes) | En attente utilisateur | Tokens `--vx-v4-*` (tokens.css) + pont `tokens-v4-bridge.css` chargé après glass.css ; SW `td-shell-v95` ; 0 erreur console ; overflow mobile portfolio/système = pré-existant (Lot 14) |
| 02 | Shell : sidebar, topbar, recherche, drawers, mobile nav | À faire | — | — | — | — | Préserver routes et comportements |
| 03 | Cartes, KPI, boutons, tabs, tables, filtres, états | À faire | — | — | — | — | Quatre niveaux de composants |
| 04 | Système commun de graphiques | À faire | — | — | — | — | Tooltip, légende, source, états communs |
| 05 | Briefing | À faire | — | — | — | — | Morning command center |
| 06 | Marchés | À faire | — | — | — | — | Une hiérarchie claire par sous-vue |
| 07 | Opportunités | À faire | — | — | — | — | Table premium + inspector |
| 08 | Portefeuille | À faire | — | — | — | — | Portfolio Command |
| 09 | Analyse | À faire | — | — | — | — | Graphique principal + rail décisionnel |
| 10 | Options | À faire | — | — | — | — | Workspace stratégie / payoff / Greeks |
| 11 | Performance | À faire | — | — | — | — | Equity dominante, théorique ≠ réel |
| 12 | Intelligence | À faire | — | — | — | — | Ask Vertex central |
| 13 | Système | À faire | — | — | — | — | Statuts calmes et lisibles |
| 14 | Suivis, responsive et mobile | À faire | — | — | — | — | 390 × 844 obligatoire |
| 15 | Nettoyage CSS legacy et styles inline | À faire | — | — | — | — | Retrait uniquement après migration prouvée |
| 16 | QA finale toutes pages | À faire | — | — | — | — | 0 overflow, 0 console, READONLY intact |
| 17 | PR finale vers `main` | Bloqué | — | — | — | — | Uniquement après accord explicite |

## Journal de décision

Ajouter ici les décisions validées qui modifient ou précisent la spécification.

| Date | Décision | Motif | Validé par |
|---|---|---|---|
| 2026-07-22 | Direction `Obsidian Prism` : fond noir froid, marque violet-magenta-corail, vert/rouge strictement sémantiques | Correspondre à la référence visuelle choisie et supprimer la confusion vert marque / vert gain | Utilisateur |
| 2026-07-22 | Base technique `glass-plus-charts-oz8jmh`, intégrée sur `integration/vertex-v4-clean` | Conserver les 159 commits et 88 garde-fous supplémentaires absents de `main` | Audit de consolidation |
| 2026-07-22 | General Sans + JetBrains Mono ; navigation cible à 9 espaces ; référence maître versionnée | Supprimer les contradictions de typo, navigation et référence | Consolidation V4 |
| 2026-07-22 | Lot 01 : identité runtime migrée via pont (tokens.css + `tokens-v4-bridge.css`) plutôt qu'en réécrivant glass.css | glass.css est chargé en dernier et redéfinit 64 tokens ; un pont chargé après lui applique Obsidian Prism sans reconstruire ni supprimer le legacy (retrait = Lot 15) | Claude Code |
| 2026-07-22 | Marque `--vx-v4-brand-1` = `#6e4aff` (et non `#6d4aff`) ; série bleue secondaire différée au Lot 04 | Respecter le garde-fou `test_no_blue_primary_theme` (scanne tokens.css) tout en gardant le violet prism | Claude Code |
