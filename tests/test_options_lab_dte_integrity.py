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


def test_risks_exposes_missing_iv_dte_and_spread_without_defaults():
    rows = {row['name']: row for row in options_lab._risks({'theta_burn': 0.2}, {})}
    for name, status in (
        ('IV crush', 'IV_UNAVAILABLE'),
        ('Liquidité', 'SPREAD_UNAVAILABLE'),
        ('Spread (fourchette)', 'SPREAD_UNAVAILABLE'),
        ('Résultats trimestriels', 'DTE_UNAVAILABLE'),
        ('Expiration', 'DTE_UNAVAILABLE'),
    ):
        assert rows[name]['level'] == 'INCONNU'
        assert rows[name]['coverage'] == {'available': False, 'status': status, 'read_only': True}


def test_comparator_refuses_missing_spot_or_iv_without_default_prices():
    comparator = options_lab._comparator({'sym': 'TST', 'spot': None, 'iv': None}, None, {})
    assert comparator == {
        'symbol': 'TST', 'unavailable': True, 'rows': [],
        'reason': 'matrice de véhicules indisponible — spot ou IV non reporté',
        'coverage': {
            'spot_available': False, 'iv_available': False,
            'status': 'VEHICLE_MATRIX_INPUT_UNAVAILABLE', 'read_only': True,
        },
    }


def test_comparator_does_not_invent_pop_or_break_even_metrics():
    star = {'sym': 'TST', 'spot': 100, 'iv': 30, 'pop': None}
    comparator = options_lab._comparator(star, None, {})
    rows = {row['name']: row for row in comparator['rows']}
    assert rows['Action (100 titres)']['be'] == 100.0
    assert rows['Action (100 titres)']['coverage']['break_even_observed'] is True
    for name, row in rows.items():
        assert row['pop'] is None
        assert row['coverage']['pop_available'] is False
        if name != 'Action (100 titres)':
            assert row['be'] is None
            assert row['coverage']['break_even_available'] is False


def test_strategies_expose_missing_iv_without_iv_default_scoring():
    result = options_lab._strategies({'sym': 'TST', 'iv': None}, {'spy_regime': 'CHOP', 'roro': 'RISK-ON'})
    assert result['coverage'] == {'iv_available': False, 'status': 'IV_UNAVAILABLE', 'read_only': True}
    assert 'IV indisponible' in result['ai']
    assert '40%' not in result['ai']
    assert all(row['coverage']['iv_available'] is False for row in result['items'])
