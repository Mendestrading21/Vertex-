"""vertex.alerts.engine — alertes intelligentes (§35).

Niveaux : RADAR / WATCH / ACTIONABLE / INVALIDATED / DATA_WARNING / RISK_WARNING.
Une alerte ACTIONABLE exige le dossier complet (données fraîches, sources
réconciliées, fondamental, catalyseur, setup, timing, invalidation, simulation,
liquidité, R:R, portefeuille compatible, hard gates). Anti-spam : cooldown,
déduplication, historique, changement de niveau motivé, expiration.
"""
from __future__ import annotations

import threading
import time
from collections import deque

LEVELS = ('RADAR', 'WATCH', 'ACTIONABLE', 'INVALIDATED', 'DATA_WARNING', 'RISK_WARNING')

ACTIONABLE_REQUIREMENTS = (
    'data_fresh', 'sources_reconciled', 'fundamental_ok', 'catalyst_present',
    'setup_present', 'timing_ok', 'invalidation_defined', 'simulation_done',
    'liquidity_ok', 'reward_risk_ok', 'portfolio_compatible', 'hard_gates_passed',
)

COOLDOWN_S = 30 * 60          # même (symbole, niveau) silencieux 30 min
DEFAULT_EXPIRY_S = 6 * 3600   # une alerte expire d'elle-même
MAX_HISTORY = 500


class AlertEngine:
    def __init__(self, clock=time.time) -> None:
        self._clock = clock
        self._lock = threading.Lock()
        self._history: deque = deque(maxlen=MAX_HISTORY)
        self._last_emitted: dict[tuple, float] = {}
        self._current_level: dict[str, str] = {}
        self.metrics = {'emitted': 0, 'suppressed_cooldown': 0,
                        'suppressed_duplicate': 0, 'rejected_incomplete': 0}

    def raise_alert(self, symbol: str, level: str, reason: str,
                    requirements: dict | None = None,
                    expiry_s: float = DEFAULT_EXPIRY_S) -> dict:
        symbol = symbol.upper()
        if level not in LEVELS:
            return {'emitted': False, 'error': f'niveau inconnu: {level}'}
        if level == 'ACTIONABLE':
            reqs = requirements or {}
            missing = [r for r in ACTIONABLE_REQUIREMENTS if not reqs.get(r)]
            if missing:
                self.metrics['rejected_incomplete'] += 1
                return {'emitted': False,
                        'error': f'ACTIONABLE refusé — exigences manquantes: {missing}'}
        now = self._clock()
        key = (symbol, level)
        with self._lock:
            prev_level = self._current_level.get(symbol)
            if prev_level == level:
                last = self._last_emitted.get(key, 0)
                if now - last < COOLDOWN_S:
                    self.metrics['suppressed_cooldown'] += 1
                    return {'emitted': False, 'error': 'cooldown actif (anti-spam)'}
                self.metrics['suppressed_duplicate'] += 1
                return {'emitted': False, 'error': 'niveau inchangé — pas de re-notification'}
            alert = {'symbol': symbol, 'level': level, 'reason': reason,
                     'previous_level': prev_level, 'ts': now,
                     'expires_at': now + expiry_s}
            self._history.append(alert)
            self._last_emitted[key] = now
            self._current_level[symbol] = level
            self.metrics['emitted'] += 1
            return {'emitted': True, 'alert': alert}

    def active_alerts(self) -> list[dict]:
        now = self._clock()
        with self._lock:
            return [a for a in self._history if a['expires_at'] > now
                    and self._current_level.get(a['symbol']) == a['level']]

    def history(self, symbol: str | None = None, limit: int = 100) -> list[dict]:
        with self._lock:
            items = list(self._history)
        if symbol:
            items = [a for a in items if a['symbol'] == symbol.upper()]
        return items[-limit:]

    def status(self) -> dict:
        return {'active': len(self.active_alerts()), 'metrics': dict(self.metrics)}
