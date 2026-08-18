from vertex.engines import earnings_proximity
from vertex.engines import skyler_core


def _timeline(events, provided=True):
    return {'events': events, 'coverage': {'input_channels': {'earnings_provided': provided}}}


def test_earnings_proximity_uses_declared_nearest_dte_only():
    ctx = earnings_proximity.build(_timeline([
        {'kind': 'earnings', 'dte': 12, 'date': '2026-04-10', 'source': 'calendar.earnings'},
        {'kind': 'earnings', 'dte': 5, 'date': '2026-04-03', 'source': 'calendar.earnings'},
    ]))
    assert ctx['available'] is True
    assert ctx['status'] == 'NEAREST_DATED_EARNINGS'
    assert ctx['days_to_earnings'] == 5
    assert ctx['read_only'] is True


def test_earnings_proximity_never_estimates_missing_calendar_or_dte():
    assert earnings_proximity.build(_timeline([], provided=False))['status'] == 'EARNINGS_CALENDAR_UNAVAILABLE'
    ctx = earnings_proximity.build(_timeline([{'kind': 'earnings', 'date': '2026-04-10'}]))
    assert ctx['status'] == 'DATED_EARNINGS_NO_DTE'
    assert 'days_to_earnings' not in ctx


def test_earnings_context_is_carried_without_scoring_effect():
    ctx = earnings_proximity.build(_timeline([{'kind': 'earnings', 'dte': 5, 'source': 'calendar.earnings'}]))
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, earnings_proximity_ctx=ctx)
    assert packet['contexts']['earnings_proximity'] == ctx
    assert 'earnings_proximity' not in skyler_core.score40(packet)['blocks']
