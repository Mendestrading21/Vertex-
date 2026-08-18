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
    assert rows['Volatilité du sous-jacent']['level'] == 'INCONNU'
    assert rows['Volatilité du sous-jacent']['coverage'] == {
        'available': False, 'status': 'EXPECTED_MOVE_UNAVAILABLE', 'read_only': True,
    }


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


def test_viz_refuses_missing_core_option_inputs_without_synthetic_curves():
    viz = options_lab._viz({'sym': 'TST', 'spot': None, 'strike': None, 'iv': None,
                             'dte': None, 'cost': None, 'type': 'CALL'}, [], {}, None)
    assert viz['unavailable'] is True
    assert viz['coverage']['status'] == 'OPTION_VIZ_INPUT_UNAVAILABLE'
    assert viz['payoff']['points'] == []
    assert viz['cone'] == [] and viz['theta'] == []
    assert viz['em'] == {'pct': None, 'lo': None, 'hi': None}


def test_viz_exposes_missing_expected_move_and_break_even_without_neutral_values():
    star = {'sym': 'TST', 'spot': 100, 'strike': 105, 'iv': 30, 'dte': 90,
            'cost': 250, 'type': 'CALL', 'be': None, 'em_pct': None}
    viz = options_lab._viz(star, [], {}, None)
    assert viz['unavailable'] is False
    assert viz['dist']['be'] is None and viz['dist']['p_be'] is None
    assert viz['dist']['coverage']['status'] == 'BREAK_EVEN_UNAVAILABLE'
    assert viz['em']['pct'] is None and viz['em']['lo'] is None and viz['em']['hi'] is None
    assert viz['em']['coverage']['status'] == 'EXPECTED_MOVE_UNAVAILABLE'


def test_zero_expected_move_is_not_presented_as_a_flat_range_around_spot():
    star = {'sym': 'TST', 'spot': 100, 'strike': 105, 'iv': 30, 'dte': 90,
            'cost': 250, 'type': 'CALL', 'em_pct': 0}
    viz = options_lab._viz(star, [], {}, None)
    risks = options_lab._risks(star, {})
    volatility_risk = next(row for row in risks if row['name'] == 'Volatilité du sous-jacent')
    assert viz['em']['pct'] is None
    assert viz['em']['lo'] is None and viz['em']['hi'] is None
    assert viz['em']['coverage']['status'] == 'EXPECTED_MOVE_UNAVAILABLE'
    assert volatility_risk['level'] == 'INCONNU'
    assert volatility_risk['coverage']['status'] == 'EXPECTED_MOVE_UNAVAILABLE'


def test_viz_exposes_missing_kelly_inputs_without_default_fraction():
    star = {'sym': 'TST', 'spot': 100, 'strike': 105, 'iv': 30, 'dte': 90,
            'cost': 250, 'type': 'CALL', 'pop': None, 'pot': None}
    viz = options_lab._viz(star, [], {}, None)
    assert viz['kelly']['pct'] is None
    assert viz['kelly']['coverage'] == {
        'pop_available': False, 'potential_available': False,
        'status': 'KELLY_INPUT_UNAVAILABLE', 'read_only': True,
    }


def test_viz_radar_exposes_missing_greeks_without_defaults():
    star = {'sym': 'TST', 'spot': 100, 'strike': 105, 'iv': 30, 'dte': 90,
            'cost': 250, 'type': 'CALL', 'delta': None, 'theta_burn': None}
    viz = options_lab._viz(star, [], {}, None)
    assert viz['radar']['Delta'] is None
    assert viz['radar']['Gamma'] is None
    assert viz['radar']['Theta'] is None
    assert viz['radar']['Vega'] is None
    assert viz['radar']['IV'] == 42.0
    assert viz['radar_coverage'] == {
        'available': {'delta': False, 'gamma': False, 'theta': False, 'vega': False, 'iv': True},
        'status': 'RADAR_GREEKS_PARTIAL', 'read_only': True,
    }


def test_analysis_liquidity_exposes_missing_oi_or_spread_without_imputation():
    rows = {row['key']: row for row in options_lab._analysis(
        {'sym': 'TST', 'type': 'CALL', 'oi': None, 'spread_pct': None}, {}, {}, [], {})}
    liquidity = rows['liquidity']
    assert liquidity['coverage'] == {
        'oi_available': False, 'spread_available': False,
        'status': 'LIQUIDITY_INPUT_UNAVAILABLE', 'read_only': True,
    }
    assert 'aucune imputation appliquée' in liquidity['text']


def test_analysis_options_does_not_call_missing_iv_a_correct_premium():
    rows = {row['key']: row for row in options_lab._analysis(
        {'sym': 'TST', 'type': 'CALL', 'iv': None}, {}, {}, [], {})}
    options = rows['options']
    assert options['impact'] == 'coût de prime indisponible'
    assert options['coverage'] == {
        'iv_available': False,
        'status': 'PREMIUM_COST_IV_UNAVAILABLE',
        'read_only': True,
    }


def test_committee_liquidity_excludes_missing_spread_without_default():
    board = [
        {'sym': 'MISSING', 'type': 'CALL', 'strike': 100, 'dte': 90,
         'oi': 20000, 'spread_pct': None, 'quality': 99},
        {'sym': 'VALID', 'type': 'CALL', 'strike': 100, 'dte': 90,
         'oi': 5000, 'spread_pct': 2, 'quality': 70},
    ]
    committee = {row['title']: row for row in options_lab._committee(board, {}, [], board[0])}
    liquidity = committee['Meilleure liquidité']
    assert 'VALID' in liquidity['winner']
    assert liquidity['coverage'] == {
        'available': True, 'status': 'COMMITTEE_LIQUIDITY_AVAILABLE', 'read_only': True,
    }


def test_plan_exposes_missing_dte_without_an_expiry_timeline():
    plan = options_lab._plan({'sym': 'TST', 'dte': None, 'exp': None}, {}, None)
    assert plan['timeline_coverage'] == {
        'dte_available': False, 'status': 'TRADE_PLAN_DTE_UNAVAILABLE', 'read_only': True,
    }
    steps = {step['key']: step['text'] for step in plan['steps']}
    assert 'DTE non reporté' in steps['exit']
    assert 'aucune échéance n’est inférée' in steps['expiry']


def test_timeline_missing_dte_has_no_default_ninety_day_management_dates():
    timeline = options_lab._timeline({'sym': 'TST', 'dte': None, 'cost': 250}, None)
    assert len(timeline) == 2
    assert timeline[1]['coverage'] == {
        'dte_available': False, 'status': 'TIMELINE_DTE_UNAVAILABLE', 'read_only': True,
    }
    assert all('J+90' not in row['when'] for row in timeline)
