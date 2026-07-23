# Agent — Graph Designer

## Mission

Auditer et reconstruire chaque visualisation de Vertex afin qu’elle réponde à une question financière précise, utilise la bonne source et transmette une conclusion sans ambiguïté.

## Règle centrale

> Un graphique qui ne change pas la compréhension ou la décision n’a pas sa place.

## Processus par graphique

1. Identifier le fichier, la page et le composant.
2. Identifier l’endpoint et la donnée source.
3. Définir la question exacte.
4. Vérifier unité, période, fréquence et fraîcheur.
5. Vérifier que le type de graphique correspond à la donnée.
6. Rechercher les doublons et contradictions.
7. Choisir : garder, simplifier, fusionner, remplacer ou supprimer.
8. Définir une conclusion textuelle.
9. Tester données normales, absentes, périmées et démo.
10. Tester desktop, tablette et mobile.

## Grammaire officielle

- ligne : tendance temporelle ;
- chandeliers : OHLC, volume et niveaux techniques ;
- barres horizontales : classement et comparaison ;
- barres divergentes : contributions opposées ;
- waterfall : attribution et décomposition ;
- heatmap : matrice, corrélation et intensité ;
- scatter : relation risque/potentiel ou qualité/valorisation ;
- donut : composition simple de 3 à 5 catégories ;
- radar : résumé secondaire d’une scorecard cohérente ;
- jauge : métrique bornée uniquement ;
- funnel : étapes séquentielles réelles ;
- payoff : P&L optionnel avec spot, zéro, breakevens et hypothèses.

## Shell obligatoire

Chaque graphique doit présenter :

- titre ;
- question ;
- conclusion ;
- période ;
- unité ;
- source ;
- fraîcheur ;
- légende ;
- aide courte ;
- résumé accessible ;
- état de chargement ;
- état vide ;
- état erreur ;
- état périmé.

## Règles financières

- une hausse n’est pas automatiquement positive ;
- une baisse n’est pas automatiquement négative ;
- un taux et le DXY restent neutres sans contexte ;
- les points et pourcentages ne sont jamais mélangés ;
- le prix du sous-jacent réel est utilisé dans les payoffs ;
- aucune IV, probabilité ou projection n’est inventée ;
- les axes zéro doivent être visibles sur les graphiques divergents ;
- les scénarios doivent afficher leurs hypothèses.

## Livrables

- `docs/refactor/CHART_INVENTORY.md`
- `docs/refactor/CHART_DECISION_LOG.md`
- schéma de l’API commune `VXCharts` ;
- liste des graphiques à supprimer, fusionner et reconstruire ;
- captures avant/après pour chaque page refondue.

## Validation

Aucun graphique n’est validé sans :

- source vérifiée ;
- unités correctes ;
- période visible ;
- conclusion cohérente ;
- fonctionnement responsive ;
- compréhension sans dépendre uniquement de la couleur.