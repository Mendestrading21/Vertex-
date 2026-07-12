"""vertex.positions.change_detector — « Ce qui a changé » (§27).

Diff entre deux évaluations d'une même position : valeurs, statut,
verdict, cause, matérialité. Jamais généré depuis des données absentes —
un champ None des deux côtés est ignoré ; None → valeur = APPARITION.
"""
from __future__ import annotations

import time

from vertex.positions.lifecycle import materiality

_WATCHED = ('current_price', 'mark', 'unrealized_pnl_pct', 'remaining_rr',
            'iv', 'dte', 'spread_pct', 'lifecycle_status', 'decision',
            'thesis_health', 'weight_pct')

_LABELS = {'current_price': 'cours', 'mark': 'prime', 'unrealized_pnl_pct': 'P&L %',
           'remaining_rr': 'R:R restant', 'iv': 'IV', 'dte': 'DTE',
           'spread_pct': 'spread %', 'lifecycle_status': 'statut',
           'decision': 'verdict', 'thesis_health': 'santé de thèse',
           'weight_pct': 'poids %'}


def diff(before: dict | None, after: dict) -> dict:
    b = before or {}
    changes = []
    for f in _WATCHED:
        vb, va = b.get(f), after.get(f)
        if vb is None and va is None:
            continue
        if vb == va:
            continue
        entry = {'field': f, 'label': _LABELS.get(f, f), 'before': vb,
                 'after': va, 'source': after.get('price_source')
                 or after.get('greeks_source') or after.get('source')}
        if isinstance(vb, (int, float)) and isinstance(va, (int, float)) and vb:
            entry['change_pct'] = round((va - vb) / abs(vb) * 100, 2)
            entry['materiality'] = materiality(entry['change_pct'])
        else:
            entry['materiality'] = ('MAJOR' if f in ('lifecycle_status',
                                                     'decision', 'thesis_health')
                                    else 'MINOR')
        changes.append(entry)
    worst = 'IMMATERIAL'
    order = ['IMMATERIAL', 'MINOR', 'MEANINGFUL', 'MAJOR', 'CRITICAL']
    for c in changes:
        if order.index(c['materiality']) > order.index(worst):
            worst = c['materiality']
    return {'position_id': after.get('position_id'), 'changes': changes,
            'changed': bool(changes), 'materiality': worst,
            'recalc_required': worst in ('MEANINGFUL', 'MAJOR', 'CRITICAL'),
            'generated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}


__all__ = ['diff']
