"""Le laboratoire options ne doit jamais classer une échéance absente par repli."""

from vertex.engines import options_lab


def test_tops_excludes_missing_or_invalid_dte_from_horizon_categories():
    board = [
        {'sym': 'SHORT', 'type': 'CALL', 'dte': 30, 'quality': 80, 'pop': 55},
        {'sym': 'LONG', 'type': 'CALL', 'dte': 180, 'quality': 80, 'pop': 55},
        {'sym': 'MISSING', 'type': 'CALL', 'dte': None, 'quality': 99, 'pop': 99},
        {'sym': 'INVALID', 'type': 'CALL', 'dte': 'inconnu', 'quality': 99, 'pop': 99},
    ]
    by_key = {entry['key']: entry['rows'] for entry in options_lab._tops(board, {})}
    assert [row['sym'] for row in by_key['top_short']] == ['SHORT']
    assert [row['sym'] for row in by_key['top_long']] == ['LONG']
    assert 'MISSING' not in [row['sym'] for row in by_key.get('top_leaps', [])]
    assert 'INVALID' not in [row['sym'] for row in by_key.get('top_leaps', [])]
