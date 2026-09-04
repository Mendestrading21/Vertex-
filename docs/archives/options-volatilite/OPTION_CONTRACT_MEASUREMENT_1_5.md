# Vertex — mesure contractuelle options 1.5

## Principe

Vertex mesure désormais la trajectoire d’un **contrat d’option suivi hypothétiquement** à partir de sa référence de départ et de quotes réellement observées dans le board. Cette fonctionnalité ne crée pas d’ordre, ne déduit pas de prix d’exécution et ne représente aucun gain encaissé.

| Élément | Règle mise en œuvre |
|---|---|
| Identité du contrat | `SYM|EXP|STRIKE|C/P`, avec normalisation de `125` et `125.0`. |
| Référence initiale | Priorité aux références options existantes, avec type et source conservés. |
| Marque de performance | Quote du board courant ; sinon dernier snapshot observé, clairement étiqueté. |
| Marque injectée | Une valeur `mark` passée dans l’URL ne peut plus créer une performance. |
| Absence de quote | `NO_OBSERVED_QUOTE` et rendement `None`, jamais zéro. |

## Mesure d’un contrat

Le bloc `option_contract` retourné par `GET /api/tracking/<tracking_id>/performance` indique le prix de référence, le mark observé, le mode de mark, le nombre de quotes collectées, la dernière date observée, le rendement prix, le MFE, le MAE et le drawdown. Son périmètre est systématiquement :

> `HYPOTHETICAL_OPTION_MARK_TO_OBSERVED_QUOTE` — suivi analytique, sans exécution, frais, slippage, profondeur de carnet ni assignation.

Un mark provenant du board est libellé `CURRENT_BOARD_QUOTE`. Un repli sur le dernier snapshot est `LAST_OBSERVED_SNAPSHOT` et ne doit pas être présenté comme un prix live.

## Cohortes d’options

`GET /api/tracking/options/cohort` agrège seulement les contrats ayant un rendement calculable depuis une quote observée. Les statistiques de cohortes comportent un minimum de cinq contrats mesurables par défaut ; sous ce seuil, le service expose le comptage et la raison d’indisponibilité, sans rendement moyen, médiane ni taux de réussite.

La décomposition `by_decision_at_start` compare les contrats par décision analytique initiale, mais conserve le même seuil pour chaque segment. Une cohorte de cinq contrats ne valide donc pas un segment de deux contrats.

## Limites

Les mesures actuelles sont une base de mémoire contractuelle : elles exigent encore une durée de collecte suffisante, des fenêtres de sortie comparables, et une convention explicitement documentée pour frais/slippage avant toute calibration de P&L net. Vertex conserve jusque-là une lecture descriptive et hypothétique.
