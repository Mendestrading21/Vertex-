"""Phases 16-17 : Research Factory, calibration, drift, mémoire, alertes, track record."""
import pytest

from vertex.alerts.engine import AlertEngine, ACTIONABLE_REQUIREMENTS
from vertex.engines.performance_ledger import PerformanceLedger, RECORD_TYPES
from vertex.research.factory import (Experiment, LifecycleError, run_walk_forward,
                                     walk_forward_splits, BIAS_CONTROLS,
                                     REQUIRED_DEFINITION)
from vertex.strategy.memory.learnings import active_rules, propose_rule
from vertex.strategy.memory.store import MemoryStore
from vertex.validation import drift as D
from vertex.validation.probability_calibration import (calibration_report,
                                                       display_probability,
                                                       INSUFFICIENT)


# ── Research Factory ──────────────────────────────────────────────────
def full_definition():
    return {k: f'valeur_{k}' for k in REQUIRED_DEFINITION}


def test_lifecycle_requires_definition_and_walk_forward():
    exp = Experiment('momentum-20d')
    with pytest.raises(LifecycleError):
        exp.advance('DEFINED')          # définition incomplète
    exp.definition = full_definition()
    exp.advance('DEFINED')
    exp.advance('BACKTESTED')
    exp.advance('WALK_FORWARD')
    exp.advance('PAPER_VALIDATED')
    with pytest.raises(LifecycleError):
        exp.advance('APPROVED')         # contrôles de biais absents
    exp.bias_controls = {k: 'contrôlé' for k in BIAS_CONTROLS}
    with pytest.raises(LifecycleError):
        exp.advance('APPROVED')         # pas de walk-forward dans les résultats
    exp.results['walk_forward'] = {'passed': True}
    exp.advance('APPROVED')
    assert exp.state == 'APPROVED'


def test_backtest_alone_never_activates_signal():
    exp = Experiment('beau-backtest', definition=full_definition())
    exp.advance('DEFINED')
    exp.advance('BACKTESTED')
    with pytest.raises(LifecycleError):
        exp.advance('APPROVED')


def test_walk_forward_has_no_lookahead():
    n = 400
    splits = walk_forward_splits(n, n_folds=5, embargo=5)
    for sp in splits:
        assert sp['train'][1] + sp['embargo'] <= sp['test'][0], \
            'le test doit commencer APRÈS le train + embargo'
        assert sp['train'][0] == 0

    # Un signal tricheur qui regarde le futur ne peut pas être construit ici :
    # la stratégie ne reçoit que les rendements STRICTEMENT antérieurs à i.
    seen_lengths = []
    rets = [0.001 * ((i % 7) - 3) for i in range(400)]

    def signal_fn(train):
        def strategy(past):
            seen_lengths.append(len(past))
            return 1.0
        return strategy

    res = run_walk_forward(rets, signal_fn, n_folds=4)
    assert res['total_folds'] >= 3
    for sp, length in zip(walk_forward_splits(400, 4), seen_lengths):
        assert length < 400, 'la stratégie ne doit jamais voir toute la série'


# ── Calibration des probabilités ──────────────────────────────────────
def test_probability_requires_calibration():
    res = display_probability(0.65, report=None)
    assert res['display'] == INSUFFICIENT and res['probability'] is None
    small = calibration_report([0.6] * 10, [1] * 6 + [0] * 4)
    res2 = display_probability(0.65, small)
    assert res2['display'] == INSUFFICIENT     # échantillon < 50
    forecasts = [0.3] * 50 + [0.7] * 50
    outcomes = [0] * 35 + [1] * 15 + [1] * 35 + [0] * 15
    good = calibration_report(forecasts, outcomes)
    res3 = display_probability(0.65, good)
    assert res3['probability'] == 0.65


