---
name: vertex-redesign-briefing
description: Planifier puis exécuter la refonte Black Glass de l’espace Briefing / Dashboard dans Vertex.
argument-hint: "[plan seulement | exécuter | lot précis]"
disable-model-invocation: true
---

# Refonte Briefing / Dashboard


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

- route : `/`
- fichier principal : `vertex/ui/pages/briefing.py`

## Mission

Refondre la première hauteur d’écran autour de KPI marché, régime, opportunités, portefeuille, options et performance, puis organiser les blocs secondaires sous le fold.

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

- personnalisation vxDashboardLayout
- scan_state et sources du brief
- market strip
- opportunités
- portefeuille desk
- calendrier
- états demo/stale

## Condition de sortie

La page doit conserver toutes ses fonctions, rendre les décisions plus rapides, utiliser le même système de verre gris et respecter strictement vert/rouge/orange.
