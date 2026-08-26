---
name: vertex-redesign-plan
description: Auditer tout Vertex en lecture seule et produire un plan précis de refonte Black Glass par page, composant, graphique, donnée et fichier.
argument-hint: "[image de référence, périmètre ou priorité]"
disable-model-invocation: true
context: fork
agent: Plan
disallowed-tools:
  - Write
  - Edit
  - MultiEdit
  - NotebookEdit
---

# Planification complète


Avant toute action, lire :

- `CLAUDE.md`
- `docs/VERTEX_GLASS_REDESIGN_MASTER_PLAN.md`
- `docs/claude/VERTEX_GLASS_VISUAL_CONTRACT.md`
- `docs/claude/VERTEX_CHART_CONTRACT.md`
- `docs/claude/VERTEX_REFACTOR_RULES.md`
- `docs/claude/VERTEX_PAGE_MATRIX.md`
- `docs/claude/VERTEX_ACCEPTANCE_CHECKLIST.md`

Respecter l’invariant READONLY et l’architecture Flask/Python/JS existante.


Contrainte :

> $ARGUMENTS

Ne modifier aucun fichier.

## Audit obligatoire

- routes ;
- pages ;
- sous-vues ;
- shell ;
- CSS ;
- tokens ;
- charts ;
- scripts ;
- endpoints ;
- localStorage ;
- sync ;
- tests ;
- service worker ;
- états réels/démo/stale/partial ;
- responsive ;
- accessibilité.

## Livrable

Pour chaque espace :

- état actuel ;
- fichiers ;
- données ;
- problèmes ;
- hiérarchie cible ;
- composants ;
- graphiques ;
- interactions ;
- états ;
- risques ;
- critères d’acceptation ;
- ordre d’implémentation.

Signaler explicitement les incohérences de documentation et de palette.
