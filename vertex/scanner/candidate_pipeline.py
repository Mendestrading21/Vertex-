"""vertex.scanner.candidate_pipeline — pipeline multi-étages (§22).

Ordre imposé : Fondamental → Catalyseurs → Technique → Sentiment → Anomalies →
Portefeuille → Options → Risque → Décision. Sorties : REJECTED / RADAR /
WATCH / ACTIONABLE / INVALIDATED. ACTIONABLE exige : tous les étages passés,
données fraîches et réconciliées, aucune donnée critique manquante.
"""
from __future__ import annotations

from .scan_budget import ScanBudget
from .stages import STAGE_ORDER

OUTCOMES = ('REJECTED', 'RADAR', 'WATCH', 'ACTIONABLE', 'INVALIDATED')

# Étages dont l'échec rejette immédiatement (les autres dégradent).
FATAL_STAGES = {'technical', 'anomalies', 'portfolio', 'risk'}
# Données critiques : leur absence plafonne à WATCH.
CRITICAL_MISSING = {'fundamentals', 'technical'}


def evaluate_candidate(candidate: dict) -> dict:
    """Passe un candidat par tous les étages, dans l'ordre. Retourne le dossier."""
    stages_out, missing_all = {}, set()
    outcome = None
    for name, fn in STAGE_ORDER:
        res = fn(candidate)
        stages_out[name] = res
        missing_all.update(res['missing'])
        if not res['passed']:
            outcome = 'REJECTED' if name in FATAL_STAGES or name == 'fundamental' else 'RADAR'
            break

    invalidated = bool((candidate.get('technical') or {}).get('thesis_invalidated'))
    if invalidated:
        outcome = 'INVALIDATED'

    if outcome is None:
        scores = [r['score'] for r in stages_out.values() if r['score'] is not None]
        avg = sum(scores) / len(scores) if scores else 0.0
        dq = candidate.get('data_quality') or {}
        reconciliation_ok = candidate.get('reconciliation_ok', True)
        if avg >= 65 and dq.get('actionable_allowed') and reconciliation_ok \
                and not (missing_all & CRITICAL_MISSING):
            outcome = 'ACTIONABLE'
        elif avg >= 55:
            outcome = 'WATCH'
        else:
            outcome = 'RADAR'
    scores = [r['score'] for r in stages_out.values() if r['score'] is not None]
    return {'symbol': candidate.get('symbol'), 'outcome': outcome,
            'stage_results': stages_out,
            'score': round(sum(scores) / len(scores), 1) if scores else None,
            'missing': sorted(missing_all),
            'analysis_order': [name for name, _ in STAGE_ORDER] + ['decision']}


def run_pipeline(candidates: list[dict], budget: ScanBudget | None = None) -> dict:
    """Scan complet avec budget d'entonnoir. candidates = paquets pré-remplis."""
    budget = budget or ScanBudget()
    results = [evaluate_candidate(c) for c in budget.cap('fundamental', list(candidates))]
    by_outcome: dict[str, list] = {o: [] for o in OUTCOMES}
    for r in results:
        by_outcome[r['outcome']].append(r)
    for group in by_outcome.values():
        group.sort(key=lambda r: -(r['score'] or 0))
    return {'results': results, 'by_outcome': by_outcome,
            'budget': budget.report(),
            'counts': {o: len(v) for o, v in by_outcome.items()}}
