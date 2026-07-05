"""
vertex/engines/indicators.py — INDICATEURS TECHNIQUES purs (Ch. II).

Fonctions sans état, sans dépendance applicative : entrée = séries/df pandas,
sortie = série/valeur. Source unique pour RSI / ATR / ADX — extraites du
monolithe pour être testables isolément et réutilisables.
"""

import numpy as np
import pandas as pd


def rsi(s, n=14):
    """RSI de Wilder. dn==0 (aucune baisse) → 100, jamais NaN (casserait le JSON)."""
    d = s.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return (100 - 100 / (1 + up / dn.replace(0, np.nan))).fillna(100)


def atr(df, n=14):
    """Average True Range (volatilité), lissé façon Wilder."""
    h, l, c = df['High'], df['Low'], df['Close']
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def adx(df, n=14):
    """Force de tendance (ADX). Élevé = tendance directionnelle ; bas = range/bruit."""
    h, l, c = df['High'], df['Low'], df['Close']
    up, dn = h.diff(), -l.diff()
    plus = ((up > dn) & (up > 0)) * up
    minus = ((dn > up) & (dn > 0)) * dn
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    a = tr.ewm(alpha=1 / n, adjust=False).mean()
    pdi = 100 * plus.ewm(alpha=1 / n, adjust=False).mean() / a
    mdi = 100 * minus.ewm(alpha=1 / n, adjust=False).mean() / a
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan)
    return float(dx.ewm(alpha=1 / n, adjust=False).mean().iloc[-1])


__all__ = ['rsi', 'atr', 'adx']
