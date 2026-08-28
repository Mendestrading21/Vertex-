"""Télémétrie locale et non sensible des routes Vertex."""
from __future__ import annotations

from collections import defaultdict, deque
from threading import Lock

MAX_SAMPLES = 256
_LOCK = Lock()
_SAMPLES = deque(maxlen=MAX_SAMPLES)


def record(endpoint, status_code, elapsed_ms):
    """Enregistre uniquement endpoint Flask, statut et durée — jamais chemin, IP ou corps."""
    try:
        sample = {
            'endpoint': str(endpoint or 'unmatched')[:96],
            'status_code': int(status_code),
            'elapsed_ms': round(max(0.0, float(elapsed_ms)), 3),
        }
    except (TypeError, ValueError):
        return
    with _LOCK:
        _SAMPLES.append(sample)


def summary():
    with _LOCK:
        samples = list(_SAMPLES)
    grouped = defaultdict(list)
    for row in samples:
        grouped[row['endpoint']].append(row)
    endpoints = {}
    for endpoint, rows in sorted(grouped.items()):
        values = sorted(row['elapsed_ms'] for row in rows)
        count = len(values)
        endpoints[endpoint] = {
            'count': count,
            'mean_ms': round(sum(values) / count, 3),
            'p50_ms': values[(count - 1) // 2],
            'p95_ms': values[min(count - 1, max(0, int(count * .95) - 1))],
            #  Lot 8 — p99 : c'est elle qui voit les pannes. p95 lisse encore
            #  un appel sur vingt, et c'est precisement celui-la (la chaine a
            #  75 s derriere la file unique) qui fait l'experience reelle.
            'p99_ms': values[min(count - 1, max(0, int(count * .99) - 1))],
            'max_ms': values[-1],
            'error_count': sum(1 for row in rows if row['status_code'] >= 400),
        }
    return {'read_only': True, 'max_samples': MAX_SAMPLES,
            'sample_count': len(samples), 'endpoints': endpoints}


def reset_for_test():
    with _LOCK:
        _SAMPLES.clear()


__all__ = ['record', 'summary', 'reset_for_test', 'MAX_SAMPLES']
