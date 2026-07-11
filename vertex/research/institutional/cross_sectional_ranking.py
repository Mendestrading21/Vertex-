"""vertex.research.institutional.cross_sectional_ranking — classements transversaux (§23).

Compare chaque action à son secteur, son industrie, aux indices et aux leaders.
Information seulement : aucun trade, aucun pair-trade automatique.
"""
from __future__ import annotations


def percentile_rank(value: float, population: list[float]) -> float | None:
    pop = [x for x in population if x is not None]
    if value is None or len(pop) < 5:
        return None
    below = sum(1 for x in pop if x <= value)
    return round(below / len(pop) * 100, 1)


def rank_universe(metrics_by_symbol: dict, metric_keys: list[str],
                  sector_of: dict | None = None) -> dict:
    """metrics_by_symbol: {sym: {metric: value}} → percentiles univers + secteur."""
    sector_of = sector_of or {}
    out: dict[str, dict] = {}
    populations = {k: [m.get(k) for m in metrics_by_symbol.values()] for k in metric_keys}
    sector_pops: dict[tuple, list] = {}
    for sym, m in metrics_by_symbol.items():
        sec = sector_of.get(sym)
        for k in metric_keys:
            sector_pops.setdefault((sec, k), []).append(m.get(k))
    for sym, m in metrics_by_symbol.items():
        sec = sector_of.get(sym)
        entry = {}
        for k in metric_keys:
            entry[k] = {'value': m.get(k),
                        'universe_pct': percentile_rank(m.get(k), populations[k]),
                        'sector_pct': percentile_rank(m.get(k), sector_pops.get((sec, k), []))
                        if sec else None}
        universe_pcts = [v['universe_pct'] for v in entry.values()
                         if v['universe_pct'] is not None]
        entry['_composite_pct'] = round(sum(universe_pcts) / len(universe_pcts), 1) \
            if universe_pcts else None
        out[sym] = entry
    return out


def leaders(ranked: dict, top_n: int = 10) -> list[str]:
    scored = [(s, e['_composite_pct']) for s, e in ranked.items()
              if e.get('_composite_pct') is not None]
    return [s for s, _ in sorted(scored, key=lambda x: -x[1])[:top_n]]
