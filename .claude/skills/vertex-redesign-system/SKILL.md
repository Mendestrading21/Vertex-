---
name: vertex-redesign-system
description: Planifier puis exécuter la refonte Black Glass de l’espace Système dans Vertex.
argument-hint: "[plan seulement | exécuter | lot précis]"
disable-model-invocation: true
---

# Refonte Système


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

- route : `/system`
- fichier principal : `vertex/ui/pages/system_page.py`

## Mission

Refondre connections, data, automations, settings et archive comme command center honnête de santé, fraîcheur, configuration et stockage.

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

- READONLY
- IBKR status
- TradingView
- Claude
- sync
- storage
- freshness
- jobs
- service worker
- design-system

## Condition de sortie

La page doit conserver toutes ses fonctions, rendre les décisions plus rapides, utiliser le même système de verre gris et respecter strictement vert/rouge/orange.
