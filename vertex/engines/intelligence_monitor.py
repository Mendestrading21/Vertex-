"""Surveillance de dérive des résultats Skyler réellement mesurés.

Le moniteur lit le ledger mémoire append-only. Il ne recalibre pas le moteur,
ne modifie aucune constitution et ne conclut rien lorsqu'un échantillon est trop
petit. Il est descriptif et sert à déclencher une revue humaine.
"""
from __future__ import annotations

from vertex.validation import drift


def _measured(memory, engine_version, horizon):
    decisions = {str(d.get('decision_id')): d for d in (memory or {}).get('decisions', [])
                 if isinstance(d, dict) and d.get('engine_version') == engine_version}
    out = []
    for outcome in (memory or {}).get('outcomes', []):
        if not isinstance(outcome, dict):
            continue
        decision = decisions.get(str(outcome.get('decision_id')))
        hz = (outcome.get('horizons') or {}).get(horizon) or {}
        ret = hz.get('return_pct')
        if decision is None or hz.get('status') != 'MESURE' or not isinstance(ret, (int, float)):
            continue
        out.append({'decision_id': outcome.get('decision_id'), 'return_pct': float(ret),
                    'hit': float(ret) > 0, 'regime': decision.get('regime'),
                    'level': decision.get('level'), 'option_universe': (decision.get('option') or {}).get('universe')})
    return out


def _window_assessment(samples, window_size):
    minimum = window_size * 3
    if len(samples) < minimum:
        return {'available': False, 'status': 'INSUFFICIENT_SAMPLE',
                'n_measured': len(samples), 'required': minimum}
    recent = samples[-minimum:]
    windows = [recent[i:i + window_size] for i in range(0, minimum, window_size)]
    hit_rates = [sum(1 for x in window if x['hit']) / len(window) for window in windows]
    expectancy = [round(sum(x['return_pct'] for x in window) / len(window), 3)
                  for window in windows]
    check = drift.performance_drift(hit_rates)
    return {'available': True,
            'status': 'UNDER_WATCH' if check and check.get('triggered') else 'STABLE',
            'n_measured': len(samples),
            'hit_rate_windows': [round(x, 3) for x in hit_rates],
            'expectancy_windows_pct': expectancy,
            'drift_check': check}


def _segments(samples, key, window_size):
    grouped = {}
    for sample in samples:
        value = sample.get(key)
        if value is not None:
            grouped.setdefault(str(value), []).append(sample)
    return {group: _window_assessment(values, window_size)
            for group, values in sorted(grouped.items())}


def _data_quality_drift(memory, engine_version, window_size):
    records = [d for d in (memory or {}).get('decisions', [])
               if isinstance(d, dict) and d.get('engine_version') == engine_version
               and isinstance(d.get('data_evidence'), dict)]
    usable = []
    freshness = []
    for record in records:
        evidence = record['data_evidence']
        values = (evidence.get('quality_available'), evidence.get('quality_actionable'),
                  evidence.get('reconciliation_available'), evidence.get('reconciliation_actionable'))
        freshness_values = (evidence.get('spot_freshness'), evidence.get('options_freshness'))
        if all(value is not None for value in values) and all(value is not None for value in freshness_values):
            usable.append(all(values) and not bool(evidence.get('reconciliation_blocking')))
            freshness.append(all(value in ('FRESH', 'RECENT') for value in freshness_values))
    minimum = window_size * 3
    if len(usable) < minimum:
        return {'available': False, 'status': 'INSUFFICIENT_SAMPLE',
                'n_observations': len(usable), 'required': minimum,
                'reason': 'preuves qualité/réconciliation figées insuffisantes'}
    recent = usable[-minimum:]
    recent_freshness = freshness[-minimum:]
    windows = [recent[i:i + window_size] for i in range(0, minimum, window_size)]
    freshness_windows = [recent_freshness[i:i + window_size] for i in range(0, minimum, window_size)]
    rates = [sum(1 for value in window if value) / len(window) for window in windows]
    freshness_rates = [sum(1 for value in window if value) / len(window) for window in freshness_windows]
    drop = rates[0] - rates[-1]
    freshness_drop = freshness_rates[0] - freshness_rates[-1]
    actionable_triggered = drop >= 0.20 and all(a >= b - 0.02 for a, b in zip(rates, rates[1:]))
    freshness_triggered = (freshness_drop >= 0.20 and
                           all(a >= b - 0.02 for a, b in zip(freshness_rates, freshness_rates[1:])))
    triggered = actionable_triggered or freshness_triggered
    return {'available': True, 'status': 'UNDER_WATCH' if triggered else 'STABLE',
            'n_observations': len(usable),
            'actionable_rate_windows': [round(rate, 3) for rate in rates],
            'freshness_rate_windows': [round(rate, 3) for rate in freshness_rates],
            'drift_check': {'code': 'DATA_QUALITY_DRIFT', 'actionable_drop': round(drop, 3),
                            'freshness_drop': round(freshness_drop, 3),
                            'actionable_triggered': actionable_triggered,
                            'freshness_triggered': freshness_triggered, 'triggered': triggered},
            'note': 'dérive des preuves actionnables et de fraîcheur figées ; une absence de donnée ne devient jamais une preuve'}


def assess(memory, engine_version, *, horizon='H10', window_size=10):
    """Évalue la décroissance du hit rate sur trois fenêtres non chevauchantes."""
    samples = _measured(memory, engine_version, horizon)
    minimum = window_size * 3
    base = {'engine_version': engine_version, 'horizon': horizon,
            'n_measured': len(samples), 'window_size': window_size,
            'read_only': True}
    if len(samples) < minimum:
        return {**base, 'available': False, 'status': 'INSUFFICIENT_SAMPLE',
                'reason': '%d résultats mesurés requis ; %d disponible(s)' % (minimum, len(samples)),
                'note': 'aucune dérive de performance n’est déduite sous le seuil minimal'}
    overall = _window_assessment(samples, window_size)
    return {**base, **overall,
            'by_regime': _segments(samples, 'regime', window_size),
            'by_option_universe': _segments(samples, 'option_universe', window_size),
            'data_quality_drift': _data_quality_drift(memory, engine_version, window_size),
            'note': ('dérive descriptive sur résultats du sous-jacent mesurés ; '
                     'aucune recalibration ou désactivation automatique n’est appliquée')}


__all__ = ['assess']
