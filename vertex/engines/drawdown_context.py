"""Contexte de drawdown descriptif sur clôtures canoniques, sans prévision."""
from __future__ import annotations


def build(closes, *, window_sessions=63, minimum_observations=21):
    values = []
    for close in closes or []:
        try:
            value = float(close)
        except (TypeError, ValueError):
            return {'available': False, 'status': 'INSUFFICIENT_SERIES',
                    'reason': 'clôture non numérique — drawdown non calculé', 'read_only': True}
        if value <= 0:
            return {'available': False, 'status': 'INSUFFICIENT_SERIES',
                    'reason': 'clôture non positive — drawdown non calculé', 'read_only': True}
        values.append(value)
    values = values[-int(window_sessions):]
    if len(values) < int(minimum_observations):
        return {'available': False, 'status': 'INSUFFICIENT_SERIES',
                'observations': len(values), 'minimum_observations': int(minimum_observations),
                'read_only': True, 'reason': 'historique de clôtures insuffisant'}
    peak = values[0]
    drawdowns = []
    for value in values:
        peak = max(peak, value)
        drawdowns.append((value / peak - 1.0) * 100.0)
    current = drawdowns[-1]
    return {
        'available': True,
        'status': 'AT_PEAK' if current >= -1e-9 else 'IN_DRAWDOWN',
        'window_sessions': int(window_sessions), 'observations': len(values),
        'last_close': round(values[-1], 6), 'peak_close': round(max(values), 6),
        'current_drawdown_pct': round(current, 2), 'max_drawdown_pct': round(min(drawdowns), 2),
        'read_only': True,
        'note': 'constat de drawdown sur clôtures canoniques ; ni prévision ni signal d’ordre',
    }


__all__ = ['build']
