"""vertex.ai.audit — journal des appels IA (sans secret, borné en mémoire)."""
from __future__ import annotations

import threading
import time
from collections import deque

MAX_ENTRIES = 200


class AIAudit:
    def __init__(self) -> None:
        self._entries: deque = deque(maxlen=MAX_ENTRIES)
        self._lock = threading.Lock()

    def record(self, *, symbol: str, source: str, ok: bool, errors: list | None = None,
               duration_ms: float | None = None, model: str = '') -> None:
        with self._lock:
            self._entries.append({
                'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'symbol': symbol, 'source': source, 'ok': ok,
                'errors': list(errors or [])[:5], 'duration_ms': duration_ms,
                'model': model})

    def recent(self, limit: int = 50) -> list[dict]:
        with self._lock:
            return list(self._entries)[-limit:]

    def stats(self) -> dict:
        with self._lock:
            entries = list(self._entries)
        ok = sum(1 for e in entries if e['ok'])
        fallback = sum(1 for e in entries if e['source'] == 'deterministic-fallback')
        return {'total': len(entries), 'ok': ok, 'fallbacks': fallback}


AUDIT = AIAudit()
