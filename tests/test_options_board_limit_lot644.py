from vertex.options import horizon_scanners as scanner


def _contract(index):
    return {'sym': 'TST', 'type': 'CALL', 'dte': 135, 'strike': 100 + index,
            'quality': 50, 'delta': .4, 'oi': 600, 'volume': 80, 'spread_pct': 2}


def test_scan_bounded_board_is_explicit_when_limit_reached(monkeypatch):
    monkeypatch.setattr(scanner, 'MAX_BOARD_CONTRACTS', 2)
    out = scanner.scan([_contract(i) for i in range(3)], 'SWING_3_6M', sym='TST')
    assert out['input_truncated'] is True
    assert out['input_contracts_inspected'] == 2
    assert out['input_contracts_total'] == 3
    ctx = scanner.options_context(out)
    assert ctx['input_truncated'] is True


def test_scan_reports_untruncated_input_size():
    out = scanner.scan([_contract(1)], 'SWING_3_6M', sym='TST')
    assert out['input_truncated'] is False
    assert out['input_contracts_total'] == 1
