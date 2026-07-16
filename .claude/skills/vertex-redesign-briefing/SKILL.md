---
name: vertex-redesign-briefing
description: Planifier puis exécuter la refonte Black Glass du Briefing/Dashboard Vertex.
argument-hint: "[plan seulement | exécuter | lot précis]"
disable-model-invocation: true
---

# Refonte Briefing / Dashboard

Lire `CLAUDE.md`, `docs/VERTEX_GLASS_REDESIGN_MASTER_PLAN.md` et tous les contrats `docs/claude/`.

Demande :

> $ARGUMENTS

## Cible

- route : `/`
- fichier principal : `vertex/ui/pages/briefing.py`
- question : « Que dois-je comprendre et surveiller aujourd’hui ? »

## Mission

Recomposer la première hauteur d’écran dans le style de la référence : fond noir, cartes en verre gris transparent, cinq KPI marché, régime, opportunités actives, portefeuille, options et performance. Organiser Brief, Pouls, breadth, top/flop, rotation, alertes et calendrier en second niveau.

## Procédure

1. Lire la page entière et tous ses scripts/charts.
2. Cartographier `/scan`, `scan_state`, calendrier, desk et sources du brief.
3. Capturer l’état actuel et écrire le mini-plan.
4. Préserver `vxDashboardLayout` et les clés de personnalisation.
5. Implémenter avec les primitives Black Glass existantes.
6. Uniformiser sparklines, jauges, portefeuille, options flow et performance.
7. Vérifier réel/demo/stale/partial/empty/error.
8. Vérifier 1440×900, laptop, tablette et clavier.
9. Tests, console, service worker et commit isolé.

## Condition de sortie

La décision principale est visible sans scroll en mode Confort, toutes les données restent réelles et toutes les fonctions existantes sont préservées.
