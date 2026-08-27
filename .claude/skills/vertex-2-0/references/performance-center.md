# Centre Performance, Journal et Suivi

Contrat de présentation uniquement : afficher et composer les capacités existantes ; ne pas créer les données, métriques, calculs, états ou persistance décrits.

## Séparation des populations

Ne jamais fusionner dans un même KPI :

- trades réels déclarés ;
- positions IBKR ;
- signaux théoriques moteurs ;
- idées suivies hypothétiquement ;
- simulations options.

Chaque série possède type, source, période, benchmark, taille d'échantillon et limites.

## Performance

Equity curve, benchmark, drawdown, rendement par période, distribution, contribution, setup, régime, secteur et erreurs, seulement lorsque l'échantillon le permet. Avant le minimum, afficher progression et limites.

Le premier écran utilise un `PerformanceTearsheet` compact : rendement/benchmark, equity, drawdown synchronisé, taille d'échantillon et qualité. Les niveaux suivants proposent, si les données existent déjà, heatmap mensuelle, rolling metrics, distribution, contributions, séries de gains/pertes, MAE/MFE et découpe par setup/régime. Chaque graphique critique possède une table équivalente.

## Journal

Entrée/édition sûre, thèse, setup, décision, contexte, résultat, MAE/MFE si réels, erreurs déclarées, pièces et liens vers dossier/position. Préserver les clés desk sync et backups.

## Centre de suivi

Vue transversale : positions, options, opportunités surveillées, thèses à revoir, événements proches, données stale, décisions en retard et idées hypothétiques. Chaque ligne conserve son type et renvoie vers son propriétaire.

## Apprentissages

Détecter tendances et erreurs, mais classer les sorties comme observation ou proposition. Une nouvelle règle stratégique exige preuve, validation et confirmation humaine.

Les motifs QuantStats servent uniquement de référence visuelle et de nomenclature. Ne jamais importer un calcul ou recalculer Sharpe, Sortino, drawdown, Monte Carlo ou autre métrique dans la couche UI.
