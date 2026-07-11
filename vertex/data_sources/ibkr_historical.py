"""vertex.data_sources.ibkr_historical — barres historiques IBKR (lecture seule)."""
from __future__ import annotations

from .models import SOURCE_IBKR, MODE_EOD, ProvenancedValue
from .provenance import stamp


def bars_to_provenanced(bars: list[dict], timestamp: str = '') -> ProvenancedValue:
    """bars: [{'date','open','high','low','close','volume'}…] — validées basiquement."""
    cleaned, warnings = [], []
    for b in bars or []:
        o, h, l, c = b.get('open'), b.get('high'), b.get('low'), b.get('close')
        if None in (o, h, l, c):
            warnings.append(f"barre incomplète ignorée ({b.get('date')})")
            continue
        cleaned.append({'date': b.get('date'), 'open': float(o), 'high': float(h),
                        'low': float(l), 'close': float(c),
                        'volume': b.get('volume')})
    pv = stamp(value=cleaned or None, source=SOURCE_IBKR, source_mode=MODE_EOD,
               timestamp=timestamp)
    pv.warnings.extend(warnings)
    return pv


def fetch_daily_bars(gateway, symbol: str, duration: str = '1 Y') -> ProvenancedValue:
    from ib_async import Stock
    ib = gateway.connect()
    contract = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(contract)
    raw = ib.reqHistoricalData(contract, endDateTime='', durationStr=duration,
                               barSizeSetting='1 day', whatToShow='TRADES',
                               useRTH=True, formatDate=1)
    bars = [{'date': str(b.date), 'open': b.open, 'high': b.high,
             'low': b.low, 'close': b.close, 'volume': b.volume} for b in raw]
    return bars_to_provenanced(bars)
