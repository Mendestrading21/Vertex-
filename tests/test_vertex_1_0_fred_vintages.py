"""Vertex 1.0 — LE MÊME MOIS, TROIS CHIFFRES.

`SOURCES-APIS-OPEN-SOURCE` : « FRED — clé gratuite — **adopter** […] FRED
fournit la profondeur historique et les **vintages** ».

## Ce qui a été vérifié le 26 août 2026, avec une vraie clé

Emplois non agricoles (`PAYEMS`), mois de **mai 2026**, toutes ses versions
successives :

```text
connue du 2026-06-05 au 2026-07-01 : 159 001
connue du 2026-07-02 au 2026-08-06 : 158 927
connue du 2026-08-07 a aujourd'hui : 158 861
```

**Révisé deux fois, de 140 000 emplois.** Un rétrotest qui daterait `158 861`
à mai emploierait un nombre qui **n'existait pas avant le 7 août** — du
look-ahead pur, sur la statistique la plus regardée du calendrier américain.

## Ce que FRED apporte et que BLS v1 n'a pas

`realtime_start` est exactement l'`available_at` que D-132 laissait vide faute
de source. Ces observations peuvent donc **fonder une preuve historique** — et
`exiger_disponibilite` les accepte, contrairement à celles de BLS v1.

## La précision qu'il ne faut pas s'attribuer

Sans `as_of`, FRED rend la fenêtre temps-réel **courante** : `realtime_start`
vaut la date d'interrogation, pas la date de première publication. C'est une
**borne supérieure**.

L'erreur va dans le sens sûr — un rétrotest ignore une donnée qu'il aurait pu
employer, jamais l'inverse. Mais la présenter comme exacte serait une fausse
précision, et c'est le défaut que ce programme corrige depuis D-084. D'où
`quality = 'BORNE_SUPERIEURE'` par défaut, et `'MEASURED'` sur un vintage.

## Aucun banc n'appelle le réseau

Ni la clé. Un test qui dépendrait d'une clé d'API échouerait chez qui ne l'a
pas, et un test qui appelle le réseau mesure la connexion, pas le code.
"""
from __future__ import annotations

import pytest

from vertex.data_sources import fred
from vertex.storage.point_in_time import DisponibiliteInconnue, exiger_disponibilite

#: Reponses REELLES du 26 aout 2026, reduites.
OBS_SIMPLE = {'observations': [
    {'realtime_start': '2026-08-26', 'realtime_end': '2026-08-26',
     'date': '2026-08-24', 'value': '4.7'},
    {'realtime_start': '2026-08-26', 'realtime_end': '2026-08-26',
     'date': '2026-08-21', 'value': '4.7400000000'},
    {'realtime_start': '2026-08-26', 'realtime_end': '2026-08-26',
     'date': '2026-08-20', 'value': '.'},          # absence PUBLIEE par FRED
]}

VINTAGES_PAYEMS = {'observations': [
    {'realtime_start': '2026-06-05', 'realtime_end': '2026-07-01',
     'date': '2026-05-01', 'value': '159001'},
    {'realtime_start': '2026-07-02', 'realtime_end': '2026-08-06',
     'date': '2026-05-01', 'value': '158927'},
    {'realtime_start': '2026-08-07', 'realtime_end': '9999-12-31',
     'date': '2026-05-01', 'value': '158861'},
]}


@pytest.fixture(autouse=True)
def _isole(monkeypatch):
    """Drapeau et clé factices, cache vide, réseau coupé. Un banc qui
    dépendrait d'une vraie clé échouerait chez qui ne l'a pas."""
    monkeypatch.setenv(fred.DRAPEAU, '1')
    monkeypatch.setenv(fred.VAR_CLE, 'cle-de-test-sans-valeur')
    fred.vider_cache()
    yield
    fred.vider_cache()


def _repondre(monkeypatch, charge):
    monkeypatch.setattr(fred, '_appeler', lambda p: charge)


#  ═══════════  1. la date de disponibilité est enfin là  ══════════════════════

