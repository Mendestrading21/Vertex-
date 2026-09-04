"""Phases 16-17 : Research Factory, calibration, drift, mémoire, alertes, track record."""
import pytest

from vertex.alerts.engine import AlertEngine, ACTIONABLE_REQUIREMENTS
from vertex.validation import drift as D


# ── Research Factory ──────────────────────────────────────────────────








# ── Calibration des probabilités ──────────────────────────────────────




# ── Drift ─────────────────────────────────────────────────────────────
def test_signal_decay_disables_automatically():
    decay = D.performance_drift([0.62, 0.55, 0.44, 0.30])
    assert decay['triggered']
    res = D.assess_signal([decay])
    assert res['status'] == D.STATUS_DISABLED, 'décroissance ≥ 30 pts → coupé'
    assert res['constitution_change_allowed'] is False


def test_single_drift_degrades_not_disables():
    fd = D.feature_drift([0.1 * (i % 10) for i in range(60)], [3.0] * 15)
    assert fd['triggered']
    res = D.assess_signal([fd])
    assert res['status'] == D.STATUS_DEGRADED


def test_out_of_distribution_detection():
    ood = D.out_of_distribution(9.0, [0.1 * i for i in range(40)])
    assert ood['triggered']


# ── Mémoire : règles jamais actives sans confirmation ─────────────────






# ── Track record : signal ≠ trade ─────────────────────────────────────






# ── Alertes ───────────────────────────────────────────────────────────
def test_actionable_alert_requires_full_dossier():
    eng = AlertEngine()
    res = eng.raise_alert('NVDA', 'ACTIONABLE', 'setup complet', requirements={})
    assert res['emitted'] is False and 'manquantes' in res['error']
    full = {k: True for k in ACTIONABLE_REQUIREMENTS}
    res2 = eng.raise_alert('NVDA', 'ACTIONABLE', 'setup complet', requirements=full)
    assert res2['emitted'] is True


def test_alert_cooldown_and_level_changes():
    t = [1000.0]
    eng = AlertEngine(clock=lambda: t[0])
    assert eng.raise_alert('NVDA', 'WATCH', 'setup en construction')['emitted']
    assert not eng.raise_alert('NVDA', 'WATCH', 'répétition')['emitted']
    res = eng.raise_alert('NVDA', 'INVALIDATED', 'support cassé')
    assert res['emitted'] and res['alert']['previous_level'] == 'WATCH'
    t[0] += 7 * 3600
    assert eng.active_alerts() == [], 'les alertes expirent'
