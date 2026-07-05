"""
tests/test_backtest.py — Forward-test papier (courbe d'équité + métriques).

Non-régression « golden » sur des données déterministes + garde-fous : c'est un
test PAPIER, il ne passe aucun ordre.
"""

import numpy as np
import pandas as pd
from vertex.engines import backtest as bt


def _fixture_data():
    syms = bt.WATCHLIST[:8]
    idx = pd.date_range('2023-01-01', periods=260, freq='D')
    data = {}
    for i, s in enumerate(syms):
        base = np.linspace(50 + i * 5, 90 + i * 5, 260) + 4 * np.sin(np.linspace(0, 15 + i, 260))
        c = pd.Series(base, index=idx)
        data[s] = pd.DataFrame({
            'Open': c.shift(1).fillna(c.iloc[0]), 'High': c + 1, 'Low': c - 1, 'Close': c,
            'Volume': pd.Series(np.linspace(1e6, 2e6, 260), index=idx),
        }, index=idx)
    return data


def test_golden_metrics():
    r = bt.backtest(_fixture_data())
    assert r['balance'] == 136863.1
    assert r['total'] == 36.86
    assert r['trades'] == 12
    assert r['winrate'] == 75
    assert r['sharpe'] == 60.01
    assert r['top_n'] == 5


def test_shape_and_no_nan():
    import json, math
    r = bt.backtest(_fixture_data())
    assert len(r['dates']) == len(r['equity'])
    assert all(not math.isnan(x) for x in r['equity'])
    json.dumps(r)                                    # sérialisable → JSON de /scan sûr


def test_insufficient_data_returns_none():
    idx = pd.date_range('2024-01-01', periods=30, freq='D')
    c = pd.Series(np.linspace(10, 20, 30), index=idx)
    tiny = {bt.WATCHLIST[0]: pd.DataFrame({'Close': c, 'High': c, 'Low': c, 'Volume': c}, index=idx)}
    assert bt.backtest(tiny) is None                 # < 3 titres exploitables → None honnête


def test_terminal_binding_is_the_module():
    import terminal
    assert terminal.backtest is bt.backtest
