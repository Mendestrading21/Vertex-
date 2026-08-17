"""Validation descriptive des séries datées canoniques, sans interpolation."""
from datetime import date
import math


def assess(series, *, minimum=2):
    dates = (series or {}).get('dates')
    closes = (series or {}).get('close')
    if not isinstance(dates, list) or not isinstance(closes, list) or len(dates) != len(closes):
        return {'available': False, 'status': 'TEMPORAL_EVIDENCE_REQUIRED',
                'reason': 'dates et clôtures doivent être des listes de même longueur', 'read_only': True}
    if len(dates) < minimum:
        return {'available': False, 'status': 'INSUFFICIENT_SAMPLE',
                'reason': 'nombre de points datés insuffisant', 'read_only': True}
    parsed = []
    for raw_day, raw_close in zip(dates, closes):
        try:
            day, close = date.fromisoformat(str(raw_day)[:10]), float(raw_close)
        except (TypeError, ValueError):
            return {'available': False, 'status': 'TEMPORAL_EVIDENCE_REQUIRED',
                    'reason': 'date ou clôture invalide', 'read_only': True}
        if not math.isfinite(close) or close <= 0:
            return {'available': False, 'status': 'TEMPORAL_EVIDENCE_REQUIRED',
                    'reason': 'clôture non positive ou non finie', 'read_only': True}
        parsed.append(day)
    if any(b <= a for a, b in zip(parsed, parsed[1:])):
        return {'available': False, 'status': 'TEMPORAL_EVIDENCE_REQUIRED',
                'reason': 'dates non strictement croissantes', 'read_only': True}
    gaps = sum((b - a).days > 4 for a, b in zip(parsed, parsed[1:]))
    return {'available': True, 'status': 'TEMPORAL_EVIDENCE_AVAILABLE', 'read_only': True,
            'n_observations': len(parsed), 'start': parsed[0].isoformat(), 'end': parsed[-1].isoformat(),
            'long_gaps': gaps, 'no_interpolation': True}
