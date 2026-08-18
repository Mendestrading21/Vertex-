from vertex.engines import earnings_option_overlap
from vertex.engines import skyler_core


def _options(dte):
    return {'available': True, 'best': {'dte': dte}}


def _earnings(days):
    return {'available': True, 'days_to_earnings': days}


def test_overlap_uses_only_declared_dtes():
    ctx = earnings_option_overlap.build(_options(120), _earnings(12))
    assert ctx['available'] is True
    assert ctx['status'] == 'EARNINGS_BEFORE_EXPIRY'
    assert ctx['earnings_before_option_expiry'] is True
    assert ctx['read_only'] is True


def test_overlap_refuses_missing_declared_dtes():
    assert earnings_option_overlap.build(_options(None), _earnings(12))['status'] == 'OPTION_DTE_UNAVAILABLE'
    assert earnings_option_overlap.build(_options(120), {'available': False})['status'] == 'EARNINGS_DTE_UNAVAILABLE'


def test_overlap_is_carried_without_scoring_effect():
    ctx = earnings_option_overlap.build(_options(120), _earnings(12))
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, earnings_option_overlap_ctx=ctx)
    assert packet['contexts']['earnings_option_overlap'] == ctx
    assert 'earnings_option_overlap' not in skyler_core.score40(packet)['blocks']
