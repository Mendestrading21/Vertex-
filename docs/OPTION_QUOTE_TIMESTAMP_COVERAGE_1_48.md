# Vertex — couverture d’horodatage des contrats options

Chaque contrat options expose `quote_timestamp_coverage`. Lorsqu’un `lastTradeDate` est reporté par la chaîne, il est présenté comme horodatage fourni uniquement.

Lorsqu’aucun horodatage n’est reporté, Vertex retourne `TIMESTAMP_UNAVAILABLE`. Le moteur ne déduit ni âge, ni fraîcheur, ni impact à partir de l’absence de timestamp.
