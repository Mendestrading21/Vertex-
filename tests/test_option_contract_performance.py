from vertex.tracking import performance


def _option_tracking(snapshots=None):
    return {
        'entity_type': 'OPTION', 'contract_id': 'ABC|2026-12-18|125|C',
        'reference_price': 4.0, 'reference_price_type': 'MID',
        'reference_price_source': 'options_board', 'reference_price_timestamp': '2026-08-16T10:00:00Z',
        'snapshots': snapshots or [], 'benchmark': 'SPY', 'benchmark_reference_price': None,
        'strategy_decision_at_start': 'ATTENDRE', 'strategy_score_at_start': 28,
    }


def test_option_performance_uses_current_board_quote_when_available():
    out = performance.compute(_option_tracking([{'price': 4.5, 'at': 't1'}]), 5.0)
    contract = out['option_contract']
    assert out['current_price'] == 5.0
    assert contract['mark_mode'] == 'CURRENT_BOARD_QUOTE'
    assert contract['return_pct'] == 25.0
    assert contract['quote_observations'] == 1
    assert contract['scope'] == 'HYPOTHETICAL_OPTION_MARK_TO_OBSERVED_QUOTE'


def test_option_performance_falls_back_to_last_observed_snapshot_not_fake_live_quote():
    out = performance.compute(_option_tracking([{'price': 4.8, 'at': '2026-08-16T10:05:00Z'}]), None)
    contract = out['option_contract']
    assert out['current_price'] == 4.8
    assert contract['mark_mode'] == 'LAST_OBSERVED_SNAPSHOT'
    assert contract['last_observed_at'] == '2026-08-16T10:05:00Z'
    assert contract['return_pct'] == 20.0


def test_option_performance_refuses_result_without_any_observed_quote():
    out = performance.compute(_option_tracking(), None)
    contract = out['option_contract']
    assert contract['available'] is False
    assert contract['mark_mode'] == 'NO_OBSERVED_QUOTE'
    assert contract['return_pct'] is None
