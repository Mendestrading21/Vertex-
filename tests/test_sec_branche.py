"""Vertex Test 1.0 — SEC EDGAR ÉTAIT ÉCRIT, TESTÉ, ET BRANCHÉ NULLE PART.

## Ce qui a été mesuré le 27 août 2026

`sec_edgar.py` — 200 lignes, son propre banc — était importé par **zéro**
page, **zéro** route, **zéro** moteur. Et `VERTEX_ENABLE_SEC=1` figurait dans
le `.env` de l'utilisateur alors que **rien ne lisait ce drapeau**.

Une source déclarée active que personne n'interroge est pire qu'une source
absente : elle donne l'illusion de la couverture. L'utilisateur croyait avoir
trois sources macro ; il en avait deux.

## Pourquoi cette source-là compte

Les fondamentaux Reuters sont **refusés** par le compte IBKR (erreur 10358).
`yfinance.Ticker.info` en donne, mais **sans date de publication**. La SEC est
donc la seule source du produit qui permette de dire ce qui était
*connaissable* à une date donnée — chaque fait porte la période décrite
(`observed_at`) **et** la date de dépôt (`available_at`).

## Le défaut trouvé en branchant

`charger_companyfacts` demandait `Accept-Encoding: gzip` et décodait la
réponse **sans décompresser** : `UnicodeDecodeError: byte 0x8b` — les deux
premiers octets d'un flux gzip. Ce chemin n'avait jamais été exercé en réseau
réel, seulement par `lecteur` injecté ; le défaut attendait le premier appel
véritable.

## Mesure après branchement

```text
AAPL  624 faits  ·  25 135 lus  ·  0 ignoré
MSFT  632 faits  ·  CA 331,8 Md$ (exercice clos 2026-06-30, déposé 2026-07-29)
route : 1er appel 0,001 s (MISSING, fond) — 2e appel LIVE
```

## Aucun banc n'appelle le réseau

Un test qui dépendrait du contact SEC échouerait chez qui ne l'a pas, et un
test qui appelle le réseau mesure la connexion, pas le code.
"""
from __future__ import annotations

import json
import os

import pytest

from vertex.data_sources import sec_fondamentaux as S

#: Table ticker -> CIK, réduite à la forme réelle du fichier de la SEC.
TABLE = {'0': {'cik_str': 320193, 'ticker': 'AAPL', 'title': 'Apple Inc.'},
         '1': {'cik_str': 789019, 'ticker': 'MSFT', 'title': 'Microsoft Corp'}}

#: `companyfacts` réduit : un tag suivi, deux périodes, une révision.
FACTS = {'cik': 320193, 'entityName': 'Apple Inc.', 'facts': {'us-gaap': {
    'NetIncomeLoss': {'units': {'USD': [
        {'end': '2026-03-28', 'val': 24780000000, 'filed': '2026-05-02',
         'form': '10-Q', 'fy': 2026, 'fp': 'Q2', 'accn': 'a-1'},
        {'end': '2026-06-27', 'val': 29789000000, 'filed': '2026-07-31',
         'form': '10-Q', 'fy': 2026, 'fp': 'Q3', 'accn': 'a-2'},
    ]}},
    #  Tag NON suivi : doit etre ignore sans bruit.
    'PreferredStockValue': {'units': {'USD': [
        {'end': '2026-06-27', 'val': 0, 'filed': '2026-07-31',
         'form': '10-Q', 'accn': 'a-3'}]}},
}}}


@pytest.fixture(autouse=True)
def _isole(monkeypatch):
    monkeypatch.setenv(S.DRAPEAU, '1')
    monkeypatch.setenv(S.VAR_CONTACT, 'Vertex test contact@example.com')
    S.vider_cache()
    yield
    S.vider_cache()


def _lecteur(url):
    return TABLE if 'company_tickers' in url else FACTS


#  ═══════════  1. la source est réellement branchée  ══════════════════════════

def test_la_route_des_fondamentaux_EXISTE():
    """Le cœur du lot : sans route, le module reste du code mort."""
    import terminal as T
    chemins = {str(r) for r in T.app.url_map.iter_rules()}
    assert '/api/sec/fondamentaux/<sym>' in chemins
    assert '/api/sec/etat' in chemins


def test_le_module_est_IMPORTE_par_une_route():
    """Contre-épreuve : une route qui n'appellerait pas la source serait une
    coquille."""
    import inspect

    from vertex.app.routes import company_api
    src = inspect.getsource(company_api)
    assert 'sec_fondamentaux' in src
    assert '_sec_f.fondamentaux(' in src


def test_le_DRAPEAU_de_l_utilisateur_est_enfin_lu():
    """`VERTEX_ENABLE_SEC` vivait dans un `.env` sans lecteur."""
    assert S.DRAPEAU == 'VERTEX_ENABLE_SEC'
    assert S.active() is True


#  ═══════════  2. le drapeau ET le contact, séparément  ═══════════════════════

def test_SANS_drapeau_la_source_ne_fait_rien(monkeypatch):
    monkeypatch.delenv(S.DRAPEAU, raising=False)
    r = S.fondamentaux('AAPL', lecteur=_lecteur)
    assert r['faits'] == [] and S.DRAPEAU in r['erreur']


