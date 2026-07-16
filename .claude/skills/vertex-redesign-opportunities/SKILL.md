---
name: vertex-redesign-opportunities
description: Planifier puis exécuter la refonte Black Glass de toutes les vues Opportunités Vertex.
argument-hint: "[radar | stocks | options | anomalies | calendar | tout]"
disable-model-invocation: true
---

# Refonte Opportunités

Lire `CLAUDE.md`, le plan directeur et les contrats `docs/claude/`.

Demande :

> $ARGUMENTS

## Cible

- route : `/opportunities`
- fichier : `vertex/ui/pages/opportunities_page.py`
- vues : radar, stocks, options, anomalies, calendar.

## Mission

Créer un espace de sélection rapide et crédible : classement, entonnoir, qualité × timing, conviction, filtres, tables scannables et détail contextuel.

## Points obligatoires

- vérifier `/scan`, `/api/opportunities/funnel`, scores, verdicts et qualité des données ;
- limiter le nombre d’éléments rendus par défaut ;
- sélection active neutre argentée, jamais verte ;
- vert = favorable, rouge = éviter, orange = surveiller/incertain ;
- radar : top cards, funnel, scatter et sous-scores ;
- stocks : table configurable, score, verdict, R:R, secteur, fraîcheur, sparkline ;
- options : qualité, DTE, IV, prime, liquidité, événement et lien vers `/options` ;
- anomalies : type, intensité, récence, source et impact ;
- calendar : événements/earnings, proximité positions/watchlist.

## Validation

Aucune action broker, aucun score recalculé dans l’UI, drawer accessible, états complets, responsive, tests, console et commit isolé.
