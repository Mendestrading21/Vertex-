---
name: vertex-redesign-portfolio
description: Planifier puis exécuter la refonte Black Glass de tout le Portefeuille Vertex.
argument-hint: "[team | positions | options | risk | watchlist | tout]"
disable-model-invocation: true
---

# Refonte Portefeuille

Lire `CLAUDE.md`, le plan directeur et les contrats `docs/claude/`.

Demande :

> $ARGUMENTS

## Cible

- route : `/portfolio`
- fichier : `vertex/ui/pages/portfolio_page.py`
- vues : team, positions, options, risk, watchlist.

## Mission

Transformer la page en suivi institutionnel détaillé, sans confondre positions déclarées, marques IBKR et signaux théoriques.

## Garde-fous de données

- vérifier `/api/pos-quotes` ;
- `t.cost` est le coût total ;
- une marque option est par action avant multiplication ×100 ;
- P&L absent hors ligne plutôt qu’inventé ;
- préserver `myTrades`, desk sync et READONLY.

## Cible visuelle/fonctionnelle

- synthèse persistante : valeur, P&L, exposition, cash, concentration, risque, fraîcheur ;
- team : treemap, rôles, contributeurs, places ;
- positions : table détaillée, poids, entrée, stop, thèse, risque, filtres et drawer ;
- options : capital, CALL/PUT, échéances, payoff combiné, breakevens, max gain/perte, Greeks ;
- risk : HHI, secteurs, stress, bêta, drawdown, Greeks et alertes ;
- watchlist : priorité, thèse, déclencheur, invalidation et statut.

## Validation

Tester IBKR connecté/hors ligne, portefeuille vide, options partielles, responsive, console, tests et commit isolé.
