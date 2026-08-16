"""Diagnostic de fiabilité d'une opportunité, séparé de la décision Skyler.

Il n'ajoute aucune recommandation et n'ajuste aucun score. Son rôle est de rendre
visible la solidité des preuves utilisées au moment de l'analyse.
"""
from __future__ import annotations


def build(packet, decision, option_cohort=None):
    packet, decision, cohort = packet or {}, decision or {}, option_cohort or {}
    score = decision.get('score') or {}
    gates = decision.get('gates') or []
    contexts = packet.get('contexts') or {}
    data = contexts.get('data_quality') or {}
    reconciliation = contexts.get('reconciliation') or {}
    triggered = [gate.get('id') for gate in gates if gate.get('triggered') is True]
    unknown = [gate.get('id') for gate in gates if gate.get('triggered') is None]
    insufficient = list(score.get('insufficient_blocks') or [])
    checks = {
        'no_triggered_gate': not triggered,
        'data_actionable': data.get('available') is True and data.get('actionable_allowed') is True,
        'reconciliation_actionable': (reconciliation.get('available') is True and
                                      reconciliation.get('actionable_allowed') is True and
                                      not reconciliation.get('blocking')),
        'score_complete': not insufficient,
        'gates_evaluable': not unknown,
        'score_review_threshold': (score.get('total') or 0) >= 24,
    }
    empirical = (cohort.get('cohort') or {})
    empirical_available = empirical.get('available') is True
    if triggered:
        status = 'BLOCKED_BY_GATES'
    elif not checks['data_actionable'] or not checks['reconciliation_actionable'] or unknown:
        status = 'EVIDENCE_LIMITED'
    elif insufficient:
        status = 'SCORE_INCOMPLETE'
    elif not checks['score_review_threshold']:
        status = 'LOW_CONVICTION'
    elif empirical_available:
        status = 'REVIEW_WITH_EMPIRICAL_COHORT'
    else:
        status = 'REVIEW_WITHOUT_EMPIRICAL_COHORT'
    return {
        'status': status,
        'read_only': True,
        'checks': checks,
        'triggered_gates': triggered,
        'unevaluable_gates': unknown,
        'insufficient_blocks': insufficient,
        'option_cohort_evidence': {
            'available': empirical_available,
            'n_measurable': empirical.get('n_measurable'),
            'minimum_sample': empirical.get('minimum_sample'),
            'scope': empirical.get('scope'),
        },
        'note': ('diagnostic de fiabilité des preuves, sans ajustement de score, '
                 'instruction d’ordre ou promesse de performance'),
    }


__all__ = ['build']
