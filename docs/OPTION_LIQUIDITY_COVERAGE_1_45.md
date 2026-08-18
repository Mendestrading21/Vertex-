# Vertex — couverture de liquidité options

Chaque contrat options expose `liquidity_coverage` pour distinguer les champs de liquidité réellement reportés — bid, ask, volume et open interest — des champs absents.

Un zéro reporté reste une observation distincte d’une absence de champ. Vertex ne crée pas de liquidité, de spread ni d’open interest de repli.
