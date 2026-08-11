"""tests/test_multileg_iv_units_06.py — PR n°6 (correction de calcul prouvée).

PREUVE DU BUG (avant correction) : le board d'options porte `iv` en POURCENTAGE
(ex. 40.4 = 40,4 %), mais `analyze_strategy` attend une volatilité DÉCIMALE.
`strategies_for_symbol` passait le pourcentage tel quel → volatilité ~4040 %,
donnant une PoP absurde de 100 % et un delta de call ATM saturé à 1,0 (×100).

Ces gardiens échouent AVANT la correction et passent APRÈS (conversion %→décimal
au point de jonction, sans toucher au cœur `analyze_strategy`).
"""
import math

from vertex.engines import multileg_lab


def _board(sym='TST', spot=100.0):
    """Board synthétique minimal (iv en POURCENTAGE, comme le vrai board)."""
    T = 45 / 365.0
    iv_pct = 40.0                      # 40 % — valeur réaliste, exprimée en %
    em = (iv_pct / 100.0) * math.sqrt(T)
    atm = round(spot, 1)
    mid = max(0.4, spot * em * 0.7)
    def c(typ, strike, dte):
        return {'sym': sym, 'type': typ, 'exp': '2026-09-01T00:00:00', 'dte': dte,
                'strike': strike, 'spot': spot, 'iv': iv_pct, 'delta': 0.5,
                'cost': round(mid * 100), 'oi': 12000, 'vol': 900, 'spread_pct': 3.0}
    return [c('CALL', atm, 45), c('PUT', atm, 45),
            c('CALL', round(spot * 1.06, 1), 45), c('PUT', round(spot * 0.94, 1), 45)]


def _recommended(res):
    strat = res.get('strategies') or []
    return next((s for s in strat if s.get('recommended')), strat[0] if strat else None)


def test_strategies_iv_returned_as_decimal():
    """L'IV renvoyée doit être une fraction décimale (<1.5), pas un pourcentage brut."""
    res = multileg_lab.strategies_for_symbol(_board(), 'TST', 100.0, bias='bullish')
    assert res.get('available'), res
    assert res['iv'] is not None
    assert res['iv'] < 1.5, f"iv renvoyée = {res['iv']} (pourcentage non converti)"


def test_long_call_pop_is_not_impossible_100():
    """Une PoP de 100 % pour un call long à débit est impossible (bug d'unité d'IV)."""
    res = multileg_lab.strategies_for_symbol(_board(), 'TST', 100.0, bias='bullish')
    call = next((s for s in res['strategies'] if s.get('kind') == 'long_call'), None)
    assert call is not None
    pop = call.get('probability_of_profit')
    assert pop is not None
    assert pop < 95.0, f"PoP call long = {pop} % (IV mal dimensionnée → distribution dégénérée)"


def test_atm_long_call_delta_not_saturated():
    """Le delta d'un call ATM long doit être ~0,4-0,7 par action (×100), pas saturé à 100."""
    res = multileg_lab.strategies_for_symbol(_board(), 'TST', 100.0, bias='bullish')
    call = next((s for s in res['strategies'] if s.get('kind') == 'long_call'), None)
    assert call is not None and call.get('greeks') is not None
    delta = call['greeks']['delta']
    assert 20.0 < delta < 90.0, f"delta call ATM = {delta} (saturé → IV mal dimensionnée)"
    # theta d'une option longue doit être négatif (érosion de la valeur temps)
    assert call['greeks']['theta'] < 0, f"theta = {call['greeks']['theta']} (attendu < 0)"


def test_decimal_iv_hint_not_double_converted():
    """Un iv_hint déjà décimal (0.4) ne doit pas être re-divisé par 100."""
    res = multileg_lab.strategies_for_symbol(_board(), 'TST', 100.0, iv_hint=0.4, bias='bullish')
    assert res.get('available')
    assert 0.3 < res['iv'] < 0.5, f"iv décimale altérée = {res['iv']}"
