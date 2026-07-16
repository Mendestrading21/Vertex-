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

- routes et sous-vues ;
- shell, navigation, overlays et responsive ;
- CSS, tokens, styles inline et aliases legacy ;
- tous les graphiques et modules `VXCharts` ;
- endpoints, moteurs, schémas et fraîcheur ;
- localStorage, desk sync et données IBKR ;
- tests, service worker et PWA ;
- états réel, demo, stale, partial, empty et error ;
- accessibilité, clavier et performances.

## Livrable

Pour chaque espace :

- état actuel avec chemins et lignes ;
- contrats de données ;
- problèmes fonctionnels et visuels ;
- hiérarchie cible ;
- composants à conserver, fusionner, supprimer ou créer ;
- graphiques cibles ;
- interactions et filtres ;
- états ;
- risques ;
- critères d’acceptation ;
- fichiers probables ;
- ordre d’implémentation.

Signaler explicitement les incohérences de documentation et de palette. Attendre la validation avant toute exécution.
