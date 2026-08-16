"""Régressions de validation walk-forward Skyler, purement descriptives."""

from datetime import date, timedelta

from vertex.engines import walk_forward_validation as walk


ENGINE = 'walk-test'


def _memory(returns, *, missing_date=False):
    decisions, outcomes = [], []
    start = date(2025, 1, 2)
    for index, value in enumerate(returns):
        decision_id = 'd%03d' % index
        session_date = None if missing_date and index == 0 else (start + timedelta(days=index)).isoformat()
        decisions.append({'decision_id': decision_id, 'engine_version': ENGINE,
                          'session_date': session_date, 'decision': 'ACHETER',
                          'score_total': 30, 'scenarios': {'available': True,
                          'bear': {'return_pct': -5.0}, 'base': {'return_pct': 5.0}}})
        outcomes.append({'decision_id': decision_id, 'horizons': {'H10': {
                         'status': 'MESURE', 'return_pct': value}}})
    return {'schema': 1, 'decisions': decisions, 'outcomes': outcomes}


def test_walk_forward_requires_two_full_embargoed_folds():
    out = walk.assess(_memory([3.0] * 59), ENGINE, horizon='H10')
    assert out['available'] is False
    assert out['status'] == 'INSUFFICIENT_SAMPLE'
    assert out['required_dated_sessions'] == 60
    assert 'robustesse' in out['note']


def test_walk_forward_rejects_results_without_frozen_session_date():
    out = walk.assess(_memory([3.0] * 60, missing_date=True), ENGINE, horizon='H10')
    assert out['available'] is False
    assert out['status'] == 'TEMPORAL_EVIDENCE_REQUIRED'
    assert out['n_excluded_missing_session_date'] == 1


def test_walk_forward_reports_consistent_oos_evidence_without_claiming_future_returns():
    out = walk.assess(_memory([3.0] * 60), ENGINE, horizon='H10')
    assert out['available'] is True
    assert out['status'] == 'OOS_CONSISTENT'
    assert out['n_folds'] == 2
    assert out['embargo_sessions'] == 10
    assert all(fold['train_end'] < fold['embargo_start'] < fold['oos_start']
               for fold in out['folds'])
    assert 'ne prouve ni rendement futur' in out['note']


def test_walk_forward_flags_repeated_oos_degradation():
    out = walk.assess(_memory([3.0] * 20 + [-12.0] * 40), ENGINE, horizon='H10')
    assert out['available'] is True
    assert out['status'] == 'OOS_DEGRADED'
    assert out['n_degraded_folds'] == 2
    assert all(fold['degradation_flag'] for fold in out['folds'])


def test_validation_route_is_read_only_and_validates_horizon(tmp_path, monkeypatch):
    import terminal
    from vertex.engines import decision_memory as memory
    from vertex.engines import skyler_core as skyler
    from vertex.services import persist

    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    payload = _memory([3.0] * 60)
    for decision in payload['decisions']:
        decision['engine_version'] = skyler.ENGINE_VERSION
    persist.save_json(memory.MEMORY_FILE, payload)

    client = terminal.app.test_client()
    response = client.get('/api/skyler/validation?horizon=H10')
    assert response.status_code == 200
    body = response.get_json()
    assert body['read_only'] is True
    assert body['status'] == 'OOS_CONSISTENT'
    bad = client.get('/api/skyler/validation?horizon=H999')
    assert bad.status_code == 400
    assert bad.get_json()['error'] == 'horizon_invalide'
