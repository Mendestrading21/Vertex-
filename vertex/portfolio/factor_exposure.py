"""vertex.portfolio.factor_exposure — exposition factorielle agrégée du portefeuille."""
from __future__ import annotations

from vertex.research.institutional.factor_model import FACTORS, factor_exposures


def portfolio_factor_exposure(snapshot, stock_data: dict,
                              bench_returns: list[float] | None = None) -> dict:
    """stock_data : {symbol: dict d'entrées factor_model}. Pondère par les poids réels."""
    weights = snapshot.weights()
    agg: dict[str, dict] = {f: {'value': 0.0, 'coverage_pct': 0.0} for f in FACTORS}
    for p in snapshot.positions:
        data = stock_data.get(p.symbol)
        w = (weights.get(p.symbol) or 0) / 100
        if not data or not w:
            continue
        exp = factor_exposures(data, bench_returns)
        for f in FACTORS:
            v = (exp.get(f) or {}).get('value')
            if v is not None:
                agg[f]['value'] += w * v
                agg[f]['coverage_pct'] += w * 100
    for f in FACTORS:
        cov = agg[f]['coverage_pct']
        agg[f]['value'] = round(agg[f]['value'], 3) if cov > 0 else None
        agg[f]['coverage_pct'] = round(cov, 1)
        if 0 < cov < 60:
            agg[f]['note'] = 'couverture partielle — exposition indicative'
    return agg
