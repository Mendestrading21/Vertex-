from vertex.engines import open_interest_concentration
from vertex.engines import skyler_core


def _board():
    return [
        {'sym': 'TST', 'dte': 100, 'strike': 100, 'oi': 50},
        {'sym': 'TST', 'dte': 120, 'strike': 100, 'oi': 100},
        {'sym': 'TST', 'dte': 150, 'strike': 110, 'oi': 50},
        {'sym': 'TST', 'dte': 120, 'strike': 120, 'oi': 0},
        {'sym': 'TST', 'dte': 45, 'strike': 100, 'oi': 999},
        {'sym': 'OTHER', 'dte': 120, 'strike': 100, 'oi': 999},
    ]


def test_oi_concentration_uses_reported_swing_horizon_oi_only():
    ctx = open_interest_concentration.build(_board(), sym='TST')
    assert ctx['available'] is True
    assert ctx['total_reported_open_interest'] == 200
    assert ctx['top_strike'] == 100
    assert ctx['top_strike_share_pct'] == 75.0
    assert ctx['coverage']['oi_zero_reported_count'] == 1


def test_oi_concentration_distinguishes_missing_from_zero_reported():
    ctx = open_interest_concentration.build([{'sym': 'TST', 'dte': 100, 'strike': 100, 'oi': 0}], sym='TST')
    assert ctx['available'] is False
    assert ctx['status'] == 'NO_POSITIVE_OI_REPORTED'
    missing = open_interest_concentration.build([{'sym': 'TST', 'dte': 100, 'strike': 100}], sym='TST')
    assert missing['status'] == 'OI_UNAVAILABLE'


def test_oi_concentration_is_carried_without_scoring_effect():
    ctx = open_interest_concentration.build(_board(), sym='TST')
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'},
                                      open_interest_concentration_ctx=ctx)
    assert packet['contexts']['open_interest_concentration'] == ctx
    assert 'open_interest_concentration' not in skyler_core.score40(packet)['blocks']
