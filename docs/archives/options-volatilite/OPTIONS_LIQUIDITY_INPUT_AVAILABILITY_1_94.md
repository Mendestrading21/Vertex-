# Vertex — Disponibilité des intrants de liquidité options

Le diagnostic de liquidité du laboratoire options exige désormais un open interest (OI) et un spread numériques non négatifs réellement reportés.

| Intrants | Résultat |
|---|---|
| OI et spread disponibles | Score de liquidité calculé selon les seuils existants |
| OI ou spread absent/invalide | Score indisponible, statut `LIQUIDITY_INPUT_UNAVAILABLE` |

Le moteur n’emploie plus un OI zéro ou un spread de 8 % en remplacement d’un champ manquant. Sa couverture expose séparément la présence des deux mesures.

> Ce diagnostic est descriptif, sans ordre, estimation implicite ou garantie de résultat. Vertex demeure en lecture seule.
