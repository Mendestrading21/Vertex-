# Centre Portefeuille et Risque

Contrat de présentation uniquement : afficher et composer les capacités existantes ; ne pas créer les données, moteurs, calculs, états ou persistance décrits.

## Mission

Répondre à : **que possède le portefeuille, pourquoi, avec quelles expositions, quels risques, quelles échéances de revue et quel impact d'une nouvelle idée ?**

## Synthèse

Valeur, cash, exposition nette/brute, P&L selon disponibilité, allocation, concentration, liquidité, risque options, fraîcheur et réconciliation IBKR. Principaux contributeurs/détracteurs, alertes et thèses à revoir.

## Positions

Table configurable : instrument, type, quantité, coût, mark/source, valeur, poids, P&L, rôle, thèse, score, risque, invalidation, cible si canonique, prochaine revue et fraîcheur. Drawer : graphique, thèse, scénarios, catalyseurs, historique, portefeuille et journal.

## Allocation et expositions

Actif, secteur, devise, pays, thème, facteur et rôle. Fournir look-through ETF seulement avec holdings point-in-time. Montrer concentration et overlap avant d'ajouter une nouvelle idée.

## Risque

HHI, top positions, bêta, corrélations, diversification, drawdown, stress tests, calendrier d'événements, liquidité et Greeks agrégés. Les limites et breaches viennent d'une règle réelle, jamais du design.

## Watchlist et thèses

Chaque élément conserve pourquoi maintenant, catalyseur, invalidation, horizon, priorité, prochaine revue, événements, changement et historique. États de workflow : à étudier, surveillée, prête selon moteur, en attente, invalidée, archivée.

## Simulation d'impact

Avant de suivre une idée, présenter son impact théorique sur poids, concentration, secteur, devise, corrélation et risque, à partir d'hypothèses explicitement saisies ou calculées par moteur. Ce n'est ni un sizing canonique ni une préparation d'ordre.

Le lien `Tester dans le Simulateur` transmet seulement le contexte visuel disponible à `/simulator`. Comparer situation actuelle, scénario A/B/C et impact portefeuille avec la même base de données. Ne jamais enregistrer la simulation si aucun store canonique n'existe déjà.

Widgets prioritaires : trajectoire valeur/benchmark, equity + drawdown alignés, treemap d'allocation, barres de contribution, heatmap de corrélation, matrice d'exposition, calendrier des positions, concentration et table détaillée avec drawer. Un donut reste secondaire et limité à cinq catégories + Autres.
