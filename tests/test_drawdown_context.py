from vertex.engines import drawdown_context
from vertex.engines import skyler_core


def test_drawdown_context_reports_observed_current_and_max_drawdowns():
    ctx = drawdown_context.build([100.0, 120.0, 90.0, 100.0] * 6, window_sessions=24)
    assert ctx['available'] is True
    assert ctx['status'] == 'IN_DRAWDOWN'
    assert ctx['current_drawdown_pct'] < 0
    assert ctx['max_drawdown_pct'] <= ctx['current_drawdown_pct']
    assert ctx['read_only'] is True


def test_drawdown_context_refuses_short_or_invalid_series():
    assert drawdown_context.build([100.0] * 20)['available'] is False
    assert drawdown_context.build([100.0, 0.0] * 12)['status'] == 'INSUFFICIENT_SERIES'


def test_drawdown_context_is_carried_by_packet_without_scoring_effect():
    dd = drawdown_context.build([100.0, 120.0, 90.0, 100.0] * 6, window_sessions=24)
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, drawdown_ctx=dd)
    assert packet['contexts']['drawdown'] == dd
    assert 'drawdown' not in skyler_core.score40(packet)['blocks']
