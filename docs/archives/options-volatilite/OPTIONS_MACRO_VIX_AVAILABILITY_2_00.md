# Vertex — Disponibilité VIX du risque macro options

La ligne « Fed / CPI / NFP » de la matrice de risques options nécessite désormais un VIX numérique strictement positif. L’absence, une valeur invalide ou une valeur nulle ne sont plus interprétées comme un VIX inférieur à 20.

| État du VIX | Niveau de risque macro | Couverture |
|---|---|---|
| VIX positif reporté, inférieur à 20 | `MOYEN` | `MACRO_VIX_AVAILABLE` |
| VIX positif reporté, au moins égal à 20 | `ÉLEVÉ` | `MACRO_VIX_AVAILABLE` |
| VIX absent, invalide ou nul | `INCONNU` | `MACRO_VIX_UNAVAILABLE` |

> La matrice reste une lecture de risque descriptive et strictement en lecture seule. Elle ne passe aucun ordre et ne garantit aucun résultat.
