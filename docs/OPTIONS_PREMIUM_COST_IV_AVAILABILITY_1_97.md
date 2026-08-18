# Vertex — Disponibilité IV du coût de prime options

Le diagnostic « Analyse options » du laboratoire options exige désormais une IV positive, numérique et réellement reportée pour qualifier le coût de la prime.

| État de l’IV | Diagnostic de prime |
|---|---|
| IV disponible | Score et qualification existants (`prime chère` ou `prime correcte`) |
| IV absente ou invalide | Score indisponible et impact `coût de prime indisponible` |

La couverture `PREMIUM_COST_IV_AVAILABLE` ou `PREMIUM_COST_IV_UNAVAILABLE` est exposée avec la ligne. Une IV absente ne devient plus implicitement une prime correcte.

> Cette qualification est descriptive, sans ordre, prévision cachée ni garantie de résultat. Vertex demeure en lecture seule.
