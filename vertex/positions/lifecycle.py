"""vertex.positions.lifecycle — statuts, transitions, matérialité, priorité.

§14-15 : les transitions dépendent du PLAN (jamais du seul P&L) et de
seuils ajustés (ATR quand disponible) — une microvariation intraday
n'invalide jamais une thèse (§26 : matérialité). Aucun statut ne déclenche
un ordre.
"""
from __future__ import annotations

# Seuils configurables (§26)
THRESHOLDS = {
    'stop_approach_atr': 1.0,      # distance au stop < 1 ATR
    'stop_approach_pct': 3.0,      # repli sans ATR : < 3 %
    'target_approach_pct': 3.0,
    'stock_drawdown_review': -20.0,
    'option_theta_warning_dte': 30,
    'option_dte_warning': 21,
    'option_spread_warning_pct': 8.0,
    'option_liquidity_min_oi': 100,
    'option_review_loss_pct': -50.0,   # ne pas attendre -100 %
    'time_stop_sessions': (5, 8),
    'materiality_minor_pct': 0.5,
    'materiality_meaningful_pct': 2.0,
    'materiality_major_pct': 5.0,
}


def materiality(change_pct: float | None, atr_move: float | None = None) -> str:
    """IMMATERIAL/MINOR/MEANINGFUL/MAJOR/CRITICAL — jamais None en entrée requise."""
    if change_pct is None:
        return 'IMMATERIAL'
    c = abs(change_pct)
    if atr_move is not None and atr_move >= 2.5:
        return 'CRITICAL'
    if c >= THRESHOLDS['materiality_major_pct']:
        return 'MAJOR'
    if c >= THRESHOLDS['materiality_meaningful_pct']:
        return 'MEANINGFUL'
    if c >= THRESHOLDS['materiality_minor_pct']:
        return 'MINOR'
    return 'IMMATERIAL'


def stock_status(p: dict) -> str:
    """Statut cycle de vie d'une action — ordre du plan, pas du P&L."""
    if p.get('status') == 'DATA_REPAIR_REQUIRED':
        return 'DATA_REPAIR_REQUIRED'
    if p.get('closed_at') or p.get('status') == 'CLOSED':
        return 'CLOSED'
    price, stop, tp1 = p.get('current_price'), p.get('stop'), p.get('tp1')
    if price is None:
        return 'AWAITING_DATA'
    pl = p.get('unrealized_pnl_pct')
    # 1. Invalidation (stop touché/cassé) — confirmée par le prix courant
    if stop is not None and price <= stop:
        return 'INVALIDATED'
    # 2. Drawdown constitution (~-20 %) → revue obligatoire (§21)
    if pl is not None and pl <= THRESHOLDS['stock_drawdown_review']:
        return 'REVIEW_REQUIRED'
    # 3. Stop qui approche (ATR d'abord, % en repli)
    if stop is not None:
        atr_d = p.get('stop_distance_atr')
        if atr_d is not None and 0 < atr_d <= THRESHOLDS['stop_approach_atr']:
            return 'STOP_APPROACHING'
        if atr_d is None and p.get('risk_to_stop_pct') is not None \
                and -THRESHOLDS['stop_approach_pct'] <= p['risk_to_stop_pct'] < 0:
            return 'STOP_APPROACHING'
    # 4. Objectifs
    if tp1 is not None:
        if price >= tp1:
            return 'TARGET_REACHED'
        if p.get('reward_to_tp1') is not None \
                and 0 < p['reward_to_tp1'] <= THRESHOLDS['target_approach_pct']:
            return 'TARGET_APPROACHING'
    # 5. Thèse absente → revue (THESIS_REQUIRED porté par thesis_health)
    if not p.get('thesis_text'):
        return 'REVIEW_REQUIRED'
    if stop is None:
        return 'OPEN_MONITOR'     # plan incomplet : surveiller, pas sain
    return 'OPEN_HEALTHY'


