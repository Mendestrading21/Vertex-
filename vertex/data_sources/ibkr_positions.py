"""vertex.data_sources.ibkr_positions — positions réelles du compte (lecture seule).

C'est LA source des positions pour le moteur de risque (§6.9) : le risque
portefeuille se calcule sur ces positions réelles (ou sur des positions
simulées transmises EXPLICITEMENT), jamais sur les candidats du scanner.
"""
from __future__ import annotations

from .models import SOURCE_IBKR, MODE_LIVE, ProvenancedValue
from .provenance import stamp


def positions_to_provenanced(raw_positions: list[dict]) -> ProvenancedValue:
    """raw_positions: [{'symbol','position','avgCost','secType','currency'}…]"""
    cleaned = []
    for p in raw_positions or []:
        try:
            qty = float(p.get('position') or 0)
        except (TypeError, ValueError):
            continue
        if qty == 0:
            continue
        cleaned.append({'symbol': str(p.get('symbol') or '').upper(),
                        'quantity': qty,
                        'avg_cost': p.get('avgCost'),
                        'sec_type': p.get('secType') or 'STK',
                        'currency': p.get('currency') or 'USD'})
    return stamp(value=cleaned, source=SOURCE_IBKR, source_mode=MODE_LIVE)


def fetch_positions(gateway) -> ProvenancedValue:
    ib = gateway.connect()
    raw = [{'symbol': pos.contract.symbol, 'position': pos.position,
            'avgCost': pos.avgCost, 'secType': pos.contract.secType,
            'currency': pos.contract.currency}
           for pos in ib.positions()]
    return positions_to_provenanced(raw)
