# Vertex — Moteur de décision unique

`DecisionStack` (socle analytique) → `ExecutiveEngine`
(`vertex/strategy/executive_engine.py`) → décision finale. Aucune route ni
page ne publie de décision concurrente (gardien
`test_decision_engine_is_single_source`). Déterministe : mêmes entrées +
même version ⇒ même décision. Claude ne peut pas le contourner.

## Hard gates (plafonnent à ATTENDRE sauf mention)
`RR_BELOW_MINIMUM` (R:R < 2) · `REGIME_BLOCKS_NEW_RISK` (UNKNOWN ou
new_risk_allowed=false) · `DATA_QUALITY` · `SOURCE_DISAGREEMENT` ·
`BLOCKING_ANOMALY` · `NO_NEW_RISK` · `PORTFOLIO_DRAWDOWN_LIMIT` ·
`MAX_OPTIONS_REACHED` · `PORTFOLIO_FULL_NO_REPLACEMENT` ·
`THESIS_INVALIDATED` (→ RÉDUIRE si détenu).

Sortie : schéma §8 complet (scores conviction/risk/timing/asymmetry/
data_quality, blocking_rules, unknowns, audit_trail, final_decision).
Tests : `test_rr_gate_is_two`, `test_unknown_regime_blocks_risk`,
`test_executive_engine.py`.
