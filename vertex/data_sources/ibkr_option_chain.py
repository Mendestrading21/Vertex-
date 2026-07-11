"""vertex.data_sources.ibkr_option_chain — chaînes d'options IBKR (lecture seule).

Greeks : quand IBKR fournit ses modelGreeks, ils sont étiquetés BROKER_GREEKS
et PRÉFÉRÉS à tout modèle maison (§6.8). La chaîne complète n'est jamais tirée
pour tout l'univers : le chargement suit l'entonnoir §14 (expirations →
strikes filtrés → finalistes).
"""
from __future__ import annotations

from .models import SOURCE_IBKR, MODE_DELAYED, GREEKS_BROKER, ProvenancedValue
from .provenance import stamp


def contract_row(*, symbol: str, expiry: str, strike: float, right: str,
                 bid=None, ask=None, last=None, volume=None, open_interest=None,
                 iv=None, delta=None, gamma=None, theta=None, vega=None,
                 multiplier='100', currency='USD', underlying=None,
                 greeks_source: str = GREEKS_BROKER, timestamp: str = '') -> dict:
    """Ligne de contrat normalisée — TOUT contrat manipulé par les moteurs a cette forme."""
    mid = None
    if bid is not None and ask is not None and float(ask) > 0:
        mid = (float(bid) + float(ask)) / 2
    return {
        'symbol': symbol.upper(), 'underlying': (underlying or symbol).upper(),
        'expiry': expiry, 'strike': float(strike), 'right': right.upper()[:1],
        'bid': bid, 'ask': ask, 'mid': mid, 'last': last,
        'volume': volume, 'open_interest': open_interest,
        'iv': iv, 'delta': delta, 'gamma': gamma, 'theta': theta, 'vega': vega,
        'greeks_source': greeks_source,
        'multiplier': multiplier, 'currency': currency,
        'timestamp': timestamp,
    }


def chain_to_provenanced(rows: list[dict], timestamp: str = '') -> ProvenancedValue:
    return stamp(value=list(rows or []), source=SOURCE_IBKR,
                 source_mode=MODE_DELAYED, timestamp=timestamp)


def fetch_expirations(gateway, symbol: str) -> list[str]:
    """Étape 1 de l'entonnoir : seulement les expirations (pas les chaînes)."""
    from ib_async import Stock
    ib = gateway.connect()
    stock = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(stock)
    params = ib.reqSecDefOptParams(stock.symbol, '', stock.secType, stock.conId)
    expirations: set[str] = set()
    for p in params:
        expirations.update(p.expirations)
    return sorted(expirations)


def fetch_contract_details(gateway, symbol: str, expiry: str,
                           strikes: list[float], right: str = 'C') -> ProvenancedValue:
    """Étape finale de l'entonnoir : détails complets pour une poignée de finalistes."""
    from ib_async import Option
    ib = gateway.connect()
    contracts = [Option(symbol, expiry, k, right, 'SMART', currency='USD')
                 for k in strikes]
    contracts = [c for c in ib.qualifyContracts(*contracts) if c.conId]
    tickers = ib.reqTickers(*contracts) if contracts else []
    rows = []
    for c, t in zip(contracts, tickers):
        mg = getattr(t, 'modelGreeks', None)
        rows.append(contract_row(
            symbol=symbol, expiry=expiry, strike=c.strike, right=right,
            bid=t.bid if t.bid and t.bid > 0 else None,
            ask=t.ask if t.ask and t.ask > 0 else None,
            last=t.last if t.last == t.last else None,
            volume=int(t.volume) if t.volume and t.volume == t.volume else None,
            open_interest=None,
            iv=getattr(mg, 'impliedVol', None) if mg else None,
            delta=getattr(mg, 'delta', None) if mg else None,
            gamma=getattr(mg, 'gamma', None) if mg else None,
            theta=getattr(mg, 'theta', None) if mg else None,
            vega=getattr(mg, 'vega', None) if mg else None,
            greeks_source=GREEKS_BROKER if mg else 'MODEL_ESTIMATE',
            timestamp=t.time.isoformat() if t.time else ''))
    return chain_to_provenanced(rows)
