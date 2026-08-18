"""Volatilité baissière descriptive sur clôtures canoniques, sans prévision."""
from __future__ import annotations

import math


def build(closes, *, window_sessions=20, minimum_observations=21):
    values = []
    for close in closes or []:
        try:
            value = float(close)
        except (TypeError, ValueError):
            return {'available': False, 'status': 'INSUFFICIENT_SERIES',
                    'reason': 'clôture non numérique — volatilité baissière non calculée', 'read_only': True}
        if value <= 0:
            return {'available': False, 'status': 'INSUFFICIENT_SERIES',
                    'reason': 'clôture non positive — volatilité baissière non calculée', 'read_only': True}
        values.append(value)
    values = values[-int(window_sessions) - 1:]
    if len(values) < int(minimum_observations):
        return {'available': False, 'status': 'INSUFFICIENT_SERIES',
                'observations': len(values), 'minimum_observations': int(minimum_observations),
                'read_only': True, 'reason': 'historique de clôtures insuffisant'}
    returns = [values[index] / values[index - 1] - 1.0 for index in range(1, len(values))]
    downside = [min(0.0, value) for value in returns]
    semi_deviation = math.sqrt(sum(value * value for value in downside) / len(downside)) * math.sqrt(252) * 100.0
    negatives = sum(1 for value in returns if value < 0)
    return {
        'available': True,
        'status': 'NO_NEGATIVE_RETURNS' if negatives == 0 else 'OBSERVED_DOWNSIDE_VOLATILITY',
        'window_sessions': int(window_sessions), 'observations': len(values),
        'return_observations': len(returns), 'negative_return_count': negatives,
        'negative_return_share_pct': round(100.0 * negatives / len(returns), 2),
        'downside_deviation_annual_pct': round(semi_deviation, 2),
        'read_only': True,
        'note': 'semi-déviation annualisée des rendements observés ; ni prévision ni signal d’ordre',
    }


__all__ = ['build']
