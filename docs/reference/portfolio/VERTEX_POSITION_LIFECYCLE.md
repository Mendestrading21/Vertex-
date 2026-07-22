# Vertex — Cycle de vie (§14-15)

Actions : NEW · AWAITING_DATA · OPEN_HEALTHY · OPEN_MONITOR · WEAKENING ·
AT_RISK · STOP_APPROACHING · INVALIDATED · TARGET_APPROACHING ·
TARGET_REACHED · REVIEW_REQUIRED · CLOSED · DATA_REPAIR_REQUIRED.

Options : + THETA_WARNING · IV_CRUSH_RISK · EARNINGS_RISK · DTE_WARNING ·
SPREAD_WARNING · LIQUIDITY_WARNING · UNDERLYING_STOP_APPROACHING ·
UNDERLYING_INVALIDATED · PROFIT_TAKING_ZONE · EXPIRED.

## Règles clés
- Le verdict dépend du PLAN, jamais du seul P&L. Une gagnante peut devenir
  mauvaise, une perdante garder une thèse valide.
- Invalidation = franchissement CONFIRMÉ du niveau (prix ≤ stop), **jamais**
  une microvariation intraday (`test_thesis_is_not_invalidated_by_small_move`).
- Action ~-20 % → REVIEW_REQUIRED (réécriture de thèse exigée).
- Option : REVIEW_REQUIRED dès -50 %, sans attendre -100 %.

## Matérialité (§26)
IMMATERIAL/MINOR/MEANINGFUL/MAJOR/CRITICAL — seuils configurables
(`THRESHOLDS`). Recalcul déclenché seulement ≥ MEANINGFUL.

## Priorité (§28)
P0_CRITICAL (invalidation, réparation, option expirée) > P1_HIGH (stop/
objectif/earnings/theta/DTE proches) > P2_NORMAL > P3_LOW (sain).
