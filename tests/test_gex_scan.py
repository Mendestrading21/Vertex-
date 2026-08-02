"""tests/test_gex_scan.py — radar de positionnement GEX multi-titres."""
from vertex.options import gex_scan


def _board():
    return [
        # AAA : gros net GEX positif (stabilisant, haussier)
        {'sym': 'AAA', 'type': 'CALL', 'strike': 110, 'gamma': 0.06, 'oi': 8000, 'spot': 100},
        {'sym': 'AAA', 'type': 'PUT', 'strike': 90, 'gamma': 0.01, 'oi': 500, 'spot': 100},
        # BBB : net négatif (accélérateur)
        {'sym': 'BBB', 'type': 'PUT', 'strike': 45, 'gamma': 0.05, 'oi': 4000, 'spot': 50},
        # CCC : inexploitable (pas d'OI) → ignoré
        {'sym': 'CCC', 'type': 'CALL', 'strike': 210, 'gamma': 0.04, 'oi': None, 'spot': 200},
    ]


def test_scan_ranks_by_abs_net_gex():
    d = gex_scan.scan(_board())
    assert d['empty'] is False
    assert d['symbols_scanned'] == 3
    assert d['symbols_usable'] == 2                    # CCC ignoré, jamais estimé
    assert [r['symbol'] for r in d['rows']] == ['AAA', 'BBB']   # |net| décroissant
    aaa = d['rows'][0]
    assert aaa['regime'] == 'stabilisant' and aaa['bias'] == 'haussier'
    assert d['rows'][1]['regime'] == 'accelerateur'


def test_counts_and_climate():
    d = gex_scan.scan(_board())
    assert d['counts']['stabilisant'] == 1 and d['counts']['accelerateur'] == 1
    assert d['climate'] == 'régimes mixtes selon les titres'


def test_spot_fallback_from_detail():
    board = [{'sym': 'DDD', 'type': 'CALL', 'strike': 105, 'gamma': 0.05, 'oi': 1000}]
    d = gex_scan.scan(board, {'DDD': {'price': 100}})
    assert d['rows'] and d['rows'][0]['spot'] == 100


def test_top_bound():
    d = gex_scan.scan(_board(), top=1)
    assert len(d['rows']) == 1 and d['rows'][0]['symbol'] == 'AAA'


def test_empty_board_honest():
    d = gex_scan.scan([])
    assert d['empty'] is True and d['rows'] == [] and d['reason']
