"""vertex.market.indicators — indicateurs techniques purs et testables (§12).

Moyennes mobiles, RSI, ATR, bandes de Bollinger, VWAP — calculés à partir de
séries RÉELLES. Aucune valeur inventée : point indisponible (fenêtre trop
courte) → None, aligné sur la série d'entrée. Sans dépendance à pandas :
utilisable partout (analyse, portefeuille, marchés) sans surcoût.
"""
from __future__ import annotations

import math


def _floats(xs):
    out = []
    for x in xs or []:
        try:
            out.append(float(x))
        except (TypeError, ValueError):
            out.append(None)
    return out


def sma(values, window):
    """Moyenne mobile simple. Rend une liste alignée (None avant `window`)."""
    v = _floats(values)
    n = len(v)
    out = [None] * n
    if window <= 0:
        return out
    acc = 0.0
    cnt = 0
    from collections import deque
    q = deque()
    for i, x in enumerate(v):
        if x is None:
            # réinitialise la fenêtre sur trou de données (honnêteté)
            q.clear(); acc = 0.0; cnt = 0
            continue
        q.append(x); acc += x; cnt += 1
        if len(q) > window:
            acc -= q.popleft(); cnt -= 1
        if len(q) == window:
            out[i] = round(acc / window, 4)
    return out


def ema(values, span):
    """Moyenne mobile exponentielle (lissage 2/(span+1))."""
    v = _floats(values)
    out = [None] * len(v)
    if span <= 0:
        return out
    k = 2.0 / (span + 1.0)
    prev = None
    for i, x in enumerate(v):
        if x is None:
            continue
        prev = x if prev is None else (x * k + prev * (1 - k))
        out[i] = round(prev, 4)
    return out


def rsi(values, period=14):
    """RSI de Wilder. Rend une liste alignée (None avant `period`)."""
    v = _floats(values)
    n = len(v)
    out = [None] * n
    if n <= period:
        return out
    gains, losses = [], []
    for i in range(1, n):
        if v[i] is None or v[i - 1] is None:
            gains.append(0.0); losses.append(0.0)
            continue
        d = v[i] - v[i - 1]
        gains.append(max(0.0, d)); losses.append(max(0.0, -d))
    if len(gains) < period:
        return out
    avg_g = sum(gains[:period]) / period
    avg_l = sum(losses[:period]) / period
    for i in range(period, len(gains) + 1):
        if i > period:
            avg_g = (avg_g * (period - 1) + gains[i - 1]) / period
            avg_l = (avg_l * (period - 1) + losses[i - 1]) / period
        rs = (avg_g / avg_l) if avg_l > 0 else float('inf')
        out[i] = round(100.0 - 100.0 / (1.0 + rs), 1) if avg_l > 0 else 100.0
    return out


def atr(highs, lows, closes, period=14):
    """Average True Range (Wilder). None tant que < period true ranges."""
    h, l, c = _floats(highs), _floats(lows), _floats(closes)
    n = min(len(h), len(l), len(c))
    out = [None] * n
    if n <= period:
        return out
    trs = [None]
    for i in range(1, n):
        if None in (h[i], l[i], c[i - 1]):
            trs.append(None); continue
        trs.append(max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])))
    vals = [t for t in trs[1:period + 1] if t is not None]
    if len(vals) < period:
        return out
    a = sum(vals) / period
    out[period] = round(a, 4)
    for i in range(period + 1, n):
        if trs[i] is None:
            out[i] = round(a, 4); continue
        a = (a * (period - 1) + trs[i]) / period
        out[i] = round(a, 4)
    return out


def bollinger(values, window=20, mult=2.0):
    """Bandes de Bollinger : {mid, upper, lower} alignées sur `values`."""
    v = _floats(values)
    n = len(v)
    mid = sma(v, window)
    upper = [None] * n
    lower = [None] * n
    for i in range(n):
        if mid[i] is None:
            continue
        window_vals = [x for x in v[i - window + 1:i + 1] if x is not None]
        if len(window_vals) < window:
            continue
        m = mid[i]
        var = sum((x - m) ** 2 for x in window_vals) / window
        sd = math.sqrt(var)
        upper[i] = round(m + mult * sd, 4)
        lower[i] = round(m - mult * sd, 4)
    return {'mid': mid, 'upper': upper, 'lower': lower}


def vwap(highs, lows, closes, volumes):
    """VWAP cumulé (typical price pondéré par le volume). None si volume nul."""
    h, l, c = _floats(highs), _floats(lows), _floats(closes)
    vol = _floats(volumes)
    n = min(len(h), len(l), len(c), len(vol))
    out = [None] * n
    cum_pv = 0.0
    cum_v = 0.0
    for i in range(n):
        if None in (h[i], l[i], c[i], vol[i]) or vol[i] <= 0:
            out[i] = round(cum_pv / cum_v, 4) if cum_v > 0 else None
            continue
        tp = (h[i] + l[i] + c[i]) / 3.0
        cum_pv += tp * vol[i]
        cum_v += vol[i]
        out[i] = round(cum_pv / cum_v, 4)
    return out


__all__ = ['sma', 'ema', 'rsi', 'atr', 'bollinger', 'vwap']
