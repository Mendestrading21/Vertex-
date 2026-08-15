"""Construction déterministe du paquet de décision servi par Strategy OS.

Ce module interdit la complétude implicite : une route peut dériver des éléments
purement descriptifs à partir du scan, mais les preuves critiques absentes
(réconciliation des sources ou risque portefeuille) restent visibles et plafonnent
la décision à ``ATTENDRE``. Il ne déclenche aucun ordre et ne conserve aucune donnée.
"""
from __future__ import annotations

from vertex.engines.anomaly_context import build as build_anomaly_context
from vertex.market.regime_engine import classify_regime

INCOMPLETE_PACKET_RULE = 'DECISION_PACKET_INCOMPLETE'
CRITICAL_SECTIONS = ('data_quality', 'reconciliation', 'guard')


def _source_quality(scan_state: dict, detail: dict) -> tuple[dict, bool]:
    supplied = detail.get('data_quality') or scan_state.get('data_quality')
    if isinstance(supplied, dict) and 'actionable_allowed' in supplied:
        out = dict(supplied)
        out.setdefault('overall', 'MISSING')
        out['derived'] = False
        return out, True
    source = scan_state.get('source') or ''
    overall = 'DEMO' if source == 'demo' else ('RECENT' if source else 'MISSING')
    return {
        'overall': overall,
        'actionable_allowed': bool(source and source != 'demo'),
        'derived': True,
        'warning': 'qualité dérivée du scan global — paquet valeur par valeur absent',
    }, False


def _reconciliation(scan_state: dict, detail: dict) -> tuple[dict, bool]:
    supplied = detail.get('reconciliation') or scan_state.get('reconciliation')
    if isinstance(supplied, dict) and 'actionable_allowed' in supplied:
        out = dict(supplied)
        out['derived'] = False
        return out, True
    return {
        'actionable_allowed': False,
        'derived': True,
        'warning': 'réconciliation spot/chaîne/contrat absente — décision actionnable interdite',
    }, False


def _guard(scan_state: dict, detail: dict) -> tuple[dict, bool]:
    supplied = detail.get('guard') or scan_state.get('guard')
    if isinstance(supplied, dict):
        out = dict(supplied)
        out.setdefault('blocking_rules', [])
        out.setdefault('mandatory_reviews', [])
        out['derived'] = False
        return out, True
    return {
        'blocking_rules': [],
        'mandatory_reviews': [],
        'derived': True,
        'warning': 'risque portefeuille non calculé pour ce paquet',
    }, False


def _actual_anomalies(symbol: str, detail: dict) -> list[dict]:
    context = build_anomaly_context(symbol, detail)
    return context.get('events') or []


def _market_regime(scan_state: dict) -> dict:
    market = scan_state.get('market') or {}
    inputs = {
        'index_trend': {'TREND': 'UP', 'CHOP': 'FLAT'}.get(market.get('regime'),
                                                             market.get('spy_trend')),
        'breadth_pct': market.get('breadth'),
        'vix': market.get('vix'),
        'leadership': ('CYCLICAL' if market.get('risk') == 'Risk-On'
                       else 'DEFENSIVE' if market.get('risk') == 'Risk-Off' else None),
    }
    try:
        return classify_regime(inputs)
    except Exception as exc:  # un classifieur indisponible ne doit jamais autoriser un trade
        return {'regime': 'UNKNOWN', 'adjustments': {'new_risk_allowed': False},
                'warning': 'classifieur de régime indisponible: %s' % type(exc).__name__}


def build(symbol: str, detail: dict | None, scan_state: dict | None) -> dict:
    """Construit un paquet prêt pour ``executive_engine.decide``.

    Le statut `complete` signifie que les trois preuves critiques proviennent d’un
    calcul explicite. Les métriques descriptives peuvent rester disponibles lorsque
    le paquet est incomplet, mais une entrée nouvelle est alors bloquée.
    """
    detail = detail or {}
    scan_state = scan_state or {}
    plan = detail.get('plan') or {}
    data_quality, quality_complete = _source_quality(scan_state, detail)
    reconciliation, reconciliation_complete = _reconciliation(scan_state, detail)
    guard, guard_complete = _guard(scan_state, detail)
    completeness = {
        'data_quality': quality_complete,
        'reconciliation': reconciliation_complete,
        'guard': guard_complete,
    }
    missing = [name for name in CRITICAL_SECTIONS if not completeness[name]]
    blocking_rules = list(guard.get('blocking_rules') or [])
    if missing and INCOMPLETE_PACKET_RULE not in blocking_rules:
        blocking_rules.append(INCOMPLETE_PACKET_RULE)
    guard['blocking_rules'] = blocking_rules
    guard['packet_complete'] = not missing
    guard['missing_sections'] = missing

    return {
        'symbol': symbol,
        'fundamental': {'score': detail.get('st_fund') or detail.get('fund_score')},
        'catalysts': {'score': 60 if detail.get('earnings_dte') is not None else None},
        'technical': {
            'score': detail.get('score'),
            'reward_risk': detail.get('rr') or (plan.get('rr') if isinstance(plan, dict) else None),
            'timing_score': detail.get('st_timing'),
            'overextended': (detail.get('ext_atr') or 0) >= 2.5,
            'thesis_invalidated': bool(detail.get('thesis_invalidated')),
        },
        'sentiment': {'score': detail.get('rs')},
        'anomalies': _actual_anomalies(symbol, detail),
        'data_quality': data_quality,
        'reconciliation': reconciliation,
        'guard': guard,
        'market_regime': _market_regime(scan_state),
        'option_selection': detail.get('option_selection') or {},
        'decision_packet': {
            'complete': not missing,
            'missing_sections': missing,
            'completeness': completeness,
            'source': scan_state.get('source') or None,
        },
    }


__all__ = ['build', 'INCOMPLETE_PACKET_RULE', 'CRITICAL_SECTIONS']
