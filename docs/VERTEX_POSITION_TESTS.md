# Vertex — Tests positions (§42-43)

`tests/test_position_intelligence.py` — 41 golden numériques, tous verts.

Couverture : modèles & sources, réconciliation (doublon/quantité/coût,
IBKR offline ne clôture rien), calculs actions (P&L, distance stop, R:R,
poids, MAE/MFE), calculs options (P&L, breakeven, intrinsèque, delta/theta
positionnels signés, divergence Greeks, multiplicateur une fois), cycle de
vie (invalidation confirmée vs micro-move, drawdown, DTE warning, review
avant -100 %), priorité, matérialité, agrégation (CALLS/PUTS séparés,
liste d'action), change detector, dédup alertes, audit, et **sûreté**
(aucun chemin d'ordre, tout is_readonly).

Suite complète du dépôt : **597 passed**. 8 pages navigateur : 0 erreur
console. Parcours positions §44 (P1/P4/P7 + audit) : PASS en démo.
