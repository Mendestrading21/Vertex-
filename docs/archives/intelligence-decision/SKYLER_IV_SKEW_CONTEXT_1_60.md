# Vertex — skew IV call-put Skyler

Le contexte `iv_skew` réutilise le calcul existant de skew : médiane des IV des puts hors de la monnaie moins médiane des IV des calls hors de la monnaie, sur les contrats du symbole effectivement disponibles.

Le calcul n’est disponible que si le spot et des IV OTM exploitables existent des deux côtés. Sinon il produit `SPOT_UNAVAILABLE` ou `INSUFFICIENT_OTM_CALL_PUT_IV`, avec le nombre de contrats réellement considérés. Il n’interpole pas de surface, ne prévoit pas la volatilité et ne modifie ni score, ni gate, ni verdict.
