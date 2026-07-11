"""vertex.data_sources.ibkr_market_data — snapshots de marché IBKR horodatés.

Lecture seule (via IbkrGateway). Chaque snapshot revient en ProvenancedValue :
LIVE si le flux est temps réel, DELAYED/FROZEN clairement indiqués sinon.
"""
from __future__ import annotations

from .models import SOURCE_IBKR, MODE_LIVE, MODE_DELAYED, MODE_FROZEN, ProvenancedValue
from .provenance import stamp

# marketDataType IBKR : 1 live, 2 frozen, 3 delayed, 4 delayed-frozen
_MODE_BY_TYPE = {1: MODE_LIVE, 2: MODE_FROZEN, 3: MODE_DELAYED, 4: MODE_DELAYED}


def snapshot_to_provenanced(ticker_data: dict, market_data_type: int = 3) -> ProvenancedValue:
    """Convertit un snapshot brut {'last','bid','ask','close','time'} en valeur tracée."""
    mode = _MODE_BY_TYPE.get(int(market_data_type or 3), MODE_DELAYED)
    price = ticker_data.get('last') or ticker_data.get('close')
    pv = stamp(value={'last': ticker_data.get('last'), 'bid': ticker_data.get('bid'),
                      'ask': ticker_data.get('ask'), 'close': ticker_data.get('close'),
                      'price': price},
               source=SOURCE_IBKR, source_mode=mode,
               timestamp=ticker_data.get('time') or '')
    if price is None:
        pv.value = None
        pv.warnings.append('snapshot sans prix exploitable')
    bid, ask = ticker_data.get('bid'), ticker_data.get('ask')
    if bid is not None and ask is not None and 0 < float(ask) < float(bid):
        pv.warnings.append(f'marché croisé: bid {bid} > ask {ask}')
    return pv


def fetch_snapshot(gateway, symbol: str, exchange: str = 'SMART',
                   currency: str = 'USD') -> ProvenancedValue:
    """Snapshot spot pour un symbole (requiert TWS/Gateway ouvert)."""
    from ib_async import Stock  # paresseux : mode dégradé sans dépendance
    ib = gateway.connect()
    contract = Stock(symbol, exchange, currency)
    ib.qualifyContracts(contract)
    ticker = ib.reqTickers(contract)[0]
    data = {'last': ticker.last if ticker.last == ticker.last else None,
            'bid': ticker.bid if ticker.bid and ticker.bid > 0 else None,
            'ask': ticker.ask if ticker.ask and ticker.ask > 0 else None,
            'close': ticker.close if ticker.close == ticker.close else None,
            'time': ticker.time.isoformat() if ticker.time else ''}
    return snapshot_to_provenanced(data, getattr(ib.client, 'marketDataType', 3))
