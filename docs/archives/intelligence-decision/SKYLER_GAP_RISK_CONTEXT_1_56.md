# Vertex — contexte de gaps observés Skyler

Le contexte `gap_risk` mesure les écarts observés entre l’ouverture d’une séance et la clôture de la séance précédente sur une fenêtre de vingt séances. Il publie le dernier gap, le maximum absolu observé et la fréquence des gaps d’au moins 2 %.

Il exige 21 observations OHLC canoniques complètes et cohérentes. Si l’ouverture ou la clôture manque, le statut est `INSUFFICIENT_OHLC` : Vertex ne reconstruit jamais une ouverture, ne prédit pas le prochain gap et ne modifie ni score, ni gate, ni verdict.
