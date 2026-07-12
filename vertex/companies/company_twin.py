"""vertex.companies.company_twin — jumeau analytique d'une entreprise (§16).

Agrège CE QUE LES MOTEURS FOURNISSENT déjà : profil (activité, segments),
pairs sectoriels, fondamentaux (croissance, marges, valorisation), plus le
contexte scan (score, catalyseurs, plan). Chaque champ absent reste None —
jamais un zéro déguisé.
"""
from __future__ import annotations

import time


def company_twin(sym: str, scan_state: dict | None = None) -> dict:
    sym = sym.upper()
    out = {'symbol': sym, 'as_of': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'profile': None, 'peers': [], 'fundamentals': None,
           'valuation': None, 'catalysts': {}, 'scan': None, 'missing': []}

    try:
        from vertex.data import company as _company
        prof = _company._fetch_profile(sym)  # cache hebdo interne
        out['profile'] = prof or None
        if not prof:
            out['missing'].append('profil')
    except Exception:
        out['missing'].append('profil')
    try:
        from vertex.data import company as _company
        out['peers'] = _company.peers(sym) or []
    except Exception:
        out['missing'].append('pairs')

    detail = ((scan_state or {}).get('detail') or {}).get(sym) or {}
    if detail:
        out['scan'] = {'score': detail.get('score'), 'verdict': detail.get('verdict'),
                       'sector': detail.get('sector'), 'plan': detail.get('plan'),
                       'earnings_dte': detail.get('earnings_dte')}
        if detail.get('earnings_dte') is not None:
            out['catalysts']['earnings_in_days'] = detail['earnings_dte']
    else:
        out['missing'].append('scan')

    fund = ((scan_state or {}).get('fundamentals') or {}).get('by_sym', {}).get(sym)
    if fund:
        out['fundamentals'] = fund
    else:
        out['missing'].append('fondamentaux')

    return out


def snapshot_key_fields(twin: dict) -> dict:
    """Champs comparés par le détecteur de changement (significatifs)."""
    f = twin.get('fundamentals') or {}
    scan = twin.get('scan') or {}
    return {
        'score': scan.get('score'),
        'verdict': scan.get('verdict'),
        'earnings_dte': scan.get('earnings_dte'),
        'pe': f.get('pe'),
        'rev_growth': f.get('rev_growth') or f.get('growth'),
        'margin': f.get('margin') or f.get('margins'),
    }


__all__ = ['company_twin', 'snapshot_key_fields']
