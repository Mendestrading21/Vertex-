"""vertex.validation.drift — dérive de modèle et décomposition de signal (§31).

Un signal en drift est dégradé, mis sous surveillance ou désactivé (la
désactivation AUTOMATIQUE d'un signal technique est permise — sécurité).
La constitution stratégique, elle, ne peut jamais être modifiée automatiquement.
"""
from __future__ import annotations

import math

DRIFT_CODES = ('FEATURE_DRIFT', 'DATA_QUALITY_DRIFT', 'CALIBRATION_DRIFT',
               'PERFORMANCE_DRIFT', 'REGIME_DRIFT', 'SIGNAL_DECAY',
               'OUT_OF_DISTRIBUTION')

STATUS_ACTIVE = 'ACTIVE'
STATUS_DEGRADED = 'DEGRADED'
STATUS_WATCH = 'UNDER_WATCH'
STATUS_DISABLED = 'DISABLED'


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _std(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def feature_drift(reference: list[float], recent: list[float]) -> dict | None:
    """Drift d'une feature : |moyenne récente - référence| en écarts-types."""
    if len(reference) < 30 or len(recent) < 10:
        return None
    sd = _std(reference)
    if not sd:
        return None
    z = abs(_mean(recent) - _mean(reference)) / sd
    return {'code': 'FEATURE_DRIFT', 'zscore': round(z, 2), 'triggered': z >= 2.0}


def performance_drift(hit_rates_windows: list[float]) -> dict | None:
    """Décroissance du taux de réussite d'un signal sur fenêtres successives."""
    if len(hit_rates_windows) < 3:
        return None
    first, last = hit_rates_windows[0], hit_rates_windows[-1]
    monotonic_down = all(a >= b - 0.02 for a, b in
                         zip(hit_rates_windows, hit_rates_windows[1:]))
    decay = first - last
    return {'code': 'SIGNAL_DECAY', 'decay': round(decay, 3),
            'triggered': decay >= 0.15 and monotonic_down}


def out_of_distribution(value: float, reference: list[float]) -> dict | None:
    if len(reference) < 30:
        return None
    lo, hi = min(reference), max(reference)
    span = hi - lo or 1e-9
    outside = value < lo - 0.1 * span or value > hi + 0.1 * span
    return {'code': 'OUT_OF_DISTRIBUTION', 'value': value,
            'range': [lo, hi], 'triggered': outside}


def assess_signal(checks: list[dict | None]) -> dict:
    """Agrège les contrôles → statut du signal.

    1 drift déclenché → DEGRADED ; 2 → UNDER_WATCH ; ≥3 ou SIGNAL_DECAY fort
    → DISABLED (automatique, sécurité).
    """
    triggered = [c for c in checks if c and c.get('triggered')]
    codes = [c['code'] for c in triggered]
    if not triggered:
        status = STATUS_ACTIVE
    elif len(triggered) == 1:
        status = STATUS_DEGRADED
    elif len(triggered) == 2:
        status = STATUS_WATCH
    else:
        status = STATUS_DISABLED
    decay = next((c for c in triggered if c['code'] == 'SIGNAL_DECAY'), None)
    if decay and decay.get('decay', 0) >= 0.30:
        status = STATUS_DISABLED
    return {'status': status, 'triggered': codes,
            'auto_disable_allowed': True,
            'constitution_change_allowed': False,
            'note': ('signal désactivé automatiquement par sécurité — la constitution, '
                     'elle, ne change jamais automatiquement') if status == STATUS_DISABLED
            else ''}
