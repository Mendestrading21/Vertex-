"""vertex.tracking.benchmark — performance relative au benchmark (§15).

Alpha depuis le suivi = rendement de l'entité − rendement du benchmark (SPY) sur
la même fenêtre. Purs, None si donnée manquante.
"""
from __future__ import annotations

from .returns import simple_return


def benchmark_return(bench_reference, bench_current):
    """Rendement du benchmark sur la fenêtre du suivi, en %."""
    return simple_return(bench_reference, bench_current)


def alpha_since(entity_return_pct, benchmark_return_pct):
    """Alpha = rendement entité − rendement benchmark (points de %). None si l'un manque."""
    if entity_return_pct is None or benchmark_return_pct is None:
        return None
    return round(entity_return_pct - benchmark_return_pct, 2)


__all__ = ['benchmark_return', 'alpha_since']
