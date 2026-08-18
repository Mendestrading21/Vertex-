# Vertex 1.0 — Politique de nettoyage

Le nettoyage vise à supprimer l'ambiguïté, pas l'historique utile.

## Fichiers

Un fichier legacy peut être supprimé seulement si :

1. ses consommateurs sont inventoriés ;
2. son remplacement canonique est en production ;
3. les tests de parité sont verts ;
4. aucun import, route, template, script ou documentation active ne le référence ;
5. le rollback est documenté.

## Branches

Chaque branche historique reçoit un statut `MERGED`, `SUPERSEDED`, `UNIQUE`, `BROKEN` ou `UNKNOWN`. `UNIQUE` et `UNKNOWN` ne sont jamais supprimées automatiquement.

## Documentation

Les documents historiques volumineux peuvent être déplacés vers une archive, mais les décisions actives restent exclusivement sous `docs/vertex-1.0/`.

## Design

Remplacer avant de supprimer. Une nouvelle couche visuelle doit réduire le nombre total de thèmes/styles actifs. Aucun empilement de CSS « temporaire » sans date de retrait.

## Agents et skills

Un seul skill orchestre le produit : `/vertex-1-0`. Les agents spécialisés sont des outils subordonnés et ne peuvent pas créer leur propre doctrine produit.
