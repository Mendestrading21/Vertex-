# Vertex — contexte IV-HV des options

Le payload `/options/<sym>` expose `iv_hv_context` lorsque l’IV ATM observée et la volatilité réalisée sur 20 séances sont toutes deux disponibles. Il fournit l’écart en points de pourcentage, le ratio et un statut descriptif : `IV_ABOVE_HV`, `IV_BELOW_HV` ou `IV_NEAR_HV`.

Si l’une des deux mesures manque, le statut est `INSUFFICIENT_IV_HV`. Vertex n’impute aucune volatilité, ne transforme pas l’écart en prévision et ne modifie ni score, ni décision, ni scénario.

Le contexte options Skyler transporte également `iv_hv_context` lorsque les clôtures canoniques sont disponibles. Cette donnée reste informative : elle ne modifie ni le mandat, ni les gates, ni le verdict.
