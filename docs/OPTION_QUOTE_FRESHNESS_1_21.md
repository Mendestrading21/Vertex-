# Vertex — fraîcheur des quotes options

Chaque candidat du mandat `SWING_3_6M` porte `quote_freshness`, construit uniquement depuis l’âge de quote effectivement fourni. Les statuts sont `QUOTE_FRESH`, `QUOTE_STALE` et `QUOTE_FRESHNESS_UNAVAILABLE`.

Le diagnostic est en lecture seule. Une quote rassis ou sans âge reste visible avec son statut ; Vertex ne la rafraîchit pas artificiellement, ne la retire pas silencieusement et ne crée aucun ordre.
