"""vertex.data_sources.ibkr_scheduler — file de requêtes IBKR à priorités (§14).

Aucune connexion ici : le scheduler ordonne, déduplique, cache et borne les
requêtes ; l'exécution réelle est déléguée à un worker injecté (lecture seule).
Objectif : ne jamais saturer le pacing IBKR ni charger toutes les chaînes de
l'univers — pipeline entonnoir (scan → shortlist → finalistes).
"""
from __future__ import annotations

import heapq
import itertools
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable

# Priorités (plus petit = plus urgent), ordre imposé par la constitution §14.
PRIO_OPEN_POSITIONS = 1
PRIO_STOPS = 2
PRIO_ACTIONABLE = 3
PRIO_TRADINGVIEW = 4
PRIO_WATCHLIST = 5
PRIO_SHORTLIST = 6
PRIO_UNIVERSE = 7

DEFAULT_TTL_S = 60.0
DEFAULT_TIMEOUT_S = 45.0          # aligné sur le RequestTimeout IBKR existant
DEFAULT_MAX_RETRIES = 3
DEFAULT_MAX_CONCURRENT = 4
DEFAULT_MAX_MARKET_LINES = 90     # limite de lignes de marché simultanées
CIRCUIT_OPEN_AFTER = 5            # échecs consécutifs → circuit ouvert
CIRCUIT_COOLDOWN_S = 120.0
STALE_REQUEST_S = 300.0           # une requête en file depuis 5 min est annulée


@dataclass(order=True)
class _QueuedRequest:
    priority: int
    seq: int
    key: str = field(compare=False)
    fn: Callable[[], Any] = field(compare=False)
    enqueued_at: float = field(compare=False, default_factory=time.monotonic)
    ttl: float = field(compare=False, default=DEFAULT_TTL_S)


class CircuitOpen(RuntimeError):
    """IBKR en échec répété — circuit ouvert, on refuse les requêtes un moment."""


class IbkrScheduler:
    """File priorisée avec dédup, cache TTL, retry borné et circuit breaker.

    Usage : ``sched.submit('spot:NVDA', PRIO_WATCHLIST, fetch_fn)`` puis
    ``sched.run_pending()`` depuis le worker unique IBKR (l'app garde son
    modèle « un seul worker » anti-blocage).
    """

    def __init__(self, max_concurrent: int = DEFAULT_MAX_CONCURRENT,
                 max_market_lines: int = DEFAULT_MAX_MARKET_LINES,
                 timeout_s: float = DEFAULT_TIMEOUT_S,
                 max_retries: int = DEFAULT_MAX_RETRIES,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._heap: list[_QueuedRequest] = []
        self._queued: set[str] = set()
        self._cache: dict[str, tuple[float, Any]] = {}
        self._lock = threading.Lock()
        self._seq = itertools.count()
        self._clock = clock
        self.max_concurrent = max_concurrent
        self.max_market_lines = max_market_lines
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self._active = 0
        self._consecutive_failures = 0
        self._circuit_open_until = 0.0
        self.metrics = {'submitted': 0, 'deduplicated': 0, 'cache_hits': 0,
                        'executed': 0, 'failures': 0, 'retries': 0,
                        'cancelled_stale': 0, 'circuit_opened': 0}

    # ── état ──────────────────────────────────────────────────────────
    @property
    def circuit_open(self) -> bool:
        return self._clock() < self._circuit_open_until

    def status(self) -> dict:
        with self._lock:
            return {'queue_size': len(self._heap), 'active': self._active,
                    'circuit_open': self.circuit_open,
                    'cache_entries': len(self._cache), 'metrics': dict(self.metrics)}

    # ── soumission ────────────────────────────────────────────────────
    def submit(self, key: str, priority: int, fn: Callable[[], Any],
               ttl: float = DEFAULT_TTL_S) -> bool:
        """Ajoute une requête. Retourne False si dédupliquée ou déjà en cache frais."""
        now = self._clock()
        with self._lock:
            self.metrics['submitted'] += 1
            cached = self._cache.get(key)
            if cached and now - cached[0] < ttl:
                self.metrics['cache_hits'] += 1
                return False
            if key in self._queued:
                self.metrics['deduplicated'] += 1
                return False
            heapq.heappush(self._heap, _QueuedRequest(priority, next(self._seq), key, fn, now, ttl))
            self._queued.add(key)
            return True

    def get_cached(self, key: str, ttl: float = DEFAULT_TTL_S) -> Any | None:
        with self._lock:
            cached = self._cache.get(key)
            if cached and self._clock() - cached[0] < ttl:
                return cached[1]
            return None

    # ── exécution (appelée par le worker unique) ──────────────────────
    def run_pending(self, budget: int | None = None) -> list[tuple[str, Any]]:
        """Exécute jusqu'à `budget` requêtes (défaut max_concurrent). Séquentiel :
        le worker IBKR est unique par conception (anti-blocage)."""
        if self.circuit_open:
            raise CircuitOpen(f'circuit IBKR ouvert encore {self._circuit_open_until - self._clock():.0f}s')
        budget = self.max_concurrent if budget is None else budget
        results: list[tuple[str, Any]] = []
        for _ in range(budget):
            req = self._pop_next()
            if req is None:
                break
            results.append((req.key, self._execute(req)))
        return results

    def _pop_next(self) -> _QueuedRequest | None:
        now = self._clock()
        with self._lock:
            while self._heap:
                req = heapq.heappop(self._heap)
                self._queued.discard(req.key)
                if now - req.enqueued_at > STALE_REQUEST_S:
                    self.metrics['cancelled_stale'] += 1
                    continue  # requête trop ancienne — annulée, le monde a changé
                return req
            return None

    def _execute(self, req: _QueuedRequest) -> Any:
        delay = 1.0
        last_exc: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                with self._lock:
                    self._active += 1
                try:
                    value = req.fn()
                finally:
                    with self._lock:
                        self._active -= 1
                with self._lock:
                    self._cache[req.key] = (self._clock(), value)
                    self.metrics['executed'] += 1
                    self._consecutive_failures = 0
                return value
            except Exception as exc:
                last_exc = exc
                with self._lock:
                    self.metrics['failures'] += 1
                    self._consecutive_failures += 1
                    if self._consecutive_failures >= CIRCUIT_OPEN_AFTER:
                        self._circuit_open_until = self._clock() + CIRCUIT_COOLDOWN_S
                        self.metrics['circuit_opened'] += 1
                        break
                if attempt < self.max_retries - 1:
                    with self._lock:
                        self.metrics['retries'] += 1
                    time.sleep(min(delay, 8.0))
                    delay *= 2
        return {'error': f'{last_exc.__class__.__name__}: {last_exc}'} if last_exc else None
