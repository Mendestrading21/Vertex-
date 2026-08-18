# Vertex — Disponibilité du classement TOP Low IV

Le classement « TOP Low IV » ne peut comparer que des IV positives, numériques et effectivement reportées. Une IV absente, booléenne, nulle ou invalide ne reçoit plus une valeur artificielle permettant de la classer comme « convexité la moins chère ».

| État de la chaîne | Sortie `TOP Low IV` |
|---|---|
| Au moins une IV positive et numérique | Contrats classés, statut `TOP_LOW_IV_AVAILABLE` |
| Aucune IV positive et numérique | Liste vide explicitement servie, statut `TOP_LOW_IV_UNAVAILABLE` |

La couverture inclut le nombre de contrats avec IV exploitable et le nombre de contrats exclus. Le classement est descriptif, sans ordre ni garantie financière.
