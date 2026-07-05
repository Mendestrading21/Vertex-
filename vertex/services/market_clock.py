"""
vertex/services/market_clock.py — HORLOGE DE MARCHÉ US (Ch. II).

Détermine la phase de séance à New York. Pur (dépend de l'heure), sans état
applicatif : extrait du monolithe pour être testable en injectant l'heure.

Phases : pré-marché 4h–9h30 · séance 9h30–16h · après-bourse 16h–20h · sinon fermé.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

_OPEN, _CLOSE = 570, 960          # 9:30 et 16:00 en minutes
_PRE_OPEN, _AFTER_CLOSE = 240, 1200   # 4:00 et 20:00


def session_of(et):
    """Phase de séance pour un datetime ET donné (testable sans horloge réelle)."""
    t = et.hour * 60 + et.minute
    weekday = et.weekday() < 5
    if weekday and _OPEN <= t < _CLOSE:
        return 'open'
    if weekday and _PRE_OPEN <= t < _OPEN:
        return 'pre'
    if weekday and _CLOSE <= t < _AFTER_CLOSE:
        return 'after'
    return 'closed'


def market_status(now=None):
    """État du marché US. `now` (datetime ET) injectable pour les tests."""
    try:
        et = now or datetime.now(ZoneInfo('America/New_York'))
        session = session_of(et)
        return {'open': session == 'open', 'session': session,
                'et': et.strftime('%H:%M ET')}
    except Exception:
        return {'open': False, 'session': 'closed', 'et': '—'}


__all__ = ['market_status', 'session_of']
