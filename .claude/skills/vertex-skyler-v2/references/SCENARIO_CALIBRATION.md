# SKYLER V2 — SCÉNARIOS, PROBABILITÉS ET CALIBRATION

## 1. Principe

Une probabilité n’est pas une décoration. Elle doit être produite par une méthode documentée, versionnée et mesurable après coup.

Skyler ne doit jamais écrire « 70 % de probabilité » parce que le dossier paraît convaincant. Il doit relier la probabilité à des observations historiques, un modèle explicite ou une estimation structurée dont les limites sont affichées.

## 2. Les trois scénarios obligatoires

### Pessimiste

Décrit une évolution défavorable plausible, pas uniquement la catastrophe absolue.

Il inclut :

- déclencheur négatif ;
- chemin de prix ;
- horizon ;
- cible ;
- perte action ;
- perte option ;
- changement d’IV ;
- invalidation de la thèse ;
- réponse analytique autorisée.

### Probable

Décrit le scénario central conditionnel aux informations actuellement disponibles.

Il ne doit pas être confondu avec une certitude ou une cible analyste moyenne.

### Exceptionnel

Décrit le scénario où plusieurs catalyseurs positifs se combinent.

Il doit rester plausible et expliciter les conditions nécessaires. Il ne peut pas être une simple multiplication arbitraire du scénario probable.

## 3. Cohérence interne

Règles :

- les probabilités totalisent 100 % avec une tolérance de calcul documentée ;
- le scénario pessimiste possède un rendement inférieur au probable ;
- le scénario exceptionnel possède un rendement supérieur au probable ;
- les horizons sont compatibles ;
- chaque scénario possède une invalidation ou une condition de sortie ;
- aucune cible n’est produite sans méthode ;
- l’impact option utilise le même spot, la même IV, le même temps et les mêmes unités que le moteur canonique.

## 4. Sources de probabilité

Ordre de préférence :

1. distribution historique conditionnelle comparable ;
2. modèle statistique ou Monte Carlo documenté ;
3. probabilités implicites options ajustées et étiquetées ;
4. combinaison bayésienne de signaux calibrés ;
5. estimation structurée du comité, plafonnée en confiance.

Une estimation du comité sans historique ne doit jamais être présentée comme une probabilité empirique.

## 5. Construction conditionnelle

Les probabilités doivent considérer :

- régime de marché ;
- secteur ;
- tendance ;
- volatilité ;
- valorisation ;
- révisions ;
- type de catalyseur ;
- délai ;
- liquidité ;
- positionnement options ;
- distance à l’invalidation ;
- événements binaires.

La population historique utilisée doit être suffisamment comparable. Sinon, afficher `sample_quality: LOW`.

## 6. Expected Value

Pour les rendements :

```text
EV = Σ(probabilité_i × rendement_i)
```

Pour les montants :

```text
EV_cash = Σ(probabilité_i × P&L_i)
```

Règles :

- probabilités en fraction, pas en pourcentage brut ;
- P&L après coût et slippage lorsque l’analyse prétend être exécutable ;
- perte maximale séparée de l’EV ;
- CVaR ou tail loss affiché lorsque disponible ;
- EV positive ne contourne jamais un hard gate.

## 7. Probabilité de doublement d’une option

La probabilité de doublement doit être une estimation séparée de la probabilité de profit.

Événement :

```text
valeur_option_horizon >= 2 × coût_total_exécutable
```

Le modèle doit préciser :

- horizon de mesure ;
- dynamique du sous-jacent ;
- volatilité utilisée ;
- évolution d’IV ;
- taux ;
- dividende ;
- spread/slippage ;
- méthode de pricing ;
- nombre de simulations ;
- seed ou reproductibilité ;
- intervalle d’erreur.

La probabilité de doublement ne doit jamais être dérivée directement du delta.

## 8. Scénarios spot × temps × IV

Pour chaque contrat candidat, produire une grille minimale :

