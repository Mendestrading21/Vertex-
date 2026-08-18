# Vertex — Disponibilité DTE des simulations options

La route `GET /api/options/scenarios/<sym>` refuse désormais une simulation si le meilleur contrat n’a pas un DTE numérique entier et non négatif.

| État du DTE | Résultat |
|---|---|
| Entier non négatif reporté | Simulation autorisée sous réserve des autres données requises |
| Absent, illisible, négatif ou fractionnaire | `empty: true` avec `input_coverage.status: DTE_UNAVAILABLE` |

La route ne remplace plus un DTE absent par zéro. Elle retourne un refus structuré au lieu d’inventer une échéance ou de calculer une prime théorique sur une donnée non prouvée.

> Les simulations restent des estimations clairement limitées, sans ordre, garantie ni exécution. Vertex demeure en lecture seule.
