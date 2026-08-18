# Gouvernance Git — Vertex 1.0

## Branches actives

- `main`: seule ligne de release;
- `agent/vertex-1-0-<sujet>`: travail courant;
- aucune nouvelle branche d'intégration permanente.

## Branches historiques

Les branches `agent/skyler-v2-lot-*`, anciennes intégrations, V4, Total
Rebuild, Neon Glass et Signal OS ne servent jamais de base. Elles restent
temporairement consultables jusqu'à l'inventaire de leurs capacités uniques.

## PR

- une PR cohérente, pas une PR par micro-lot;
- base `main`;
- brouillon pendant le développement;
- preuves CI, risques et rollback obligatoires;
- aucune fusion automatique;
- pas de fusion d'une branche fortement divergente sans extraction sélective.

## Nettoyage

Le nettoyage des centaines de branches et anciennes PR est une action
distincte:

1. exporter l'inventaire;
2. associer chaque branche à un commit/PR/capacité;
3. marquer `MERGED`, `SUPERSEDED`, `UNIQUE` ou `UNKNOWN`;
4. récupérer les actifs uniques;
5. créer un tag/archive si nécessaire;
6. supprimer uniquement après validation humaine.

## Protection recommandée de `main`

- PR obligatoire;
- CI `test` et `safety` obligatoires;
- branche à jour avant fusion;
- conversations résolues;
- force push et suppression interdits;
- au moins une validation humaine.
