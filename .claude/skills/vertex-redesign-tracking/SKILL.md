---
name: vertex-redesign-tracking
description: Planifier puis exécuter la refonte Black Glass de l’espace Tracking dans Vertex.
argument-hint: "[plan seulement | exécuter | lot précis]"
disable-model-invocation: true
---

# Refonte Tracking


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

## Route et fichier

- route : `/tracking`
- fichier principal : `vertex/static/vertex/js/pages/tracking.js et route/page associée`

## Mission

Harmoniser le suivi hypothétique des idées, la comparaison SPY, les statuts et les détails, sans confusion avec des positions réelles.

## Procédure

1. Lire entièrement le fichier principal et ses imports/scripts.
2. Inventorier les endpoints et contrats de données.
3. Capturer l’état actuel.
4. Écrire le mini-plan de la page.
5. Vérifier que les fondations Black Glass sont déjà en place.
6. Implémenter sans recalculer les données dans l’UI.
7. Uniformiser chaque graphique avec le contrat global.
8. Tester tous les états.
9. Vérifier navigateur, console, responsive et clavier.
10. Lancer les tests.
11. Bumper le service worker si le shell statique change.
12. Commit isolé.

## Points de contrôle

- hypothétique
- benchmark SPY
- rendements
- freshness
- archive
- états vides

## Condition de sortie

La page doit conserver toutes ses fonctions, rendre les décisions plus rapides, utiliser le même système de verre gris et respecter strictement vert/rouge/orange.
