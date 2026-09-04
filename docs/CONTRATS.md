# Contrats de gouvernance nommés dans le code

Six noms de contrats apparaissent dans les docstrings de `vertex/`. Ils ne
désignent pas des modules : ce sont des **règles de conception** que le code
respecte et que ce document définit. `tests/test_promesses_docstrings.py`
vérifie que chacun est défini quelque part — un contrat cité mais introuvable
serait une promesse creuse.

## `SKYLER_ARCHITECTURE`

Le packet de décision est construit une fois, puis traité comme immuable. Les
étapes en aval lisent le packet ; aucune ne le mute. Une valeur absente reste
absente jusqu'au rendu, où elle est nommée comme telle.

## `ADVERSARIAL_COMMITTEE`

Toute orientation passe par une contradiction explicite : le moteur produit
l'argument favorable **et** l'argument défavorable, avec les données qui les
soutiennent. Une orientation sans contre-argument mesuré est incomplète, pas
« confiante ».

## `OPTIONS_CORRECTNESS`

Aucun prix, prime, Greek, IV ou probabilité d'option n'est inventé, interpolé
silencieusement ni recopié d'une échéance voisine. Une entrée manquante rend le
calcul indisponible et le dit ; elle ne produit jamais un zéro.

## `SCENARIO_CALIBRATION`

Un scénario porte ses hypothèses, son horizon et la source de sa distribution.
Une probabilité affichée sans calibration mesurable est présentée comme une
estimation non calibrée, jamais comme une probabilité.

## `DECISION_ENGINE`

Un seul `AdviceResult` fait autorité, produit par `vertex.strategy`. Aucun autre
module ne produit de vocabulaire décisionnel final. `tests/test_production_guards_canonical.py`
le vérifie.

## `PORTFOLIO_FIT`

Une orientation est évaluée contre le portefeuille **déclaré par l'utilisateur** :
concentration, corrélation, budget de risque. Aucune source externe ne fournit
ces positions.

## Notation

`S_T` désigne le prix du sous-jacent à l'échéance dans les formules d'options.
C'est une notation mathématique, pas un identifiant de code.
