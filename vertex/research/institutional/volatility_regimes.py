"""vertex.research.institutional.volatility_regimes — régimes de volatilité (§23)."""
from __future__ import annotations

import math


def _std(xs):
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def classify_vol_regime(returns: list[float], vix: float | None = None,
                        vix_percentile: float | None = None) -> dict:
    """Régime de vol d'un titre ou d'un indice, sur ses rendements quotidiens."""
    out = {'regime': 'UNKNOWN', 'rv_10d': None, 'rv_60d': None, 'ratio': None, 'notes': []}
    if len(returns) < 70:
        out['notes'].append('historique insuffisant (< 70 séances)')
        return out
    rv10 = _std(returns[-10:]) * math.sqrt(252)
    rv60 = _std(returns[-60:]) * math.sqrt(252)
    out['rv_10d'], out['rv_60d'] = round(rv10, 4), round(rv60, 4)
    if rv60:
        ratio = rv10 / rv60
        out['ratio'] = round(ratio, 2)
        if ratio >= 1.6:
            out['regime'] = 'EXPANSION'
        elif ratio <= 0.6:
            out['regime'] = 'COMPRESSION'
        else:
            out['regime'] = 'NORMAL'
    if vix is not None and vix_percentile is not None:
        if vix_percentile >= 90:
            out['notes'].append(f'VIX au {vix_percentile:.0f}e percentile — stress de marché')
        elif vix_percentile <= 10:
            out['notes'].append('VIX écrasé — complaisance possible, options peu chères')
    return out
