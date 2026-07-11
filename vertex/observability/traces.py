"""vertex.observability.traces — traces d'exécution bornées en mémoire."""
import threading
import time
from collections import deque

MAX_TRACES = 300


class Traces:
    def __init__(self):
        self._items = deque(maxlen=MAX_TRACES)
        self._lock = threading.Lock()

    def add(self, kind: str, detail: str, ok: bool = True):
        with self._lock:
            self._items.append({'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                'kind': kind, 'detail': str(detail)[:300], 'ok': ok})

    def recent(self, limit: int = 100):
        with self._lock:
            return list(self._items)[-limit:]


TRACES = Traces()
