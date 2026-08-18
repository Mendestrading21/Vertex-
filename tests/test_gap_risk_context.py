from vertex.engines import gap_risk_context
from vertex.engines import skyler_core


def _detail(count=25):
    closes = [100.0 + index for index in range(count)]
    opens = [100.0] + [closes[index - 1] * (1.03 if index % 5 == 0 else 1.0) for index in range(1, count)]
    return {'series': {'open': opens, 'close': closes}}


def test_gap_context_reports_only_observed_ohlc_gaps():
    ctx = gap_risk_context.build(_detail())
    assert ctx['available'] is True
    assert ctx['status'] == 'OBSERVED_GAPS'
    assert ctx['material_gap_count'] > 0
    assert ctx['max_abs_gap_pct'] >= 3.0
    assert ctx['read_only'] is True


def test_gap_context_refuses_missing_or_short_ohlc():
    assert gap_risk_context.build({'series': {'close': [100.0] * 25}})['available'] is False
    assert gap_risk_context.build(_detail(20))['status'] == 'INSUFFICIENT_OHLC'


def test_gap_context_is_carried_without_scoring_effect():
    ctx = gap_risk_context.build(_detail())
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, gap_risk_ctx=ctx)
    assert packet['contexts']['gap_risk'] == ctx
    assert 'gap_risk' not in skyler_core.score40(packet)['blocks']
