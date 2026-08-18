# Vertex — contexte de proximité des résultats Skyler

Le contexte `earnings_proximity` examine uniquement les événements `earnings` provenant du calendrier fourni. Lorsqu’un DTE non négatif est déclaré, il expose le résultat le plus proche et sa provenance.

Sans calendrier, le statut est `EARNINGS_CALENDAR_UNAVAILABLE`. Une date sans DTE reste `DATED_EARNINGS_NO_DTE` : Vertex ne convertit pas un format de date non normalisé en nombre de jours, n’estime pas de publication et ne modifie ni score, ni gate, ni verdict.
