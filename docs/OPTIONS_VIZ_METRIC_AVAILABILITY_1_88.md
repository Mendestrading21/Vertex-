# Vertex — Disponibilité des métriques de visualisation options

Les visualisations options distinguent désormais l’absence d’une métrique du cas où elle vaut réellement zéro.

| Métrique | Donnée requise | Statut si absente |
|---|---|---|
| Probabilité de franchissement | Point mort positif reporté | `BREAK_EVEN_UNAVAILABLE` ; `p_be: null` |
| Mouvement attendu | `em_pct` numérique non négatif reporté | `EXPECTED_MOVE_UNAVAILABLE` ; plage `null` |

Une absence de point mort n’est plus remplacée par le strike, et une absence de mouvement attendu ne produit plus une plage artificiellement égale au spot.

> Les champs restent descriptifs et en lecture seule, sans prévision cachée, ordre ou garantie de résultat.
