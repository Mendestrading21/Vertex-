---
name: vertex-redesign-intelligence
description: Planifier puis exécuter la refonte Black Glass de toutes les vues Intelligence Vertex.
argument-hint: "[analyst | committee | strategy | impacts | research | memory | tout]"
disable-model-invocation: true
---

# Refonte Intelligence

Lire `CLAUDE.md`, le plan directeur et les contrats `docs/claude/`.

Demande :

> $ARGUMENTS

## Cible

- route : `/intelligence`
- fichier : `vertex/ui/pages/intelligence_page.py`
- vues : analyst, committee, strategy, impacts, research, memory.

## Mission

Rendre immédiatement visible la frontière entre moteurs déterministes, IA explicative, mémoire utilisateur, recherche et confirmation humaine.

## Points obligatoires

- analyst : formulaire, verdict moteur, explication IA, scorecard, audit trail et provenance ;
- committee : convergence, répartition, matrice, filtres et désaccords ;
- strategy : constitution, hard gates, versions, options autorisées et confirmation ;
- impacts : flux, chaîne d’impact, confiance et distinction corrélation/causalité ;
- research : pipeline IDEA→APPROVED, OOS, PSR/DSR/PBO et statuts ;
- memory : thèses, notes, règles observed/proposed/confirmed, recherche et versioning ;
- l’IA explique mais ne décide jamais ;
- aucune règle n’est activée sans confirmation humaine.

## Validation

IA disponible/indisponible, ticker absent, sources partielles, comité vide, recherche vide, mémoire vide, responsive, console, tests et commit isolé.
