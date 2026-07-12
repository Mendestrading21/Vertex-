"""vertex.tracking.performance — synthèse de performance d'un suivi (§15/§18).

Assemble rendement depuis le suivi, rendement/alpha vs SPY, MFE/MAE, drawdown,
durée, et l'étiquette d'honnêteté. Un gain est TOUJOURS présenté comme
« rendement hypothétique depuis le suivi », jamais comme un gain encaissé.
"""
from __future__ import annotations

from . import returns as R
from . import benchmark as B

HYPOTHETICAL_LABEL = 'Rendement hypothétique depuis le suivi'


def compute(tracking, current_price, *, bench_current=None, sessions=None,
            calendar_days=None, current_decision=None, current_score=None):
    """Rend le bloc de performance d'un suivi.

    `tracking` : dict modèle. `current_price` : marque actuelle de l'entité.
    `bench_current` : marque actuelle du benchmark (SPY)."""
    ref = tracking.get('reference_price')
    bench_ref = tracking.get('benchmark_reference_price')
    values = [s.get('price') for s in (tracking.get('snapshots') or [])
              if s.get('price') is not None]
    if ref is not None:
        values = [ref] + values
    if current_price is not None:
        values = values + [current_price]

    ret = R.simple_return(ref, current_price)
    bench_ret = B.benchmark_return(bench_ref, bench_current)
    mm = R.mae_mfe(ref, values)
    dd = R.drawdown_from_high(values)

    d0 = tracking.get('strategy_decision_at_start')
    s0 = tracking.get('strategy_score_at_start')
    return {
        'label': HYPOTHETICAL_LABEL,
        'is_hypothetical': True,
        'reference_price': ref,
        'reference_price_type': tracking.get('reference_price_type'),
        'reference_price_source': tracking.get('reference_price_source'),
        'reference_price_timestamp': tracking.get('reference_price_timestamp'),
        'current_price': current_price,
        'return_pct': ret,
        'benchmark': tracking.get('benchmark'),
        'benchmark_return_pct': bench_ret,
        'alpha_pct': B.alpha_since(ret, bench_ret),
        'mfe_pct': mm['mfe_pct'],
        'mae_pct': mm['mae_pct'],
        'high_since': mm['high'],
        'low_since': mm['low'],
        'drawdown_from_high_pct': dd,
        'sessions': sessions,
        'calendar_days': calendar_days,
        'decision_at_start': d0,
        'decision_now': current_decision,
        'decision_changed': (current_decision is not None and d0 not in (None, '')
                             and current_decision != d0),
        'score_at_start': s0,
        'score_now': current_score,
        'score_delta': (round(current_score - s0, 1)
                        if (current_score is not None and s0 is not None) else None),
        'limitations': [
            'Suivi HYPOTHÉTIQUE : aucune position réelle, aucun gain encaissé.',
            'Frais exclus ; rendement prix (dividendes/splits non intégrés sauf mention).',
        ],
    }


__all__ = ['compute', 'HYPOTHETICAL_LABEL']
