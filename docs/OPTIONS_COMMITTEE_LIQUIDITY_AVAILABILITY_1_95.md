# Vertex — Disponibilité de liquidité du comité options

La sélection « Meilleure liquidité » du comité exige désormais un open interest et un spread numériques, non négatifs et réellement reportés.

| Données de contrat | Sélection du comité |
|---|---|
| OI et spread disponibles | Éligible au classement `OI − spread × 1000` |
| OI ou spread absent/invalide | Exclu de cette sélection |

Le comité n’applique plus un spread de 5 % de secours. La ligne expose `COMMITTEE_LIQUIDITY_AVAILABLE` ou `COMMITTEE_LIQUIDITY_UNAVAILABLE` sans modifier les autres rôles du comité.

> Le comité reste descriptif et en lecture seule, sans ordre ni garantie de résultat.
