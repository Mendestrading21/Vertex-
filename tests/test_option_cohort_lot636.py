from vertex.tracking import option_cohort


def _tracking(index, ret=None, decision='ATTENDRE'):
    snapshots = [] if ret is None else [{'price': 4.0 * (1 + ret / 100), 'at': 't-%d' % index}]
    return {'tracking_id': 'opt-%d' % index, 'entity_type': 'OPTION', 'status': 'ACTIVE',
            'contract_id': 'ABC|2026-12-18|125|C', 'reference_price': 4.0,
            'reference_price_type': 'MID', 'snapshots': snapshots,
            'strategy_decision_at_start': decision, 'benchmark': 'SPY',
            'benchmark_reference_price': None}


def test_option_cohort_refuses_metrics_below_minimum_sample():
    out = option_cohort.build([_tracking(1, 10), _tracking(2, -5)], minimum=5)
    assert out['cohort']['available'] is False
    assert out['n_measurable'] == 2


def test_option_cohort_aggregates_only_observed_contract_marks():
    trackings = [_tracking(i, ret, 'ATTENDRE' if i < 6 else 'REFUSER')
                 for i, ret in enumerate([10, -5, 2, 6, -2, 1], 1)]
    out = option_cohort.build(trackings, minimum=5)
    assert out['cohort']['available'] is True
    assert out['cohort']['n_measurable'] == 6
    assert out['cohort']['win_rate'] == round(4 / 6, 3)
    assert out['by_decision_at_start']['ATTENDRE']['available'] is True


def test_option_cohort_does_not_turn_missing_quotes_into_zero_return():
    out = option_cohort.build([_tracking(1, None), _tracking(2, 5)], minimum=2)
    assert out['n_measurable'] == 1
    assert out['cohort']['available'] is False
