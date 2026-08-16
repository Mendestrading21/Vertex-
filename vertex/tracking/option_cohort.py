"""Agrégation prudente des performances de contrats options suivis.

Les données viennent exclusivement des références et snapshots observés par le
tracking. Une cohorte trop petite n'affiche pas de taux de réussite ni de rendement
moyen, afin de ne pas transformer quelques contrats en preuve statistique.
"""
from __future__ import annotations

import statistics

from . import performance

MIN_SAMPLE = 5


def _metrics(items, minimum=MIN_SAMPLE):
    returns = [item['return_pct'] for item in items if item.get('return_pct') is not None]
    base = {'n_contracts': len(items), 'n_measurable': len(returns),
            'minimum_sample': minimum,
            'scope': 'HYPOTHETICAL_OPTION_MARK_TO_OBSERVED_QUOTE'}
    if len(returns) < minimum:
        return {**base, 'available': False,
                'reason': '%d contrats mesurables requis ; %d disponible(s)' % (minimum, len(returns))}
    wins = [value for value in returns if value > 0]
    return {**base, 'available': True,
            'mean_return_pct': round(sum(returns) / len(returns), 2),
            'median_return_pct': round(statistics.median(returns), 2),
            'win_rate': round(len(wins) / len(returns), 3),
            'best_return_pct': round(max(returns), 2),
            'worst_return_pct': round(min(returns), 2)}


def build(trackings, *, minimum=MIN_SAMPLE):
    rows = []
    for tracking in (trackings or []):
        if not isinstance(tracking, dict) or tracking.get('entity_type') != 'OPTION':
            continue
        contract = performance.compute(tracking, None).get('option_contract') or {}
        rows.append({'tracking_id': tracking.get('tracking_id'),
                     'decision_at_start': tracking.get('strategy_decision_at_start') or 'NON_CLASSIFIE',
                     'status': tracking.get('status'),
                     'return_pct': contract.get('return_pct'),
                     'quote_observations': contract.get('quote_observations', 0),
                     'mark_mode': contract.get('mark_mode')})
    measurable = [row for row in rows if row['return_pct'] is not None]
    by_decision = {}
    for decision in sorted({row['decision_at_start'] for row in rows}):
        by_decision[decision] = _metrics([row for row in rows if row['decision_at_start'] == decision], minimum)
    return {
        'scope': 'HYPOTHETICAL_OPTION_MARK_TO_OBSERVED_QUOTE',
        'is_hypothetical': True,
        'n_options_tracked': len(rows),
        'n_measurable': len(measurable),
        'cohort': _metrics(rows, minimum),
        'by_decision_at_start': by_decision,
        'limitations': [
            'Aucune position réelle, aucun ordre et aucun gain encaissé.',
            'Frais, slippage, profondeur et assignation ne sont pas inclus.',
            'Les cohortes sous le seuil ne produisent aucune métrique de performance.',
        ],
    }


__all__ = ['build', 'MIN_SAMPLE']
