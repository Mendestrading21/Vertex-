"""tests/test_environment.py — SKYLER LOT 104 : environnement options figé.

Trou réel de couverture : vertex/options/environment.py (score « LONG
OPTION ENVIRONMENT » §14 — l'agrégat 5 dimensions que l'espace Options
affiche) n'avait que 3 tests de SURFACE (bornes, IV basse, tableau
vide). Les FORMULES exactes par dimension, les frontières de verdict
66/45 et l'exclusion honnête des dimensions inconnues n'étaient figées
nulle part.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
from vertex.options import environment as env
from vertex.visualization.schemas import ST_DEFAVORABLE, ST_FAVORABLE


def test_volatility_formula_median_20_is_100_and_60_plus_is_0():
    lo = env._score_volatility([{'iv': 20.0}])
    hi = env._score_volatility([{'iv': 75.0}])
    mid = env._score_volatility([{'iv': 40.0}])
    assert lo[0] == 100.0 and hi[0] == 0.0
    assert mid[0] == 50.0                      # (0.60−0.40)/(0.60−0.20)·100
    assert 'IV médiane' in mid[1]


def test_volatility_ignores_strings_and_zero_iv():
    assert env._score_volatility([{'iv': '30'}, {'iv': 0}, {}])[0] is None, (
        'IV textuelle ou nulle = indisponible — jamais convertie en silence')


def test_volatility_excludes_missing_invalid_and_boolean_iv_with_coverage():
    score, note = env._score_volatility([{'iv': 20.0}, {'iv': None}, {'iv': True}, {'iv': 0}])
    assert score == 100.0 and 'IV médiane 20 %' in note
    r = env.score_environment([{'iv': 20.0}, {'iv': None}, {'iv': True}, {'iv': 0}])
    volatility = next(d for d in r['dimensions'] if d['key'] == 'volatility')
    assert volatility['coverage'] == {
        'contracts_total': 4, 'iv_observed': 1, 'iv_missing': 1, 'iv_invalid': 2,
        'status': 'IV_SAMPLE_AVAILABLE', 'read_only': True,
    }


def test_ivrank_inverted_and_clamped():
    assert env._score_ivrank(0)[0] == 100.0    # primes bradées
    assert env._score_ivrank(100)[0] == 0.0
    assert env._score_ivrank(120)[0] == 0.0    # clamp : jamais négatif
    assert env._score_ivrank(None)[0] is None


def test_liquidity_formula_1pct_is_100_8pct_is_0_clamped_above():
    assert env._score_liquidity([{'spread_pct': 1.0}])[0] == 100.0
    assert env._score_liquidity([{'spread_pct': 8.0}])[0] == 0.0
    assert env._score_liquidity([{'spread_pct': 0.5}])[0] == 100.0   # clamp haut
    assert env._score_liquidity([{'spread_pct': 4.5}])[0] == 50.0


def test_event_risk_fraction_and_unknown_when_no_dates():
    board = [{'sym': 'A'}, {'sym': 'B'}]
    half = env._score_event(board, {'A': {'earnings_in_days': 3},
                                    'B': {'earnings_in_days': 40}})
    assert half[0] == 50.0 and '1/2' in half[1]
    none_known = env._score_event(board, {'A': {}, 'B': {}})
    assert none_known[0] is None, 'aucune date connue → INCONNU, pas 100'
    garbage = env._score_event(board, {'A': {'earnings_in_days': 'demain'},
                                       'B': {'earnings_in_days': 2}})
    assert garbage == (50.0, '1/2 titres en earnings ≤7 j'), (
        'réalité figée : une valeur non parsable compte comme CONNUE mais '
        'jamais comme imminente (elle dilue la fraction, sans faux positif)')


def test_label_boundaries_66_45_exact():
    assert env._label(66) == 'PORTEUR' and env._label(65.9) == 'MITIGE'
    assert env._label(45) == 'MITIGE' and env._label(44.9) == 'HOSTILE'
    assert env._label(None) == 'INCONNU'


def test_unknown_dimensions_excluded_from_mean_never_zeroed():
    # Une seule dimension mesurable (liquidité 100) → moyenne = 100, pas 20.
    r = env.score_environment([{'spread_pct': 1.0}])
    assert r['score'] == 100.0 and r['dimensions_known'] == 1
    assert r['dimensions_total'] == 5
    assert r['data_coverage']['coverage_pct'] == 20.0
    assert r['data_coverage']['unknown_dimensions'] == ['volatility', 'iv_rank', 'quality', 'event_risk']
    assert r['data_coverage']['read_only'] is True
    unc = r['interpretation']['uncertainties']
    assert len(unc) == 4, 'chaque dimension absente est NOMMÉE en incertitude'


def test_interpretation_status_follows_verdict():
    porteur = env.score_environment(
        [{'iv': 20.0, 'quality': 90, 'spread_pct': 1.0}])
    assert porteur['label'] == 'PORTEUR'
    assert porteur['interpretation']['status'] == ST_FAVORABLE
    hostile = env.score_environment(
        [{'iv': 75.0, 'quality': 10, 'spread_pct': 9.0}])
    assert hostile['label'] == 'HOSTILE'
    assert hostile['interpretation']['status'] == ST_DEFAVORABLE
    assert hostile['interpretation']['confidence'] == 0.6   # 3 dims sur 5
