"""tests/test_research_factory_lot117.py — SKYLER LOT 117 : Research Factory figée.

Trou réel de couverture : vertex/research/factory.py (§29) n'avait que
2 tests nominaux (définition+walk-forward requis, anti look-ahead). Les
transitions INTERDITES exactes, les erreurs NOMMÉES, l'embargo réel des
splits et le seuil « passed » du walk-forward n'étaient figés nulle
part.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
import pytest

from vertex.research.factory import (BIAS_CONTROLS, Experiment, LifecycleError,
                                     run_walk_forward, walk_forward_splits)


def test_forbidden_transitions_are_refused_by_name():
    exp = Experiment(name='t')
    with pytest.raises(LifecycleError, match='transition interdite'):
        exp.advance('BACKTESTED')          # IDEA ne saute jamais DEFINED
    approved = Experiment(name='t', state='APPROVED')
    with pytest.raises(LifecycleError):
        approved.advance('IDEA')           # APPROVED ne redevient jamais une idée
    retired = Experiment(name='t', state='RETIRED')
    for target in ('IDEA', 'APPROVED', 'REJECTED'):
        with pytest.raises(LifecycleError):
            retired.advance(target)        # RETIRED est terminal


def test_rejected_idea_can_be_reborn():
    exp = Experiment(name='t', state='REJECTED')
    exp.advance('IDEA')
    assert exp.state == 'IDEA', 'une idée rejetée peut renaître — jamais APPROVED direct'


def test_unknown_state_is_named_in_the_error():
    with pytest.raises(LifecycleError, match='QUANTIQUE'):
        Experiment(name='t').advance('QUANTIQUE')


def test_defined_requires_all_11_fields_missing_are_named():
    exp = Experiment(name='t', definition={'hypothesis': 'x'})
    with pytest.raises(LifecycleError, match='invalidation'):
        exp.advance('DEFINED')             # les manquants sont NOMMÉS


def test_approved_requires_all_12_bias_controls_named():
    exp = Experiment(name='t', state='PAPER_VALIDATED',
                     bias_controls={k: 'ok' for k in BIAS_CONTROLS[:6]})
    with pytest.raises(LifecycleError, match='survivorship|overfitting|slippage'):
        exp.advance('APPROVED')
    full = Experiment(name='t', state='PAPER_VALIDATED',
                      bias_controls={k: 'ok' for k in BIAS_CONTROLS})
    with pytest.raises(LifecycleError, match='ne suffit jamais'):
        full.advance('APPROVED')           # sans walk-forward : refus constitutionnel


def test_history_records_every_transition_with_evidence():
    exp = Experiment(name='t')
    exp.advance('REJECTED', evidence={'raison': 'pas de bord'})
    assert exp.history == [{'from': 'IDEA', 'to': 'REJECTED',
                            'evidence': {'raison': 'pas de bord'}}]


def test_splits_embargo_is_real_and_short_sample_refused():
    with pytest.raises(ValueError, match='trop court'):
        walk_forward_splits(119, n_folds=5)          # < (5+1)·20
    splits = walk_forward_splits(120, n_folds=5, embargo=5)
    assert splits[0] == {'train': (0, 20), 'test': (25, 45), 'embargo': 5}
    assert splits[-1] == {'train': (0, 100), 'test': (105, 120), 'embargo': 5}
    for sp in splits:
        assert sp['train'][0] == 0                   # passé strict depuis l'origine
        assert sp['test'][0] == sp['train'][1] + 5, 'l\'embargo sépare TOUJOURS'


def test_passed_requires_near_unanimous_positive_folds():
    up = run_walk_forward([0.01] * 120, lambda tr: (lambda w: 1.0))
    assert up['positive_folds'] == up['total_folds'] == 5
    assert up['passed'] is True and up['oos_mean'] == pytest.approx(0.01)
    down = run_walk_forward([-0.01] * 120, lambda tr: (lambda w: 1.0))
    assert down['positive_folds'] == 0 and down['passed'] is False, (
        'passed exige ≥ max(2, n−1) folds positifs — jamais un pass de complaisance')
