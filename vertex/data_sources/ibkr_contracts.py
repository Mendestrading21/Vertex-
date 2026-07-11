"""vertex.data_sources.ibkr_contracts — qualification de contrats (mapping sûr).

Vérifie qu'un symbole résout vers LE bon contrat (devise, bourse, multiplic.) —
protège contre CONTRACT_MAPPING_ERROR / CURRENCY_MISMATCH / MULTIPLIER_MISMATCH.
"""
from __future__ import annotations


def validate_stock_contract(details: dict, symbol: str) -> list[str]:
    """details: {'symbol','currency','exchange','conId'} → liste de problèmes."""
    problems = []
    if str(details.get('symbol', '')).upper() != symbol.upper():
        problems.append(f"mapping: résolu {details.get('symbol')!r} ≠ demandé {symbol!r}")
    if details.get('currency') not in (None, 'USD'):
        problems.append(f"devise inattendue: {details.get('currency')!r}")
    if not details.get('conId'):
        problems.append('conId absent — contrat non qualifié')
    return problems


def validate_option_contract(details: dict, symbol: str) -> list[str]:
    problems = validate_stock_contract(details, symbol)
    mult = details.get('multiplier')
    if mult not in (None, '', '100', 100):
        problems.append(f'multiplicateur inattendu: {mult!r} (attendu 100)')
    if details.get('right') not in ('C', 'P'):
        problems.append(f"type d'option inattendu: {details.get('right')!r}")
    return problems


def qualify_stock(gateway, symbol: str) -> dict:
    from ib_async import Stock
    ib = gateway.connect()
    contract = Stock(symbol, 'SMART', 'USD')
    qualified = ib.qualifyContracts(contract)
    if not qualified:
        return {'symbol': symbol, 'conId': None}
    c = qualified[0]
    return {'symbol': c.symbol, 'currency': c.currency,
            'exchange': c.exchange, 'conId': c.conId}
