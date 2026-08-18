# Vertex — contexte de volatilité baissière Skyler

Le contexte `downside_volatility` est calculé uniquement à partir des rendements entre clôtures canoniques. Sur vingt séances, il indique le nombre de rendements négatifs, leur part et la semi-déviation annualisée observée.

Une série contenant moins de 21 clôtures, une valeur non numérique ou une clôture non positive produit `INSUFFICIENT_SERIES`. Vertex ne complète pas l’historique, ne prédit pas la volatilité future et ne modifie ni score, ni gate, ni verdict à partir de ce contexte.
