"""Diagnostic de readiness d'une décision Skyler.

Sortie strictement descriptive : elle n'ouvre aucune possibilité d'ordre et ne
modifie ni score, ni gates, ni verdict. Son contrat sert aux interfaces et aux
agents de présentation qui doivent distinguer une décision bloquée d'un dossier
dont les preuves restent incomplètes.
"""
from __future__ import annotations


SCHEMA_VERSION = 1
_REQUIRED_CONTEXTS = ('technical', 'market', 'data_quality', 'reconciliation', 'options')


def _label(name):
    return {
        'technical': 'analyse technique',
        'market': 'régime de marché',
        'data_quality': 'qualité des données',
        'reconciliation': 'réconciliation des sources',
        'options': 'contexte options',
        'portfolio': 'contexte portefeuille',
    }.get(name, name)


def build(packet, decision):
    """Construit un statut de préparation analytique depuis des sorties existantes.

    Les gates `True` restent prioritaires. Les gates `None` et contextes absents
    restent explicitement à investiguer : ils ne deviennent jamais des accords.
    """
    packet = packet or {}
    decision = decision or {}
    contexts = packet.get('contexts') or {}
    gates = decision.get('gates') or []
    score = decision.get('score') or {}
    missing_contexts = [name for name in _REQUIRED_CONTEXTS
                        if not (contexts.get(name) or {}).get('available')]
    triggered = [g for g in gates if g.get('triggered') is True]
    unevaluable = [g for g in gates if g.get('triggered') is None]
    insufficient = list(score.get('insufficient_blocks') or [])
    actions = []
    for name in missing_contexts:
        reason = (contexts.get(name) or {}).get('reason') or 'contexte indisponible'
        actions.append({'kind': 'COLLECT_CONTEXT', 'target': name,
                        'label': 'Collecter %s' % _label(name), 'reason': reason})
    for gate in triggered:
        actions.append({'kind': 'RESOLVE_TRIGGERED_GATE', 'target': gate.get('id'),
                        'label': 'Résoudre la gate %s' % gate.get('id'),
                        'reason': gate.get('reason')})
    for gate in unevaluable:
        actions.append({'kind': 'EVALUATE_GATE', 'target': gate.get('id'),
                        'label': 'Évaluer la gate %s' % gate.get('id'),
                        'reason': gate.get('reason')})
    if triggered:
        status = 'BLOCKED_BY_GATE'
    elif missing_contexts or unevaluable:
        status = 'EVIDENCE_REQUIRED'
    elif insufficient:
        status = 'SCORE_INCOMPLETE'
    else:
        status = 'ANALYTICAL_REVIEW_READY'
    return {
        'schema_version': SCHEMA_VERSION,
        'status': status,
        'decision': decision.get('decision'),
        'score_total': score.get('total'),
        'score_max': score.get('max'),
        'capped_by_gate': decision.get('capped_by_gate'),
        'triggered_gates': [{'id': g.get('id'), 'reason': g.get('reason')} for g in triggered],
        'unevaluable_gates': [{'id': g.get('id'), 'reason': g.get('reason')} for g in unevaluable],
        'missing_contexts': missing_contexts,
        'insufficient_score_blocks': insufficient,
        'actions': actions,
        'read_only': True,
        'note': ('diagnostic de préparation analytique ; ne modifie pas la décision '
                 'et ne constitue jamais une instruction d’exécution'),
    }


__all__ = ['SCHEMA_VERSION', 'build']
