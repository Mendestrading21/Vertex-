"""vertex.research.institutional.momentum_regimes — momentum conditionné au régime (§23)."""
from __future__ import annotations


def momentum_quality(returns_12_1: float | None, returns_3m: float | None,
                     vol_annualized: float | None, market_regime: str = 'UNKNOWN') -> dict:
    """Qualité du momentum : le momentum brut ne suffit pas — il doit être
    ajusté de la volatilité et du régime (le momentum crash en PANIC/retournement)."""
    out = {'raw_12_1': returns_12_1, 'raw_3m': returns_3m,
           'vol_adjusted': None, 'regime_warning': None, 'quality': None}
    if returns_12_1 is None or vol_annualized in (None, 0):
        out['quality'] = 'UNKNOWN'
        return out
    out['vol_adjusted'] = round(returns_12_1 / vol_annualized, 2)
    if market_regime in ('PANIC', 'TREND_DOWN', 'TRANSITION'):
        out['regime_warning'] = (f'régime {market_regime}: le facteur momentum est '
                                 'historiquement fragile (risque de momentum crash)')
    aligned = returns_3m is None or (returns_3m >= 0) == (returns_12_1 >= 0)
    if out['vol_adjusted'] >= 1.0 and aligned and out['regime_warning'] is None:
        out['quality'] = 'STRONG'
    elif out['vol_adjusted'] >= 0.5 and aligned:
        out['quality'] = 'MODERATE'
    elif not aligned:
        out['quality'] = 'FADING'
    else:
        out['quality'] = 'WEAK'
    return out
