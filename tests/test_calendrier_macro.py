"""Vertex Test 1.0 — LE CALENDRIER MACRO EXPIRAIT EN SILENCE, ET SE DISAIT CERTAIN.

`VERTEX-INTELLIGENCE-2.0`, Phase 3, critère d'acceptation, mot pour mot :

> `macro_calendar.py` ne crée plus de date exacte depuis une règle approximative.

## Les trois défauts, mesurés le 26 août 2026

**1. L'expiration silencieuse.** `FOMC_2026` s'arrêtait au 9 décembre 2026 :

```text
depuis 2026-08-26, horizon 365 j : FOMC  3   NFP 12   CPI 12
depuis 2026-12-20, horizon 365 j : FOMC  0   NFP 12   CPI 12
depuis 2027-06-01, horizon 365 j : FOMC  0   NFP 12   CPI 12
```

**Zéro réunion de la Fed sur un an**, servi sans un mot, à côté de vingt-quatre
autres événements qui continuaient d'arriver. Un lecteur en conclut qu'il n'y a
pas de FOMC — pas que le calendrier s'est tu. Et l'échéance était à trois mois
et demi.

Le bloc de couverture d'`analysis_api` disait `MACRO_CALENDAR_AVAILABLE` avec
`events_loaded > 0` : **disponible** et **complet** étaient confondus.

**2. Le NFP se disait CERTAIN.** `approx: False` sur une date produite par
`_first_friday` — une **règle**, pas le calendrier officiel du BLS, que Vertex
ne consulte pas. Une règle peut coïncider avec la publication ; elle ne peut
pas en porter la certitude.

**3. Le CPI fabriquait le 13.** Marqué approximatif — honnête — mais le champ
`date` reste une date ISO précise, et un consommateur qui ignore `approx`
affiche une fausse précision. Une seule surface honorait `approx`.

## Ce que ce lot ne fait pas

Il n'ajoute **aucun appel réseau**. Les dates officielles BLS et Fed viendraient
d'un flux à contractualiser — licence, replay, point-in-time — c'est la suite de
la Phase 3. Ici on cesse de **prétendre** ; on ne prétend pas non plus avoir la
source.
"""
from __future__ import annotations

from datetime import date, timedelta

import pytest

from vertex.data import macro_calendar as M


#  ═══════════  1. `approx` DÉCOULE de la source  ══════════════════════════════

def test_une_date_issue_d_une_REGLE_ne_peut_pas_etre_certaine():
    """Le critère d'acceptation, littéralement."""
    for e in M.events(horizon_days=200, today=date(2026, 8, 26)):
        if e['source'] == M.SOURCE_REGLE:
            assert e['approx'] is True, e


def test_le_NFP_ne_se_dit_PLUS_certain():
    """Le défaut nommé : `approx: False` sur `_premier_vendredi`."""
    nfp = [e for e in M.events(horizon_days=120, today=date(2026, 8, 26))
           if e['kind'] == 'NFP']
    assert nfp, 'aucun NFP : la mesure porterait sur rien'
    assert all(e['approx'] is True for e in nfp)
    assert all(e['source'] == M.SOURCE_REGLE for e in nfp)


def test_le_FOMC_PUBLIE_reste_certain():
    """Contre-épreuve : tout marquer approximatif ne distinguerait plus rien,
    et une date réellement publiée perdrait sa valeur."""
    fomc = [e for e in M.events(horizon_days=120, today=date(2026, 8, 26))
            if e['kind'] == 'FOMC']
    assert fomc
    assert all(e['approx'] is False and e['source'] == M.SOURCE_FED for e in fomc)


def test_approx_n_est_JAMAIS_recopie_a_la_main():
    """Un `approx` posé par l'appelant finit par diverger de la source qu'il
    décrit — c'est le défaut de D-084, payé trois fois. La table l'impose."""
    assert M._APPROX_PAR_SOURCE == {M.SOURCE_FED: False, M.SOURCE_REGLE: True}
    for e in M.events(horizon_days=200, today=date(2026, 8, 26)):
        assert e['approx'] is M._APPROX_PAR_SOURCE[e['source']], e


def test_chaque_evenement_NOMME_sa_source():
    for e in M.events(horizon_days=200, today=date(2026, 8, 26)):
        assert e['source'] in (M.SOURCE_FED, M.SOURCE_REGLE), e


#  ═══════════  2. l'expiration se voit  ═══════════════════════════════════════

def test_l_horizon_qui_DEPASSE_le_calendrier_publie_le_DIT():
    """Le défaut le plus grave : une absence silencieuse se lit comme une
    absence de réunion."""
    ev = M.events(horizon_days=365, today=date(2026, 8, 26))
    alerte = [e for e in ev if e['kind'] == 'COUVERTURE']
    assert alerte, 'horizon de 365 j au-dela du 2026-12-09, et rien ne le dit'
    assert M.DERNIERE_DATE_PUBLIEE.isoformat() in alerte[0]['label']
    assert 'absence de donnée' in alerte[0]['note']


