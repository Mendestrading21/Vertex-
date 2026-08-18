# Vertex — sensibilité taux options

Un contrat options peut exposer `rate_sensitivity` uniquement lorsqu’une courbe de taux provenancée, non servie par repli, est fournie.

La mesure réévalue le prix Black-Scholes sans dividende à ±50 points de base autour du taux observé. Lorsque seule la valeur plate de secours est disponible, la sensibilité est explicitement indisponible ; elle ne produit ni scénario de marché, ni recommandation, ni ordre.
