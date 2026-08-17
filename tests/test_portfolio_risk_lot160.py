"""
LOT 160 — Caractérisation de la famille RISQUE PORTEFEUILLE :
corrélations (`vertex/portfolio/correlation.py` — consommées par
risk_engine → drapeaux du Command Center) et stress tests
(`vertex/portfolio/stress_tests.py` — servis par la route
strategy_os, §26). Deux modules à ZÉRO test direct.

Ces tests figent les gardes, les hypothèses documentées et les
scénarios — les changer devient une décision explicite. Données
déterministes (graine fixe).
"""

import numpy as np

from vertex.portfolio import correlation as co
from vertex.portfolio import stress_tests as stt
from vertex.portfolio.models import Position, PortfolioSnapshot


def _series():
    rng = np.random.default_rng(5)
    a = list(rng.normal(0, 1, 60))
    b = [-x for x in a]
    c = [x * 0.9 + y for x, y in zip(a, rng.normal(0, 0.1, 60))]
    return a, b, c


class _Profil:
    portfolio_max_drawdown_pct = -15.0


def _snap():
    return PortfolioSnapshot(positions=[
        Position('AAA', 10, last_price=100.0, beta=1.5, sector='Tech'),
        Position('BBB', 10, last_price=100.0, beta=None, sector='Sante'),
    ], cash=1000.0)


# ═══ correlation ═══

def test_corr_bornes_identite_et_opposition():
    a, b, _ = _series()
    assert co._corr(a, a) == 1.0
    assert co._corr(a, b) == -1.0


def test_corr_gardes_moins_de_30_points_et_variance_nulle():
    a, _, _ = _series()
    assert co._corr(a[:29], a[:29]) is None       # < 30 points → None
    assert co._corr([1.0] * 40, a[:40]) is None   # série constante → None


def test_matrice_paires_triees_seuils_et_contrat():
    a, b, c = _series()
    m = co.correlation_matrix({'B': b, 'A': a, 'C': c})
    assert list(m['pairs']) == ['A/B', 'A/C', 'B/C']     # symboles triés
    assert m['high_pairs'] == {'A/C': m['pairs']['A/C']}  # seuil ≥ 0.8
    assert m['pairs']['A/C'] >= 0.8
    # moyenne négative (A/B et B/C ≈ -1) → pas d'avertissement (seuil 0.7)
    assert m['average'] < 0.7 and m['warning'] is None
    assert m['symbols_covered'] == ['A', 'B', 'C']


def test_matrice_vide_honnete():
    assert co.correlation_matrix({}) == {
        'pairs': {}, 'average': None, 'high_pairs': {},
        'symbols_covered': [],
        'coverage': {'measured_pairs': 0, 'total_pairs': 0,
                     'unmeasured_pairs': [], 'coverage_pct': 0.0,
                     'read_only': True,
                     'note': 'paires sans historique commun suffisant ne reçoivent aucune corrélation'},
        'warning': None}


def test_candidat_moyenne_des_correlations_ou_none():
    a, b, c = _series()
    r = co.candidate_correlation(a, {'X': c, 'Y': b})
    assert r is not None and -1 <= r <= 1
    assert co.candidate_correlation(a, {}) is None       # rien à comparer


# ═══ stress_tests ═══

def test_choc_marche_beta_inconnu_vaut_1_documente():
    # AAA bêta 1.5, BBB bêta None → 1.0 (hypothèse DOCUMENTÉE dans
    # assumptions). Poids 33.33 % chacun (+ cash 33.33 %) :
    # SPY -5 % → (0.3333×1.5 + 0.3333×1.0) × -5 = -4.17 %.
    r = stt.run_stress_tests(_snap(), _Profil())
    assert r['scenarios']['SPY_MINUS_5']['impact_pct'] == -4.17
    assert r['scenarios']['SPY_MINUS_10']['impact_pct'] == -8.33
    assert any('bêta 1.0 si inconnu' in a for a in r['assumptions'])


def test_secteur_dominant_et_cash_protege_correlations_a_un():
    r = stt.run_stress_tests(_snap(), _Profil())
    top = r['scenarios']['TOP_SECTOR_MINUS_15']
    assert top['sector'] == 'Tech' and top['impact_pct'] == -5.0  # -15 × 33.33 %
    # CORRELATIONS_TO_ONE : choc -10 % sur les ACTIONS seulement —
    # le cash (33 %) protège : -10 × 66.67 % = -6.67.
    assert r['scenarios']['CORRELATIONS_TO_ONE']['impact_pct'] == -6.67


def test_sensibilite_taux_inconnue_none_honnete_fournie_calculee():
    sans = stt.run_stress_tests(_snap(), _Profil())
    assert sans['scenarios']['RATES_PLUS_50BP']['impact_pct'] is None
    assert 'inconnue' in sans['scenarios']['RATES_PLUS_50BP']['note']
    avec = stt.run_stress_tests(_snap(), _Profil(), rate_sensitivity_bp=-0.02)
    assert avec['scenarios']['RATES_PLUS_50BP']['impact_pct'] == -1.0
    assert avec['scenarios']['RATES_MINUS_50BP']['impact_pct'] == 1.0  # symétrique


def test_equite_incalculable_stress_refuses():
    vide = PortfolioSnapshot(positions=[Position('X', 1, last_price=None)], cash=0.0)
    r = stt.run_stress_tests(vide, _Profil())
    assert r['scenarios'] == {}
    assert any('refusés' in w for w in r['warnings'])


def test_pire_scenario_et_alerte_drawdown():
    class ProfilSerre:
        portfolio_max_drawdown_pct = -3.0
    ok = stt.run_stress_tests(_snap(), _Profil())
    assert ok['worst_case_pct'] == -8.33 and ok['warnings'] == []
    serre = stt.run_stress_tests(_snap(), ProfilSerre())
    assert any('dépasse le drawdown max' in w for w in serre['warnings'])


def test_les_10_scenarios_declares_tous_presents():
    r = stt.run_stress_tests(_snap(), _Profil(),
                             rate_sensitivity_bp=-0.02)
    assert set(r['scenarios']) == set(stt.SCENARIOS)
