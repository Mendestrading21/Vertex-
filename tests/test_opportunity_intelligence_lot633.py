from vertex.engines import opportunity_attribution as attribution
from vertex.engines import intelligence_monitor as monitor


def _packet(missing=False):
    return {'contexts': {'technical': {'available': True},
                         'options': {'available': not missing},
                         'data_quality': {'available': True}}}


def _decision(gates=None):
    return {'score': {'total': 30, 'max': 40,
                      'blocks': {'trend': {'points': 8, 'max': 10},
                                 'risk': {'points': 4, 'max': 10}},
                      'insufficient_blocks': []},
            'gates': gates or []}


def test_opportunity_attribution_exposes_gate_before_score_driver():
    out = attribution.build(_packet(), _decision([
        {'id': 'SPREAD_EXCESSIVE', 'triggered': True, 'reason': 'spread large'}]))
    assert out['status'] == 'REJECTED_BY_GATES'
    assert out['drivers'][0]['block'] == 'trend'
    assert out['read_only'] is True


def test_opportunity_attribution_requires_missing_evidence():
    out = attribution.build(_packet(missing=True), _decision())
    assert out['status'] == 'EVIDENCE_REQUIRED'
    assert out['missing_contexts'] == ['options']


def _memory(n=30):
    decisions, outcomes = [], []
    for index in range(n):
        decision_id = 'd-%d' % index
        decisions.append({'decision_id': decision_id, 'engine_version': 'test-v1',
                          'regime': 'NORMAL', 'level': 'A', 'option': {'universe': 'SWING_3_6M'},
                          'data_evidence': {'quality_available': True, 'quality_actionable': True,
                                            'reconciliation_available': True, 'reconciliation_actionable': True,
                                            'reconciliation_blocking': False,
                                            'spot_freshness': 'FRESH', 'options_freshness': 'RECENT'}})
        ret = 1.0 if index < 20 else -1.0
        outcomes.append({'decision_id': decision_id,
                         'horizons': {'H10': {'status': 'MESURE', 'return_pct': ret}}})
    return {'decisions': decisions, 'outcomes': outcomes}


def test_performance_monitor_detects_hit_rate_decay_only_with_sample():
    out = monitor.assess(_memory(), 'test-v1', horizon='H10', window_size=10)
    assert out['available'] is True
    assert out['status'] == 'UNDER_WATCH'
    assert out['hit_rate_windows'] == [1.0, 1.0, 0.0]


def test_performance_monitor_refuses_to_infer_drift_under_sample_threshold():
    out = monitor.assess(_memory(29), 'test-v1', horizon='H10', window_size=10)
    assert out['available'] is False
    assert out['status'] == 'INSUFFICIENT_SAMPLE'


def test_performance_monitor_segments_regime_and_option_universe():
    out = monitor.assess(_memory(), 'test-v1', horizon='H10', window_size=10)
    assert out['by_regime']['NORMAL']['available'] is True
    assert out['by_option_universe']['SWING_3_6M']['status'] == 'UNDER_WATCH'


def test_data_quality_drift_is_separate_and_requires_frozen_evidence():
    memory = _memory()
    for record in memory['decisions'][-10:]:
        record['data_evidence']['quality_actionable'] = False
    out = monitor.assess(memory, 'test-v1', horizon='H10', window_size=10)
    quality = out['data_quality_drift']
    assert quality['available'] is True
    assert quality['status'] == 'UNDER_WATCH'
    assert quality['drift_check']['code'] == 'DATA_QUALITY_DRIFT'


def test_data_quality_drift_detects_stale_quotes_despite_available_sources():
    memory = _memory()
    for record in memory['decisions'][-10:]:
        record['data_evidence']['spot_freshness'] = 'STALE'
        record['data_evidence']['options_freshness'] = 'STALE'
    out = monitor.assess(memory, 'test-v1', horizon='H10', window_size=10)
    quality = out['data_quality_drift']
    assert quality['status'] == 'UNDER_WATCH'
    assert quality['freshness_rate_windows'] == [1.0, 1.0, 0.0]
    assert quality['drift_check']['freshness_triggered'] is True
