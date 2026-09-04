# Vertex — couverture de réconciliation des prix

Chaque rapport de réconciliation expose sa `coverage` : observation spot disponible, contrats options, prix sous-jacent reportés par la chaîne, comparaisons de prix effectivement possibles et comparaison d’horodatages disponible.

Lorsque moins de deux observations comparables sont disponibles, le statut est `INSUFFICIENT_COMPARABLE_SOURCES`. Vertex ne calcule alors aucune moyenne, aucun prix synthétique et aucune divergence artificielle.

Cette métadonnée est descriptive et ne modifie ni les incohérences détectées ni les plafonds de décision existants.
