"""Lot 9 — mémo des étapes aval du scan (backtest + solveur de strike) : byte-identique.

Les deux sont des fonctions déterministes ; leur mémoïsation (clés = entrées exactes)
doit renvoyer un résultat STRICTEMENT identique au calcul frais — jamais un chiffre qui bouge.
"""
import json


def test_backtest_memo_equals_fresh():
    import terminal
    import vertex.engines.backtest as bt
    from vertex.data.universe import WATCHLIST
    data = terminal._demo_universe(list(WATCHLIST))
    fresh = bt._backtest_compute(data)
    bt._BT_MEMO['key'] = None
    m1 = bt.backtest(data)            # miss → calcule + cache
    m2 = bt.backtest(data)            # hit
    j = lambda x: json.dumps(x, sort_keys=True, default=str)
    assert j(m1) == j(fresh)          # mémoïsé == frais (byte-identique)
    assert j(m2) == j(m1)             # hit == miss


def test_strike_solver_memo_is_deterministic():
    import vertex.strategy.legacy_adapter as la
    la._STRIKE_MEMO.clear()
    a = la._strike_for_delta(123.45, 0.0821, 0.337, True, 0.42)
    b = la._strike_for_delta(123.45, 0.0821, 0.337, True, 0.42)   # hit
    la._STRIKE_MEMO.clear()
    c = la._strike_for_delta(123.45, 0.0821, 0.337, True, 0.42)   # frais
    assert a == b == c