def test_chaque_observation_porte_une_date_de_DISPONIBILITE(monkeypatch):
    """Ce que D-132 laissait vide faute de source."""
    _repondre(monkeypatch, OBS_SIMPLE)
    r = fred.observations('DGS10')
    assert r['observations']
    for o in r['observations']:
        assert o.available_at == '2026-08-26'
        assert o.disponibilite_connue is True


def test_ces_observations_sont_ACCEPTEES_comme_preuve_historique(monkeypatch):
    """La différence avec BLS v1 : une source datée contre une source qui ne
    décrit que le présent."""
    _repondre(monkeypatch, OBS_SIMPLE)
    o = fred.observations('DGS10')['observations'][0]
    assert exiger_disponibilite(o, contexte='retrotest') is o


def test_une_observation_BLS_reste_refusee():
    """Contre-épreuve croisée : le refus de D-132 tient toujours, sinon ce lot
    aurait affaibli la garde au lieu de la compléter."""
    from vertex.data_sources.macro_observation import MacroObservation
    sans = MacroObservation(series_id='CUUR0000SA0', valeur=1.0, unite='x',
                            frequence='M', observed_at='2026-07-31',
                            available_at='', provider='BLS_v1')
    with pytest.raises(DisponibiliteInconnue):
        exiger_disponibilite(sans, contexte='retrotest')


#  ═══════════  2. la précision qu'on ne s'attribue pas  ══════════════════════

def test_sans_as_of_la_disponibilite_est_une_BORNE_SUPERIEURE(monkeypatch):
    """`realtime_start` vaut alors la date d'interrogation. La présenter comme
    exacte serait une fausse précision (D-084)."""
    _repondre(monkeypatch, OBS_SIMPLE)
    o = fred.observations('DGS10')['observations'][0]
    assert o.quality == fred.QUALITE_BORNE
    assert o.notes and 'BORNE SUPERIEURE' in o.notes[0]


def test_un_VINTAGE_donne_la_premiere_publication_exacte(monkeypatch):
    """C'est ce que la requête de vintage demande explicitement."""
    _repondre(monkeypatch, VINTAGES_PAYEMS)
    v = fred.vintages('PAYEMS', '2026-05-01')['versions']
    assert v[0].quality == 'MEASURED'
    assert v[0].available_at == '2026-06-05'


def test_l_etat_DECLARE_la_nature_de_la_disponibilite_par_defaut():
    e = fred.etat()
    assert e['vintages'] is True
    assert e['available_at_par_defaut'] == fred.QUALITE_BORNE
    assert e['date_de_publication_fournie'] is True


#  ═══════════  3. les révisions, mesurées  ════════════════════════════════════

def test_les_TROIS_versions_de_mai_2026_sont_rendues(monkeypatch):
    """Le cœur du lot : le même mois, trois chiffres."""
    _repondre(monkeypatch, VINTAGES_PAYEMS)
    r = fred.vintages('PAYEMS', '2026-05-01')
    assert r['revisions'] == 2
    assert [v.valeur for v in r['versions']] == [159001.0, 158927.0, 158861.0]


def test_chaque_version_porte_son_RANG_et_la_precedente(monkeypatch):
    """Sans la précédente, on voit un chiffre ; avec elle, on voit une
    révision — et c'est la révision qui informe."""
    _repondre(monkeypatch, VINTAGES_PAYEMS)
    v = fred.vintages('PAYEMS', '2026-05-01')['versions']
    #  `revision` est 0-INDEXE : 0 = publication d'origine, pas encore revisee.
    #  Mon banc affirmait 1,2,3 ; le module documentait « 0 pour la premiere »,
    #  et c'est lui qui a raison — une revision 1 sur une valeur jamais revisee
    #  se lirait comme une correction qui n'a pas eu lieu.
    assert [x.revision for x in v] == [0, 1, 2]
    assert v[0].precedente is None, 'la premiere version ne remplace rien'
    assert v[1].precedente == 159001.0
    assert v[2].precedente == 158927.0


