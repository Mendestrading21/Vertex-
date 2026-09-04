# Vertex — Disponibilité des visualisations options

Les visualisations du laboratoire options — payoff, cône, distribution, décroissance thêta et mouvement attendu — exigent désormais des intrants de contrat effectivement reportés.

| Intrant | Condition |
|---|---|
| Spot, strike et prime | Valeur numérique positive |
| IV | Valeur numérique positive |
| DTE | Entier strictement positif |
| Type de contrat | `CALL` ou `PUT` |

Lorsqu’un de ces éléments manque ou est invalide, `unavailable` est `true`, le statut est `OPTION_VIZ_INPUT_UNAVAILABLE` et les courbes sont vides. Aucun spot à 100, IV à 35 %, DTE à 30 jours ou prime à 100 n’est utilisé.

> Les visualisations restent descriptives et en lecture seule. Elles ne génèrent ni ordre ni garantie de résultat.
