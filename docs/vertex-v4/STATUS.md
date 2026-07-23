# VERTEX V4 — STATUS

Branche d’intégration : `integration/vertex-v4-clean`

Référence : `docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md`

## Règles de suivi

- Un seul lot actif à la fois.
- Claude Code met ce fichier à jour après chaque audit, commit, capture et validation.
- Une case `Code terminé` ne signifie pas `Lot approuvé`.
- La fusion vers `main` est interdite sans accord explicite.

> **✅ FUSIONNÉ DANS `integration/vertex-v4-clean` (2026-07-22, commit `cf60597`).**
> Sur autorisation utilisateur (« Fusionne »), les lots **01, 02, 03, 04, QA
> conformité, 06 (Marchés + enrichissements)** et **10 (partiel : carte Activité
> Options)** sont consolidés dans l'intégration. Les PR #6→#12 sont fermées
> (leurs commits sont dans l'intégration). `main` n'est PAS touchée (D-010).
> Les lignes ci-dessous conservent le détail par lot ; « Statut » = état au
> moment du lot. Reste ouvert : 05, 07, 08, 09, 10 (workspace complet), 11-17.

| Lot | Périmètre | Statut | Branche / commit | Tests | Captures | Revue visuelle | Notes |
|---:|---|---|---|---|---|---|---|
| 00 | Consolidation, baseline et inventaire | **Terminé — à valider** | `integration/vertex-v4-clean` | 981 passés, 2 ignorés | 24 références + manifeste | En attente utilisateur | 8 routes 200, `/markets` 302 attendu, health OK, client-log 0 |
| 01 | Tokens, palette, typo, profondeur | **Validé (visuel utilisateur)** | `claude/v4-01-foundations` · PR #6 | 981 passés, 2 ignorés | 18 (3 viewports × 6 routes) | ✅ Utilisateur (Go) | Tokens `--vx-v4-*` (tokens.css) + pont `tokens-v4-bridge.css` chargé après glass.css ; SW `td-shell-v95` ; 0 erreur console ; overflow mobile portfolio/système = pré-existant (Lot 14) |
| 02 | Shell : sidebar, topbar, recherche, drawers, mobile nav | **Validé (visuel utilisateur)** | `claude/v4-02-shell` (empilé sur Lot 01) | 981 passés, 2 ignorés | 18 (3 viewports × 6 routes) | En attente utilisateur | `shell.css` chargé en dernier : sidebar 180px, topbar 58px glass, logo + item actif violet prism, focus recherche violet, nav mobile violette ; routes/comportements/nav (8) inchangés ; SW `td-shell-v96` ; 0 erreur console ; overflow mobile portfolio/système = pré-existant (Lot 14) |
| 03 | Cartes, KPI, boutons, tabs, tables, filtres, états | **Validé (visuel utilisateur)** | `claude/v4-03-components` (empilé sur Lot 02) | 981 passés, 2 ignorés | 18 (3 viewports × 6 routes) | En attente utilisateur | `components-v4.css` chargé en dernier : sélection violet prism (carte active, onglet, chip, segmented), accent hero prism, rayons de contrôle V4 ; sémantique pos/neg/warn des tuiles inchangée ; SW `td-shell-v97` ; 0 erreur console ; overflow mobile portfolio/système pré-existant (Lot 14) |
| 04 | Système commun de graphiques | **Terminé — à valider** | `claude/v4-04-charts` (empilé sur Lot 03) | 981 passés, 2 ignorés | captures pages graphiques | En attente utilisateur | Thème JS + registre `palette.py` migrés en Obsidian Prism : série principale violet prism, magenta/teal/ambre secondaires, benchmark gris, tooltip verre V4 ; single-series déjà violet via pont ; **série bleue secondaire différée** (nécessite d'assouplir les gardiens zéro-bleu — accord utilisateur requis) ; pas de bump SW (contenu JS/py) ; 0 erreur console |
| 05 | Briefing | À faire | — | — | — | — | Morning command center |
| 06 | Marchés | **Terminé — à valider** | `claude/v4-06-markets` (empilé sur QA) | 981 passés, 2 ignorés | markets 3 viewports | En attente utilisateur | 9e espace explicite (`markets_page.py`) : `/markets` sert une vraie page (fini le 302) réutilisant /scan + /api/market/summary + /api/market/regime — hero climat, indices, chart S&P dominant (violet prism), volatilité/régime, secteurs, participation ; 5 sous-vues ?view= ; nav 8→9 (tests MAJ) ; SW `td-shell-v98` ; 0 erreur console ; 0 overflow 3 viewports ; AUCUN nouveau moteur/donnée |
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
| 2026-07-22 | Fusion des lots 01-04 + QA + 06 + 10(partiel) dans `integration/vertex-v4-clean` (`cf60597`) ; PR #6-#12 fermées ; `main` intacte | Consolider le V4 livré sur autorisation utilisateur (« Fusionne ») ; retarget PR refusé (diff vide) → fermeture | Utilisateur |
| 2026-07-22 | Marchés · vue Volatilité enrichie des implications du régime (adjustments `/api/market/regime`) | Rendre les sous-vues substantives avec données réelles déjà servies, sans nouveau moteur | Claude Code |
