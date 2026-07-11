"""vertex.research.institutional.sector_rotation — rotation sectorielle (§23)."""
from __future__ import annotations


def analyze_rotation(sector_returns: dict, benchmark_return_20d: float | None = None,
                     breadth_by_sector: dict | None = None) -> dict:
    """sector_returns: {secteur: {'r20': float, 'r5': float}} — relatif au marché."""
    breadth_by_sector = breadth_by_sector or {}
    improving, deteriorating, accelerating = [], [], []
    for sec, r in (sector_returns or {}).items():
        r20, r5 = r.get('r20'), r.get('r5')
        if r20 is None:
            continue
        rel20 = r20 - (benchmark_return_20d or 0)
        if rel20 > 0.01:
            improving.append((sec, round(rel20, 4)))
        elif rel20 < -0.01:
            deteriorating.append((sec, round(rel20, 4)))
        if r5 is not None and r20 and r5 > r20 / 4 * 1.5:
            accelerating.append(sec)
    improving.sort(key=lambda x: -x[1])
    deteriorating.sort(key=lambda x: x[1])
    defensive = {'Santé', 'Conso de base', 'Utilities', 'HEALTHCARE', 'STAPLES', 'UTILITIES'}
    cyclical = {'Technologie', 'Industrie', 'Conso discrétionnaire', 'Finance',
                'TECH', 'INDUSTRIALS', 'DISCRETIONARY', 'FINANCIALS'}
    top3 = {s for s, _ in improving[:3]}
    rotation = 'DEFENSIVE' if top3 & defensive and not top3 & cyclical else \
               'CYCLICAL' if top3 & cyclical and not top3 & defensive else 'MIXED'
    weights = sorted((abs(v) for _, v in improving + deteriorating), reverse=True)
    concentration = round(sum(weights[:2]) / sum(weights), 2) if len(weights) > 2 and sum(weights) else None
    return {'improving': improving, 'deteriorating': deteriorating,
            'accelerating': accelerating, 'leadership': improving[0][0] if improving else None,
            'rotation_style': rotation,
            'breadth_by_sector': breadth_by_sector,
            'extreme_concentration': bool(concentration and concentration > 0.75),
            'concentration': concentration}
