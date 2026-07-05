"""
tests/test_market_clock.py — Horloge de marché US (phases de séance).

Heure injectable → test déterministe des frontières pré / séance / après / fermé.
"""

from datetime import datetime
from zoneinfo import ZoneInfo
from vertex.services import market_clock as mc

_ET = ZoneInfo('America/New_York')


def _et(y, m, d, hh, mm):
    return datetime(y, m, d, hh, mm, tzinfo=_ET)


def test_session_boundaries_on_a_weekday():
    # 2026-07-06 est un lundi
    assert mc.session_of(_et(2026, 7, 6, 8, 0)) == 'pre'
    assert mc.session_of(_et(2026, 7, 6, 9, 29)) == 'pre'
    assert mc.session_of(_et(2026, 7, 6, 9, 30)) == 'open'
    assert mc.session_of(_et(2026, 7, 6, 15, 59)) == 'open'
    assert mc.session_of(_et(2026, 7, 6, 16, 0)) == 'after'
    assert mc.session_of(_et(2026, 7, 6, 19, 59)) == 'after'
    assert mc.session_of(_et(2026, 7, 6, 20, 0)) == 'closed'
    assert mc.session_of(_et(2026, 7, 6, 3, 0)) == 'closed'


def test_weekend_is_closed():
    # 2026-07-04 samedi, 2026-07-05 dimanche
    assert mc.session_of(_et(2026, 7, 4, 12, 0)) == 'closed'
    assert mc.session_of(_et(2026, 7, 5, 12, 0)) == 'closed'


def test_market_status_shape_and_open_flag():
    st = mc.market_status(now=_et(2026, 7, 6, 10, 0))
    assert st['open'] is True and st['session'] == 'open'
    assert 'ET' in st['et']
    closed = mc.market_status(now=_et(2026, 7, 6, 22, 0))
    assert closed['open'] is False and closed['session'] == 'closed'


def test_terminal_uses_the_module():
    import terminal
    assert terminal.market_status is mc.market_status
