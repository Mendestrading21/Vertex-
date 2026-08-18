"""Contexte descriptif de proximité des résultats, sans estimation de date."""
from __future__ import annotations


def build(timeline):
    timeline = timeline or {}
    channels = ((timeline.get('coverage') or {}).get('input_channels') or {})
    provided = channels.get('earnings_provided')
    earnings = [event for event in (timeline.get('events') or [])
                if isinstance(event, dict) and event.get('kind') == 'earnings']
    if provided is not True:
        return {'available': False, 'status': 'EARNINGS_CALENDAR_UNAVAILABLE', 'read_only': True,
                'reason': 'calendrier de résultats non fourni — date jamais estimée'}
    dated_dte = []
    dated_without_dte = 0
    for event in earnings:
        dte = event.get('dte')
        if isinstance(dte, (int, float)) and dte >= 0:
            dated_dte.append((float(dte), event))
        elif event.get('date') is not None:
            dated_without_dte += 1
    if not dated_dte:
        return {'available': True, 'status': ('DATED_EARNINGS_NO_DTE' if dated_without_dte else 'NO_DATED_EARNINGS'),
                'earnings_events': len(earnings), 'dated_without_dte': dated_without_dte,
                'read_only': True,
                'note': 'aucun nombre de jours déclaré — proximité non déduite d’une date non normalisée'}
    dte, event = min(dated_dte, key=lambda item: item[0])
    return {'available': True, 'status': 'NEAREST_DATED_EARNINGS',
            'earnings_events': len(earnings), 'dated_earnings_with_dte': len(dated_dte),
            'days_to_earnings': round(dte, 2), 'source': event.get('source'),
            'date': event.get('date'), 'read_only': True,
            'note': 'proximité issue uniquement d’un DTE de calendrier déclaré ; ni estimation ni signal d’ordre'}


__all__ = ['build']
