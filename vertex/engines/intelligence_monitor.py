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
    recent = samples[-minimum:]
    windows = [recent[i:i + window_size] for i in range(0, minimum, window_size)]
    hit_rates = [sum(1 for x in w if x['hit']) / len(w) for w in windows]
    expectancy = [round(sum(x['return_pct'] for x in w) / len(w), 3) for w in windows]
    check = drift.performance_drift(hit_rates)
    triggered = bool(check and check.get('triggered'))
    return {**base, 'available': True,
            'status': 'UNDER_WATCH' if triggered else 'STABLE',
            'hit_rate_windows': [round(x, 3) for x in hit_rates],
            'expectancy_windows_pct': expectancy,
            'drift_check': check,
            'note': ('dérive descriptive sur résultats du sous-jacent mesurés ; '
                     'aucune recalibration ou désactivation automatique n’est appliquée')}


__all__ = ['assess']
