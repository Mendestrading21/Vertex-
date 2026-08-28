"""vertex.data_sources.ibkr_market_data — snapshots de marché IBKR horodatés.

Lecture seule (via IbkrGateway). Chaque snapshot revient en ProvenancedValue :
LIVE si le flux est temps réel, DELAYED/FROZEN clairement indiqués sinon.
"""
from __future__ import annotations

from .models import SOURCE_IBKR, MODE_LIVE, MODE_DELAYED, MODE_FROZEN, ProvenancedValue
from .provenance import stamp
from vertex.data_sources import ibkr_gateway

# marketDataType IBKR : 1 live, 2 frozen, 3 delayed, 4 delayed-frozen
_MODE_BY_TYPE = {1: MODE_LIVE, 2: MODE_FROZEN, 3: MODE_DELAYED, 4: MODE_DELAYED}

#: Le type n'a pas pu être OBSERVÉ. Ce n'est pas 3 : c'est « on ne sait pas ».
#: G5 exige que le type de marché soit capturé PAR REQUÊTE ; le confondre avec
#: « différé » ferait passer une ignorance pour une mesure.
TYPE_INCONNU = 0


def type_observe(ticker_data: dict) -> int:
    """Le type de données déduit des champs qu'IBKR a RÉELLEMENT remplis.

    `ib_async` 2.1.0 n'expose aucun moyen de relire le type demandé : il n'a
    que le setter `reqMarketDataType`. Le code lisait donc `client.marketDataType`,
    un attribut qui n'existe pas, et retombait **silencieusement** sur « différé »
    à chaque appel — mesuré sur session réelle le 24 août 2026, sonde
    `mode_donnees` en échec.

    Le ticker, lui, le dit : IBKR remplit `delayedLast/delayedBid/delayedAsk`
    au lieu des champs directs quand la donnée est différée. C'est une
    observation, pas une hypothèse.

    Ce qu'on ne peut PAS distinguer par les champs : temps réel contre figé —
    les deux remplissent `last`. On rend alors `TYPE_INCONNU` plutôt que de
    revendiquer `LIVE`, parce que se tromper vers « live » présenterait une
    clôture de la veille comme un cours de séance.
    """
    if any(ticker_data.get(k) is not None
           for k in ('delayedLast', 'delayedBid', 'delayedAsk')):
        return 3
    return TYPE_INCONNU


def snapshot_to_provenanced(ticker_data: dict,
                            market_data_type: int = TYPE_INCONNU) -> ProvenancedValue:
    """Convertit un snapshot brut {'last','bid','ask','close','time'} en valeur tracée.

    `market_data_type` vient de l'appelant quand il SAIT ce qu'il a demandé.
    Sinon `TYPE_INCONNU` : le mode retombe sur `DELAYED` — la direction
    prudente — mais la valeur porte l'aveu, au lieu de laisser croire que le
    différé a été constaté.
    """
    demande = int(market_data_type or TYPE_INCONNU)
    mode = _MODE_BY_TYPE.get(demande, MODE_DELAYED)
    price = ticker_data.get('last') or ticker_data.get('close')
    pv = stamp(value={'last': ticker_data.get('last'), 'bid': ticker_data.get('bid'),
                      'ask': ticker_data.get('ask'), 'close': ticker_data.get('close'),
                      'price': price},
               source=SOURCE_IBKR, source_mode=mode,
               timestamp=ticker_data.get('time') or '')
    if demande == TYPE_INCONNU:
        pv.warnings.append(
            "type de marché non observé — mode prudent DELAYED, pas une mesure")
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
    Stock = ibkr_gateway.classe('Stock')  # porte unique, paresseuse
    ib = gateway.connect()
    contract = Stock(symbol, exchange, currency)
    ib.qualifyContracts(contract)
    ticker = ib.reqTickers(contract)[0]
    def _direct(v):
        return v if v == v and (v is None or v > 0) else None

    def _champ(nom):
        return _direct(getattr(ticker, nom, None))

    data = {'last': ticker.last if ticker.last == ticker.last else None,
            'bid': ticker.bid if ticker.bid and ticker.bid > 0 else None,
            'ask': ticker.ask if ticker.ask and ticker.ask > 0 else None,
            'close': ticker.close if ticker.close == ticker.close else None,
            'delayedLast': _champ('delayedLast'),
            'delayedBid': _champ('delayedBid'),
            'delayedAsk': _champ('delayedAsk'),
            'time': ticker.time.isoformat() if ticker.time else ''}
    #  OBSERVÉ, plus supposé : `ib_async` n'expose pas le type demandé, et
    #  l'ancien `getattr(ib.client, 'marketDataType', 3)` lisait un attribut
    #  inexistant — donc « différé » à chaque appel, sans jamais l'avoir constaté.
    return snapshot_to_provenanced(data, type_observe(data))
