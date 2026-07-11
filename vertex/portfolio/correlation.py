"""vertex.portfolio.correlation — corrélations du portefeuille réel."""
from __future__ import annotations

import math


def _corr(a: list[float], b: list[float]) -> float | None:
    n = min(len(a), len(b))
    if n < 30:
        return None
    a, b = a[-n:], b[-n:]
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((x - mb) ** 2 for x in b)
    if not va or not vb:
        return None
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return round(cov / math.sqrt(va * vb), 3)


def correlation_matrix(returns_by_symbol: dict) -> dict:
    syms = sorted(returns_by_symbol)
    matrix = {}
    for i, s1 in enumerate(syms):
        for s2 in syms[i + 1:]:
            c = _corr(returns_by_symbol[s1], returns_by_symbol[s2])
            if c is not None:
                matrix[f'{s1}/{s2}'] = c
    values = list(matrix.values())
    avg = round(sum(values) / len(values), 3) if values else None
    high_pairs = {k: v for k, v in matrix.items() if v >= 0.8}
    return {'pairs': matrix, 'average': avg, 'high_pairs': high_pairs,
            'symbols_covered': syms,
            'warning': ('corrélation moyenne élevée — diversification illusoire'
                        if avg is not None and avg >= 0.7 else None)}


def candidate_correlation(candidate_returns: list[float],
                          returns_by_symbol: dict) -> float | None:
    cors = [c for c in (_corr(candidate_returns, r) for r in returns_by_symbol.values())
            if c is not None]
    return round(sum(cors) / len(cors), 3) if cors else None