def test_une_serie_JAMAIS_revisee_rend_une_seule_version(monkeypatch):
    """Contre-épreuve : si tout ressortait multi-versions, le compte ne
    mesurerait rien."""
    _repondre(monkeypatch, {'observations': [VINTAGES_PAYEMS['observations'][0]]})
    r = fred.vintages('PAYEMS', '2026-05-01')
    assert r['revisions'] == 0 and len(r['versions']) == 1


def test_chaque_observation_porte_un_IDENTIFIANT_qui_inclut_le_vintage(monkeypatch):
    """Deux versions du même mois sont deux faits distincts : un identifiant
    qui ne porterait que la date les confondrait."""
    _repondre(monkeypatch, VINTAGES_PAYEMS)
    v = fred.vintages('PAYEMS', '2026-05-01')['versions']
    ids = {x.provider_record_id for x in v}
    assert len(ids) == 3
    assert 'PAYEMS:2026-05-01@2026-06-05' in ids


#  ═══════════  4. l'absence publiée est nommée  ═══════════════════════════════

def test_le_marqueur_POINT_de_FRED_est_nomme_et_non_jete(monkeypatch):
    """FRED écrit `.` pour une période sans valeur — un jour férié sur une
    série quotidienne. Ce n'est ni zéro ni une erreur : c'est une absence."""
    _repondre(monkeypatch, OBS_SIMPLE)
    r = fred.observations('DGS10')
    assert len(r['observations']) == 2
    assert len(r['manquantes']) == 1
    assert r['manquantes'][0]['observed_at'] == '2026-08-20'
    assert r['manquantes'][0]['marqueur_source'] == '.'


def test_une_serie_COMPLETE_ne_declare_aucune_manquante(monkeypatch):
    _repondre(monkeypatch, {'observations': OBS_SIMPLE['observations'][:2]})
    assert fred.observations('DGS10')['manquantes'] == []


#  ═══════════  5. drapeau, clé, quota — la source ne s'impose pas  ════════════

def test_SANS_drapeau_la_source_ne_fait_RIEN(monkeypatch):
    monkeypatch.delenv(fred.DRAPEAU, raising=False)
    r = fred.observations('DGS10')
    assert r['observations'] == [] and r['erreur']


def test_SANS_cle_la_source_ne_pretend_pas_etre_active(monkeypatch):
    """Une source activée sans clé échouerait à chaque appel, et l'échec
    passerait pour une panne de FRED."""
    monkeypatch.setenv(fred.VAR_CLE, '')
    assert fred.active() is False
    r = fred.observations('DGS10')
    assert 'cle' in r['erreur'].lower()


def test_une_serie_INCONNUE_est_refusee_sans_appel():
    r = fred.observations('SERIE_INEXISTANTE')
    assert r['observations'] == [] and 'inconnue' in r['erreur']


def test_le_quota_atteint_ne_fabrique_aucune_donnee(monkeypatch):
    monkeypatch.setattr(fred, 'MAX_APPELS_MINUTE', 1)
    _repondre(monkeypatch, OBS_SIMPLE)
    fred.observations('DGS10', force=True)
    r = fred.observations('DGS10', force=True)
    assert r['observations'] == [] and 'quota' in r['erreur']


def test_un_ECHEC_reseau_ne_rend_pas_une_liste_vide_muette(monkeypatch):
    def _tombe(p):
        raise OSError('reseau coupe')
    monkeypatch.setattr(fred, '_appeler', _tombe)
    r = fred.observations('DGS10')
    assert r['observations'] == [] and 'reseau coupe' in r['erreur']


#  ═══════════  6. l'unité n'est pas devinée  ══════════════════════════════════

def test_chaque_serie_declare_son_unite_REELLE():
    """`DGS10` est un pourcentage, `PAYEMS` un nombre en milliers. Les
    confondre afficherait 158 861 % de chômage."""
    assert fred.SERIES['DGS10']['unite'] == '%'
    assert fred.SERIES['PAYEMS']['unite'] == 'milliers'
    assert 'indice' in fred.SERIES['CPIAUCSL']['unite']
    for sid, meta in fred.SERIES.items():
        assert meta['unite'] and meta['libelle'] and meta['frequence'], sid
