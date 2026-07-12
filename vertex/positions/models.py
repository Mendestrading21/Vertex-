"""vertex.positions.models — modèles canoniques (§5/§8/§9).

Une donnée inconnue reste None — JAMAIS convertie en zéro. Chaque position
porte source, provenance, qualité et `is_readonly: True` (invariant).
"""
from __future__ import annotations

import time
from datetime import datetime, date

SOURCES = ('IBKR', 'MANUAL', 'PAPER', 'SIMULATED', 'IMPORTED', 'ARCHIVED')
# Priorité de fiabilité (§5) : réelle IBKR > manuelle > paper > simulée.
SOURCE_PRIORITY = {'IBKR': 0, 'MANUAL': 1, 'IMPORTED': 2, 'PAPER': 3,
                   'SIMULATED': 4, 'ARCHIVED': 5}

STOCK_STATUSES = (
    'NEW', 'AWAITING_DATA', 'OPEN_HEALTHY', 'OPEN_MONITOR', 'STRENGTHENING',
    'WEAKENING', 'AT_RISK', 'STOP_APPROACHING', 'INVALIDATED',
    'TARGET_APPROACHING', 'TARGET_REACHED', 'REVIEW_REQUIRED',
    'CLOSE_REPORTED', 'CLOSED', 'ARCHIVED', 'DATA_REPAIR_REQUIRED')

OPTION_STATUSES = (
    'NEW', 'AWAITING_CONTRACT_DATA', 'OPEN_HEALTHY', 'OPEN_MONITOR',
    'PROFIT_TAKING_ZONE', 'PARTIAL_PROFIT_REPORTED', 'RUNNER_ACTIVE',
    'TIME_STOP_APPROACHING', 'THETA_WARNING', 'IV_CRUSH_RISK',
    'EARNINGS_RISK', 'DTE_WARNING', 'SPREAD_WARNING', 'LIQUIDITY_WARNING',
    'UNDERLYING_STOP_APPROACHING', 'UNDERLYING_INVALIDATED',
    'CONTRACT_DATA_STALE', 'REVIEW_REQUIRED', 'CLOSE_REPORTED', 'CLOSED',
    'EXPIRED', 'DATA_REPAIR_REQUIRED')

ANALYTIC_ACTIONS = ('MAINTENIR', 'SURVEILLER', 'SÉCURISER',
                    'RENFORCEMENT_POSSIBLE', 'RÉDUIRE',
                    'SORTIE_ANALYTIQUE_PROPOSÉE', 'INVALIDÉE')

PRIORITIES = ('P0_CRITICAL', 'P1_HIGH', 'P2_NORMAL', 'P3_LOW')


def _f(v):
    try:
        return float(v) if v is not None and v != '' else None
    except (TypeError, ValueError):
        return None


def _dte(exp: str | None) -> int | None:
    if not exp:
        return None
    try:
        d = datetime.strptime(str(exp)[:10], '%Y-%m-%d').date()
        return (d - date.today()).days
    except ValueError:
        return None


def _holding_days(opened: str | None) -> int | None:
    if not opened:
        return None
    try:
        d = datetime.strptime(str(opened)[:10], '%Y-%m-%d').date()
        return (date.today() - d).days
    except ValueError:
        return None


def base_position(trade: dict, source: str = 'MANUAL',
                  status_hint: str | None = None) -> dict:
    """Enveloppe commune §5 — champs inconnus = None, is_readonly toujours True."""
    sym = str(trade.get('sym') or trade.get('symbol') or '').upper()
    return {
        'position_id': str(trade.get('id') or f'{source}:{sym}'),
        'source': source if source in SOURCES else 'MANUAL',
        'source_reference': trade.get('source_reference') or ('desk:myTrades' if source == 'MANUAL' else source.lower()),
        'account_id': trade.get('account_id'),
        'symbol': sym,
        'currency': str(trade.get('currency') or 'USD').upper(),
        'status': status_hint or 'NEW',
        'opened_at': trade.get('added') or trade.get('opened_at'),
        'closed_at': trade.get('closed') or None,
        'last_reconciled_at': None,
        'data_quality': {'issues': [], 'overall': 'UNKNOWN'},
        'is_real': source in ('IBKR', 'MANUAL', 'IMPORTED'),
        'is_readonly': True,
    }


