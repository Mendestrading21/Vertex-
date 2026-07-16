---
name: vertex-redesign-tracking
description: Planifier puis exécuter la refonte Black Glass de l’espace Tracking et des suivis hypothétiques Vertex.
argument-hint: "[plan seulement | exécuter | lot précis]"
disable-model-invocation: true
---

# Refonte Tracking

Lire `CLAUDE.md`, le plan directeur et les contrats `docs/claude/`.

Demande :

> $ARGUMENTS

## Cible

- route : `/tracking`
- script principal connu : `vertex/static/vertex/js/pages/tracking.js`
- rechercher la route et la page associées avant modification.

## Mission

Harmoniser le suivi analytique hypothétique avec le Black Glass, sans jamais le confondre avec des positions ou performances réelles.

## Points obligatoires

- KPI suivis actifs/résolus ;
- performance de chaque idée vs SPY ;
- alpha, verdict initial, date et horizon ;
- barres signées vert/rouge, benchmark gris ;
- fraîcheur et statut ;
- détail, archive et empty states ;
- badge « hypothétique » orange ou neutre explicite ;
- aucun frais/dividende ou position réelle inventé.

## Validation

Aucun suivi, suivi actif, suivi résolu, benchmark absent, données stale, valeurs positives/négatives, responsive, console, tests et commit isolé.
