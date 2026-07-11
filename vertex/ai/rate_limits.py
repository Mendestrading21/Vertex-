"""vertex.ai.rate_limits — limitation de débit des appels IA."""
from __future__ import annotations

import threading
import time


class RateLimiter:
    """Fenêtre glissante simple : max_calls par window_s."""

    def __init__(self, max_calls: int = 20, window_s: float = 60.0,
                 clock=time.monotonic) -> None:
        self.max_calls = max_calls
        self.window_s = window_s
        self._calls: list[float] = []
        self._lock = threading.Lock()
        self._clock = clock

    def allow(self) -> bool:
        now = self._clock()
        with self._lock:
            self._calls = [t for t in self._calls if now - t < self.window_s]
            if len(self._calls) >= self.max_calls:
                return False
            self._calls.append(now)
            return True

    def status(self) -> dict:
        now = self._clock()
        with self._lock:
            active = [t for t in self._calls if now - t < self.window_s]
            return {'used': len(active), 'max': self.max_calls, 'window_s': self.window_s}
