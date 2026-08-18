# Vertex — Couverture IV de l’environnement options

Le diagnostic d’environnement options ne comptabilise désormais que les IV positives, numériques et réellement reportées. Les IV absentes, textuelles, nulles, négatives ou booléennes sont exclues de la médiane plutôt que converties en zéro.

| Champ de couverture | Signification |
|---|---|
| `iv_observed` | Nombre d’IV valides incluses dans la médiane |
| `iv_missing` | Contrats sans champ IV |
| `iv_invalid` | IV non numériques, nulles, négatives ou booléennes |
| `status` | `IV_SAMPLE_AVAILABLE` ou `IV_SAMPLE_UNAVAILABLE` |

La couverture est attachée à la dimension `volatility` du score d’environnement. Les dimensions inconnues restent exclues de la moyenne globale.

> Cette couverture décrit les données disponibles ; elle ne crée ni ordre, ni prévision, ni garantie de résultat. Vertex demeure en lecture seule.
