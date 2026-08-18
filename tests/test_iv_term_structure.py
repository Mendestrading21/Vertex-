from vertex.engines import iv_term_structure
from vertex.engines import skyler_core


def _board():
    return [
        {'sym': 'TST', 'dte': 30, 'iv': 40.0}, {'sym': 'TST', 'dte': 45, 'iv': 44.0},
        {'sym': 'TST', 'dte': 120, 'iv': 30.0}, {'sym': 'TST', 'dte': 150, 'iv': 34.0},
        {'sym': 'OTHER', 'dte': 30, 'iv': 99.0},
    ]


def test_term_structure_uses_observed_short_and_long_contracts_for_symbol():
    ctx = iv_term_structure.build(_board(), sym='TST')
    assert ctx['available'] is True
    assert ctx['status'] == 'OBSERVED_IV_TERM_STRUCTURE'
    assert ctx['short_median_iv'] == 42.0
    assert ctx['long_median_iv'] == 32.0
    assert ctx['long_minus_short_iv_points'] == -10.0
    assert ctx['coverage']['contracts_considered'] == 4


def test_term_structure_refuses_missing_short_or_long_observations():
    ctx = iv_term_structure.build([{'sym': 'TST', 'dte': 30, 'iv': 40.0}], sym='TST')
    assert ctx['available'] is False
    assert ctx['status'] == 'INSUFFICIENT_SHORT_LONG_IV'


def test_term_structure_is_carried_without_scoring_effect():
    ctx = iv_term_structure.build(_board(), sym='TST')
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, iv_term_structure_ctx=ctx)
    assert packet['contexts']['iv_term_structure'] == ctx
    assert 'iv_term_structure' not in skyler_core.score40(packet)['blocks']
