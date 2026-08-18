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


def test_committee_excludes_missing_or_invalid_dte_from_horizon_winners():
    board = [
        {'sym': 'SHORT', 'type': 'CALL', 'dte': 30, 'quality': 80, 'pop': 55},
        {'sym': 'LONG', 'type': 'CALL', 'dte': 180, 'quality': 80, 'pop': 55},
        {'sym': 'MISSING', 'type': 'CALL', 'dte': None, 'quality': 99, 'pop': 99},
        {'sym': 'INVALID', 'type': 'CALL', 'dte': 'inconnu', 'quality': 99, 'pop': 99},
    ]
    committee = options_lab._committee(board, {}, [], board[0])
    by_title = {row['title']: row['winner'] for row in committee}
    assert 'SHORT' in by_title['Meilleur court terme']
    assert 'LONG' in by_title['Meilleur long terme']
    assert by_title['Meilleur LEAPS'] == '—'


def test_overview_leaps_count_excludes_missing_or_invalid_dte():
    board = [
        {'sym': 'VALID', 'type': 'CALL', 'dte': 365, 'quality': 70, 'iv': 30, 'pop': 55},
        {'sym': 'MISSING', 'type': 'CALL', 'dte': None, 'quality': 99, 'iv': 30, 'pop': 55},
        {'sym': 'INVALID', 'type': 'CALL', 'dte': 'inconnu', 'quality': 99, 'iv': 30, 'pop': 55},
    ]
    overview = options_lab._overview(board, {}, {}, False)
    assert overview['leaps'] == 1


def test_risks_exposes_missing_theta_without_default_erosion():
    theta = next(row for row in options_lab._risks({'iv': 30, 'dte': 180}, {})
                 if row['name'] == 'Thêta (érosion du temps)')
    assert theta['level'] == 'INCONNU'
    assert theta['coverage'] == {
        'available': False,
        'status': 'THETA_BURN_UNAVAILABLE',
        'read_only': True,
    }
    assert 'non quantifiée' in theta['impact']
