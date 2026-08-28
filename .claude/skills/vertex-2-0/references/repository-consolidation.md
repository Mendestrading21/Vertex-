# Consolidation et nettoyage du dépôt

## Objectif

Une seule autorité active, un propriétaire par capacité et aucun vestige qui
continue à influencer Claude ou le runtime. Nettoyer progressivement, sans
confondre ancien, dupliqué et mort.

## Ordre

1. Inventorier.
2. Classer : actif, compatibilité, donnée, preuve historique, généré, mort.
3. Choisir le propriétaire canonique.
4. Migrer tous les consommateurs et les données.
5. Ajouter tests de non-réapparition.
6. Prouver parité et rollback.
7. Retirer dans une PR dédiée.

## Skills et gouvernance

Le seul dossier actif est `.claude/skills/vertex-2-0`. Supprimer anciens
skills, aliases, orchestrateurs de page et agents qui recréent une doctrine
concurrente seulement après intégration de leurs règles encore utiles. Root
`CLAUDE.md`, règles étroites et skill maître doivent se référencer sans cycle.

Les documents historiques peuvent rester comme preuves s'ils portent un
bandeau explicite et ne sont pas routés comme sources actives. Éviter de les
réécrire pour leur donner l'apparence d'une vérité actuelle.

## Code

- propriétaires de routes et blueprints ;
- navigation et shell ;
- moteurs legacy/canoniques ;
- wrappers de sources ;
- stores et schémas ;
- CSS/tokens/composants ;
- chart core et vendors ;
- scripts, tests, fixtures et assets.

Pour chaque retrait, rechercher imports statiques/dynamiques, chaînes,
enregistrement Flask, CLI, tests, docs, service worker, localStorage, données
persistées et usages navigateur. Une absence dans `rg` ne suffit pas si le
chargement est dynamique.

## Branches et PR

Ne jamais supprimer en masse les branches distantes dans le même chantier que
le runtime. Produire un inventaire : PR ouverte, branche protégée, ancêtre,
commits non fusionnés, archive utile, propriétaire et décision. La suppression
de branches est un acte distinct avec liste explicite et validation humaine.

## Critères de retrait

- aucun consommateur actif ;
- fonctionnalité couverte par le propriétaire canonique ;
- tests et captures de parité ;
- migration des données terminée ;
- documentation et imports mis à jour ;
- rollback connu ;
- diff limité et revue humaine.
