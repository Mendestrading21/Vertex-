# Vertex — couverture de courbe de taux

Chaque `RateQuote` expose `curve_coverage` pour indiquer le nombre de tenors fournis, leur liste, la provenance et la disponibilité d’un horodatage de courbe.

Lorsque la courbe est absente, Vertex sert uniquement le taux plat de repli documenté avec `status: FALLBACK_FLAT_RATE`. Ce repli n’est jamais présenté comme une courbe de marché observée.
