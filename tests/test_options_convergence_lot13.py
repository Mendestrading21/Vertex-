"""tests/test_options_convergence_lot13.py — LOT 13 : convergence options.

Trois implémentations Black-Scholes vivent dans le dépôt (legacy_engine,
scenario_pricer, multileg_lab._leg_greeks). legacy ↔ scenario_pricer était
déjà verrouillé (test_calculations_golden) ; la TROISIÈME restait sans
comparaison — une dérive silencieuse du labo multi-jambes serait invisible.
Accord + parité : caractérisations ATTENDUES VERTES (dites). Devise : né
ROUGE (l'hypothèse USD n'était jamais déclarée).
"""
import math

from vertex.engines import multileg_lab as ML
from vertex.options.legacy_engine import _bs_price, _greeks

_CAS = [                                     # (spot, strike, dte_jours, iv)
    (100.0, 100.0, 30, 0.25),                # ATM court
    (100.0, 120.0, 180, 0.35),               # OTM call 6 mois
    (250.0, 200.0, 90, 0.20),                # ITM call
    (50.0, 55.0, 365, 0.60),                 # haute vol 1 an
]


def _leg(typ, strike, qty=1.0):
    return {'type': typ, 'strike': strike, 'qty': qty, 'premium': 1.0}


def _unitaires(typ, spot, strike, T, iv):
    """Greeks multileg ramenés à UNE option (÷ qty·multiplicateur)."""
    g = ML._leg_greeks(spot, _leg(typ, strike), T, iv)
    m = ML._mult(_leg(typ, strike))
    return {k: v / m for k, v in g.items()}


def test_multileg_et_legacy_convergent_sur_delta_gamma_theta_vega():
    """r identique (0.045), q=0 : les deux implémentations doivent coïncider.
    Tolérances serrées — une divergence est un bug, pas un arrondi."""
    assert ML.R_DEFAULT == 0.045, 'les taux par défaut ont divergé entre moteurs'
    for spot, strike, dte, iv in _CAS:
        T = dte / 365.0
        for typ, is_call in (('call', True), ('put', False)):
            d, g, t, v = _greeks(spot, strike, T, iv, is_call)
            u = _unitaires(typ, spot, strike, T, iv)
            assert abs(u['delta'] - d) < 1e-9, (typ, spot, strike, dte, iv)
            assert abs(u['gamma'] - g) < 1e-9, (typ, spot, strike)
            assert abs(u['theta'] - t) < 1e-9, (typ, spot, strike)
            assert abs(u['vega'] - v) < 1e-9, (typ, spot, strike)


def test_parite_call_put_des_greeks_multileg():
    """delta_C − delta_P = e^(−qT) (=1 si q=0) ; gamma et vega identiques."""
    for spot, strike, dte, iv in _CAS:
        T = dte / 365.0
        c = _unitaires('call', spot, strike, T, iv)
        p = _unitaires('put', spot, strike, T, iv)
        assert abs((c['delta'] - p['delta']) - 1.0) < 1e-9
        assert abs(c['gamma'] - p['gamma']) < 1e-12
        assert abs(c['vega'] - p['vega']) < 1e-12


def test_parite_prix_call_put_legacy():
    """C − P = S − K·e^(−rT) (parité, q=0) sur tous les cas."""
    for spot, strike, dte, iv in _CAS:
        T = dte / 365.0
        c = _bs_price(spot, strike, T, iv, True)
        p = _bs_price(spot, strike, T, iv, False)
        assert abs((c - p) - (spot - strike * math.exp(-0.045 * T))) < 1e-9


def test_jambe_stock_delta_un_gamma_zero():
    """La jambe `stock` (multiplicateur 1) est linéaire : delta=qty, rien d'autre.
    C'est elle qui fait du labo un simulateur Actions/ETF."""
    g = ML._leg_greeks(100.0, {'type': 'stock', 'qty': 3.0}, 0.25, 0.3)
    assert g['delta'] == 3.0
    assert g['gamma'] == g['theta'] == g['vega'] == 0.0
    assert ML._mult({'type': 'stock'}) == 1.0
    assert ML._mult({'type': 'call'}) == 100.0


def test_multiplicateur_dans_le_pnl():
    """1 call = 100× ; le P&L à l'échéance le porte."""
    out = ML.analyze_strategy([_leg('call', 100.0)], spot=100.0, iv=0.25,
                              days_to_exp=30)
    assert out.get('available') is True
    #  au point de grille le plus proche de 120 : (intrinsèque − prime 1) × 100
    pt = min(out['payoff'], key=lambda pt: abs(pt['price'] - 120.0))
    attendu = (max(pt['price'] - 100.0, 0.0) - 1.0) * 100.0
    assert abs(pt['pnl'] - attendu) < 1e-6, (pt, attendu)


def test_la_devise_est_declaree_jamais_implicite():
    """Né ROUGE : les montants multileg sont en USD sans jamais le dire.
    Le bloc model doit déclarer la devise (aucune conversion n'existe)."""
    out = ML.analyze_strategy([_leg('call', 100.0)], spot=100.0, iv=0.25,
                              days_to_exp=30)
    model = out.get('model') or {}
    assert model.get('currency') == 'USD'
    assert 'conversion' in str(model.get('currency_note', '')).lower()
