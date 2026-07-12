"""vertex.positions.alerts — alertes consolidées de positions (§29).

Types canoniques + anti-spam : déduplication par clé (type, position),
cooldown, résolution, réouverture uniquement si l'état a réellement changé.
Une alerte DÉCRIT — elle ne déclenche jamais un ordre.
"""
from __future__ import annotations

import time

TYPES = ('POSITION_INVALIDATED', 'STOP_APPROACHING', 'TARGET_APPROACHING',
         'THESIS_WEAKENING', 'CATALYST_CHANGED', 'EARNINGS_APPROACHING',
         'OPTION_TIME_STOP', 'OPTION_THETA_WARNING', 'OPTION_IV_CRUSH_RISK',
         'OPTION_DTE_WARNING', 'OPTION_LIQUIDITY_WARNING',
         'PORTFOLIO_CONCENTRATION', 'PORTFOLIO_DRAWDOWN', 'DECISION_CHANGED',
         'DATA_STALE', 'DATA_CONFLICT')

_STATUS_TO_ALERT = {
    'INVALIDATED': 'POSITION_INVALIDATED',
    'UNDERLYING_INVALIDATED': 'POSITION_INVALIDATED',
    'STOP_APPROACHING': 'STOP_APPROACHING',
    'UNDERLYING_STOP_APPROACHING': 'STOP_APPROACHING',
    'TARGET_APPROACHING': 'TARGET_APPROACHING',
    'TARGET_REACHED': 'TARGET_APPROACHING',
    'THETA_WARNING': 'OPTION_THETA_WARNING',
    'DTE_WARNING': 'OPTION_DTE_WARNING',
    'EARNINGS_RISK': 'EARNINGS_APPROACHING',
    'SPREAD_WARNING': 'OPTION_LIQUIDITY_WARNING',
    'LIQUIDITY_WARNING': 'OPTION_LIQUIDITY_WARNING',
    'IV_CRUSH_RISK': 'OPTION_IV_CRUSH_RISK',
    'TIME_STOP_APPROACHING': 'OPTION_TIME_STOP',
    'DATA_REPAIR_REQUIRED': 'DATA_CONFLICT',
}

COOLDOWN_S = 1800


class PositionAlerts:
    def __init__(self):
        self._active: dict[tuple, dict] = {}

    def evaluate(self, positions: list[dict], now: float | None = None) -> list[dict]:
        """Retourne les NOUVELLES alertes (dédupliquées/cooldown)."""
        now = now or time.time()
        fresh = []
        for p in positions:
            atype = _STATUS_TO_ALERT.get(p.get('lifecycle_status') or '')
            if (p.get('data_quality') or {}).get('overall') == 'STALE':
                atype = atype or 'DATA_STALE'
            if not atype:
                # résolution : l'état déclencheur a disparu
                for key in [k for k in self._active if k[1] == p.get('position_id')]:
                    self._active[key]['resolved'] = True
                continue
            key = (atype, p.get('position_id'))
            cur = self._active.get(key)
            if cur and not cur.get('resolved') and now - cur['ts'] < COOLDOWN_S:
                continue                          # dédup + cooldown
            if cur and cur.get('resolved') is not True and now - cur['ts'] < COOLDOWN_S:
                continue
            alert = {'type': atype, 'position_id': p.get('position_id'),
                     'symbol': p.get('symbol'), 'status': p.get('lifecycle_status'),
                     'ts': now, 'resolved': False,
                     'detail': {'pl_pct': p.get('unrealized_pnl_pct'),
                                'dte': p.get('dte'),
                                'priority': p.get('priority')}}
            self._active[key] = alert
            fresh.append(alert)
        return fresh

    def active(self) -> list[dict]:
        return [a for a in self._active.values() if not a.get('resolved')]


ALERTS = PositionAlerts()

__all__ = ['TYPES', 'PositionAlerts', 'ALERTS']
