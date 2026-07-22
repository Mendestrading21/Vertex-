# VERTEX V4 — STATUS

Branche d’intégration : `redesign/vertex-v4-master`

Référence : `docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md`

## Règles de suivi

- Un seul lot actif à la fois.
- Claude Code met ce fichier à jour après chaque audit, commit, capture et validation.
- Une case `Code terminé` ne signifie pas `Lot approuvé`.
- La fusion vers `main` est interdite sans accord explicite.

| Lot | Périmètre | Statut | Branche / commit | Tests | Captures | Revue visuelle | Notes |
|---:|---|---|---|---|---|---|---|
| 00 | Baseline, inventaire des pages et captures actuelles | À faire | — | — | — | — | Ne rien modifier pendant l’inventaire |
| 01 | Tokens, palette, typo, profondeur | À faire | — | — | — | — | Supprimer le conflit Copper / Signal Green |
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
