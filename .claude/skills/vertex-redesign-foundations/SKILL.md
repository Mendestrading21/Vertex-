---
name: vertex-redesign-foundations
description: Implémenter les fondations Black Glass de Vertex : tokens, surfaces, shell, primitives et thème graphique, sans refaire les pages métier.
argument-hint: "[tokens seulement | shell | primitives | charts-core | tout le socle]"
disable-model-invocation: true
---

# Fondations Black Glass


Avant toute action, lire :

- `CLAUDE.md`
- `docs/VERTEX_GLASS_REDESIGN_MASTER_PLAN.md`
- `docs/claude/VERTEX_GLASS_VISUAL_CONTRACT.md`
- `docs/claude/VERTEX_CHART_CONTRACT.md`
- `docs/claude/VERTEX_REFACTOR_RULES.md`
- `docs/claude/VERTEX_PAGE_MATRIX.md`
- `docs/claude/VERTEX_ACCEPTANCE_CHECKLIST.md`

Respecter l’invariant READONLY et l’architecture Flask/Python/JS existante.


Demande :

> $ARGUMENTS

## Périmètre

- tokens ;
- documentation design ;
- surfaces verre ;
- shell ;
- navigation ;
- topbar ;
- drawers/modales ;
- buttons ;
- tabs ;
- forms ;
- tables ;
- states ;
- chart theme.

## Exclusions

- ne pas réorganiser les pages métier ;
- ne pas modifier les moteurs ;
- ne pas changer les contrats de données ;
- ne pas supprimer les compatibilités avant inventaire.

## Validation

- page Design System ;
- routes principales ;
- focus ;
- contrastes ;
- desktop/laptop/tablette ;
- tests palette ;
- tests UI ;
- service worker.
