"""Profil d’instrument déterministe pour les diagnostics multi-actifs Vertex.

La taxonomie n’est pas un flux de marché : elle n’infère jamais une exposition
ou une composition d’ETF absente. Les symboles non couverts restent inconnus.
"""
from __future__ import annotations

from vertex.market.sectors import SECTOR_MAP


ETF_SECTOR_PROXY = {
    'SMH': 'Semiconducteurs', 'SOXX': 'Semiconducteurs',
    'IGV': 'Software', 'SKYY': 'Software',
    'XLK': 'Big Tech', 'QQQ': 'Big Tech',
    'XLY': 'Conso', 'XLP': 'Conso',
    'XLV': 'Sante', 'XLF': 'Finance', 'XLE': 'Energie',
    'ARKK': 'Infra-IA',
}
BROAD_ETFS = {'SPY', 'VOO', 'IVV', 'IWM', 'DIA', 'VTI', 'VT'}


def build(symbol, detail=None):
    sym = str(symbol or '').upper()
    detail = detail or {}
    declared = str(detail.get('asset_type') or detail.get('quoteType') or
                   detail.get('instrument_type') or '').upper()
    if sym in ETF_SECTOR_PROXY:
        asset_class, source, sector = 'ETF', 'CURATED_SECTOR_PROXY', ETF_SECTOR_PROXY[sym]
        classification = 'SECTOR_PROXY_ETF'
    elif sym in BROAD_ETFS:
        asset_class, source, sector = 'ETF', 'CURATED_BROAD_PROXY', None
        classification = 'BROAD_MARKET_ETF'
    elif declared in ('ETF', 'MUTUALFUND'):
        asset_class, source, sector = 'ETF', 'DECLARED_SOURCE', detail.get('sector')
        classification = 'DECLARED_ETF'
    elif sym in SECTOR_MAP:
        asset_class, source, sector = 'EQUITY', 'VERTEX_SECTOR_MAP', SECTOR_MAP[sym]
        classification = 'SECTOR_MEMBER_EQUITY'
    elif declared in ('EQUITY', 'STOCK'):
        asset_class, source, sector = 'EQUITY', 'DECLARED_SOURCE', detail.get('sector')
        classification = 'DECLARED_EQUITY'
    else:
        asset_class, source, sector = 'UNKNOWN', 'NO_CANONICAL_CLASSIFICATION', None
        classification = 'UNCLASSIFIED'
    return {
        'symbol': sym, 'asset_class': asset_class, 'classification': classification,
        'classification_source': source, 'sector_proxy': sector,
        'requires': {
            'spot_quote': True, 'dated_history': True,
            'data_quality_proof': True, 'reconciliation_proof': True,
            'option_board_if_options_are_assessed': True,
        },
        'note': ('profil descriptif : aucune composition, exposition ou recommandation '
                 'n’est déduite hors des sources déclarées'),
    }


__all__ = ['build', 'ETF_SECTOR_PROXY', 'BROAD_ETFS']
