"""Détection descriptive de rupture de régime sur une série datée.

Inspiré des principes de détection de points de rupture, ce module compare une
fenêtre récente aux rendements antérieurs réellement observés. Il ne prédit pas
un marché, ne modifie aucune décision et refuse de conclure lorsque les dates,
les clôtures ou la variabilité de référence ne sont pas prouvées.
"""
from __future__ import annotations

import math
from datetime import date

import numpy as np


BASELINE_RETURNS = 60
RECENT_RETURNS = 20
MIN_CLOSES = BASELINE_RETURNS + RECENT_RETURNS + 1
VOLATILITY_EXPANSION_RATIO = 1.80
MEAN_SHIFT_Z = 2.50


def _finite_close(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) and value > 0 else None


def _valid_date(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        return date.fromisoformat(value[:10]).isoformat()
    except (TypeError, ValueError):
        return None


def _unavailable(status, reason, *, n_observations=0):
    return {'available': False, 'status': status, 'reason': reason,
            'n_observations': n_observations, 'read_only': True,
            'does_not_change_decision': True}


def assess(series, *, baseline_returns=BASELINE_RETURNS, recent_returns=RECENT_RETURNS):
    """Compare 60 rendements de référence aux 20 plus récents, sans look-ahead.

    La portion récente est toujours postérieure à la référence. Les seuils sont
    descriptifs : ratio de volatilité >= 1,80 et déplacement normalisé de la
    moyenne >= 2,50. Ils signalent une revue, jamais une instruction de marché.
    """
    if baseline_returns < 20 or recent_returns < 5:
        return _unavailable('INVALID_CONFIGURATION', 'fenêtres de référence invalides')
    dates = (series or {}).get('dates')
    closes = (series or {}).get('close')
    if not isinstance(dates, list) or not isinstance(closes, list) or len(dates) != len(closes):
        return _unavailable('TEMPORAL_EVIDENCE_REQUIRED', 'série de clôtures datée absente ou incohérente')
    points = []
    for raw_date, raw_close in zip(dates, closes):
        day, close = _valid_date(raw_date), _finite_close(raw_close)
        if day is None or close is None:
            return _unavailable('TEMPORAL_EVIDENCE_REQUIRED', 'date ou clôture non exploitable',
                                n_observations=len(points))
        points.append((day, close))
    if len(points) < baseline_returns + recent_returns + 1:
        return _unavailable('INSUFFICIENT_SAMPLE', '%d clôtures datées requises' %
                            (baseline_returns + recent_returns + 1), n_observations=len(points))
    if any(later[0] <= earlier[0] for earlier, later in zip(points, points[1:])):
        return _unavailable('TEMPORAL_EVIDENCE_REQUIRED', 'dates non strictement croissantes',
                            n_observations=len(points))

    selected = points[-(baseline_returns + recent_returns + 1):]
    returns = np.asarray([(current / previous - 1.0) for (_, previous), (_, current)
                          in zip(selected, selected[1:])], dtype=float)
    baseline, recent = returns[:baseline_returns], returns[baseline_returns:]
    baseline_std = float(np.std(baseline, ddof=1))
    recent_std = float(np.std(recent, ddof=1))
    if baseline_std <= 1e-12:
        return _unavailable('TEMPORAL_EVIDENCE_REQUIRED', 'variabilité de référence insuffisante',
                            n_observations=len(selected))
    baseline_mean, recent_mean = float(np.mean(baseline)), float(np.mean(recent))
    volatility_ratio = recent_std / baseline_std
    mean_shift_z = (recent_mean - baseline_mean) / (baseline_std / math.sqrt(recent_returns))
    baseline_return = math.prod(1.0 + value for value in baseline) - 1.0
    recent_return = math.prod(1.0 + value for value in recent) - 1.0
    flags = []
    if volatility_ratio >= VOLATILITY_EXPANSION_RATIO:
        flags.append('VOLATILITY_REGIME_BREAK')
    if abs(mean_shift_z) >= MEAN_SHIFT_Z:
        flags.append('MEAN_RETURN_REGIME_BREAK')
    if baseline_return * recent_return < 0 and abs(mean_shift_z) >= MEAN_SHIFT_Z:
        flags.append('DIRECTIONAL_REGIME_REVERSAL')
    status = 'REGIME_BREAK_WATCH' if flags else 'REGIME_CONTINUITY'
    return {
        'available': True, 'status': status, 'read_only': True,
        'does_not_change_decision': True, 'n_observations': len(selected),
        'as_of': selected[-1][0], 'baseline_start': selected[0][0],
        'baseline_end': selected[baseline_returns][0],
        'recent_start': selected[baseline_returns][0], 'recent_end': selected[-1][0],
        'baseline_returns': baseline_returns, 'recent_returns': recent_returns,
        'volatility_ratio': round(volatility_ratio, 3),
        'mean_shift_z': round(mean_shift_z, 3),
        'baseline_return_pct': round(baseline_return * 100.0, 3),
        'recent_return_pct': round(recent_return * 100.0, 3),
        'flags': flags,
        'thresholds': {'volatility_expansion_ratio': VOLATILITY_EXPANSION_RATIO,
                       'mean_shift_z': MEAN_SHIFT_Z},
        'note': ('changement statistique observé : revue analytique requise ; ce diagnostic ne prédit pas le régime futur et ne modifie rien automatiquement'
                 if flags else
                 'aucune rupture statistique détectée aux seuils publiés ; ce constat ne prédit pas le régime futur'),
    }


__all__ = ['assess', 'BASELINE_RETURNS', 'RECENT_RETURNS']
