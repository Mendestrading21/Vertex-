# Laboratoire de stratégies et validation financière

## Positionnement

Vertex compare des hypothèses et documente leur robustesse. Il ne découvre pas
une « meilleure stratégie » universelle, ne promet aucun rendement et ne
transforme aucun backtest en ordre. Le laboratoire est une sous-vue d'Analyse
et du Simulateur, pas une nouvelle navigation primaire tant qu'un usage réel ne
justifie pas sa promotion.

## Contrat `StrategySpec`

Toute stratégie testable conserve : identifiant/version, univers point-in-time,
classe d'actif, timeframe, signal d'entrée, sortie, invalidation, sizing
théorique, contraintes, benchmark, calendrier de décision, données requises,
coûts, slippage, hypothèses de liquidité, période d'entraînement, période de
validation, seed et propriétaire du moteur.

Les familles admises sont des catégories de recherche : tendance/momentum,
breakout, retour à la moyenne, force relative, événement/catalyseur,
factoriel/qualité, volatilité/options, carry autorisé par les données,
paires/relatif et couverture. Chaque famille entre séparément, avec une thèse
économique et des limites. Aucun catalogue n'est activé par défaut.

## Pipeline anti-illusion

1. Geler données, univers, calendrier et versions.
2. Valider schéma, unités, fuseaux, corporate actions et trous.
3. Construire le signal sans accès au futur.
4. Appliquer délais, coûts, spread, slippage et règles de liquidité.
5. Séparer développement, validation et test final chronologiquement.
6. Utiliser walk-forward ; purger/embargo les fenêtres qui se chevauchent.
7. Comparer au benchmark et à des baselines simples.
8. Mesurer sensibilité des paramètres, régimes et sous-périodes.
9. Tester stabilité par bootstrap/Monte Carlo uniquement avec méthode définie.
10. Corriger la multiplication des essais et conserver les essais rejetés.
11. Rejouer le résultat depuis un manifeste immuable.
12. Soumettre l'interprétation à validation humaine avant toute conclusion.

Interdire look-ahead, survivorship bias, univers actuel appliqué au passé,
réinvestissement implicite, remplissage au prix impossible, coûts nuls par
défaut, sélection du meilleur essai après observation et changement silencieux
des paramètres.

## Sortie `StrategyEvidence`

La sortie contient : population, période, benchmark, observations, trades
théoriques, exposition, turnover, coûts, rendement annualisé si pertinent,
volatilité, drawdown, ratio risque/rendement, taux de réussite, payoff,
distribution, tail risk, stabilité par régime, sensibilité des paramètres,
intervalle/incertitude, qualité des données, biais connus et statut
`EXPLORATOIRE`, `VALIDÉ_HORS_ÉCHANTILLON`, `DÉGRADÉ` ou `REJETÉ`.

Un ratio seul ne permet jamais de classer une stratégie. Afficher au minimum
rendement, drawdown, exposition, turnover, coûts, échantillon et stabilité.
Une probabilité ou un score de confiance exige calibration hors échantillon.

## Widgets du laboratoire

- `StrategyMatrix` : stratégies × robustesse, risque, coûts, régimes et statut.
- `EquityDrawdownPair` : equity et drawdown liés sur la même période.
- `RegimeBreakdown` : résultats par régime avec population visible.
- `ParameterStabilityMap` : surface de sensibilité, jamais « optimum » isolé.
- `WalkForwardTimeline` : fenêtres train/validation/test et purges visibles.
- `ReturnDistribution` : distribution, zéro, quantiles et tails.
- `TradeDiagnostics` : MFE/MAE, durée, coûts et séquences si le moteur existe.
- `FailureLedger` : essais rejetés, biais, données manquantes et changements.
- `StrategyCompareTray` : trois variantes maximum sur mêmes données et unités.

## Multi-actifs

- **Actions/ETF** : corporate actions, survivorship, volume, spread, benchmark,
  frais et look-through seulement si sourcé.
- **Options** : chaîne point-in-time, bid/ask, multiplicateur, exercice,
  assignation, IV/Greeks, expirations, liquidité et absence de données
  historiques explicitée. Ne jamais reconstruire une chaîne passée avec la
  chaîne actuelle.
- **Forex** : paire et sens, calendriers, rollover/swap uniquement si fourni,
  conversion, session et pip value canonique.
- **Portefeuille** : rebalancement, drift, turnover, contraintes, concentration
  et benchmark ; les positions utilisateur ne deviennent pas des données de
  backtest.

## Références GitHub qualifiées

Ces projets apportent des méthodes, jamais une adoption automatique :

| Projet | Apport possible | Décision Vertex |
|---|---|---|
| [skfolio](https://github.com/skfolio/skfolio) | optimisation, risque, walk-forward, validation purgée et stress | meilleur candidat d'étude pour validation portefeuille ; lot séparé, golden tests |
| [PyBroker](https://github.com/edtechre/pybroker) | backtests walk-forward, slippage, bootstrap et signaux | référence de contrat d'expérience ; ne pas remplacer les moteurs sans preuve |
| [vectorbt](https://github.com/polakowo/vectorbt) | exploration vectorisée de nombreuses variantes | sandbox de recherche seulement ; licence/version et risque d'overfit à auditer |
| [options_portfolio_backtester](https://github.com/lambdaclass/options_portfolio_backtester) | stratégies options, sweeps et couverture tail-risk | inspiration de scénarios ; valider couverture et données historiques |
| [QuantLib](https://github.com/lballabio/QuantLib) | pricing, Greeks et moteurs financiers testés | candidat de référence pour validation numérique, pas dépendance UI |
| [QuantStats](https://github.com/ranaroussi/quantstats) | métriques et tear sheets | formes et résultats croisés par golden tests |
| [QuantInvestStrats](https://github.com/ArturSepp/QuantInvestStrats) | performance, risque, backtesting et factsheets | référence pour attribution et présentation |

Avant adoption : licence, maintenance, version Python, dépendances, précision,
unités, performance, reproductibilité, couverture de tests, coût de retrait et
parité avec les moteurs Vertex. N'importer jamais un framework d'exécution
d'ordres pour obtenir son backtester.

## Tests financiers obligatoires

- golden cases documentés et double calcul indépendant ;
- invariants de dimension, signe, devise et multiplicateur ;
- propriété zéro variation → résultat nul hors coûts ;
- symétrie/monotonicité seulement lorsque mathématiquement vraie ;
- aucune observation future dans une feature ;
- mêmes intrants + versions + seed → même résultat ;
- coûts plus élevés ne peuvent améliorer artificiellement le résultat net ;
- échec fermé sur unité, quote, calendrier ou contrat ambigu ;
- jeu hostile : NaN, infini, zéro, valeurs négatives impossibles, split,
  timezone, DST, expiration, données dupliquées et trous.

L'IA peut expliquer pourquoi un résultat est fragile. Elle ne sélectionne pas
un modèle, ne réécrit pas une règle et ne transforme pas la robustesse en
certitude.
