from vertex.engines import downside_volatility
from vertex.engines import skyler_core


def test_downside_volatility_reports_only_observed_negative_returns():
    closes = [100.0, 102.0, 98.0, 99.0, 95.0] * 5
    ctx = downside_volatility.build(closes, window_sessions=20)
    assert ctx['available'] is True
    assert ctx['status'] == 'OBSERVED_DOWNSIDE_VOLATILITY'
    assert ctx['negative_return_count'] > 0
    assert ctx['downside_deviation_annual_pct'] > 0
    assert ctx['read_only'] is True


def test_downside_volatility_requires_canonical_history():
    assert downside_volatility.build([100.0] * 20)['available'] is False
    assert downside_volatility.build([100.0, 0.0] * 12)['status'] == 'INSUFFICIENT_SERIES'


def test_downside_context_is_carried_without_scoring_effect():
    ctx = downside_volatility.build([100.0, 102.0, 98.0, 99.0, 95.0] * 5, window_sessions=20)
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, downside_volatility_ctx=ctx)
    assert packet['contexts']['downside_volatility'] == ctx
    assert 'downside_volatility' not in skyler_core.score40(packet)['blocks']
