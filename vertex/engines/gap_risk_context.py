"""Gaps ouverture versus clôture observés, sans prévision ni substitution OHLC."""
from __future__ import annotations


def build(detail, *, window_sessions=20, minimum_observations=21, material_gap_pct=2.0):
    series = (detail or {}).get('series') or {}
    opens, closes = series.get('open'), series.get('close')
    if not isinstance(opens, (list, tuple)) or not isinstance(closes, (list, tuple)) or len(opens) != len(closes):
        return {'available': False, 'status': 'INSUFFICIENT_OHLC', 'read_only': True,
                'reason': 'ouvertures et clôtures canoniques absentes ou non alignées'}
    pairs = []
    for opening, prior_close in zip(opens[1:], closes[:-1]):
        try:
            opening, prior_close = float(opening), float(prior_close)
        except (TypeError, ValueError):
            return {'available': False, 'status': 'INSUFFICIENT_OHLC', 'read_only': True,
                    'reason': 'OHLC non numérique — gaps non calculés'}
        if opening <= 0 or prior_close <= 0:
            return {'available': False, 'status': 'INSUFFICIENT_OHLC', 'read_only': True,
                    'reason': 'OHLC non positif — gaps non calculés'}
        pairs.append((opening / prior_close - 1.0) * 100.0)
    pairs = pairs[-int(window_sessions):]
    if len(pairs) < int(minimum_observations) - 1:
        return {'available': False, 'status': 'INSUFFICIENT_OHLC', 'read_only': True,
                'observations': len(pairs) + 1, 'minimum_observations': int(minimum_observations),
                'reason': 'historique OHLC insuffisant pour les gaps observés'}
    material = [gap for gap in pairs if abs(gap) >= float(material_gap_pct)]
    return {'available': True, 'status': 'OBSERVED_GAPS', 'window_sessions': int(window_sessions),
            'observations': len(pairs) + 1, 'latest_gap_pct': round(pairs[-1], 2),
            'max_abs_gap_pct': round(max(abs(gap) for gap in pairs), 2),
            'material_gap_threshold_pct': float(material_gap_pct),
            'material_gap_count': len(material),
            'material_gap_share_pct': round(100.0 * len(material) / len(pairs), 2),
            'read_only': True,
            'note': 'gaps ouverture/clôture observés ; ni prévision ni signal d’ordre'}


__all__ = ['build']
