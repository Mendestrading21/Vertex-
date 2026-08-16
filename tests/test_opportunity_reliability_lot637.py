from vertex.engines import opportunity_reliability as reliability


def _packet(data=True, reconciliation=True):
    return {'contexts': {
        'data_quality': {'available': data, 'actionable_allowed': data},
        'reconciliation': {'available': reconciliation, 'actionable_allowed': reconciliation,
                           'blocking': False},
    }}


def _decision(score=30, gates=None, insufficient=None):
    return {'score': {'total': score, 'insufficient_blocks': insufficient or []},
            'gates': gates or []}


def _cohort(available=False):
    return {'cohort': {'available': available, 'n_measurable': 5 if available else 2,
                       'minimum_sample': 5,
                       'scope': 'HYPOTHETICAL_OPTION_MARK_TO_OBSERVED_QUOTE'}}


def test_reliability_blocks_a_triggered_gate_before_all_other_evidence():
    out = reliability.build(_packet(), _decision(gates=[{'id': 'OI_INSUFFICIENT', 'triggered': True}]), _cohort(True))
    assert out['status'] == 'BLOCKED_BY_GATES'
    assert out['triggered_gates'] == ['OI_INSUFFICIENT']
    assert out['read_only'] is True


def test_reliability_requires_proven_data_before_review():
    out = reliability.build(_packet(data=False), _decision(), _cohort(True))
    assert out['status'] == 'EVIDENCE_LIMITED'
    assert out['checks']['data_actionable'] is False


def test_reliability_distinguishes_empirical_cohort_from_insufficient_sample():
    without = reliability.build(_packet(), _decision(), _cohort(False))
    with_cohort = reliability.build(_packet(), _decision(), _cohort(True))
    assert without['status'] == 'REVIEW_WITHOUT_EMPIRICAL_COHORT'
    assert with_cohort['status'] == 'REVIEW_WITH_EMPIRICAL_COHORT'
