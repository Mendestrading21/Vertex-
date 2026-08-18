"""vertex.options.call_selector — moteur CALL principal (§20).

Présente AU MAXIMUM : 1 BALANCED, 1 DYNAMIC, 1 ULTRA_CONVEX — et désigne UN
seul contrat principal. Complètement séparé du moteur PUT tactique
(bearish_tactical.py) : ce module ne touche jamais un PUT.
"""
from __future__ import annotations

from . import contract_filter, contract_scorer, scenario_pricer
from .models import CALL_CATEGORIES, CATEGORY_DYNAMIC, UnderlyingSetup


def _holding_plan(profile, holding_days: int | None) -> tuple[int, list[int]]:
    """Résout l’horizon de détention sans cacher un défaut hors profil."""
    configured = ((getattr(profile, 'options_profile', {}) or {}).get('swing_3_6m') or {}).get(
        'holding_plan_sessions', [5, 10, 15])
    plan = [int(day) for day in configured if isinstance(day, (int, float)) and day > 0]
    plan = plan or [5, 10, 15]
    if holding_days is None:
        return plan[len(plan) // 2], plan
    if int(holding_days) <= 0:
        raise ValueError('holding_days doit être strictement positif')
    return int(holding_days), plan


def select_calls(contracts: list[dict], setup: UnderlyingSetup, profile,
                 rate_curve=None, surface_context: dict | None = None,
                 holding_days: int | None = None) -> dict:
    """Pipeline : filtres durs → catégories → simulation → score → 1 par catégorie.

    Retourne {'per_category': {cat: ScoredContract.to_dict() | None},
              'primary': ..., 'rejected': [...], 'notes': [...]}.
    """
    assert setup.direction == 'LONG', 'call_selector ne traite que la direction LONG'
    resolved_holding_days, holding_plan_sessions = _holding_plan(profile, holding_days)
    out = {'per_category': {c: None for c in CALL_CATEGORIES},
           'primary': None, 'rejected': [], 'notes': [],
           'holding_days': resolved_holding_days,
           'holding_plan_sessions': holding_plan_sessions}
    filtered = contract_filter.hard_filter(contracts, profile,
                                           spot=setup.spot, right='C')
    out['rejected'] = [{'contract': {k: r['contract'].get(k) for k in
                                     ('strike', 'expiry', 'dte', 'mid')},
                        'reasons': r['reasons']} for r in filtered['rejected']]
    if not filtered['kept']:
        out['notes'].append('aucun contrat CALL ne passe les filtres durs')
        return out

    buckets = contract_filter.bucket_by_category(filtered['kept'], profile)
    best_per_cat = {}
    for cat in CALL_CATEGORIES:
        scored = []
        for c in buckets.get(cat, []):
            sim = scenario_pricer.simulate(c, setup, rate_curve=rate_curve,
                                           holding_days=resolved_holding_days)
            sc = contract_scorer.score_contract(c, cat, sim, profile, setup,
                                                surface_context=surface_context)
            scored.append(sc)
        scored = [s for s in scored if s.score > 0]
        if scored:
            best = max(scored, key=lambda s: s.score)
            best_per_cat[cat] = best
            out['per_category'][cat] = best.to_dict()

    if not best_per_cat:
        out['notes'].append('aucun contrat scoré positivement — pas de recommandation forcée')
        return out

    # Contrat principal : meilleur score, DYNAMIC prioritaire à score proche.
    ranked = sorted(best_per_cat.items(), key=lambda kv: kv[1].score, reverse=True)
    primary_cat, primary = ranked[0]
    dyn = best_per_cat.get(CATEGORY_DYNAMIC)
    if dyn is not None and primary_cat != CATEGORY_DYNAMIC \
            and dyn.score >= primary.score * 0.92:
        primary_cat, primary = CATEGORY_DYNAMIC, dyn
        out['notes'].append('DYNAMIC retenu comme principal (catégorie centrale, score comparable)')
    out['primary'] = {'category': primary_cat, **primary.to_dict()}
    return out
