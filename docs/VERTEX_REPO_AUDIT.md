# VERTEX — Audit complet du dépôt (branches · worktrees · fichiers · positions)

> État au 2026-07-15. Audit **lecture seule** : aucune branche/commit/fichier modifié
> pendant l'inventaire. Objectif : savoir EXACTEMENT où est quoi avant de tout consolider.

## 1. Les DEUX lignées de code (le piège de fond)

| Lignée | C'est quoi | Fichiers-clés | Où |
|--------|-----------|---------------|-----|
| **ANCIENNE — monolithe** | Tout l'UI en chaînes Python dans `terminal.py` (~10 400 lignes), CSS/JS inline, palette orange+bleu+vert | `terminal.py` gros, **PAS** de `vertex/static/vertex/css/`, PAS de `vertex/ui/pages/` | `main` (`a0d4d23` « Add files via upload ») + branches monolithe |
| **NOUVELLE — modulaire** ✅ | « Vertex Master Redesign » : pages `vertex/ui/pages/*.py`, design system CSS `vertex/static/vertex/css/*.css`, ~30 modules JS de graphiques, shell, routes blueprint | `vertex/ui/pages/`, `vertex/static/vertex/css/` (15), `vertex/static/vertex/js/charts/` (30) | branches **MODULAR** ci-dessous |

⚠️ **`main` = ANCIENNE version.** La refonte visuelle n'a JAMAIS été mergée sur main. Les worktrees créés depuis `a0d4d23` tombent sur l'ancien monolithe.

## 2. Carte des branches (16 locales)

**MODULAR (nouvelle refonte visuelle) — les seules qui comptent pour le visuel :**

| Branche | Date | vs main | Rôle | GitHub ? |
|---------|------|:------:|------|:--------:|
| ⭐ **`integration/vertex-visual-merge`** | 07-15 | +132/-1 | **VERSION COMPLÈTE = la fusion.** Cockpit institutionnel **+** obsidian visual-rebuild. Superset de tout. | ❌ local |
| `feature/vertex-institutional-experience-overhaul` | 07-13 | +115/-1 | Input « cockpit institutionnel » de la fusion (17 commits derrière integration) | ❌ local |
| `claude/vertex-visual-rebuild-1ofi8r` | 07-15 | +90/-1 | Input « obsidian visual-rebuild » de la fusion | ✅ **sur GitHub** |
| `feature/vertex-visual-command-center` | 07-13 | +91/-1 | Ancienne piste visuelle (absorbée) | ❌ local |
| `vertex-strategy-os` | 07-13 | +76/-1 | Piste modulaire antérieure | ❌ local |

**MONOLITHE (ancienne version / obsolètes) :**

| Branche | Date | Note |
|---------|------|------|
| `main` | 07-14 | `a0d4d23` — ancienne version, HEAD par défaut du repo |
| `vertex-system-launch` | 07-09 | monolithe « production » d'avant refonte |
| `backup/vertex-local-20260707` · `cloud-integrated` · `claude/vertex-{analysis,extreme-refinement,final-design-brief,master-rebuild}` | 07-06→08 | vieilles pistes monolithe, obsolètes |
| `claude/vertex-modifications-bc6d39` · `vertex-version-checkout-2a289a` · `vertex-visual-rebuild-9b3698` | 07-14 | branches `a0d4d23` (worktrees techniques Claude) |

## 3. GitHub (origin `origin (Vertex-)`)

5 branches poussées : `main` (ancienne), **`claude/vertex-visual-rebuild-1ofi8r`** (un seul input modulaire), `claude/vertex-strategy-os-h17dso`, `claude/vertex-improvements-kybc4p`, `claude/vertex-system-launch-0bsizs`.

➡️ **La version complète `integration/vertex-visual-merge` n'est PAS sur GitHub.** GitHub est en retard : son `main` est l'ancien monolithe, et seule une moitié de la refonte (`…-1ofi8r`) y est.

## 4. Worktrees (4)

| Chemin | Pointe sur | État |
|--------|-----------|------|
| `IBKT-DASHBORD--main` (principal) | `feature/vertex-institutional-experience-overhaul` | WIP session préc. → **rangé en `git stash`** |
| `.claude/worktrees/vertex-modifications-bc6d39` | **`139f0fb` (HEAD détaché = integration)** | ⚠️ **détaché** ; contient l'**identité Signal Green appliquée (WIP non-committé)** |
| `.claude/worktrees/vertex-version-checkout-2a289a` | `a0d4d23` détaché | ancien monolithe (jetable) |
| `.claude/worktrees/vertex-visual-rebuild-9b3698` | `claude/vertex-visual-rebuild-9b3698` (`a0d4d23`) | worktree de MA session — ancien monolithe (travail initial perdu, jetable) |

## 5. Stashes / tags

- `stash@{0}` (sur feature) : `signal-green-session-wip 2026-07-15` — filet de sécurité, récupérable.
- Tags : `backup/institutional-preMerge`, `backup/visual-rebuild-preMerge` (sécurité avant fusion), `vertex-premium-2026-07-07` (archive).

## 6. Fichiers (version complète = integration) — 599 fichiers suivis

- `vertex/` **314** : `ui/` (25, dont `pages/`), `static/` (44 = 15 CSS + 30 JS charts), `engines/`, `options/`, `research/`, `app/` (routes blueprint), `ai/`, `strategy/`, `portfolio/`, `positions/`, `market/`, `visualization/` (registre palette), etc.
- `docs/` **~191 .md** · `tests/` **74** · `terminal.py` (entrée app, monte les blueprints) · lanceurs `.bat/.command`.
- **Données runtime gitignorées** (jamais commitées) : `.env`, `*_cache.json`, `desk_data.json`, `tracking.json`, `breadth_history.json`, `edge_ledger.jsonl`, `desk_backup_*.json`, `__pycache__/`, `.vertex_secret`, `docs/screenshots/`…

## 7. État du travail Signal Green (cette session)

Appliqué sur la **version complète** (worktree `vertex-modifications-bc6d39`) : identité VERTEX SIGNAL GREEN (tokens.css, palette.py, shell font-link Inter/IBM Plex Mono, 10 CSS + 5 JS remappés orange→signal, 2 tests palette mis à jour). **881 tests verts, 0 orange résiduel**, vérifié navigateur. **Non committé**, sur HEAD détaché.

## 8. Recommandations de consolidation (« mettre tout à jour avec ces positions »)

1. **Rattacher + committer** le Signal Green : dans le worktree `vertex-modifications-bc6d39`, `git checkout integration/vertex-visual-merge` (rattache la branche au HEAD détaché sans perdre les fichiers), puis committer → l'identité verte est enfin SUR la branche complète.
2. **Faire de `integration/vertex-visual-merge` la référence unique** (tout le monde bosse dessus). Optionnel : la renommer `feature/vertex-signal-terminal`.
3. **Pousser sur GitHub** la version complète (nouvelle branche origin) — aujourd'hui GitHub est en retard.
4. **Promouvoir sur `main`** — SEULEMENT avec ton accord explicite (règle CLAUDE.md).
5. **Nettoyer** : supprimer les branches monolithe obsolètes (07-06/08) + les worktrees jetables `vertex-version-checkout-2a289a` et `vertex-visual-rebuild-9b3698` + `git stash drop` une fois le Signal Green committé.

> Aucune de ces actions n'est faite : cet audit ne fait que cartographier. Les
> opérations git destructives (promotion main, suppression de branches, push)
> attendent ton feu vert.
