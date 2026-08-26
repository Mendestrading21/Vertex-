"""Vertex 1.0 — LA PREMIÈRE SÉRIE OFFICIELLE, ET SA DATE INCONNUE.

`SOURCES-APIS-OPEN-SOURCE` : « BLS API — v1 **sans clé** — CPI, emploi,
salaires et séries officielles — **adopter** ». Phase 3, critère : « backfill
point-in-time sans look-ahead ».

## Ce qui a été vérifié le 26 août 2026, en appelant vraiment

```text
POST https://api.bls.gov/publicAPI/v1/timeseries/data/
     {"seriesid": ["CUUR0000SA0"], "startyear": "2025", "endyear": "2026"}

status : REQUEST_SUCCEEDED     19 observations
{'year': '2026', 'period': 'M07', 'value': '333.918', 'latest': 'true'}
```

Sans clé, comme annoncé. Plafond documenté : 25 requêtes par jour et par
adresse — **ces bancs n'appellent donc jamais le réseau**, sinon la suite de
tests épuiserait le quota du produit.

## Le piège, visible dans la réponse elle-même

Les seules clés d'une observation sont `footnotes`, `latest`, `period`,
`periodName`, `value`, `year`. **Aucune date de publication.**

Une série macro en a pourtant deux : la période qu'elle **décrit**, et
l'instant où elle devient **connaissable**. Le CPI de juillet est publié à la
mi-août ; l'employer en juillet donnerait à un rétrotest une information que le
marché n'avait pas.

`available_at` reste donc **vide**, et `exiger_disponibilite` refuse ces
valeurs comme preuve historique. Elles restent utilisables pour décrire le
présent — c'est leur usage ici.

## Un défaut de mon propre adaptateur, trouvé en comptant

Le premier appel brut rendait **19** observations ; mon adaptateur en produisait
**18**. J'en écartais une **en silence** — précisément le défaut que ce
programme corrige partout ailleurs.

C'était octobre 2025, pour lequel BLS écrit `value: '-'` : sa façon de dire
« pas de valeur publiée ». Un mois sans CPI n'est pas un mois qu'on n'a pas
demandé, et l'écarter sans le dire ferait croire à une série continue.
"""
from __future__ import annotations

import json

import pytest

from vertex.data_sources import bls
from vertex.data_sources.macro_observation import (MacroObservation, couverture,
                                                   fin_de_periode, frequence_de)
from vertex.storage.point_in_time import DisponibiliteInconnue, exiger_disponibilite

#: La reponse REELLE du 26 aout 2026, reduite — octobre 2025 compris, avec son
#: marqueur `-`. Aucun banc n'appelle le reseau : le quota v1 est de 25/jour.
REPONSE = {
    'status': 'REQUEST_SUCCEEDED', 'message': [],
    'Results': {'series': [{'seriesID': 'CUUR0000SA0', 'data': [
        {'year': '2026', 'period': 'M07', 'periodName': 'July',
         'value': '333.918', 'latest': 'true', 'footnotes': [{}]},
        {'year': '2026', 'period': 'M06', 'periodName': 'June',
         'value': '333.952', 'footnotes': [{}]},
        {'year': '2025', 'period': 'M10', 'periodName': 'October',
         'value': '-', 'footnotes': [{}]},
    ]}]},
}


@pytest.fixture(autouse=True)
def _isole(monkeypatch):
    """Drapeau posé, cache vide, réseau coupé — un banc ne consomme jamais le
    quota réel."""
    monkeypatch.setenv(bls.DRAPEAU, '1')
    bls.vider_cache()
    monkeypatch.setattr(bls, '_appeler', lambda ids, d, f: json.loads(json.dumps(REPONSE)))
    yield
    bls.vider_cache()


#  ═══════════  1. la période décrite, datée à sa FIN  ═════════════════════════

