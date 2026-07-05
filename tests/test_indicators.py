"""
tests/test_indicators.py — Indicateurs techniques purs (RSI / ATR / ADX).

Extraits du monolithe : testés isolément, valeurs bornées, jamais de NaN
(un NaN casserait le JSON de /scan).
"""

import numpy as np
import pandas as pd
from vertex.engines import indicators as ind


def _df(closes, highs=None, lows=None):
    c = pd.Series([float(x) for x in closes])
    h = pd.Series([float(x) for x in (highs or [x + 1 for x in closes])])
    l = pd.Series([float(x) for x in (lows or [x - 1 for x in closes])])
    return pd.DataFrame({'High': h, 'Low': l, 'Close': c})


def test_rsi_bounded_and_no_nan():
    r = ind.rsi(pd.Series(np.linspace(10, 50, 60)))
    assert r.notna().all()
    assert (r >= 0).all() and (r <= 100).all()


def test_rsi_all_up_is_100():
    # série strictement croissante → aucune baisse → RSI = 100, pas NaN
    r = ind.rsi(pd.Series(range(1, 40)))
    assert r.iloc[-1] == 100


def test_rsi_all_down_is_low():
    r = ind.rsi(pd.Series(range(40, 1, -1)))
    assert r.iloc[-1] < 5


def test_atr_positive_and_aligned():
    df = _df(list(range(20, 60)))
    a = ind.atr(df)
    assert len(a) == len(df)
    assert float(a.iloc[-1]) > 0


def test_adx_returns_bounded_float():
    df = _df(list(range(20, 80)))            # tendance nette → ADX élevé
    v = ind.adx(df)
    assert isinstance(v, float)
    assert 0 <= v <= 100


def test_adx_trend_higher_than_chop():
    trend = ind.adx(_df(list(range(20, 90))))
    chop = ind.adx(_df([40 + (i % 2) for i in range(70)]))   # dents de scie
    assert trend > chop


def test_terminal_aliases_point_to_module():
    import terminal
    assert terminal._rsi is ind.rsi
    assert terminal._atr is ind.atr
    assert terminal._adx is ind.adx