def option_status(p: dict) -> str:
    if p.get('status') == 'DATA_REPAIR_REQUIRED':
        return 'DATA_REPAIR_REQUIRED'
    if p.get('closed_at') or p.get('status') == 'CLOSED':
        return 'CLOSED'
    dte = p.get('dte')
    if dte is not None and dte < 0:
        return 'EXPIRED'
    spot, stop = p.get('underlying_price'), p.get('underlying_stop')
    right = p.get('right')
    if spot is not None and stop is not None:
        breached = spot <= stop if right == 'CALL' else spot >= stop
        if breached:
            return 'UNDERLYING_INVALIDATED'
        near = (abs(spot - stop) / spot * 100) <= THRESHOLDS['stop_approach_pct'] if spot else False
        if near:
            return 'UNDERLYING_STOP_APPROACHING'
    pl = p.get('unrealized_pnl_pct')
    if pl is not None and pl <= THRESHOLDS['option_review_loss_pct']:
        return 'REVIEW_REQUIRED'    # ne pas attendre -100 % (§21)
    if dte is not None and dte <= THRESHOLDS['option_dte_warning']:
        return 'DTE_WARNING'
    if p.get('days_to_earnings') is not None and p['days_to_earnings'] <= 7:
        return 'EARNINGS_RISK'
    if p.get('spread_pct') is not None \
            and p['spread_pct'] >= THRESHOLDS['option_spread_warning_pct']:
        return 'SPREAD_WARNING'
    if p.get('open_interest') is not None \
            and p['open_interest'] < THRESHOLDS['option_liquidity_min_oi']:
        return 'LIQUIDITY_WARNING'
    if dte is not None and dte <= THRESHOLDS['option_theta_warning_dte']:
        return 'THETA_WARNING'
    if p.get('mark') is None:
        return 'AWAITING_CONTRACT_DATA'
    if pl is not None and pl >= 50:
        return 'PROFIT_TAKING_ZONE'   # zone +50 % : sécuriser 60-70 % (plan)
    return 'OPEN_HEALTHY'


def priority(p: dict) -> str:
    """P0_CRITICAL > P1_HIGH > P2_NORMAL > P3_LOW (§28)."""
    st = p.get('lifecycle_status') or ''
    if st in ('INVALIDATED', 'UNDERLYING_INVALIDATED', 'EXPIRED',
              'DATA_REPAIR_REQUIRED'):
        return 'P0_CRITICAL'
    if st in ('STOP_APPROACHING', 'UNDERLYING_STOP_APPROACHING',
              'TARGET_APPROACHING', 'TARGET_REACHED', 'REVIEW_REQUIRED',
              'THETA_WARNING', 'DTE_WARNING', 'EARNINGS_RISK',
              'SPREAD_WARNING', 'LIQUIDITY_WARNING', 'PROFIT_TAKING_ZONE',
              'TIME_STOP_APPROACHING', 'IV_CRUSH_RISK'):
        return 'P1_HIGH'
    if st in ('OPEN_HEALTHY',):
        return 'P3_LOW'
    return 'P2_NORMAL'


def action_for(p: dict) -> str:
    """Action analytique (§19) — recommandation, jamais un ordre."""
    st = p.get('lifecycle_status') or ''
    if st in ('INVALIDATED', 'UNDERLYING_INVALIDATED'):
        return 'INVALIDÉE'
    if st in ('REVIEW_REQUIRED', 'DATA_REPAIR_REQUIRED', 'EXPIRED'):
        return 'RÉDUIRE' if (p.get('unrealized_pnl_pct') or 0) < -15 else 'SURVEILLER'
    if st in ('TARGET_REACHED', 'PROFIT_TAKING_ZONE'):
        return 'SÉCURISER'
    if st in ('STOP_APPROACHING', 'UNDERLYING_STOP_APPROACHING',
              'THETA_WARNING', 'DTE_WARNING', 'EARNINGS_RISK',
              'SPREAD_WARNING', 'LIQUIDITY_WARNING', 'TARGET_APPROACHING'):
        return 'SURVEILLER'
    return 'MAINTENIR'


__all__ = ['THRESHOLDS', 'materiality', 'stock_status', 'option_status',
           'priority', 'action_for']