@pytest.mark.parametrize('annee,periode,attendu', [
    (2026, 'M07', '2026-07-31'),
    (2026, 'M02', '2026-02-28'),
    (2024, 'M02', '2024-02-29'),      # bissextile
    (2026, 'Q2', '2026-06-30'),
    (2026, 'M13', '2026-12-31'),      # moyenne annuelle BLS
    (2026, 'A01', '2026-12-31'),
])
def test_une_periode_est_datee_a_sa_FIN(annee, periode, attendu):
    """Une statistique mensuelle décrit le mois **entier** : la dater au 1er
    laisserait croire qu'elle décrivait déjà le mois à son premier jour."""
    assert fin_de_periode(annee, periode) == attendu


@pytest.mark.parametrize('annee,periode', [
    (2026, 'M00'), (2026, 'M14'), (2026, 'Z9'), (2026, ''), ('x', 'M01'),
])
def test_une_periode_ILLISIBLE_n_est_pas_datee_au_hasard(annee, periode):
    assert fin_de_periode(annee, periode) == ''


def test_la_frequence_est_LUE_et_non_supposee():
    assert frequence_de('M07') == 'M' and frequence_de('Q2') == 'Q'
    assert frequence_de('A01') == 'A' and frequence_de('X9') == ''


#  ═══════════  2. `available_at` reste INCONNU, et le refus tient  ════════════

def test_aucune_observation_ne_porte_une_date_de_DISPONIBILITE():
    """L'API v1 ne la fournit pas. La remplir avec l'instant de réception —
    l'erreur naturelle — ferait croire qu'une statistique publiée à la mi-août
    était lisible fin juillet."""
    r = bls.observations('CUUR0000SA0')
    assert r['observations']
    for o in r['observations']:
        assert o.available_at == ''
        assert o.disponibilite_connue is False


def test_ces_valeurs_sont_REFUSEES_comme_preuve_historique():
    """Le critère de la Phase 3 rendu impossible, pas seulement recommandé."""
    o = bls.observations('CUUR0000SA0')['observations'][0]
    with pytest.raises(DisponibiliteInconnue):
        exiger_disponibilite(o, contexte='retrotest CPI')


def test_la_couverture_COMPTE_les_observations_sans_disponibilite():
    """« Certaines » n'aide personne à décider. Un nombre, si."""
    c = couverture(bls.observations('CUUR0000SA0')['observations'])
    assert c['observations'] == c['sans_date_de_disponibilite'] == 2
    assert c['utilisable_comme_preuve_historique'] is False


def test_une_observation_DATEE_serait_acceptee():
    """Contre-épreuve : le refus doit venir de l'absence de date, pas d'un rejet
    systématique — sinon aucune source ne pourrait jamais servir de preuve."""
    o = MacroObservation(series_id='X', valeur=1.0, unite='%', frequence='M',
                         observed_at='2026-07-31', available_at='2026-08-12T12:30:00Z',
                         provider='TEST')
    assert exiger_disponibilite(o, contexte='test') is o
    assert couverture([o])['utilisable_comme_preuve_historique'] is True


#  ═══════════  3. la période sans valeur est NOMMÉE  ══════════════════════════

def test_une_periode_SANS_valeur_publiee_est_nommee():
    """Le défaut de mon propre adaptateur : 19 brut → 18 servies, une écartée
    en silence. BLS écrit `-` pour dire « pas de valeur »."""
    r = bls.observations('CUUR0000SA0')
    assert len(r['observations']) == 2
    assert len(r['manquantes']) == 1
    m = r['manquantes'][0]
    assert m['periode'] == '2025M10'
    assert m['marqueur_source'] == '-'
    assert 'non publiee' in m['motif']
    assert m['observed_at'] == '2025-10-31'


