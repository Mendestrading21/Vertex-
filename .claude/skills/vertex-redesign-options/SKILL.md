---
name: vertex-redesign-options
description: Planifier puis exécuter la refonte Black Glass de tout l’espace Options Intelligence Vertex.
argument-hint: "[overview | volatility | radar | scenarios | events | tout]"
disable-model-invocation: true
---

# Refonte Options

Lire `CLAUDE.md`, le plan directeur et les contrats `docs/claude/`.

Demande :

> $ARGUMENTS

## Cible

- route : `/options`
- fichier : `vertex/ui/pages/options_intel_page.py`
- vues : overview, volatility, radar, scenarios, events.

## Mission

Construire un desk options professionnel centré sur convexité, volatilité, liquidité, événements et risque, toujours en lecture seule.

## Correction préalable

Corriger la documentation obsolète : Options est déjà un espace principal du shell.

## Points obligatoires

- cartographier `/api/options/*` et les contrats réels ;
- vérifier prime, multiplicateur, spot, DTE, IV et OI ;
- overview : environnement, CALL/PUT, qualité, liquidité, IV, événement, meilleurs contrats ;
- volatility : term structure, smile/skew, OI par strike et lecture moteur ;
- radar : filtres DTE/type/liquidité/score, conviction et drawer ;
- scenarios : heatmap spot×temps, theta, IV sensitivity, payoff et stratégies multi-jambes ;
- afficher PoP, max gain/perte, breakevens, Delta/Gamma/Theta/Vega/Vanna/Vomma si disponibles ;
- events : earnings, expected move, gap risk et timeline ;
- réduire le violet et distinguer CALL/PUT par label, forme et motif.

## Validation

Aucun chemin d’ordre, refus honnête des données manquantes, cas live/delayed/partial, responsive, console, tests math/UI et commit isolé.
