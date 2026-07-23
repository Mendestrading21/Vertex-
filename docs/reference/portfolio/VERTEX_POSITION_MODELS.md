# Vertex — Modèles de positions

## Sources (§5) — priorité de fiabilité
IBKR (0) > MANUAL (1) > IMPORTED (2) > PAPER (3) > SIMULATED (4) > ARCHIVED.
Une position simulée n'est jamais présentée comme réelle (`is_real=False`).
Toute position porte `is_readonly=True`.

## Position action (§8)
`stock_position(trade)` — schéma desk : `cost` = TOTAL investi, donc
`average_cost = cost / quantity`. Champs plan (stop/tp1-3), calculs
(market_value, pnl, MAE/MFE, weight), cycle (lifecycle_status), thèse.

## Position option (§9)
`option_position(trade)` — prime/action = `cost / (qty × multiplicateur)`.
Identité contrat `contract_id = SYM|exp|strike|C|P`. Greeks positionnels,
scénarios, plan sur le sous-jacent, event_risk.

Détail : `vertex/positions/models.py`.
