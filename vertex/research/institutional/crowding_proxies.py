"""vertex.research.institutional.crowding_proxies — proxies HONNÊTES de crowding (§23).

On ne connaît PAS les positions des hedge funds sans source réelle : chaque
signal est un proxy étiqueté, jamais une certitude.
"""
from __future__ import annotations

PROXY_DISCLAIMER = ('proxy de positionnement — les positions réelles des fonds '
                    'sont INCONNUES sans source dédiée')


def crowding_score(stock: dict) -> dict:
    """stock : {'correlation_to_leaders', 'etf_weight_pct', 'analyst_buy_ratio',
    'momentum_percentile', 'iv_percentile', 'sector_concentration', 'rvol'}.
    Rend un score 0-100 + composantes, chaque composante marquée proxy."""
    components = []

    def comp(name, value, threshold, weight, note):
        if value is None:
            return
        triggered = value >= threshold
        components.append({'name': name, 'value': value, 'triggered': triggered,
                           'weight': weight, 'note': f'{note} ({PROXY_DISCLAIMER})'})

    comp('HIGH_CORRELATION', stock.get('correlation_to_leaders'), 0.8, 20,
         'corrélation élevée aux leaders de momentum')
    comp('ETF_CONCENTRATION', stock.get('etf_weight_pct'), 4.0, 15,
         'poids important dans les ETF populaires')
    comp('ANALYST_CONSENSUS', stock.get('analyst_buy_ratio'), 0.85, 15,
         'consensus analystes quasi unanime')
    comp('EXTREME_MOMENTUM', stock.get('momentum_percentile'), 92, 20,
         'momentum au-delà du 92e percentile')
    comp('ELEVATED_IV', stock.get('iv_percentile'), 80, 10,
         'volatilité implicite élevée')
    comp('SECTOR_CONCENTRATION', stock.get('sector_concentration'), 0.4, 10,
         'concentration sectorielle du flux')
    comp('ABNORMAL_VOLUME', stock.get('rvol'), 3.0, 10,
         'volume anormal soutenu')

    score = sum(c['weight'] for c in components if c['triggered'])
    return {'score': min(100, score), 'crowded': score >= 50,
            'components': components, 'disclaimer': PROXY_DISCLAIMER}
