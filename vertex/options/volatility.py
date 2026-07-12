"""vertex.options.volatility — mesures de volatilité pures et testables (§18).

Fonctions sans effet de bord : IV rank, IV percentile, volatilité réalisée
(close-to-close annualisée), prime IV/RV. Toutes rendent None si la donnée
manque (règle de vérité — jamais de zéro inventé).
"""
from __future__ import annotations

import math

TRADING_DAYS = 252


def iv_rank(current_iv, iv_low, iv_high):
    """Position de l'IV courante dans son couloir [low, high] sur 52 sem., en %.

    100 = au plus haut de l'année, 0 = au plus bas. None si données absentes
    ou couloir dégénéré."""
    if current_iv is None or iv_low is None or iv_high is None:
        return None
    try:
        current_iv, iv_low, iv_high = float(current_iv), float(iv_low), float(iv_high)
    except (TypeError, ValueError):
        return None
    span = iv_high - iv_low
    if span <= 0:
        return None
    pct = (current_iv - iv_low) / span * 100.0
    return round(max(0.0, min(100.0, pct)), 1)


def iv_percentile(current_iv, history):
    """% des observations historiques strictement sous l'IV courante.

    history : itérable d'IV passées. None si vide."""
    if current_iv is None or not history:
        return None
    try:
        current_iv = float(current_iv)
        vals = [float(x) for x in history if x is not None]
    except (TypeError, ValueError):
        return None
    if not vals:
        return None
    below = sum(1 for v in vals if v < current_iv)
    return round(below / len(vals) * 100.0, 1)


def realized_vol(closes, window=20):
    """Vol réalisée annualisée (écart-type des log-returns close-to-close).

    Rend une fraction (0.24 = 24 %). None si moins de window+1 clôtures
    valides. Utilise l'écart-type d'échantillon (n-1)."""
    if not closes:
        return None
    try:
        c = [float(x) for x in closes if x is not None and float(x) > 0]
    except (TypeError, ValueError):
        return None
    if len(c) < window + 1:
        return None
    c = c[-(window + 1):]
    rets = [math.log(c[i] / c[i - 1]) for i in range(1, len(c))]
    n = len(rets)
    if n < 2:
        return None
    mean = sum(rets) / n
    var = sum((r - mean) ** 2 for r in rets) / (n - 1)
    daily = math.sqrt(var)
    return round(daily * math.sqrt(TRADING_DAYS), 4)


def iv_rv_premium(iv, rv):
    """Prime de l'IV sur la vol réalisée (iv - rv), en points de vol.

    Positif = les options « coûtent cher » vs le mouvement réel récent."""
    if iv is None or rv is None:
        return None
    try:
        return round(float(iv) - float(rv), 4)
    except (TypeError, ValueError):
        return None


def vol_regime(rank):
    """Classe qualitative d'un IV rank (0..100). None si rank None."""
    if rank is None:
        return None
    if rank >= 75:
        return 'ELEVEE'
    if rank >= 50:
        return 'MOYENNE_HAUTE'
    if rank >= 25:
        return 'MOYENNE_BASSE'
    return 'BASSE'


__all__ = ['iv_rank', 'iv_percentile', 'realized_vol', 'iv_rv_premium',
           'vol_regime', 'TRADING_DAYS']
