"""Volume relatif observé depuis la série de scan canonique, sans imputation."""
from __future__ import annotations

import math


def _volume(value):
    if isinstance(value, bool):
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) and value > 0 else None


def _median(values):
    values = sorted(values)
    middle = len(values) // 2
    return values[middle] if len(values) % 2 else (values[middle - 1] + values[middle]) / 2.0


def build(detail, *, lookback=20):
    """Compare le volume de la dernière séance au médian des séances précédentes.

    Une séance absente ou invalide n'est jamais remplacée. Le contexte exige une
    fenêtre antérieure complète afin de ne pas sélectionner des observations.
    """
    series = (detail or {}).get('series') or {}
    raw = series.get('volume')
    coverage = {'lookback_sessions': lookback, 'volume_series_points': len(raw) if isinstance(raw, (list, tuple)) else 0,
                'prior_valid_count': 0, 'required_prior_count': lookback}
    if not isinstance(raw, (list, tuple)) or len(raw) < lookback + 1:
        return {'available': False, 'status': 'INSUFFICIENT_VOLUME_HISTORY', 'coverage': coverage,
                'read_only': True, 'reason': 'au moins 21 volumes de séances sont requis'}
    current = _volume(raw[-1])
    prior = [_volume(value) for value in raw[-lookback - 1:-1]]
    valid_prior = [value for value in prior if value is not None]
    coverage['prior_valid_count'] = len(valid_prior)
    if current is None:
        return {'available': False, 'status': 'CURRENT_VOLUME_UNAVAILABLE', 'coverage': coverage,
                'read_only': True, 'reason': 'volume de la dernière séance absent, nul ou invalide'}
    if len(valid_prior) != lookback:
        return {'available': False, 'status': 'INCOMPLETE_PRIOR_VOLUME_WINDOW', 'coverage': coverage,
                'read_only': True, 'reason': 'fenêtre antérieure de volume incomplète'}
    median = _median(valid_prior)
    return {'available': True, 'status': 'OBSERVED_RELATIVE_VOLUME', 'coverage': coverage,
            'current_volume': int(current), 'prior_median_volume': round(median, 2),
            'current_to_prior_median_ratio': round(current / median, 4), 'read_only': True,
            'note': 'volume observé comparé à la médiane des 20 séances précédentes ; sans prévision'}


__all__ = ['build']
