"""
LOT 159 — Complément de caractérisation de l'horloge de marché US
(`vertex/services/market_clock.py`).

Les 4 tests existants (`tests/test_market_clock.py`) couvrent les
frontières 9h30/16h/20h et le week-end ; ceux-ci figent les lacunes :
la borne pré-marché 4h00, le format du champ `et`, la fin de semaine
du vendredi soir, et une LIMITE documentée — pas de calendrier de
jours fériés. Heures injectées (déterministe).
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from vertex.services import market_clock as mc

_ET = ZoneInfo('America/New_York')


def _et(y, m, d, hh, mm):
    return datetime(y, m, d, hh, mm, tzinfo=_ET)


def test_borne_pre_marche_4h00_exacte():
    # 2026-07-06 est un lundi : 3h59 fermé, 4h00 pile → pré-marché.
    assert mc.session_of(_et(2026, 7, 6, 3, 59)) == 'closed'
    assert mc.session_of(_et(2026, 7, 6, 4, 0)) == 'pre'


def test_vendredi_soir_apres_bourse_puis_ferme_tout_le_weekend():
    # Vendredi 2026-07-10 : 19h59 encore after, 20h00 fermé — et le
    # marché ne rouvre plus avant lundi.
    assert mc.session_of(_et(2026, 7, 10, 19, 59)) == 'after'
    assert mc.session_of(_et(2026, 7, 10, 20, 0)) == 'closed'
    assert mc.session_of(_et(2026, 7, 11, 10, 0)) == 'closed'   # samedi en pleine « séance »


def test_format_heure_et_zero_padde():
    st = mc.market_status(now=_et(2026, 7, 6, 9, 5))
    assert st['et'] == '09:05 ET'         # HH:MM zéro-paddé + suffixe ET
    assert st['session'] == 'pre' and st['open'] is False


def test_jours_feries_non_geres_limite_documentee():
    # LIMITE DOCUMENTÉE : l'horloge ne connaît QUE l'heure et le jour de
    # semaine — pas de calendrier de jours fériés. Le 1er janvier 2026
    # (un jeudi) est donc affiché « open » à midi. Ajouter un calendrier
    # NYSE = décision explicite future ; ce test rendra le changement
    # visible.
    assert mc.session_of(_et(2026, 1, 1, 12, 0)) == 'open'


def test_contrat_market_status():
    st = mc.market_status(now=_et(2026, 7, 6, 12, 0))
    assert set(st) == {'open', 'session', 'et'}
    assert st['open'] is True and st['session'] == 'open'
