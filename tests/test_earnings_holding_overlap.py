from vertex.engines import earnings_holding_overlap
from vertex.engines import skyler_core


def _options(sessions=(5, 10, 15)):
    return {'available': True, 'best': {'mandate': {'bounds': {'holding_plan_sessions': list(sessions)}}}}


def _earnings(days=12):
    return {'available': True, 'days_to_earnings': days}


def test_holding_overlap_never_converts_sessions_to_calendar_days():
    ctx = earnings_holding_overlap.build(_options(), _earnings())
    assert ctx['available'] is True
    assert ctx['status'] == 'UNITS_NOT_COMPARABLE'
    assert ctx['holding_plan_sessions'] == [5, 10, 15]
    assert ctx['earnings_dte_calendar_days'] == 12
    assert ctx['read_only'] is True


def test_holding_overlap_refuses_missing_plan_or_earnings_dte():
    assert earnings_holding_overlap.build({'available': True}, _earnings())['status'] == 'HOLDING_PLAN_UNAVAILABLE'
    assert earnings_holding_overlap.build(_options(), {'available': False})['status'] == 'EARNINGS_DTE_UNAVAILABLE'


def test_holding_overlap_is_carried_without_scoring_effect():
    ctx = earnings_holding_overlap.build(_options(), _earnings())
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, earnings_holding_overlap_ctx=ctx)
    assert packet['contexts']['earnings_holding_overlap'] == ctx
    assert 'earnings_holding_overlap' not in skyler_core.score40(packet)['blocks']
