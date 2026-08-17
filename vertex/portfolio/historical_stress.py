"""Stress test historique déterministe de portefeuille en lecture seule.

Le module ne fabrique aucun choc prospectif. Il agrège les rendements réellement
observés de toutes les positions couvertes, sur leurs séances communes datées,
afin d’exposer la pire journée, le pire intervalle de cinq séances et le repli
historique observé. Il ne produit ni ordre, ni taille d’ordre, ni allocation.
"""
from __future__ import annotations

import math


MIN_COMMON_SESSIONS = 31
ROLLING_SESSIONS = 5


def _number(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) and value > 0 else None


def _series_points(series):
    dates = (series or {}).get('dates')
    closes = (series or {}).get('close')
    if not isinstance(dates, list) or not isinstance(closes, list) or len(dates) != len(closes):
        return {}
    points = {}
    for day, close in zip(dates, closes):
        value = _number(close)
        if day and value is not None:
            points[str(day)] = value
    return points


def _unavailable(status, reason, *, symbols=None, missing_symbols=None):
    return {'available': False, 'status': status, 'reason': reason,
            'symbols': list(symbols or []), 'missing_symbols': list(missing_symbols or []),
            'read_only': True, 'never_triggers_orders': True}


def assess(weights_pct, series_by_symbol, *, minimum_sessions=MIN_COMMON_SESSIONS):
    """Construit un stress historique seulement si toutes les positions sont couvertes.

    Les poids sont ceux déjà valorisés dans le contexte portefeuille. Une série
    sans dates, une valeur non finie ou moins de 31 séances communes empêchent
    toute estimation : un résultat indisponible est plus honnête qu’un panier
    partiellement stressé présenté comme complet.
    """
    weights_raw = weights_pct if isinstance(weights_pct, dict) else {}
    weights = {}
    for symbol, value in weights_raw.items():
        try:
            weight = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(weight) and weight > 0:
            weights[str(symbol)] = weight
    symbols = sorted(weights)
    if len(symbols) < 2:
        return _unavailable('INSUFFICIENT_POSITIONS', 'au moins deux positions pondérées sont requises', symbols=symbols)
    total_weight = sum(weights.values())
    if total_weight <= 0:
        return _unavailable('INVALID_WEIGHTS', 'poids portefeuille non exploitables', symbols=symbols)
    normalized = {symbol: weight / total_weight for symbol, weight in weights.items()}

    points = {symbol: _series_points((series_by_symbol or {}).get(symbol)) for symbol in symbols}
    missing = [symbol for symbol in symbols if len(points[symbol]) < minimum_sessions]
    if missing:
        return _unavailable('TEMPORAL_EVIDENCE_REQUIRED',
                            'séries datées complètes insuffisantes pour toutes les positions',
                            symbols=symbols, missing_symbols=missing)
    common = set.intersection(*(set(points[symbol]) for symbol in symbols))
    if len(common) < minimum_sessions:
        return _unavailable('TEMPORAL_EVIDENCE_REQUIRED',
                            'moins de %d séances communes datées entre les positions' % minimum_sessions,
                            symbols=symbols)
    dates = sorted(common)
    daily = []
    for previous_day, day in zip(dates, dates[1:]):
        contributions = {}
        valid = True
        for symbol in symbols:
            previous, current = points[symbol][previous_day], points[symbol][day]
            if previous <= 0:
                valid = False
                break
            contributions[symbol] = normalized[symbol] * (current / previous - 1.0)
        if valid:
            daily.append({'date': day, 'portfolio_return': sum(contributions.values()),
                          'contributions': contributions})
    if len(daily) < minimum_sessions - 1:
        return _unavailable('TEMPORAL_EVIDENCE_REQUIRED', 'rendements communs datés insuffisants', symbols=symbols)

    worst_day = min(daily, key=lambda item: item['portfolio_return'])
    rolling = []
    for index in range(ROLLING_SESSIONS - 1, len(daily)):
        window = daily[index - ROLLING_SESSIONS + 1:index + 1]
        cumulative = math.prod(1.0 + item['portfolio_return'] for item in window) - 1.0
        rolling.append({'start': window[0]['date'], 'end': window[-1]['date'], 'return_pct': cumulative * 100.0})
    worst_rolling = min(rolling, key=lambda item: item['return_pct']) if rolling else None

    wealth, peak, worst_drawdown = 1.0, 1.0, 0.0
    for item in daily:
        wealth *= 1.0 + item['portfolio_return']
        peak = max(peak, wealth)
        worst_drawdown = min(worst_drawdown, wealth / peak - 1.0)
    negative_contributors = {symbol: value for symbol, value in worst_day['contributions'].items() if value < 0}
    dominant_symbol = min(negative_contributors, key=negative_contributors.get) if negative_contributors else None
    loss_total = abs(sum(negative_contributors.values()))
    dominant_share = (abs(negative_contributors[dominant_symbol]) / loss_total
                      if dominant_symbol and loss_total else None)
    flags = []
    if dominant_share is not None and dominant_share >= 0.50:
        flags.append('HISTORICAL_TAIL_CONCENTRATION')
    return {
        'available': True, 'status': 'HISTORICAL_STRESS_AVAILABLE', 'read_only': True,
        'never_triggers_orders': True, 'symbols': symbols, 'n_common_sessions': len(dates),
        'method': 'rendements journaliers pondérés sur séances datées communes ; historique observé, pas une prévision',
        'worst_1d': {'date': worst_day['date'], 'portfolio_return_pct': round(worst_day['portfolio_return'] * 100.0, 3),
                      'contributions_pct': {symbol: round(value * 100.0, 3)
                                            for symbol, value in sorted(worst_day['contributions'].items())}},
        'worst_5d': ({**worst_rolling, 'return_pct': round(worst_rolling['return_pct'], 3)} if worst_rolling else None),
        'historical_max_drawdown_pct': round(worst_drawdown * 100.0, 3),
        'largest_worst_day_contributor': dominant_symbol,
        'largest_worst_day_loss_share': round(dominant_share, 3) if dominant_share is not None else None,
        'flags': flags,
        'note': ('historique commun insuffisant ne serait jamais remplacé par un choc supposé ; '
                 'ces pertes observées ne prédisent pas les pertes futures'),
    }


__all__ = ['assess', 'MIN_COMMON_SESSIONS']
