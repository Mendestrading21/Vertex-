---
name: vertex-redesign-performance
description: Planifier puis exécuter la refonte Black Glass de toutes les vues Performance Vertex.
argument-hint: "[overview | journal | track-record | learnings | tout]"
disable-model-invocation: true
---

# Refonte Performance

Lire `CLAUDE.md`, le plan directeur et les contrats `docs/claude/`.

Demande :

> $ARGUMENTS

## Cible

- route : `/performance`
- fichier : `vertex/ui/pages/performance_page.py`
- vues : overview, journal, track-record, learnings.

## Mission

Mesurer la méthode sans fabriquer de track record et sans mélanger signaux théoriques et trades réels déclarés.

## Points obligatoires

- vérifier `VXEntities`/journal et `/api/track-record` ;
- préserver le parcours progressif avant le minimum de trades ;
- overview : KPI, equity, benchmark, drawdown, rendement mensuel et distribution ;
- journal : table, filtres ticker/setup/régime/date, édition et erreurs ;
- track-record : séparation visuelle absolue théorie/réel ;
- learnings : leçons, erreurs récurrentes, setups, régime et règles proposées ;
- equity argent, benchmark gris, drawdown rouge sous zéro ;
- ne pas présenter la courbe fantôme comme une performance réelle.

## Validation

0/1/5/20+ trades, gains/pertes, profit factor infini, données incomplètes, responsive, clavier, console, tests et commit isolé.
