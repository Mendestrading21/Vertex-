# SKYLER V2 — OPTIONS CORRECTNESS CONTRACT

## Objectif

Les calculs options peuvent influencer une décision financière. Toute approximation, unité ou convention doit être explicite, testée et visible.

## Unités canoniques

### Volatilité implicite

Ne jamais utiliser une heuristique silencieuse du type « si IV > 1,5, diviser par 100 » dans le cœur métier.

Utiliser une frontière de normalisation explicite :

```python
ImpliedVol(value=40.4, unit="PERCENT")
ImpliedVol(value=0.404, unit="DECIMAL")
```

Après normalisation interne : IV en décimal.

### Prime

Séparer :

- prime par action ;
- prime par contrat ;
- multiplicateur ;
- coût total ;
- devise.

Ne jamais réutiliser un champ `cost` sans contrat de donnée documenté.

### Greeks

Documenter les unités :

- delta : variation de valeur par mouvement de 1 unité du sous-jacent ;
- gamma : variation du delta par mouvement de 1 unité ;
- theta : variation par jour ;
- vega : variation par point d’IV ou unité de vol, explicitement indiqué ;
- vanna : convention et unité ;
- vomma : convention et unité ;
- charm : convention temporelle et unité.

## Validation des entrées

Refuser honnêtement si :

- spot <= 0 ;
- strike <= 0 ;
- DTE < 0 ;
- quantité = 0 ;
- prime manquante pour un payoff nécessitant une prime ;
- IV <= 0 pour Greeks/PoP ;
- bid > ask ;
- valeur NaN/inf ;
- expiration antérieure ;
- type de jambe inconnu ;
- multiplicateur non supporté ou absent lorsque critique.

Les raisons de refus doivent être structurées et testées.

## Payoff et asymptotes

Pour une stratégie multi-jambes, calculer les pentes terminales.

Vers le haut :

- exposition nette positive aux calls/actions → gain potentiellement illimité ;
- exposition nette négative aux calls/actions → perte potentiellement illimitée ;
- exposition nette nulle → payoff borné vers le haut.

Vers le bas :

- le sous-jacent ne descend pas sous zéro ;
- calculer précisément le payoff à zéro ;
- ne pas conclure « perte bornée » sans vérifier l’asymptote haute.

Sortie minimale :

```json
{
  "max_profit": null,
  "max_profit_unbounded": true,
  "max_loss": -500,
  "max_loss_unbounded": false
}
```

Un flag illimité doit primer sur toute valeur numérique issue d’une grille finie.

## Probabilité de profit

Toute PoP doit indiquer :

- modèle ;
- mesure utilisée ;
- drift ;
- taux ;
- dividende ;
- IV ;
- horizon ;
- méthode d’intégration ;
- limites.

Ne jamais présenter une PoP risque-neutre comme fréquence historique certaine.

Tests minimum :

- call long débit : PoP < 100 % ;
- put long débit : PoP < 100 % ;
- spread borné : gain/perte exacts ;
- short call : perte illimitée ;
- iron condor : ailes bornent les pertes ;
- IV pourcentage/décimal : résultats équivalents après normalisation explicite ;
- DTE nul : Greeks/PoP gérés honnêtement.

## Probabilité de doublement

La probabilité de doublement n’est pas une simple PoP.

Elle doit utiliser une condition de valeur future :

```text
P(option_value_horizon >= 2 × coût_total_exécutable)
```

Le modèle doit intégrer, selon disponibilité :

- distribution du spot ;
- horizon de sortie distinct de l’expiration ;
- IV future ou scénarios d’IV ;
- theta ;
- taux/dividende ;
- spread/slippage ;
- événement binaire ;
- scénarios multiples.

Si le modèle n’est pas calibré, afficher `ESTIMATED` et une confiance réduite.

## Liquidité

Pour chaque contrat :

- bid ;
- ask ;
- mid ;
- spread absolu ;
- spread en % ;
- volume ;
- OI ;
- âge de la quote ;
- source.

Le coût exécutable ne doit pas être le mid sans avertissement. Prévoir au minimum :

- scénario optimiste au mid ;
- scénario réaliste ;
- scénario défavorable à l’ask/bid selon le sens.

## DTE et mandat

Scanners séparés :

- TACTICAL : 20–60 ;
- SWING : 60–180 ;
- LEAPS : 180–540.

Ne jamais sélectionner automatiquement l’échéance proche de 35 DTE pour une requête LEAPS.

## Profil actif

Avant ranking :

1. charger le profil actif ;
2. filtrer les stratégies interdites ;
3. filtrer DTE/delta/liquidité ;
4. appliquer hard gates ;
5. seulement ensuite calculer le classement.

Une stratégie interdite peut être analysée en laboratoire, mais :

- jamais marquée recommandée ;
- badge `HORS_MANDAT` ;
- aucun sizing ;
- risques illimités visibles.

## GEX, Vanna, Charm et Max Pain

Toujours afficher les conventions.

- GEX dealer est une inférence basée sur une convention de positionnement ;
- OI ne révèle pas avec certitude qui est long ou short ;
- Max Pain est descriptif, pas prédictif ;
- les walls dépendent de la qualité de chaîne ;
- Vanna/Charm peuvent changer avec spot, IV, temps et expiration.

Sortie :

- `generator: deterministic` ;
- `convention` ;
- `contracts_used` ;
- `coverage_pct` si calculable ;
- `warnings` ;
- `as_of`.

## Tests de référence

Créer des cas calculables à la main :

1. call long ;
2. put long ;
3. bull call spread ;
4. bear put spread ;
5. short put ;
6. short call ;
7. straddle ;
8. iron condor ;
9. combinaison action + option ;
10. entrée invalide.

Pour chaque cas : prime, payoff à plusieurs spots, breakeven, asymptote, Greeks attendus en signe et ordre de grandeur.

## Modification d’un calcul

Procédure impérative :

1. reproduire le bug ;
2. test rouge ;
3. documenter unité et convention ;
4. corriger le point de jonction le plus étroit ;
5. test vert ;
6. tests de non-régression ;
7. comparer avant/après sur données synthétiques contrôlées ;
8. vérifier l’UI et les labels ;
9. rapport de validation ;
10. arrêt pour revue humaine.
