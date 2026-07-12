"""vertex.companies.change_detector — détection de changement fondamental (§16).

Compare deux snapshots du jumeau analytique. Un changement SIGNIFICATIF
déclenche : nouveau snapshot + recalcul de la décision (le moteur exécutif
unique reste le seul décideur) — jamais un ordre.
"""
from __future__ import annotations

from vertex.companies.company_twin import snapshot_key_fields

# Seuils de signification (relatifs quand la grandeur s'y prête)
_REL_THRESHOLD = 0.15   # ±15 % sur PE / croissance / marge
_SCORE_THRESHOLD = 8    # points de score scan


def detect_changes(before: dict, after: dict) -> dict:
    """{changed, changes:[{field, before, after, kind}], recalc_required}."""
    b = snapshot_key_fields(before or {})
    a = snapshot_key_fields(after or {})
    changes = []
    for field in b:
        vb, va = b.get(field), a.get(field)
        if vb is None and va is None:
            continue
        if vb is None or va is None:
            changes.append({'field': field, 'before': vb, 'after': va,
                            'kind': 'APPARITION' if vb is None else 'DISPARITION'})
            continue
        if field == 'verdict':
            if vb != va:
                changes.append({'field': field, 'before': vb, 'after': va,
                                'kind': 'DECISION_CHANGED'})
            continue
        if field == 'score':
            if abs(float(va) - float(vb)) >= _SCORE_THRESHOLD:
                changes.append({'field': field, 'before': vb, 'after': va,
                                'kind': 'SCORE_SHIFT'})
            continue
        if field == 'earnings_dte':
            if vb != va and (va is not None and float(va) <= 7):
                changes.append({'field': field, 'before': vb, 'after': va,
                                'kind': 'EVENT_APPROACHING'})
            continue
        try:
            if vb and abs(float(va) - float(vb)) / abs(float(vb)) >= _REL_THRESHOLD:
                changes.append({'field': field, 'before': vb, 'after': va,
                                'kind': 'FUNDAMENTAL_SHIFT'})
        except (TypeError, ValueError, ZeroDivisionError):
            continue
    return {'changed': bool(changes), 'changes': changes,
            'recalc_required': bool(changes)}


__all__ = ['detect_changes']
