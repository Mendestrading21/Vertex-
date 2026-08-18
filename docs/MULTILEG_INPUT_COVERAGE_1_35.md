# Vertex — couverture des entrées multi-jambes

Chaque analyse multi-jambes disponible expose `input_coverage`, qui indique la couverture des primes, bid/ask, IV, DTE et sous-jacent nécessaires aux sorties dérivées.

Une prime manquante continue de refuser le calcul de P&L. Un bid/ask absent laisse le slippage non chiffré ; il ne reçoit jamais de valeur de repli. Cette couverture est descriptive et strictement en lecture seule.