def stock_position(trade: dict, source: str = 'MANUAL') -> dict:
    """Modèle canonique action/ETF/fonds/crypto (§8) depuis un trade desk.
    Schéma desk : cost = TOTAL investi."""
    p = base_position(trade, source)
    snap = trade.get('entrySnap') or {}
    qty = _f(trade.get('qty'))
    cost_basis = _f(trade.get('cost'))
    avg = (cost_basis / qty) if (cost_basis is not None and qty) else _f(trade.get('entryPrice'))
    ttype = str(trade.get('type') or 'STK').upper()
    asset = {'STK': 'STOCK', 'ETF': 'ETF', 'FUND': 'FUND',
             'CRYPTO': 'CRYPTO'}.get(ttype, 'STOCK')
    p.update({
        'asset_type': asset,
        'company_name': trade.get('name'),
        'role': None,                      # affecté par le team engine
        'quantity': qty,
        'average_cost': round(avg, 4) if avg is not None else None,
        'cost_basis': cost_basis,
        'current_price': None, 'market_value': None,
        'unrealized_pnl': None, 'unrealized_pnl_pct': None,
        'realized_pnl': _f(trade.get('pnl')),
        'total_return': None,
        'holding_days': _holding_days(trade.get('added')),
        'high_since_entry': None, 'low_since_entry': None,
        'mae': None, 'mfe': None, 'drawdown_from_peak': None,
        'weight_pct': None,
        'stop': _f(snap.get('stop') or trade.get('myStop')),
        'tp1': _f(snap.get('tgt') or trade.get('myTgt') or trade.get('target1')),
        'tp2': _f(trade.get('target2')), 'tp3': _f(trade.get('target3')),
        'risk_to_stop': None, 'risk_to_stop_pct': None,
        'reward_to_tp1': None, 'reward_to_tp2': None, 'reward_to_tp3': None,
        'remaining_rr': None,
        'thesis_id': None,
        'thesis_text': (snap.get('thesis') or trade.get('note') or None),
        'thesis_health': 'UNKNOWN',
        'next_catalyst': None, 'earnings_at': None, 'days_to_earnings': None,
        'decision': None, 'lifecycle_status': p['status'],
        'last_updated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    })
    return p


def option_position(trade: dict, source: str = 'MANUAL') -> dict:
    """Modèle canonique option (§9). Prime PAR ACTION dérivée du coût total
    desk (cost = qty × prime × 100)."""
    p = base_position(trade, source)
    snap = trade.get('entrySnap') or {}
    qty = _f(trade.get('qty'))
    cost_total = _f(trade.get('cost'))
    mult = _f(trade.get('multiplier')) or 100.0
    avg = (cost_total / (qty * mult)) if (cost_total is not None and qty) else None
    right = 'PUT' if (trade.get('right') == 'P' or str(trade.get('type', '')).upper() == 'PUT') else 'CALL'
    exp = trade.get('exp')
    p.update({
        'asset_type': 'OPTION',
        'underlying_symbol': p['symbol'],
        'contract_id': f"{p['symbol']}|{exp or ''}|{trade.get('strike') if trade.get('strike') is not None else ''}|{'P' if right == 'PUT' else 'C'}",
        'conid': trade.get('conid'),
        'right': right,
        'strike': _f(trade.get('strike')),
        'expiration': exp,
        'dte': _dte(exp),
        'multiplier': mult,
        'quantity': qty,
        'average_cost': round(avg, 4) if avg is not None else None,
        'capital_committed': cost_total,
        'bid': None, 'ask': None, 'mid': None, 'last': None, 'mark': None,
        'market_value': None,
        'unrealized_pnl': None, 'unrealized_pnl_pct': None,
        'realized_pnl': _f(trade.get('pnl')),
        'underlying_price': None,
        'intrinsic_value': None, 'extrinsic_value': None, 'breakeven': None,
        'spread_absolute': None, 'spread_pct': None,
        'volume': None, 'open_interest': None, 'volume_oi_ratio': None,
        'iv': None, 'iv_rank': None, 'iv_percentile': None,
        'realized_volatility': None,
        'delta': None, 'gamma': None, 'theta': None, 'vega': None,
        'greeks_source': 'UNAVAILABLE',
        'entry_underlying': _f(snap.get('spot')),
        'underlying_stop': _f(snap.get('stop')),
        'underlying_tp1': _f(snap.get('tgt')),
        'underlying_tp2': None, 'underlying_tp3': None,
        'estimated_value_at_stop': None, 'estimated_value_at_tp1': None,
        'estimated_value_at_tp2': None, 'estimated_value_at_tp3': None,
        'planned_loss_pct': None, 'remaining_rr': None,
        'time_stop_at': None,
        'earnings_at': None, 'days_to_earnings': None, 'event_risk': [],
        'thesis_text': (snap.get('thesis') or trade.get('note') or None),
        'thesis_health': 'UNKNOWN',
        'decision': None, 'lifecycle_status': p['status'],
        'last_updated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    })
    return p


__all__ = ['SOURCES', 'SOURCE_PRIORITY', 'STOCK_STATUSES', 'OPTION_STATUSES',
           'ANALYTIC_ACTIONS', 'PRIORITIES', 'base_position',
           'stock_position', 'option_position']
