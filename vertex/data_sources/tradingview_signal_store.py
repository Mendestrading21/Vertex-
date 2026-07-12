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
SIGNAL_FRESH_S = 6 * 3600      # un signal reçu il y a > 6 h est « rassis » (côté serveur)


class TradingViewSignalStore:
    def __init__(self, clock=time.time) -> None:
        self._signals: deque = deque(maxlen=MAX_SIGNALS)
        self._seen_keys: dict[str, float] = {}
        self._lock = threading.Lock()
        self._clock = clock
        self._configured = False   # le secret webhook est-il réellement défini ?
        self.metrics = {'accepted': 0, 'rejected_replay': 0, 'rejected_duplicate': 0,
                        'rejected_invalid': 0}

    def set_configured(self, flag: bool) -> None:
        """Déclaré par le blueprint : le webhook a-t-il un secret actif ?

        Permet à status() de distinguer « non configuré » de « configuré, en
        attente d'un 1er signal » — sinon l'UI ment sur l'état de connexion."""
        self._configured = bool(flag)

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
            # Purge des clés de dédup expirées (évite une croissance mémoire non bornée).
            if len(self._seen_keys) > MAX_SIGNALS:
                self._seen_keys = {k: t for k, t in self._seen_keys.items()
                                   if now - t < DEDUP_WINDOW_S}
            self._seen_keys[key] = now
            entry = {'symbol': symbol, 'signal': signal, 'event_ts': event_ts,
                     'received_ts': now, 'payload': dict(payload or {}),
                     'action': 'REEVALUATE'}  # jamais un achat
            self._signals.append(entry)
            self.metrics['accepted'] += 1
        return {'accepted': True, 'reason': 'ok', 'entry': entry}

    def recent(self, symbol: str | None = None, limit: int = 50) -> list[dict]:
        """Signaux récents, chacun enrichi de son âge serveur (age_s) + fraîcheur."""
        now = self._clock()
        with self._lock:
            items = list(self._signals)
        if symbol:
            items = [s for s in items if s['symbol'] == symbol.upper()]
        out = []
        for s in items[-limit:]:
            age = round(now - s.get('received_ts', now), 1)
            e = dict(s)
            e['age_s'] = age
            e['fresh'] = age <= SIGNAL_FRESH_S
            out.append(e)
        return out

    def status(self) -> dict:
        """État honnête : configuré ≠ reçu. Distingue off / en attente / actif."""
        now = self._clock()
        with self._lock:
            n = len(self._signals)
            newest = self._signals[-1]['received_ts'] if n else None
            fresh_n = sum(1 for s in self._signals
                          if now - s.get('received_ts', now) <= SIGNAL_FRESH_S)
            metrics = dict(self.metrics)
            configured = self._configured
        newest_age = round(now - newest, 1) if newest is not None else None
        state = ('DISABLED' if not configured
                 else 'ACTIVE' if fresh_n else 'WAITING')
        return {'stored': n, 'fresh': fresh_n, 'configured': configured,
                'state': state, 'newest_age_s': newest_age, 'metrics': metrics}


# Store partagé de l'app (instancié une fois, consommé par le webhook + moteurs)
SIGNAL_STORE = TradingViewSignalStore()
