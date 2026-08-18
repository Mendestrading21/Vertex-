from vertex.engines import decision_evidence


def test_evidence_refuses_missing_instrumental_quality_and_reconciliation():
    quality, reconciliation = decision_evidence.for_symbol({}, 'TST')
    assert quality['available'] is False
    assert reconciliation['available'] is False
    assert 'absent' in quality['reason']
    assert 'absent' in reconciliation['reason']


def test_evidence_uses_only_matching_symbol_packet_and_preserves_actionability():
    state = {
        'analytics_packets': [
            {'symbol': 'OTHER', 'quality': {'overall': 'FRESH', 'actionable_allowed': True}},
            {'symbol': 'TST', 'quality': {'overall': 'STALE', 'actionable_allowed': False,
                                           'warnings': ['OPTIONS_STALE']},
             'sources': {'spot': {'quality': 'RECENT'}, 'options': {'quality': 'STALE'}},
             'reconciliation': {'actionable_allowed': False, 'blocking': True,
                                'reason': 'sources non comparables'}},
        ]
    }
    quality, reconciliation = decision_evidence.for_symbol(state, 'TST')
    assert quality['available'] is True
    assert quality['overall'] == 'STALE'
    assert quality['actionable_allowed'] is False
    assert quality['freshness'] == {'spot': 'RECENT', 'options': 'STALE'}
    assert reconciliation['available'] is True
    assert reconciliation['actionable_allowed'] is False
    assert reconciliation['blocking'] is True


def test_evidence_does_not_promote_global_reconciliation_to_symbol_evidence():
    quality, reconciliation = decision_evidence.for_symbol(
        {'reconciliation': {'actionable_allowed': True}}, 'TST')
    assert quality['available'] is False
    assert reconciliation['available'] is False
