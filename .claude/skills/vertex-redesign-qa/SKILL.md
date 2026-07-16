---
name: vertex-redesign-qa
description: Auditer et valider une branche de refonte Vertex contre le plan Black Glass, les invariants métier, les tests et la cohérence graphique.
argument-hint: "[branche, phase ou page]"
disable-model-invocation: true
---

# QA Black Glass


Avant toute action, lire :

- `CLAUDE.md`
- `docs/VERTEX_GLASS_REDESIGN_MASTER_PLAN.md`
- `docs/claude/VERTEX_GLASS_VISUAL_CONTRACT.md`
- `docs/claude/VERTEX_CHART_CONTRACT.md`
- `docs/claude/VERTEX_REFACTOR_RULES.md`
- `docs/claude/VERTEX_PAGE_MATRIX.md`
- `docs/claude/VERTEX_ACCEPTANCE_CHECKLIST.md`

Respecter l’invariant READONLY et l’architecture Flask/Python/JS existante.


Cible :

> $ARGUMENTS

## Audit

- diff Git ;
- fichiers touchés ;
- invariants READONLY ;
- données réelles ;
- palette ;
- tokens ;
- surfaces ;
- cohérence des graphiques ;
- responsive ;
- accessibilité ;
- erreurs console ;
- tests ;
- service worker ;
- documentation.

## Sortie

Classer chaque constat :

- bloquant ;
- majeur ;
- mineur ;
- polish.

Ne corriger automatiquement que si l’utilisateur demande explicitement l’exécution. Sinon produire un rapport avec fichiers et lignes.
