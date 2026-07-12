# Vertex — Calculs actions (§10)

Toutes les valeurs vérifiées par golden tests (`test_position_intelligence.py`).

| Grandeur | Formule | Golden |
|---|---|---|
| Coût moyen | cost_basis / quantity | 1000/10 = 100 |
| Valeur de marché | price × quantity | 115×10 = 1150 |
| P&L latent | market_value − cost_basis | 1150−1000 = 150 |
| P&L % | pnl / cost_basis × 100 | 15,0 % |
| Distance stop % | (stop/price − 1)×100 | (90/100−1)=−10 % |
| Risque monétaire | (price − stop) × qty | (100−90)×10 = 100 |
| R:R restant | (tp1 − price)/(price − stop) | (130−100)/(100−90)=3,0 |
| Poids | valeur / total portefeuille | 1000/4000 = 25 % |
| MAE / MFE | min/max (v/cost − 1) | −10 % / +20 % |

Règles : donnée absente → None (jamais 0) ; prix rassis rendu visible
(`price_stale`, qualité STALE) ; distance au stop en ATR quand l'ATR moteur
est disponible. Splits/dividendes/devises : hérités des marques desk/IBKR
(la couche positions ne réajuste pas silencieusement).
