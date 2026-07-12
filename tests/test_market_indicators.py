"""Tests §12 — indicateurs techniques purs vertex.market.indicators."""
from vertex.market import indicators as ind


def test_sma_basic_and_alignment():
    out = ind.sma([1, 2, 3, 4, 5], 3)
    assert out[:2] == [None, None]
    assert out[2] == 2.0 and out[3] == 3.0 and out[4] == 4.0


def test_sma_none_resets_window():
    out = ind.sma([1, 2, None, 4, 5, 6], 3)
    assert out[5] == 5.0
    assert out[3] is None and out[4] is None


def test_ema_seeds_and_flat():
    out = ind.ema([10, 10, 10, 10], 3)
    assert out[0] == 10.0
    assert all(abs(x - 10.0) < 1e-6 for x in out)


def test_ema_reacts_to_change():
    out = ind.ema([10, 10, 20], 2)
    assert abs(out[-1] - 16.6667) < 1e-3


def test_rsi_all_gains_is_high():
    out = ind.rsi(list(range(1, 40)), period=14)
    assert out[14] is not None and out[-1] >= 99.0


def test_rsi_none_before_period():
    assert all(x is None for x in ind.rsi([1, 2, 3], period=14))


def test_atr_positive_and_aligned():
    n = 30
    highs = [100 + i + 1 for i in range(n)]
    lows = [100 + i - 1 for i in range(n)]
    closes = [100 + i for i in range(n)]
    out = ind.atr(highs, lows, closes, period=14)
    assert out[13] is None and out[14] is not None and out[-1] > 0


def test_bollinger_bands_ordered():
    v = [10, 11, 9, 12, 8, 13, 7, 14, 6, 15, 5, 16]
    b = ind.bollinger(v, window=4, mult=2.0)
    for i in range(len(v)):
        if b['mid'][i] is not None and b['upper'][i] is not None:
            assert b['lower'][i] <= b['mid'][i] <= b['upper'][i]


def test_bollinger_flat_series_zero_width():
    b = ind.bollinger([5, 5, 5, 5, 5], window=3)
    assert b['upper'][4] == b['mid'][4] == b['lower'][4] == 5.0


def test_vwap_matches_manual():
    out = ind.vwap([11, 12], [9, 10], [10, 11], [100, 300])
    tp0 = (11 + 9 + 10) / 3
    tp1 = (12 + 10 + 11) / 3
    expected = (tp0 * 100 + tp1 * 300) / 400
    assert abs(out[1] - round(expected, 4)) < 1e-3


def test_vwap_zero_volume_is_none():
    assert ind.vwap([10], [10], [10], [0])[0] is None