def test_un_calendrier_EPUISE_ne_rend_pas_un_silence():
    """Après le 9 décembre 2026, plus aucune date FOMC n'est connue. Le produit
    doit le dire, pas rendre douze NFP et zéro Fed."""
    for jour in (date(2026, 12, 20), date(2027, 6, 1)):
        ev = M.events(horizon_days=365, today=jour)
        assert not [e for e in ev if e['kind'] == 'FOMC']
        assert [e for e in ev if e['kind'] == 'COUVERTURE'], jour
        assert M.couverture(365, jour)['fomc_epuise'] is True


def test_un_horizon_COUVERT_ne_declenche_AUCUNE_alerte():
    """Contre-épreuve : un avertissement présent en toute circonstance ne
    distingue plus rien et finit ignoré (D-088)."""
    ev = M.events(horizon_days=30, today=date(2026, 8, 26))
    assert not [e for e in ev if e['kind'] == 'COUVERTURE']
    assert M.couverture(30, date(2026, 8, 26))['fomc_horizon_depasse'] is False


def test_la_couverture_COMPTE_les_jours_non_couverts():
    """« Il manque quelque chose » n'informe pas. « 260 jours » se vérifie."""
    c = M.couverture(365, date(2026, 8, 26))
    attendu = (date(2026, 8, 26) + timedelta(days=365) - M.DERNIERE_DATE_PUBLIEE).days
    assert c['fomc_jours_non_couverts'] == attendu > 0
    assert c['fomc_publie_jusqu_a'] == '2026-12-09'


def test_la_couverture_dit_qu_elle_ne_LIT_aucun_calendrier_BLS():
    """Ne pas prétendre avoir la source est la moitié du travail ; le dire est
    l'autre moitié."""
    c = M.couverture(120, date(2026, 8, 26))
    assert c['reseau'] is False
    assert 'calendrier officiel' in c['note']
    assert M.SOURCE_REGLE in c['sources'] and M.SOURCE_FED in c['sources']


#  ═══════════  3. le contrat existant survit  ═════════════════════════════════

def test_les_champs_HISTORIQUES_sont_tous_conserves():
    """Une correction qui casse ses consommateurs n'est pas une correction."""
    for e in M.events(horizon_days=120, today=date(2026, 8, 26)):
        for cle in ('kind', 'date', 'label', 'importance', 'approx', 'note', 'dte'):
            assert cle in e, (cle, e)


def test_le_nom_historique_FOMC_2026_reste_lisible():
    assert M.FOMC_2026 == M.FOMC_PUBLIE


def test_les_evenements_restent_TRIES_et_dans_l_horizon():
    aujourd = date(2026, 8, 26)
    ev = M.events(horizon_days=120, today=aujourd)
    dates = [e['date'] for e in ev]
    assert dates == sorted(dates)
    for e in ev:
        d = date.fromisoformat(e['date'])
        assert aujourd <= d <= aujourd + timedelta(days=120), e
        assert e['dte'] == (d - aujourd).days


def test_un_horizon_nul_ne_fait_pas_tomber_le_calendrier():
    assert isinstance(M.events(horizon_days=0, today=date(2026, 8, 26)), list)


#  ═══════════  4. les routes servent la couverture  ═══════════════════════════

@pytest.fixture()
def client(tmp_path, monkeypatch):
    import os
    os.environ.setdefault('NO_IBKR', '1')
    os.environ.setdefault('START_ON_IMPORT', '0')
    from vertex.services import persist
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    from vertex.strategy.release import activate_release_profile
    activate_release_profile()
    import terminal
    return terminal.app.test_client()


def test_la_route_calendrier_SERT_la_couverture(client):
    r = client.get('/cal-feed')
    assert r.status_code == 200
    c = r.get_json().get('macro_couverture')
    assert c and 'fomc_publie_jusqu_a' in c


def test_le_statut_distingue_DISPONIBLE_de_COMPLET():
    """`MACRO_CALENDAR_AVAILABLE` avec `events_loaded > 0` ne disait rien de la
    complétude : c'est ce qui rendait l'expiration invisible."""
    import pathlib
    src = (pathlib.Path(__file__).resolve().parents[1] / 'vertex' / 'app'
           / 'routes' / 'analysis_api.py').read_text(encoding='utf-8')
    assert 'MACRO_CALENDAR_PARTIAL' in src
    i = src.index('MACRO_CALENDAR_PARTIAL')
    assert 'couverture' in src[max(0, i - 400):i + 400]
