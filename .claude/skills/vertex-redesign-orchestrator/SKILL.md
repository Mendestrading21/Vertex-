---
name: vertex-redesign-orchestrator
description: Orchestrer la refonte complète Black Glass de Vertex, depuis l’audit jusqu’à la QA, par phases validées et commits isolés.
argument-hint: "[phase, priorité ou contrainte]"
disable-model-invocation: true
---

# Orchestrateur global Vertex

Avant toute action, lire :

- `CLAUDE.md`
- `docs/VERTEX_GLASS_REDESIGN_MASTER_PLAN.md`
- `docs/claude/VERTEX_GLASS_VISUAL_CONTRACT.md`
- `docs/claude/VERTEX_CHART_CONTRACT.md`
- `docs/claude/VERTEX_REFACTOR_RULES.md`
- `docs/claude/VERTEX_PAGE_MATRIX.md`
- `docs/claude/VERTEX_ACCEPTANCE_CHECKLIST.md`

Contrainte utilisateur :

> $ARGUMENTS

## Mission

Piloter le chantier complet sans modification monolithique.

## Procédure

1. Vérifier branche, HEAD, worktrees, stashes et état Git.
2. Vérifier que la branche est basée sur la version modulaire réellement utilisée.
3. Capturer la baseline de toutes les pages.
4. Afficher le plan et les fichiers de la phase.
5. Obtenir la validation avant une phase destructive si elle n’est pas déjà explicite.
6. Exécuter une seule phase cohérente.
7. Lancer tests ciblés puis suite complète.
8. Vérifier navigateur, console, responsive et états de données.
9. Bumper le service worker si nécessaire.
10. Faire un commit isolé et documenter le rollback.
11. Résumer avant la phase suivante.

## Ordre

0. baseline
1. source de vérité design
2. shell
3. primitives
4. charts core
5. briefing
6. marchés
7. opportunités
8. portefeuille
9. analyse
10. options
11. performance
12. intelligence
13. système
14. tracking et routes secondaires
15. responsive/a11y
16. QA/release

## Garde-fous

- ne jamais toucher aux moteurs pour faciliter un visuel sans justification ;
- ne jamais inventer une donnée ;
- ne jamais pousser sur `main` sans accord ;
- ne jamais regrouper plusieurs pages majeures dans un commit ;
- ne jamais déclarer une phase terminée sans preuves ;
- préserver `READONLY=True`, la sync desk et les données personnelles.
