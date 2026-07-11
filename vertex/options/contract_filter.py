"""vertex.options.contract_filter — filtres durs avant scoring (§20).

Un contrat écarté ici ne sera jamais scoré : DTE hors bornes constitution,
liquidité intraitable, anomalie bloquante, catégorie sans bande delta.
"""
from __future__ import annotations

from . import liquidity
from .models import CALL_CATEGORIES, CATEGORY_BEARISH_TACTICAL
from vertex.anomalies import option_anomalies
from vertex.anomalies.models import any_blocking


def dte_within_constitution(dte: int | None, profile) -> bool:
    if dte is None:
        return False
    d = profile.dte
    return d.absolute_minimum <= dte <= d.absolute_maximum


def delta_band(category: str, profile) -> tuple[float, float] | None:
    cat = profile.category(category)
    if not cat:
        return None
    if category == CATEGORY_BEARISH_TACTICAL:
        return (cat['delta_abs_min'], cat['delta_abs_max'])
    return (cat['delta_min'], cat['delta_max'])


def in_delta_band(contract: dict, category: str, profile) -> bool:
    band = delta_band(category, profile)
    delta = contract.get('delta')
    if band is None or delta is None:
        return False
    return band[0] <= abs(float(delta)) <= band[1]


def hard_filter(contracts: list[dict], profile, spot: float | None = None,
                right: str = 'C') -> dict:
    """Retourne {'kept': [...], 'rejected': [{'contract', 'reasons'}...]}."""
    kept, rejected = [], []
    for c in contracts or []:
        reasons: list[str] = []
        if c.get('right') != right:
            continue
        dte = c.get('dte')
        if not dte_within_constitution(dte, profile):
            d = profile.dte
            reasons.append(f'DTE {dte} hors bornes constitution '
                           f'[{d.absolute_minimum}, {d.absolute_maximum}]')
        liq = liquidity.assess(c)
        if not liq['tradeable']:
            reasons.append('liquidité intraitable: ' + '; '.join(liq['issues'] or ['n/d']))
        anomalies = option_anomalies.check_contract(c, spot=spot)
        if any_blocking(anomalies):
            reasons.append('anomalie bloquante: ' +
                           ', '.join(a.code for a in anomalies if a.blocking))
        if reasons:
            rejected.append({'contract': c, 'reasons': reasons})
        else:
            c = dict(c)
            c['_liquidity'] = liq
            c['_anomalies'] = anomalies
            kept.append(c)
    return {'kept': kept, 'rejected': rejected}


def bucket_by_category(contracts: list[dict], profile) -> dict:
    """Répartit les contrats gardés dans leurs catégories (bandes de delta)."""
    buckets = {cat: [] for cat in CALL_CATEGORIES}
    for c in contracts:
        for cat in CALL_CATEGORIES:
            if in_delta_band(c, cat, profile):
                buckets[cat].append(c)
    return buckets
