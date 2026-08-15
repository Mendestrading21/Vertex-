"""Production de preuves décisionnelles au moment du scan.

Les paquets produits ici décrivent uniquement ce qui est effectivement présent
dans le cycle courant. Une chaîne d’options sans horodatage, par exemple, reste
MISSING ; elle n’est pas rendue actionnable par déduction.
"""
from __future__ import annotations

from datetime import datetime, timezone

from .models import (
    AnalyticsPacket, MODE_DELAYED, MODE_EOD, MODE_NONE, SOURCE_FALLBACK_EOD,
    SOURCE_SECONDARY, SOURCE_UNAVAILABLE, missing,
)
from .provenance import stamp
from .quality import grade_packet
from .reconciliation import (
    ReconciliationReport, reconcile_contract, reconcile_spot,
    reconcile_spot_vs_options,
)


def _iso(value):
    if value is None:
        return ''
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    if hasattr(value, 'to_pydatetime'):
        value = value.to_pydatetime()
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    if isinstance(value, str):
        return value
    return ''


def _source(scan_source):
    text = str(scan_source or '').lower()
    if 'stooq' in text and 'yfinance' not in text:
        return SOURCE_FALLBACK_EOD, MODE_EOD, True
    if 'yfinance' in text:
        return SOURCE_SECONDARY, MODE_EOD, 'stooq' in text
    return SOURCE_UNAVAILABLE, MODE_NONE, False


def _frame_timestamp(frame):
    try:
        return _iso(frame.index[-1])
    except Exception:
        return ''


def _contract_spot(contract):
    for key in ('underlying_price', 'underlyingPrice', 'spot', 'underlying_last'):
        if contract.get(key) not in (None, ''):
            return contract.get(key)
    return None


def _contracts(board, symbol):
    return [contract for contract in (board or [])
            if str(contract.get('sym') or contract.get('underlying') or '').upper() == symbol.upper()]


def build_symbol(symbol, detail, frame, scan_source, options_board=None, options_as_of=None):
    """Construit les preuves et le rapport de réconciliation pour un titre."""
    detail = detail or {}
    source, mode, fallback = _source(scan_source)
    packet = AnalyticsPacket(symbol=symbol)
    timestamp = _frame_timestamp(frame)
    price = detail.get('price')
    if price not in (None, '') and timestamp:
        packet.set_source('spot', stamp(price, source, mode, timestamp, fallback_used=fallback))
    else:
        packet.set_source('spot', missing('spot ou horodatage de série indisponible'))
    closes = ((detail.get('series') or {}).get('close') or [])
    if closes and timestamp:
        packet.set_source('history', stamp(len(closes), source, mode, timestamp, fallback_used=fallback))
    else:
        packet.set_source('history', missing('série de clôtures canonique indisponible'))

    contracts = _contracts(options_board, symbol)
    option_ts = _iso(options_as_of)
    if contracts and option_ts:
        packet.set_source('options', stamp(len(contracts), SOURCE_SECONDARY, MODE_DELAYED, option_ts))
    elif contracts:
        packet.set_source('options', missing('chaîne d’options présente sans horodatage explicite'))
    else:
        packet.set_source('options', missing('aucun contrat options pour ce titre'))
    packet.set_source('fundamentals', missing('horodatage fondamental par titre non fourni'))
    packet.set_source('catalysts', missing('horodatage de catalyseurs par titre non fourni'))
    quality = grade_packet(packet)

    report = ReconciliationReport(symbol)
    quotes = [{'source': 'SCAN', 'price': price, 'timestamp': timestamp, 'currency': 'USD'}]
    for contract in contracts:
        option_spot = _contract_spot(contract)
        if option_spot not in (None, ''):
            quotes.append({'source': 'OPTION_CHAIN', 'price': option_spot,
                           'timestamp': option_ts, 'currency': contract.get('currency') or 'USD'})
        reconcile_contract(symbol, contract, report)
    reconcile_spot(symbol, quotes, report)
    if contracts:
        reconcile_spot_vs_options(symbol, timestamp, option_ts, report)
    return packet.to_dict(), report.to_dict()


def build_scan(detail_by_symbol, frames, scan_source, options_board=None, options_as_of=None):
    packets, reconciliations = [], {}
    for symbol, detail in (detail_by_symbol or {}).items():
        packet, report = build_symbol(symbol, detail, (frames or {}).get(symbol), scan_source,
                                      options_board=options_board, options_as_of=options_as_of)
        packets.append(packet)
        reconciliations[symbol] = report
        detail['data_quality'] = packet.get('quality') or {}
        detail['reconciliation'] = report
    return packets, reconciliations


__all__ = ['build_symbol', 'build_scan']
