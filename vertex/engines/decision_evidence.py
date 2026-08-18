"""Preuves de qualité et de réconciliation consommées par Skyler.

Ce module ne déduit jamais une donnée fraîche de la seule présence d’un scan.
Il sélectionne uniquement une preuve explicitement produite par le pipeline ;
l’absence de preuve reste un contexte indisponible et est gérée par une gate.
"""
from __future__ import annotations


def _packet_for(scan_state, symbol):
    packets = ((scan_state or {}).get('analytics_packets') or
               (scan_state or {}).get('data_packets') or [])
    if isinstance(packets, dict):
        packets = list(packets.values())
    for packet in packets:
        if isinstance(packet, dict) and str(packet.get('symbol', '')).upper() == str(symbol).upper():
            return packet
    return {}


def for_symbol(scan_state, symbol, detail=None):
    """Retourne ``(qualité, réconciliation)`` au format Skyler.

    Les producteurs autorisés sont un AnalyticsPacket de scan, un détail de titre
    explicitement enrichi, ou une table de réconciliation par symbole. Aucun
    fallback ne transforme une source globale en preuve instrumentale.
    """
    state, detail = scan_state or {}, detail or {}
    packet = _packet_for(state, symbol)
    quality = packet.get('quality') or detail.get('data_quality') or {}
    sources = packet.get('sources') or {}
    freshness = {
        'spot': (sources.get('spot') or {}).get('quality'),
        'options': (sources.get('options') or {}).get('quality'),
    }
    raw_rec = (packet.get('reconciliation') or detail.get('reconciliation') or
               (state.get('reconciliation_by_symbol') or {}).get(str(symbol).upper()) or {})
    if quality:
        data_quality = {
            'available': True,
            'overall': quality.get('overall'),
            'warnings': list(quality.get('warnings') or []),
            'actionable_allowed': quality.get('actionable_allowed') is True,
            'freshness': freshness,
            'source': 'analytics_packet' if packet.get('quality') else 'detail',
        }
    else:
        data_quality = {'available': False,
                        'reason': 'AnalyticsPacket de qualité absent pour ce titre'}
    if raw_rec:
        reconciliation = {
            'available': True,
            'actionable_allowed': raw_rec.get('actionable_allowed') is True,
            'reason': raw_rec.get('reason') or raw_rec.get('summary'),
            'blocking': bool(raw_rec.get('blocking')),
            'source': 'analytics_packet' if packet.get('reconciliation') else 'detail_or_state',
        }
    else:
        reconciliation = {'available': False,
                          'reason': 'rapport de réconciliation absent pour ce titre'}
    return data_quality, reconciliation


__all__ = ['for_symbol']