def test_out_of_distribution_blocks_probability():
    forecasts = [0.3] * 50 + [0.7] * 50
    outcomes = [0] * 35 + [1] * 15 + [1] * 35 + [0] * 15
    good = calibration_report(forecasts, outcomes)
    res = display_probability(0.65, good, out_of_distribution=True)
    assert res['display'] == INSUFFICIENT
    res2 = display_probability(0.65, good, model_in_drift=True)
    assert res2['display'] == INSUFFICIENT


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
def test_unconfirmed_rule_never_applied(tmp_path):
    store = MemoryStore(tmp_path / 'memory.json')
    rule = propose_rule(store, 'éviter les earnings J-1', 'ne pas ouvrir la veille')
    assert rule['status'] == 'PROPOSED'
    assert active_rules(store) == []
    with pytest.raises(PermissionError):
        store.set_status('vxStrategyRules', rule['id'], 'CONFIRMED')
    store.set_status('vxStrategyRules', rule['id'], 'CONFIRMED', confirmed_by_human=True)
    assert len(active_rules(store)) == 1


def test_memory_keys_are_neutral():
    from vertex.strategy.memory.schemas import STORAGE_KEYS
    for key in STORAGE_KEYS:
        assert key.startswith('vxStrategy')


def test_memory_persists(tmp_path):
    path = tmp_path / 'memory.json'
    store = MemoryStore(path)
    store.add('vxStrategyTheses', {'symbol': 'NVDA', 'thesis': 'IA'}, status='OBSERVED')
    reloaded = MemoryStore(path)
    assert len(reloaded.entries('vxStrategyTheses')) == 1


# ── Track record : signal ≠ trade ─────────────────────────────────────
def test_track_record_separates_signal_and_trade():
    ledger = PerformanceLedger()
    sig = ledger.record('SIGNAL', 'NVDA', {'verdict': 'setup haussier'})
    alert = ledger.record('ALERT', 'NVDA', parent_id=sig['id'])
    reco = ledger.record('RECOMMENDATION', 'NVDA', parent_id=alert['id'])
    dec = ledger.record('USER_DECISION', 'NVDA', {'accepted': True}, parent_id=reco['id'])
    pos = ledger.record('REAL_POSITION', 'NVDA', parent_id=dec['id'])
    for i in range(6):
        s = ledger.record('SIGNAL', f'SYM{i}')
        ledger.close(s['id'], {'return_pct': 8.0, 'spy_return_pct': 2.0})
    for i in range(6):
        p = ledger.record('REAL_POSITION', f'SYM{i}')
        ledger.close(p['id'], {'return_pct': -2.0, 'spy_return_pct': 2.0})
    m_sig = ledger.metrics('SIGNAL')
    m_pos = ledger.metrics('REAL_POSITION')
    assert m_sig['expectancy_pct'] > 0 > m_pos['expectancy_pct'], \
        'performances signal et position calculées séparément'
    assert 'théorique' in m_sig['metrics_scope']
    assert 'réel' in m_pos['metrics_scope']
    funnel = ledger.funnel()
    assert set(funnel) == set(RECORD_TYPES)


def test_track_record_honest_with_small_sample():
    ledger = PerformanceLedger()
    s = ledger.record('SIGNAL', 'NVDA')
    ledger.close(s['id'], {'return_pct': 50.0})
    m = ledger.metrics('SIGNAL')
    assert 'win_rate' not in m
    assert 'honnêteté' in m['note']


def test_breakdown_by_context():
    ledger = PerformanceLedger()
    for i in range(8):
        s = ledger.record('SIGNAL', f'A{i}')
        ledger.close(s['id'], {'return_pct': 5.0 if i % 2 else -3.0,
                               'regime': 'TREND_UP' if i % 2 else 'CHOP',
                               'delta': 0.35, 'dte': 120})
    bk = ledger.breakdown('SIGNAL', 'regime')
    assert bk['TREND_UP']['mean_pct'] > bk['CHOP']['mean_pct']


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
