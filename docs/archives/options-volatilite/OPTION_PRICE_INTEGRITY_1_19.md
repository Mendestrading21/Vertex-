# Vertex — cohérence de prix d’option

## Objectif

Avant de calculer une volatilité implicite, des grecques, une probabilité descriptive ou un score de qualité, Vertex vérifie que le prix observé respecte les bornes européennes sans dividende du modèle Black-Scholes utilisé par le moteur.

> Une quote hors bornes est une donnée non interprétable, pas une opportunité. Vertex la rejette avant tout calcul analytique et ne crée ni volatilité, ni grecque, ni signal de remplacement.

| Contrat | Borne basse | Borne haute |
|---|---:|---:|
| Call | `max(0, S − K·e^(−rT))` | `S` |
| Put | `max(0, K·e^(−rT) − S)` | `K·e^(−rT)` |

Une tolérance numérique minimale est visible dans la sortie afin de tenir compte de l’arrondi de cotation ; elle ne représente pas une marge de marché ni une hypothèse de slippage.

## Contrat de sortie

| Statut | Présentation autorisée |
|---|---|
| `OPTION_PRICE_COHERENT` | Le prix se situe dans les bornes du modèle. Cela ne valide ni la liquidité, ni l’IV du fournisseur, ni l’opportunité. |
| `PRICE_OUTSIDE_NO_ARBITRAGE` | Refuser toute interprétation de l’option ; afficher les bornes et le prix observé si la quote est présentée. |
| `OPTION_INPUT_INSUFFICIENT` | Expliquer que spot, strike, durée ou prix ne permet pas le contrôle. Ne pas déduire une IV. |

Le champ `price_integrity` d’un contrat board est descriptif et en lecture seule. Lorsqu’une quote est rejetée, la réponse options expose `option_price_rejections` et `option_price_rejection_count`, avec le statut, les bornes et `derived_metrics_withheld=true`; elle ne contient alors ni IV, ni grecques, ni probabilités dérivées. Les contrôles de spread, OI, DTE, qualité et les hard gates de la Constitution restent indépendants.
