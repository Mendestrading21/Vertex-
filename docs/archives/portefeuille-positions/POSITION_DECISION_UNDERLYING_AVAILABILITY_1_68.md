# Vertex — Disponibilité du sous-jacent dans la décision de position

La route `GET /api/position-decision/<sym>` expose désormais `underlying_availability` en complément de `underlying`.

| Situation | `status` | Interprétation |
|---|---|---|
| Analyse sous-jacente retournée | `UNDERLYING_ANALYSIS_AVAILABLE` | Le contexte sous-jacent est présent, même si sa décision est `DATA_INSUFFICIENT` |
| Repli technique de l’analyse | `UNDERLYING_ANALYSIS_UNAVAILABLE` | La décision de position reste calculée, mais l’absence de contexte est déclarée |

Le statut n’expose aucune erreur interne. Le champ `does_not_change_recommendation` confirme que l’ajout est descriptif : il ne modifie ni la recommandation, ni les règles de risque, ni une éventuelle décision d’utilisateur.

> Vertex demeure un système d’analyse en lecture seule. Ce statut n’exécute aucun ordre et ne constitue pas une garantie de résultat.
