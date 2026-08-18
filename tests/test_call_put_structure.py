from vertex.engines import call_put_structure
from vertex.engines import skyler_core


def test_call_put_structure_uses_observed_contracts_for_symbol_only():
    board = [{'sym': 'TST', 'type': 'CALL'}, {'sym': 'TST', 'type': 'CALL'},
             {'sym': 'TST', 'type': 'PUT'}, {'sym': 'OTHER', 'type': 'PUT'}]
    ctx = call_put_structure.build(board, sym='TST')
    assert ctx['available'] is True
    assert ctx['status'] == 'OBSERVED_CALL_PUT_STRUCTURE'
    assert ctx['call_put_ratio'] == 2.0
    assert ctx['coverage'] == {'contracts_considered': 3, 'calls': 2, 'puts': 1}


def test_call_put_structure_marks_one_sided_or_missing_board():
    assert call_put_structure.build([], sym='TST')['status'] == 'OPTION_BOARD_UNAVAILABLE'
    assert call_put_structure.build([{'sym': 'TST', 'type': 'CALL'}], sym='TST')['status'] == 'ONE_SIDED_CONTRACT_SET'


def test_call_put_structure_is_carried_without_scoring_effect():
    ctx = call_put_structure.build([{'sym': 'TST', 'type': 'CALL'}, {'sym': 'TST', 'type': 'PUT'}], sym='TST')
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, call_put_structure_ctx=ctx)
    assert packet['contexts']['call_put_structure'] == ctx
    assert 'call_put_structure' not in skyler_core.score40(packet)['blocks']
