"""vertex.tracking.returns — calculs de rendement du suivi (§15).

Purs et testables. Rendement simple (current/reference − 1), MAE/MFE, drawdown
depuis le plus haut, ajustement de split. None si donnée absente (jamais 0).
"""
from __future__ import annotations


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def simple_return(reference_price, current_price):
    """(current/reference) − 1, en pourcentage. None si l'un manque ou ref ≤ 0."""
    ref, cur = _num(reference_price), _num(current_price)
    if ref is None or cur is None or ref <= 0:
        return None
    return round((cur / ref - 1.0) * 100.0, 2)


def split_adjust(reference_price, split_ratio):
    """Ajuste la référence pour un split (ratio 2 = 2-for-1 → prix ÷ 2)."""
    ref, r = _num(reference_price), _num(split_ratio)
    if ref is None or r is None or r <= 0:
        return ref
    return round(ref / r, 4)


def mae_mfe(reference_price, observed_values):
    """Rend {mfe_pct, mae_pct, high, low} sur les valeurs observées (incluant
    la référence). MFE = meilleur rendement atteint, MAE = pire. None si vide."""
    ref = _num(reference_price)
    vals = [v for v in (_num(x) for x in (observed_values or [])) if v is not None]
    if ref is None or ref <= 0 or not vals:
        return {'mfe_pct': None, 'mae_pct': None, 'high': None, 'low': None}
    hi, lo = max(vals), min(vals)
    return {'mfe_pct': round((hi / ref - 1) * 100, 2),
            'mae_pct': round((lo / ref - 1) * 100, 2),
            'high': round(hi, 4), 'low': round(lo, 4)}


def drawdown_from_high(observed_values):
    """Drawdown courant depuis le plus haut observé, en % (≤ 0). None si vide."""
    vals = [v for v in (_num(x) for x in (observed_values or [])) if v is not None]
    if not vals:
        return None
    hi = max(vals)
    if hi <= 0:
        return None
    cur = vals[-1]
    return round((cur / hi - 1) * 100, 2)


__all__ = ['simple_return', 'split_adjust', 'mae_mfe', 'drawdown_from_high']
