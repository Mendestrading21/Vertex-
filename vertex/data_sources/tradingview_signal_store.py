"""vertex.data_sources.tradingview_signal_store — stockage des signaux TradingView.

Un signal TradingView est une INFORMATION : il déclenche une réévaluation,
jamais un achat (§32). Store en mémoire avec dédup + anti-replay, persistable.
"""
from __future__ import annotations

import threading
import time
from collections import deque

ALLOWED_SIGNALS = (
    'CORRECTION_DEEP', 'SUPPORT_RECLAIM', 'BREAKOUT_CONFIRMED', 'BREAKOUT_RETEST',
    'MOMENTUM_ACCELERATION', 'VOLUME_EXPANSION', 'VOLATILITY_COMPRESSION',
    'VOLATILITY_EXPANSION', 'TREND_ALIGNMENT', 'FAILED_BREAKOUT', 'THESIS_INVALIDATION',
)

MAX_SIGNALS = 500
REPLAY_WINDOW_S = 15 * 60      # un timestamp plus vieux que 15 min est rejeté
DEDUP_WINDOW_S = 10 * 60       # même (symbole, signal) sous 10 min = doublon


class TradingViewSignalStore:
    def __init__(self, clock=time.time) -> None:
        self._signals: deque = deque(maxlen=MAX_SIGNALS)
        self._seen_keys: dict[str, float] = {}
        self._lock = threading.Lock()
        self._clock = clock
        self.metrics = {'accepted': 0, 'rejected_replay': 0, 'rejected_duplicate': 0,
                        'rejected_invalid': 0}

    def add(self, symbol: str, signal: str, event_ts: float,
            payload: dict | None = None) -> dict:
        """Valide et stocke. Retourne {'accepted': bool, 'reason': str}."""
        now = self._clock()
        symbol = (symbol or '').strip().upper()
        signal = (signal or '').strip().upper()
        if not symbol or not symbol.isalnum() or len(symbol) > 8:
            self.metrics['rejected_invalid'] += 1
            return {'accepted': False, 'reason': 'symbole invalide'}
        if signal not in ALLOWED_SIGNALS:
            self.metrics['rejected_invalid'] += 1
            return {'accepted': False, 'reason': f'signal inconnu: {signal}'}
        try:
            event_ts = float(event_ts)
        except (TypeError, ValueError):
            self.metrics['rejected_invalid'] += 1
            return {'accepted': False, 'reason': 'timestamp invalide'}
        if event_ts > now + 120:
            self.metrics['rejected_invalid'] += 1
            return {'accepted': False, 'reason': 'timestamp dans le futur'}
        if now - event_ts > REPLAY_WINDOW_S:
            self.metrics['rejected_replay'] += 1
            return {'accepted': False, 'reason': 'timestamp trop ancien (anti-replay)'}
        key = f'{symbol}:{signal}'
        with self._lock:
            last = self._seen_keys.get(key)
            if last is not None and now - last < DEDUP_WINDOW_S:
                self.metrics['rejected_duplicate'] += 1
                return {'accepted': False, 'reason': 'doublon (fenêtre de dédup)'}
            self._seen_keys[key] = now
            entry = {'symbol': symbol, 'signal': signal, 'event_ts': event_ts,
                     'received_ts': now, 'payload': dict(payload or {}),
                     'action': 'REEVALUATE'}  # jamais un achat
            self._signals.append(entry)
            self.metrics['accepted'] += 1
        return {'accepted': True, 'reason': 'ok', 'entry': entry}

    def recent(self, symbol: str | None = None, limit: int = 50) -> list[dict]:
        with self._lock:
            items = list(self._signals)
        if symbol:
            items = [s for s in items if s['symbol'] == symbol.upper()]
        return items[-limit:]

    def status(self) -> dict:
        with self._lock:
            return {'stored': len(self._signals), 'metrics': dict(self.metrics)}


# Store partagé de l'app (instancié une fois, consommé par le webhook + moteurs)
SIGNAL_STORE = TradingViewSignalStore()
