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

Respecter l’invariant READONLY et l’architecture Flask/Python/JS existante.


Contrainte utilisateur :

> $ARGUMENTS

## Mission

Piloter le chantier complet sans le transformer en modification monolithique.

## Procédure

1. Vérifier branche, état Git et HEAD.
2. Produire ou actualiser le plan de la phase.
3. Afficher les fichiers qui seront touchés.
4. Attendre validation avant la première phase destructive si l’utilisateur ne l’a pas déjà donnée.
5. Exécuter une seule phase cohérente.
6. Lancer tests ciblés puis suite complète.
7. Vérifier le navigateur et la console.
8. Bumper le service worker si nécessaire.
9. Faire un commit isolé.
10. Résumer avant de passer à la phase suivante.

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
- ne jamais pousser sur main sans accord ;
- ne jamais exécuter plusieurs pages majeures dans un seul commit ;
- ne jamais déclarer une phase terminée sans preuves.