- spot : pessimiste / probable / exceptionnel ;
- temps : immédiat / horizon catalyseur / horizon de sortie ;
- IV : contraction / stable / expansion.

Chaque cellule contient :

- valeur théorique ;
- P&L ;
- rendement ;
- theta consommé ;
- hypothèses ;
- statut estimé.

Les cellules impossibles ou insuffisantes restent `n/d`.

## 9. Événements binaires

Avant résultats, décision réglementaire ou procès :

- séparer scénario événement et scénario hors événement ;
- utiliser expected move et historique de réaction ;
- inclure IV crush ;
- ne pas utiliser une distribution normale simple si les queues historiques sont significatives ;
- afficher la perte possible même si la direction est correcte mais le mouvement insuffisant.

## 10. Ledger de décision

Chaque décision est figée avec :

- `decision_id` ;
- version du moteur ;
- timestamp ;
- données et fraîcheur ;
- scénarios ;
- probabilités ;
- décision ;
- déclencheur ;
- invalidation ;
- score ;
- confiance ;
- portefeuille au moment de la décision ;
- objection adverse ;
- résultat futur observé.

Les décisions historiques ne sont jamais recalculées silencieusement avec un nouveau moteur.

## 11. Fenêtres d’évaluation

Mesurer au minimum :

- 5 séances ;
- 20 séances ;
- 60 séances ;
- horizon du catalyseur ;
- horizon déclaré de la décision ;
- échéance option lorsque pertinent.

Éviter de juger un scénario 12 mois après cinq jours.

## 12. Métriques de calibration

### Brier Score

Pour événements binaires : plus faible est meilleur.

### Log Loss

Pénalise fortement les certitudes incorrectes.

### Calibration bins

Comparer prévisions 50–60 %, 60–70 %, etc. aux fréquences réalisées.

### Sharpness

Mesurer si le moteur produit des probabilités informatives ou reste toujours proche de 50 %.

### Coverage

Part des décisions réellement évaluables avec données complètes.

### MAE / MFE

- excursion adverse maximale ;
- excursion favorable maximale.

### Scenario hit rate

Identifier quel scénario contenait le résultat observé.

### Ranking quality

Comparer S+/S/A/B aux rendements et risques réalisés, sans confondre performance brute et qualité de décision.

## 13. Calibration par contexte

Découper les résultats par :

- régime ;
- secteur ;
- horizon ;
- action/call/put ;
- niveau ;
- type de catalyseur ;
- IV percentile ;
- qualité des données ;
- mode réel/démo ;
- taille d’échantillon.

Ne pas modifier les poids sur un petit échantillon. Toute recalibration exige :

1. échantillon minimum défini ;
2. validation hors-échantillon ;
3. version du moteur ;
4. comparaison avant/après ;
5. rollback.

## 14. Prévention du look-ahead

Interdictions :

- utiliser une donnée publiée après la décision ;
- recalculer les fondamentaux historiques avec la dernière valeur ;
- sélectionner les meilleurs seuils sur toute la période puis annoncer un backtest honnête ;
- modifier une décision historique après connaissance du résultat ;
- exclure silencieusement les trades non gagnants ou les données manquantes.

## 15. Décision de recalibration

La calibration ne modifie pas automatiquement la Constitution.

Elle peut proposer :

- ajustement de poids ;
- plafond de confiance ;
- filtre de régime ;
- seuil de liquidité ;
- retrait d’un signal inutile ;
- ajout d’une confirmation.

Toute proposition est documentée et soumise à validation humaine.

## 16. Tests obligatoires

- probabilités totalisent 100 % ;
- EV calculée avec unités cohérentes ;
- probabilité de doublement distincte de PoP ;
- résultats reproductibles avec seed ;
- aucune donnée future dans les features ;
- décision historique immuable ;
- calibration séparée par version du moteur ;
- échantillon insuffisant empêche une recalibration automatique ;
- une forte confiance incorrecte est correctement pénalisée ;
- mode sans IV refuse les calculs options dépendant de l’IV.
