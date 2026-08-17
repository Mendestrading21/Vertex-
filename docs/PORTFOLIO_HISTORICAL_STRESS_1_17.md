# Vertex — stress historique du portefeuille

## Objectif

Le bloc `decision.portfolio.stress_test` complète le contexte des **positions réelles déclarées** avec un test de stress exclusivement historique. Il agrège les rendements journaliers pondérés de toutes les positions couvertes sur leurs dates communes afin de montrer le pire jour, le pire intervalle de cinq séances et le repli historique observé.

> Ce bloc n’est ni une prévision, ni un scénario macro supposé, ni une instruction de portefeuille. Il ne place aucun ordre, ne propose aucune taille et ne remplace pas les gates, le score ou les limites de la Constitution.

## Preuves requises

| Condition | Traitement |
|---|---|
| Au moins deux positions à poids strictement positif | Sinon `INSUFFICIENT_POSITIONS`. |
| Une série de clôtures datée et valide pour chaque position | Sinon `TEMPORAL_EVIDENCE_REQUIRED`, avec les symboles non couverts. |
| Au moins 31 séances communes datées | Sinon aucun stress de panier n’est produit. |
| Poids issus du contexte portefeuille valorisé | Les rendements ne sont jamais pondérés par une allocation inventée. |

Les prix sont convertis en rendements journaliers sur des dates communes. Le pire jour expose les contributions de chaque ligne, et `HISTORICAL_TAIL_CONCENTRATION` est signalé lorsqu’une seule ligne explique au moins 50 % de la perte négative de cette journée. Ce flag est descriptif et demande une revue humaine ; il n’ouvre, ne ferme ni ne modifie une position.

## Sorties et limites

| Champ | Base | Limite d’interprétation |
|---|---|---|
| `worst_1d` | Plus faible rendement journalier pondéré observé. | Ce n’est pas une perte maximale future. |
| `worst_5d` | Plus faible rendement composé sur cinq séances observées. | Les cinq séances ne sont pas une projection de durée de détention. |
| `historical_max_drawdown_pct` | Repli maximal de la courbe historique pondérée. | Il ne comprend ni frais, ni slippage, ni P&L de contrat options non observé. |
| `largest_worst_day_contributor` | Plus forte contribution négative lors du pire jour. | Il éclaire la concentration historique, sans recommander de réduction ou d’ajout. |

Quand une preuve est absente, Vertex conserve `available=false` au lieu de produire un panier partiel présenté comme complet. Les corrélations et ce stress restent complémentaires : le premier décrit la co-mouvance moyenne, le second les pertes observées du panier sur les dates communes.
