from vertex.engines import iv_skew_context
from vertex.engines import skyler_core


def _board():
    return [
        {'sym': 'TST', 'type': 'PUT', 'strike': 90, 'iv': 42.0},
        {'sym': 'TST', 'type': 'PUT', 'strike': 95, 'iv': 40.0},
        {'sym': 'TST', 'type': 'CALL', 'strike': 105, 'iv': 30.0},
        {'sym': 'TST', 'type': 'CALL', 'strike': 110, 'iv': 28.0},
        {'sym': 'OTHER', 'type': 'PUT', 'strike': 80, 'iv': 90.0},
    ]


def test_iv_skew_uses_observed_otm_contracts_for_symbol_only():
    ctx = iv_skew_context.build(_board(), sym='TST', spot=100)
    assert ctx['available'] is True
    assert ctx['status'] == 'OBSERVED_OTM_IV_SKEW'
    assert ctx['skew_iv_points'] == 12.0
    assert ctx['coverage'] == {'contracts_considered': 4, 'put_otm_with_iv': 2, 'call_otm_with_iv': 2}


def test_iv_skew_refuses_absent_spot_or_one_sided_iv():
    assert iv_skew_context.build(_board(), sym='TST', spot=None)['status'] == 'SPOT_UNAVAILABLE'
    ctx = iv_skew_context.build([{'sym': 'TST', 'type': 'PUT', 'strike': 90, 'iv': 42.0}], sym='TST', spot=100)
    assert ctx['status'] == 'INSUFFICIENT_OTM_CALL_PUT_IV'


def test_iv_skew_is_carried_without_scoring_effect():
    ctx = iv_skew_context.build(_board(), sym='TST', spot=100)
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, iv_skew_ctx=ctx)
    assert packet['contexts']['iv_skew'] == ctx
    assert 'iv_skew' not in skyler_core.score40(packet)['blocks']
