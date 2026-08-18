"""Performance relative descriptive sur séries canoniques alignées, sans prédiction."""
from __future__ import annotations


def _points(series):
    if not isinstance(series, dict):
        return None
    dates, closes = series.get('dates'), series.get('close')
    if not isinstance(dates, list) or not isinstance(closes, list) or len(dates) != len(closes):
        return None
    out, order = {}, []
    for date, close in zip(dates, closes):
        try:
            value = float(close)
        except (TypeError, ValueError):
            continue
        if date and value > 0:
            key = str(date)
            out[key] = value
            order.append(key)
    return out, order


def build(asset_series, benchmark_series, *, windows=(20, 63)):
    asset = _points(asset_series)
    benchmark = _points(benchmark_series)
    if asset is None or benchmark is None:
        return {'available': False, 'status': 'INSUFFICIENT_ALIGNED_SERIES',
                'read_only': True, 'reason': 'séries datées canoniques absentes ou invalides'}
    asset_values, asset_order = asset
    benchmark_values, _benchmark_order = benchmark
    common = [date for date in asset_order if date in benchmark_values]
    if len(common) < 2:
        return {'available': False, 'status': 'INSUFFICIENT_ALIGNED_SERIES',
                'common_observations': len(common), 'read_only': True,
                'reason': 'moins de deux clôtures datées communes avec le benchmark'}
    measures = []
    for window in windows:
        window = int(window)
        if len(common) < window + 1:
            continue
        start, end = common[-window - 1], common[-1]
        asset_return = (asset_values[end] / asset_values[start] - 1.0) * 100.0
        benchmark_return = (benchmark_values[end] / benchmark_values[start] - 1.0) * 100.0
        measures.append({'window_sessions': window, 'asset_return_pct': round(asset_return, 2),
                         'benchmark_return_pct': round(benchmark_return, 2),
                         'excess_return_pct': round(asset_return - benchmark_return, 2)})
    if not measures:
        return {'available': False, 'status': 'INSUFFICIENT_ALIGNED_SERIES',
                'common_observations': len(common), 'required_windows': list(windows),
                'read_only': True, 'reason': 'historique commun insuffisant pour les fenêtres déclarées'}
    return {'available': True, 'status': 'OBSERVED_RELATIVE_PERFORMANCE',
            'benchmark': 'SPY', 'common_observations': len(common), 'windows': measures,
            'read_only': True,
            'note': 'performance relative observée sur clôtures datées communes ; ni prévision ni signal d’ordre'}


__all__ = ['build']
