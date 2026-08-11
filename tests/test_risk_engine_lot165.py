"""
LOT 165 — Caractérisation du moteur de risque du portefeuille RÉEL
(`vertex/portfolio/risk_engine.py`, §26 — servi par strategy_os ;
seule l'honnêteté des greeks était couverte par test_calc_honesty).

Ces tests figent la garde de provenance, les règles de discipline
(-25 % portefeuille / -20 % par titre / plafond d'options) et les
agrégats — les changer devient une décision explicite.
"""

import pytest

from vertex.portfolio.models import Position, PortfolioSnapshot
from vertex.portfolio.risk_engine import portfolio_risk


class _Profil:
    max_stock_weight_pct = 15.0
    portfolio_max_drawdown_pct = -25.0
    stock_max_drawdown_pct = -20.0
    max_simultaneous_options = 3


def _snap():
    # BIG 1000 (66.67 %), SML 200 (13.33 %, -23 % vs coût), cash 300 —
    # équité 1500 contre un pic de 2000 → drawdown -25 % PILE.
    return PortfolioSnapshot(positions=[
        Position('BIG', 10, avg_cost=50.0, last_price=100.0, beta=1.5, sector='Tech'),
        Position('SML', 2, avg_cost=130.0, last_price=100.0, beta=0.5, sector='Tech'),
    ], cash=300.0, provenance='REAL', peak_equity=2000.0)


# ── Garde de provenance : jamais sur les candidats du scanner ────────────────

def test_provenance_scanner_refusee():
    with pytest.raises(ValueError):
        portfolio_risk(PortfolioSnapshot(provenance='SCANNER'), _Profil())


# ── Poids, concentration, secteurs, bêta ─────────────────────────────────────

def test_surpoids_hhi_secteur_et_beta_pondere():
    r = portfolio_risk(_snap(), _Profil())
    assert r['overweight'] == {'BIG': 66.67}                 # > max 15 %
    assert any('BIG: poids 66.67%' in w for w in r['warnings'])
    assert r['hhi'] == 0.4623                                # (0.6667² + 0.1333²)
    assert r['sector_weights'] == {'Tech': 80.0}
    assert any('secteur Tech à 80.0%' in w for w in r['warnings'])   # > 40 %
    assert r['beta'] == 1.07     # 0.6667×1.5 + 0.1333×0.5 (pondéré par poids)


def test_beta_none_sans_aucun_beta_connu():
    snap = PortfolioSnapshot(positions=[Position('A', 1, last_price=100.0)],
                             cash=0, provenance='SIMULATED')
    assert portfolio_risk(snap, _Profil())['beta'] is None   # jamais un 1.0 inventé


# ── Règles de discipline : -25 % portefeuille, -20 % par titre ───────────────

def test_drawdown_25_pct_pile_bloque_tout_nouveau_risque():
    r = portfolio_risk(_snap(), _Profil())
    assert r['drawdown_pct'] == -25.0
    assert r['no_new_risk'] is True                          # borne INCLUSE (≤)
    assert any('AUCUN nouveau risque' in w for w in r['warnings'])


def test_titre_sous_moins_20_pct_revue_obligatoire():
    r = portfolio_risk(_snap(), _Profil())
    assert r['per_stock_pl_pct'] == {'BIG': 100.0, 'SML': -23.1}
    assert any('SML: -23.1%' in w and 'revue de position obligatoire' in w
               for w in r['warnings'])


# ── Exposition options : plafond et agrégat honnête ──────────────────────────

def test_plafond_options_depasse_bloque_et_partial_signale():
    og = [{'delta': 0.5, 'theta': -0.1}, {'delta': None},
          {'delta': 0.3}, {'delta': 0.2}]
    snap = PortfolioSnapshot(positions=[Position('A', 1, last_price=100.0)],
                             cash=0, provenance='SIMULATED')
    r = portfolio_risk(snap, _Profil(), options_greeks=og)
    g = r['options_exposure']
    assert g['open_options'] == 4 and r['no_new_risk'] is True   # 4 > max 3
    assert g['delta'] == 1.0                  # somme des seuls deltas CONNUS
    assert g['gamma'] is None                 # aucun gamma → None, pas 0
    assert g['greeks_partial'] is True        # un delta manquant → signalé


def test_sans_options_greeks_defauts_none():
    snap = PortfolioSnapshot(positions=[Position('A', 1, last_price=100.0)],
                             cash=0, provenance='SIMULATED')
    g = portfolio_risk(snap, _Profil())['options_exposure']
    assert g == {'delta': None, 'gamma': None, 'theta': None, 'vega': None,
                 'open_options': 0}


# ── Contrat de sortie ────────────────────────────────────────────────────────

def test_contrat_du_rapport_de_risque():
    r = portfolio_risk(_snap(), _Profil())
    assert set(r) == {'provenance', 'as_of', 'equity', 'weights',
                      'sector_weights', 'hhi', 'beta', 'correlations',
                      'drawdown_pct', 'per_stock_pl_pct', 'options_exposure',
                      'overweight', 'no_new_risk', 'warnings'}
    assert r['provenance'] == 'REAL' and r['equity'] == 1500.0
