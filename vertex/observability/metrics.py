"""vertex.observability.metrics — compteurs et jauges du Strategy OS (§37)."""
from __future__ import annotations

import threading
import time


class Metrics:
    """Registre simple thread-safe : compteurs, jauges, durées (aucun secret)."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: dict[str, float] = {}
        self._gauges: dict[str, float] = {}
        self._timings: dict[str, list] = {}

    def inc(self, name: str, value: float = 1) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + value

    def gauge(self, name: str, value: float) -> None:
        with self._lock:
            self._gauges[name] = value

    def timing(self, name: str, ms: float) -> None:
        with self._lock:
            samples = self._timings.setdefault(name, [])
            samples.append(ms)
            if len(samples) > 200:
                del samples[:-200]

    def timer(self, name: str):
        metrics = self

        class _Timer:
            def __enter__(self):
                self._t0 = time.monotonic()
                return self

            def __exit__(self, *exc):
                metrics.timing(name, (time.monotonic() - self._t0) * 1000)
                return False
        return _Timer()

    def snapshot(self) -> dict:
        with self._lock:
            timings = {}
            for name, samples in self._timings.items():
                if samples:
                    s = sorted(samples)
                    timings[name] = {'n': len(s), 'p50_ms': round(s[len(s) // 2], 1),
                                     'p95_ms': round(s[int(len(s) * 0.95) - 1], 1),
                                     'max_ms': round(s[-1], 1)}
            return {'counters': dict(self._counters), 'gauges': dict(self._gauges),
                    'timings': timings}


METRICS = Metrics()
