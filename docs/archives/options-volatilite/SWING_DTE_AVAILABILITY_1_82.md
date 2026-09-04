# Vertex — Disponibilité DTE du moteur swing

La projection swing n’utilise plus une maturité de 30 jours lorsque le DTE du contrat est absent. Elle exige un DTE entier strictement positif et réellement reporté.

| DTE | Projection swing | Statut d’annotation |
|---|---|---|
| Entier positif reporté | Calcul possible sous réserve des autres entrées | `SWING_DTE_AVAILABLE` |
| Absent, illisible, négatif, nul ou fractionnaire | `(None, False)` sans projection | `SWING_DTE_UNAVAILABLE` |

Cette règle évite qu’un gamma, un rendement swing ou une érosion temporelle soient calculés sur une maturité non prouvée.

> Le moteur swing est analytique, ne crée aucun ordre et ne garantit aucun résultat. Vertex demeure en lecture seule.
