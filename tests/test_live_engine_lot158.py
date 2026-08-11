"""
LOT 158 — Caractérisation de la règle unique de fraîcheur du LIVE
ENGINE (`vertex/services/live_engine.py` — LE moteur de
synchronisation dont dépendent toutes les pages ; le Sync Center et
la vue Système affichent ses états).

Les 13 tests existants (`tests/test_live_engine.py`) couvrent les
flux (status/refresh/forçage/routes) ; ceux-ci figent les BORNES
EXACTES des seuils par domaine, les formats de libellés et le cycle
de forçage — les changer devient une décision explicite.
"""

import pytest

from vertex.services import live_engine as le

# Les seuils publiés par domaine : (frais, rassis) en secondes.
SEUILS = {
    'prices': (300, 1800),           # 5 min / 30 min
    'options': (3600, 6 * 3600),     # 1 h / 6 h
    'companies': (48 * 3600, 8 * 86400),
    'news': (2 * 3600, 12 * 3600),
    'calendar': (86400, 4 * 86400),
    'weekly': (8 * 86400, 15 * 86400),
    'ai': (300, 1800),
}


# ── Bornes STRICTES : à la borne exacte on bascule déjà ──────────────────────

@pytest.mark.parametrize('domaine', sorted(SEUILS))
def test_bornes_strictes_par_domaine(domaine):
    fresh, stale = SEUILS[domaine]
    assert le.calculate_freshness(fresh - 1, domaine)[0] == 'ok'
    assert le.calculate_freshness(fresh, domaine)[0] == 'stale'      # borne = déjà rassis
    assert le.calculate_freshness(stale - 1, domaine)[0] == 'stale'
    assert le.calculate_freshness(stale, domaine)[0] == 'offline'    # borne = déjà hors ligne


def test_domaine_inconnu_defauts_600_3600():
    assert le.calculate_freshness(599, 'domaine-inconnu')[0] == 'ok'
    assert le.calculate_freshness(600, 'domaine-inconnu')[0] == 'stale'
    assert le.calculate_freshness(3600, 'domaine-inconnu')[0] == 'offline'


# ── Libellés humains : unités et bascules exactes ────────────────────────────

@pytest.mark.parametrize('age,libelle', [
    (0, 'il y a 0s'), (59, 'il y a 59s'),
    (60, 'il y a 1 min'), (3599, 'il y a 59 min'),
    (3600, 'il y a 1 h'), (86399, 'il y a 23 h'),
    (86400, 'il y a 1 j'), (200000, 'il y a 2 j'),
])
def test_libelles_humains_bascules_s_min_h_j(age, libelle):
    assert le.calculate_freshness(age, 'prices')[1] == libelle


def test_age_inconnu_jamais_synchronise():
    assert le.calculate_freshness(None) == ('offline', 'jamais synchronisé')


# ── Forçage de cycle : réveil immédiat puis réarmement ───────────────────────

def test_wait_force_reveille_puis_se_rearme():
    # Un domaine forcé réveille l'attente (True) et l'événement est
    # CONSOMMÉ : la même attente redevient un timeout silencieux (False).
    le.force_event('lot158-test').set()
    assert le.wait_force('lot158-test', 0.01) is True
    assert le.wait_force('lot158-test', 0.01) is False


def test_force_event_meme_objet_par_domaine():
    # Le registre rend toujours LE même Event pour un domaine donné —
    # les boucles et le Sync Center partagent l'objet.
    assert le.force_event('lot158-bis') is le.force_event('lot158-bis')
