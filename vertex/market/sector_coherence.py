"""Cohérence descriptive entre un instrument et l’agrégat sectoriel Vertex."""
from __future__ import annotations


def build(profile, detail=None, sectors=None):
    detail, sectors = detail or {}, sectors or []
    sector = profile.get('sector_proxy')
    aggregate = next((row for row in sectors if row.get('sector') == sector), None)
    if not sector or not aggregate:
        return {
            'available': False, 'sector': sector,
            'reason': ('instrument sans proxy sectoriel déclaré' if not sector else
                       'agrégat sectoriel absent du scan courant'),
        }
    score = detail.get('score')
    avg = aggregate.get('avg_score')
    relative = None
    if score is not None and avg is not None:
        try:
            relative = round(float(score) - float(avg), 1)
        except (TypeError, ValueError):
            pass
    members = aggregate.get('members') or []
    rank = next((idx + 1 for idx, item in enumerate(members)
                 if str(item.get('symbol') or '').upper() == profile.get('symbol')), None)
    return {
        'available': True, 'asset_class': profile.get('asset_class'), 'sector': sector,
        'sector_avg_score': avg, 'sector_pct_buy': aggregate.get('pct_buy'),
        'sector_risk_band': aggregate.get('risk_band'),
        'sector_leader': aggregate.get('leader'),
        'instrument_score_minus_sector_avg': relative,
        'instrument_rank_in_sector': rank,
        'members_count': aggregate.get('n'),
        'note': ('contexte comparatif descriptif ; ne modifie ni le score ni le verdict'),
    }


__all__ = ['build']
