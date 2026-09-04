# Vertex — Disponibilité des intrants de matrice de risques

La matrice de risques du laboratoire options ne remplace plus l’IV, le DTE ou le spread absents par des seuils de secours.

| Ligne de risque | Donnée nécessaire | Statut en cas d’absence |
|---|---|---|
| IV crush | IV positive | `IV_UNAVAILABLE` et niveau `INCONNU` |
| Liquidité et spread | Spread non négatif | `SPREAD_UNAVAILABLE` et niveau `INCONNU` |
| Résultats trimestriels | DTE positif | `DTE_UNAVAILABLE` et niveau `INCONNU` |

Chaque ligne concernée expose `coverage` avec son statut de disponibilité. Les scénarios, seuils et impacts réels restent inchangés lorsque la donnée est reportée.

> Les statuts sont descriptifs, sans ordre, prévision cachée ou garantie de résultat. Vertex demeure en lecture seule.
