"""Contexte d’anomalies homogène pour les chemins de décision Skyler.

Le moteur enrichi n’est activé que si une série OHLCV complète est réellement
présente. Sinon, le scan de clôtures historique reste le repli explicite ; aucun
prix, volume ou benchmark n’est reconstruit ou inventé.
"""
from __future__ import annotations

from vertex.data import series as _series
from vertex.engines import anomaly as _basic
from vertex.anomalies.stock_anomalies import detect_stock_anomalies


def _bars(detail):
    raw = (detail or {}).get('series') or {}
    fields = ('open', 'high', 'low', 'close', 'volume')
    arrays = {key: raw.get(key) for key in fields}
    if not all(isinstance(values, (list, tuple)) for values in arrays.values()):
        return []
    lengths = {len(values) for values in arrays.values()}
    if len(lengths) != 1 or not lengths or next(iter(lengths)) < 30:
        return []
    out = []
    for index in range(next(iter(lengths))):
        row = {key: arrays[key][index] for key in fields}
        try:
            if any(float(row[key]) <= 0 for key in ('open', 'high', 'low', 'close')):
                return []
        except (TypeError, ValueError):
            return []
        out.append(row)
    return out


def build(symbol, detail, benchmark_detail=None):
    """Retourne un format compatible avec Skyler, avec provenance explicite."""
    closes, source = _series.closes(detail)
    baseline = _basic.scan(closes) if closes else {'available': False, 'events': []}
    bars = _bars(detail)
    if not bars:
        baseline['available'] = bool(closes)
        baseline['provenance'] = 'CLOSE_ONLY'
        baseline['limitations'] = ['OHLCV complet absent — analyse enrichie non exécutée']
        return baseline
    context = {}
    benchmark, _ = _series.closes(benchmark_detail)
    if benchmark:
        context['benchmark_closes'] = benchmark
    enriched = [event.to_dict() for event in detect_stock_anomalies(symbol, bars, context=context)]
    return {
        **baseline,
        'available': True,
        'events': enriched,
        'provenance': 'OHLCV_ENRICHED',
        'series_source': source,
        'limitations': ([] if benchmark else ['benchmark absent — modules relatifs non exécutés']),
    }


__all__ = ['build']
