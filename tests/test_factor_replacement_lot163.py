"""
LOT 163 — Caractérisation de l'exposition factorielle
(`vertex/portfolio/factor_exposure.py`) et du moteur de remplacement
(`vertex/portfolio/replacement_engine.py`) — deux modules zéro-test
(§25). Dépendances research/ monkeypatchées (déterministe, léger).

+ VÉRIFICATION DE VIE des deux legacy (voir rapport) :
legacy_basket_risk et legacy_adapter sont VIVANTS — servis par
analysis_api/command/risk_engine et command/terminal respectivement.

Ces tests figent la pondération par poids réels, l'honnêteté de
couverture et la logique de remplacement (proposition, jamais une
exécution) — les changer devient une décision explicite.
"""

import pytest

from vertex.portfolio import factor_exposure as fe
from vertex.portfolio import replacement_engine as rep
from vertex.portfolio.models import Position, PortfolioSnapshot
from vertex.research.institutional.factor_model import FACTORS
from vertex.research.institutional.factor_model import factor_exposures


@pytest.fixture()
def _fake_factors(monkeypatch):
    # Chaque titre expose la valeur 'v' de sa fiche sur TOUS les facteurs.
    monkeypatch.setattr(fe, 'factor_exposures',
                        lambda data, bench=None: {f: {'value': data.get('v', 1.0)}
                                                  for f in FACTORS})


def _snap_50_50():
    return PortfolioSnapshot(positions=[
        Position('AAA', 10, last_price=100.0),
        Position('BBB', 10, last_price=100.0),
    ], cash=0.0)


# ═══ factor_exposure : pondération et honnêteté de couverture ═══

def test_exposition_ponderee_par_les_poids_reels(_fake_factors):
    agg = fe.portfolio_factor_exposure(_snap_50_50(),
                                       {'AAA': {'v': 2.0}, 'BBB': {'v': 1.0}})
    # 0.5×2.0 + 0.5×1.0 = 1.5, couverture 100 % → pas de note.
    assert agg['MARKET'] == {'value': 1.5, 'coverage_pct': 100.0}


def test_couverture_partielle_signalee(_fake_factors):
    # BBB sans fiche : exposition 0.5×2.0 = 1.0 mais couverture 50 % →
    # note « couverture partielle — exposition indicative » (honnêteté).
    agg = fe.portfolio_factor_exposure(_snap_50_50(), {'AAA': {'v': 2.0}})
    m = agg['MARKET']
    assert m['value'] == 1.0 and m['coverage_pct'] == 50.0
    assert 'couverture partielle' in m['note']


def test_aucune_donnee_value_none_jamais_zero_invente(_fake_factors):
    agg = fe.portfolio_factor_exposure(_snap_50_50(), {})
    assert agg['MARKET'] == {'value': None, 'coverage_pct': 0.0}
    assert set(agg) == set(FACTORS)          # les 10 facteurs toujours présents


def test_beta_is_explicitly_available_only_with_benchmark():
    returns = [0.01 if i % 2 else -0.005 for i in range(40)]
    with_benchmark = factor_exposures({'returns': returns}, returns)
    without_benchmark = factor_exposures({'returns': returns}, None)
    assert with_benchmark['BETA']['value'] is not None
    assert without_benchmark['BETA']['value'] is None
    assert 'benchmark absent' in without_benchmark['BETA']['note']


# ═══ replacement_engine : proposition, jamais une exécution ═══

def _team():
    return PortfolioSnapshot(positions=[
        Position('OLD1', 1, last_price=100.0, role='ATTACKER'),
        Position('OLD2', 1, last_price=100.0, role='ATTACKER'),
        Position('DEF', 1, last_price=100.0, role='DEFENDER'),
    ], cash=0.0)


def test_place_disponible_pas_de_remplacement(monkeypatch):
    monkeypatch.setattr(rep, 'candidate_fit', lambda s, p, c: {'blocked': False})
    r = rep.propose_replacement(_team(), None, {'symbol': 'NEW', 'role': 'ATTACKER'})
    assert r['replacement_candidate'] is None
    assert 'place disponible' in r['notes'][0]


def test_bloque_propose_la_plus_faible_du_role_decision_humaine(monkeypatch):
    monkeypatch.setattr(rep, 'candidate_fit', lambda s, p, c: {'blocked': True})
    r = rep.propose_replacement(_team(), None, {'symbol': 'NEW', 'role': 'ATTACKER'},
                                {'OLD1': 40, 'OLD2': 70, 'NEW': 80})
    assert r['replacement_candidate'] == {'symbol': 'OLD1', 'role': 'ATTACKER',
                                          'score': 40}
    assert 'décision humaine requise' in r['notes'][0]   # jamais une exécution


def test_candidat_moins_bon_remplacement_deconseille(monkeypatch):
    monkeypatch.setattr(rep, 'candidate_fit', lambda s, p, c: {'blocked': True})
    r = rep.propose_replacement(_team(), None, {'symbol': 'NEW', 'role': 'ATTACKER'},
                                {'OLD1': 40, 'OLD2': 70, 'NEW': 30})
    assert 'n’améliore pas' in r['notes'][0]
    assert 'déconseillé' in r['notes'][0]


def test_role_sans_membre_pool_global(monkeypatch):
    # Aucun GOALKEEPER en équipe → le pool devient TOUTES les positions
    # (comportement documenté) — la plus faible globale est proposée.
    monkeypatch.setattr(rep, 'candidate_fit', lambda s, p, c: {'blocked': True})
    r = rep.propose_replacement(_team(), None, {'symbol': 'NEW', 'role': 'GOALKEEPER'},
                                {'DEF': 10, 'OLD1': 50, 'OLD2': 60, 'NEW': 90})
    assert r['replacement_candidate']['symbol'] == 'DEF'


def test_sans_scores_defaut_50_et_score_none_honnete(monkeypatch):
    # Sans dictionnaire de scores : départage au défaut 50, mais le score
    # AFFICHÉ reste None (pas un 50 inventé à l'écran).
    monkeypatch.setattr(rep, 'candidate_fit', lambda s, p, c: {'blocked': True})
    r = rep.propose_replacement(_team(), None, {'symbol': 'NEW', 'role': 'ATTACKER'})
    assert r['replacement_candidate']['score'] is None
    assert 'décision humaine requise' in r['notes'][0]
