# Vertex — Concentration d’open interest Skyler

Le contexte `open_interest_concentration` agrège l’open interest tel qu’il est reporté dans le board options pour les contrats situés entre **90 et 180 DTE**, soit l’horizon d’échéance du mandat `SWING_3_6M`.

| Champ | Signification |
|---|---|
| `total_reported_open_interest` | Somme des open interests positifs reportés dans l’horizon |
| `top_strike` | Strike portant le plus grand open interest agrégé |
| `top_strike_share_pct` | Part de l’open interest positif total portée par ce strike |
| `coverage` | Contrats, champs OI présents, zéros reportés et données absentes ou invalides |

Les valeurs d’open interest nulles sont conservées comme **zéros reportés** et distinguées des champs absents ou invalides. Le contexte retourne `NO_POSITIVE_OI_REPORTED` lorsque les champs OI disponibles sont nuls, `OI_UNAVAILABLE` lorsqu’aucun champ OI exploitable n’est rapporté, et `NO_CONTRACTS_IN_SWING_HORIZON` lorsqu’il n’existe aucun contrat 90–180 DTE.

> Une concentration d’open interest n’est pas une inférence de positionnement, une prévision de prix ou un signal d’exécution. Elle ne modifie ni score, ni gate, ni verdict. Vertex reste en lecture seule et toute décision financière comporte un risque de perte.
