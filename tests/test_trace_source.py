"""tests/test_trace_source.py — LOT 14 (vérif phase D) : fuite de jeton interne.

Mesuré au navigateur (390 px, scan sans contributeur) : l'étape DONNÉE de la
DecisionTrace affichait « unavailable » — le jeton interne anglais de
terminal.py:515 rendu BRUT. Né ROUGE.
"""
from vertex.ui.pages.briefing import _trace_aujourdhui


def test_le_jeton_interne_unavailable_ne_fuit_jamais():
    html = _trace_aujourdhui({'source': 'unavailable'})
    assert 'unavailable' not in html
    assert 'Aucune source' in html
    #  distinct d'un scan jamais servi : ici le scan a TOURNÉ, aucune source n'a répondu
    assert 'répondu' in html


def test_scan_jamais_servi_reste_distinct():
    html = _trace_aujourdhui({})
    assert 'aucun scan servi' in html
    assert 'unavailable' not in html


def test_une_vraie_source_reste_affichee():
    html = _trace_aujourdhui({'source': 'yfinance+stooq', 'scan_ts_h': '12:00'})
    assert 'yfinance+stooq' in html
