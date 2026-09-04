from vertex.engines import decision_readiness as readiness


def _packet(**contexts):
    base = {
        'technical': {'available': True}, 'market': {'available': True},
        'data_quality': {'available': True}, 'reconciliation': {'available': True},
        'options': {'available': True},
    }
    base.update(contexts)
    return {'contexts': base}


def _decision(gates=None, blocks=None):
    return {'decision': 'ACHETER', 'capped_by_gate': None,
            'score': {'total': 30, 'max': 40, 'insufficient_blocks': blocks or []},
            'gates': gates or []}


def test_triggered_gate_has_priority_over_other_readiness_states():
    out = readiness.build(_packet(data_quality={'available': False, 'reason': 'stale'}), _decision([
        {'id': 'SPREAD_EXCESSIVE', 'triggered': True, 'reason': 'spread 10% dépasse le mandat'},
        {'id': 'OI_INSUFFICIENT', 'triggered': None, 'reason': 'OI absent'},
    ]))
    assert out['status'] == 'BLOCKED_BY_GATE'
    assert out['triggered_gates'][0]['id'] == 'SPREAD_EXCESSIVE'
    assert out['missing_contexts'] == ['data_quality']
    assert out['read_only'] is True


def test_unevaluable_gate_requires_evidence_without_becoming_a_trigger():
    out = readiness.build(_packet(), _decision([
        {'id': 'OI_INSUFFICIENT', 'triggered': None, 'reason': 'OI absent'},
    ]))
    assert out['status'] == 'EVIDENCE_REQUIRED'
    assert out['triggered_gates'] == []
    assert out['unevaluable_gates'][0]['id'] == 'OI_INSUFFICIENT'


def test_complete_packet_without_gates_is_ready_for_analytical_review_only():
    out = readiness.build(_packet(), _decision())
    assert out['status'] == 'ANALYTICAL_REVIEW_READY'
    assert 'instruction' in out['note']
