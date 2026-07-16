---
name: vertex-redesign-analysis
description: Planifier puis exécuter la refonte Black Glass de l’index Analyse et de la fiche canonique Vertex.
argument-hint: "[index | fiche | graphique | rail | tout]"
disable-model-invocation: true
---

# Refonte Analyse

Lire `CLAUDE.md`, le plan directeur et les contrats `docs/claude/`.

Demande :

> $ARGUMENTS

## Cible

- route : `/analysis` et fiche ticker canonique ;
- fichier : `vertex/ui/pages/analysis_page.py`.

## Mission

Conserver l’ordre métier et mettre le graphique dominant, la décision, la thèse, les dimensions, les scénarios et le plan au centre d’une fiche plus claire.

## Ordre cible

1. hero décisionnel ;
2. chandeliers dominant ;
3. rail décision/plan/risques ;
4. thèse ;
5. scorecard ;
6. fondamental ;
7. catalyseurs ;
8. technique ;
9. sentiment ;
10. anomalies/TradingView ;
11. scénarios ;
12. options ;
13. compatibilité portefeuille ;
14. historique.

## Points obligatoires

- préserver `/api/names`, récents et favoris ;
- conserver Lightweight Charts, volume, MM et niveaux du plan ;
- conserver le fallback Chart.js ;
- éviter la duplication de décision entre hero et rail ;
- navigation ancrée et sections longues repliables ;
- séparer clairement verdict déterministe et texte IA ;
- scénario conditionnel, jamais prix futur certain ;
- aucun recalcul financier dans l’UI.

## Validation

Ticker valide/invalide, données complètes/partielles, TradingView absent, options absentes, responsive, sticky rail, clavier, console, tests et commit isolé.