def test_une_serie_COMPLETE_ne_declare_aucune_manquante():
    """Contre-épreuve : une liste toujours non vide ne mesurerait rien."""
    complet = json.loads(json.dumps(REPONSE))
    complet['Results']['series'][0]['data'] = \
        complet['Results']['series'][0]['data'][:2]
    bls._appeler = lambda ids, d, f: complet
    bls.vider_cache()
    assert bls.observations('CUUR0000SA0')['manquantes'] == []


def test_le_CACHE_rend_aussi_les_manquantes():
    """Sinon la série paraîtrait continue dès le second appel — le trou
    disparaîtrait au bout de quelques secondes."""
    bls.observations('CUUR0000SA0')
    second = bls.observations('CUUR0000SA0')
    assert second['depuis_cache'] is True
    assert len(second['manquantes']) == 1


#  ═══════════  4. drapeau, quota, timeout — la source ne s'impose pas  ════════

def test_SANS_drapeau_la_source_ne_fait_RIEN(monkeypatch):
    """Une source officielle n'entre pas en service par surprise."""
    monkeypatch.delenv(bls.DRAPEAU, raising=False)
    r = bls.observations('CUUR0000SA0')
    assert r['observations'] == []
    assert 'desactivee' in r['erreur']


def test_une_serie_INCONNUE_est_refusee_sans_appel():
    r = bls.observations('SERIE_QUI_N_EXISTE_PAS')
    assert r['observations'] == [] and 'inconnue' in r['erreur']


def test_le_quota_EPUISE_ne_fabrique_aucune_donnee(monkeypatch):
    """Dépasser le plafond ferait bannir l'adresse : le repli serait alors une
    absence totale, pas une dégradation."""
    monkeypatch.setattr(bls, 'MAX_APPELS_JOUR', 1)
    bls.observations('CUUR0000SA0', force=True)
    r = bls.observations('CUUR0000SA0', force=True)
    assert 'quota' in r['erreur']
    #  Le cache perime est servi, mais SIGNALE.
    assert r.get('perime') is True and r['depuis_cache'] is True


def test_un_ECHEC_reseau_ne_rend_pas_une_liste_vide_muette(monkeypatch):
    def _tombe(ids, d, f):
        raise OSError('reseau coupe')
    monkeypatch.setattr(bls, '_appeler', _tombe)
    bls.vider_cache()
    r = bls.observations('CUUR0000SA0')
    assert r['observations'] == []
    assert 'reseau coupe' in r['erreur']


def test_un_statut_d_ERREUR_de_BLS_est_rapporte(monkeypatch):
    monkeypatch.setattr(bls, '_appeler', lambda i, d, f: {
        'status': 'REQUEST_NOT_PROCESSED', 'message': ['quota depasse']})
    bls.vider_cache()
    r = bls.observations('CUUR0000SA0')
    assert 'quota depasse' in r['erreur']


def test_l_etat_DIT_que_la_date_de_publication_manque():
    """Une surface doit pouvoir distinguer « source muette » de « source qui ne
    sait pas dater »."""
    e = bls.etat()
    assert e['cle_requise'] is False
    assert e['date_de_publication_fournie'] is False
    assert e['plafond_24h'] == bls.MAX_APPELS_JOUR
    assert 'CUUR0000SA0' in e['series_connues']


#  ═══════════  5. l'unité n'est pas devinée  ══════════════════════════════════

def test_l_unite_du_CPI_est_un_INDICE_et_non_un_pourcentage():
    """`333.918` affiché avec un `%` inventerait une inflation de 333 %."""
    o = bls.observations('CUUR0000SA0')['observations'][0]
    assert 'indice' in o.unite and '%' not in o.unite
    assert bls.SERIES['LNS14000000']['unite'] == '%'


def test_chaque_observation_porte_son_IDENTIFIANT_de_source():
    """Sans lui, deux ingestions du même fait seraient indiscernables."""
    o = bls.observations('CUUR0000SA0')['observations'][0]
    assert o.provider == 'BLS_v1'
    assert o.provider_record_id == 'CUUR0000SA0:2026M07'