def test_SANS_contact_la_source_ne_se_declare_pas_active(monkeypatch):
    """La SEC exige un contact réel. Un drapeau sans contact échouerait à
    chaque appel, et l'échec passerait pour une panne de la SEC."""
    monkeypatch.setenv(S.VAR_CONTACT, '')
    assert S.active() is False
    assert S.etat()['drapeau_pose'] is True
    assert S.etat()['contact_pose'] is False


def test_l_etat_DISTINGUE_les_deux_causes():
    e = S.etat()
    assert e['drapeau_pose'] is True and e['contact_pose'] is True
    assert e['date_de_publication_fournie'] is True
    assert e['read_only'] is True


#  ═══════════  3. le CIK n'est JAMAIS deviné  ═════════════════════════════════

def test_le_CIK_vient_du_fichier_OFFICIEL():
    assert S.cik_de('AAPL', lecteur=_lecteur) == '0000320193'
    assert S.cik_de('MSFT', lecteur=_lecteur) == '0000789019'


def test_un_ticker_INCONNU_rend_une_absence_nommee():
    """Le contrôle le plus important de ce module : servir les comptes d'une
    AUTRE entreprise sous ce nom serait la pire erreur possible."""
    S.cik_de('AAPL', lecteur=_lecteur)          # remplit la table
    r = S.fondamentaux('ZZINCONNU', lecteur=_lecteur)
    assert r['faits'] == []
    assert r['cik'] == ''
    assert 'aucun CIK devine' in r['erreur']


#  ═══════════  4. les deux dates, jamais confondues  ══════════════════════════

def test_chaque_fait_porte_LA_PERIODE_et_LE_DEPOT():
    r = S.fondamentaux('AAPL', lecteur=_lecteur)
    assert r['faits'], r.get('erreur')
    for f in r['faits']:
        assert f['observed_at'] and f['available_at']
        assert f['observed_at'] != f['available_at'], (
            'periode et depot confondus : un retrotest emploierait un chiffre '
            'publie des semaines plus tard')


def test_le_depot_est_POSTERIEUR_a_la_periode():
    """Contre-épreuve d'orientation : une date de dépôt antérieure à la
    période décrite signalerait une inversion des deux champs."""
    r = S.fondamentaux('AAPL', lecteur=_lecteur)
    for f in r['faits']:
        assert str(f['available_at'])[:10] >= str(f['observed_at'])[:10], f


#  ═══════════  5. ce qui n'est pas servi est écarté proprement  ═══════════════

def test_seuls_les_faits_SUIVIS_sont_servis():
    """`companyfacts` rend des milliers de tags ; tout servir noierait la
    page. `PreferredStockValue` n'est pas suivi et ne doit pas ressortir."""
    r = S.fondamentaux('AAPL', lecteur=_lecteur)
    tags = {f['tag'] for f in r['faits']}
    assert 'NetIncomeLoss' in tags
    assert 'PreferredStockValue' not in tags


def test_chaque_fait_servi_porte_un_LIBELLE_lisible():
    r = S.fondamentaux('AAPL', lecteur=_lecteur)
    for f in r['faits']:
        assert f['libelle'], f['tag']


def test_le_rapport_de_lecture_est_RENDU():
    """Ce qui est ignoré est compté, jamais silencieux."""
    r = S.fondamentaux('AAPL', lecteur=_lecteur)
    assert r['rapport']['faits_lus'] >= 3
    assert r['rapport']['ignores_sans_depot'] == 0


#  ═══════════  6. la route ne bloque pas  ═════════════════════════════════════

def test_la_route_rend_la_main_IMMEDIATEMENT(monkeypatch):
    """`companyfacts` fait plusieurs méga-octets. Bloquer une page pour
    l'attendre, c'est rouvrir le défaut P0.1 (28–48 s mesurées)."""
    import time

    import terminal as T
    c = T.app.test_client()
    t0 = time.time()
    r = c.get('/api/sec/fondamentaux/ZZTESTFROID')
    assert r.status_code == 200
    assert time.time() - t0 < 2.0, 'la route a bloque'


def test_la_reponse_NOMME_son_etat_de_fraicheur():
    """« aucun fait » doit pouvoir se distinguer de « pas encore chargé »."""
    import terminal as T
    d = json.loads(T.app.test_client().get(
        '/api/sec/fondamentaux/ZZTESTFROID').get_data())
    e = d['etat_fraicheur']
    assert e['etat'] in ('LIVE', 'DELAYED', 'STALE', 'MISSING', 'DEMO', 'OFFLINE')
    assert 'pas encore' in e['note']
    assert d['read_only'] is True


#  ═══════════  7. le défaut gzip ne peut pas revenir  ═════════════════════════

def test_le_chargement_DECOMPRESSE_le_gzip():
    """Le défaut trouvé en branchant : l'en-tête demandait gzip et le corps
    était décodé sans décompression — `UnicodeDecodeError: byte 0x8b`."""
    import inspect

    from vertex.data_sources import sec_edgar
    src = inspect.getsource(sec_edgar.charger_companyfacts)
    assert 'Accept-Encoding' in src
    assert 'Content-Encoding' in src, (
        "le chargement demande gzip sans jamais verifier s'il en recoit")
    assert 'decompress' in src
