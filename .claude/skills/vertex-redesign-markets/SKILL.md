---
name: vertex-redesign-markets
description: Planifier puis exécuter la refonte Black Glass de toutes les vues Marchés Vertex.
argument-hint: "[overview | macro | sectors | breadth | volatility | tout]"
disable-model-invocation: true
---

# Refonte Marchés

Lire `CLAUDE.md`, le plan directeur et les contrats `docs/claude/`.

Demande :

> $ARGUMENTS

## Cible

- route : `/markets`
- fichier : `vertex/ui/pages/markets_page.py`
- vues : overview, macro, sectors, breadth, volatility.

## Mission

Harmoniser tout l’espace avec le même verre gris, la même hiérarchie et le même thème graphique, en supprimant les visualisations redondantes sans perdre de données.

## Points obligatoires

- cartographier `/scan`, `/api/market/regime`, `/api/market/summary`, `/cal-feed` ;
- conserver les limites honnêtes de l’univers breadth ;
- ne jamais colorer automatiquement hausse VIX/taux en vert ;
- overview : régime, leadership, risque, indices, S&P, multi-indices, top/flop ;
- macro : risk-on/off, VIX, MM50/MM200, courbe des taux, calendrier ;
- sectors : classement, heatmap, rotation et treemap avec interaction croisée ;
- breadth : participation, historique, distribution, internals et waterfall ;
- volatility : VIX, rail calme/stress et contexte, sans inventer de term structure.

## Exécution

Une sous-vue ou un lot cohérent par commit. Vérifier sources, unités, périodes, fraîcheur, états, fallback table, responsive, console, tests et service worker.
