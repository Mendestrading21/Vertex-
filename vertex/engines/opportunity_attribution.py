"""Attribution déterministe d'une opportunité Skyler.

Expose les moteurs du score, les contraintes et les preuves manquantes sans
recalculer le score ni présenter une décision comme une exécution.
"""
from __future__ import annotations


def build(packet, decision):
    packet = packet or {}
    decision = decision or {}
    score = decision.get('score') or {}
    raw_blocks = score.get('blocks') or {}
    blocks = []
    for name, raw in raw_blocks.items():
        raw = raw or {}
        try:
            points = float(raw.get('points') or 0)
            maximum = float(raw.get('max') or 0)
        except (TypeError, ValueError):
            continue
        blocks.append({'block': name, 'points': points, 'max': maximum,
                       'coverage': round(points / maximum, 3) if maximum > 0 else None,
                       'status': raw.get('status'), 'reason': raw.get('reason')})
    drivers = sorted((b for b in blocks if b['points'] > 0),
                     key=lambda b: (b['coverage'] if b['coverage'] is not None else -1, b['points']),
                     reverse=True)[:3]
    weaknesses = sorted((b for b in blocks if b['max'] > b['points']),
                        key=lambda b: (b['max'] - b['points']), reverse=True)[:3]
    gates = decision.get('gates') or []
    triggered = [{'id': g.get('id'), 'reason': g.get('reason')}
                 for g in gates if g.get('triggered') is True]
    unevaluable = [{'id': g.get('id'), 'reason': g.get('reason')}
                   for g in gates if g.get('triggered') is None]
    contexts = packet.get('contexts') or {}
    missing = [name for name, value in contexts.items()
               if isinstance(value, dict) and value.get('available') is False]
    if triggered:
        status = 'REJECTED_BY_GATES'
    elif missing or unevaluable:
        status = 'EVIDENCE_REQUIRED'
    elif score.get('insufficient_blocks'):
        status = 'SCORE_INCOMPLETE'
    elif (score.get('total') or 0) >= 24:
        status = 'CANDIDATE_FOR_ANALYTICAL_REVIEW'
    else:
        status = 'LOW_CONVICTION'
    return {
        'status': status,
        'score_total': score.get('total'), 'score_max': score.get('max'),
        'drivers': drivers, 'weaknesses': weaknesses,
        'triggered_gates': triggered, 'unevaluable_gates': unevaluable,
        'missing_contexts': missing,
        'insufficient_blocks': list(score.get('insufficient_blocks') or []),
        'read_only': True,
        'note': ('attribution analytique déterministe : elle explique les preuves et '
                 'contraintes, sans instruction d’ordre ni promesse de résultat'),
    }


__all__ = ['build']
