"""Vertex 1.0 — UNE PAGE TIERCE POUVAIT ÉCRIRE DANS LE BUREAU.

## Démontré le 25 août 2026 sur le vrai produit

Vertex tourne en local pendant que l'utilisateur navigue. Toute page visitée
peut faire émettre à son navigateur un POST vers `http://localhost:5002` — une
requête *simple*, donc **sans preflight CORS**, dès lors qu'elle utilise un
`Content-Type` autorisé comme `text/plain`.

Or `/api/desk` lit son corps avec `request.get_json(force=True)`, et `force`
**ignore le `Content-Type`** :

```text
POST /api/desk   Content-Type: text/plain
                 Origin: https://site-malveillant.example
-> 200 {'ok': True, ...}    et l'ecriture a bien eu lieu
```

**Quatorze routes `POST`** existent. Aucune ne vérifiait l'origine.

## Ce qui limitait les dégâts, et ce qui ne les limitait pas

Le correctif du lot 362 empêche un push partiel d'effacer les clés absentes, et
un instantané `desk_avantperte_*.json` est pris avant écriture : les données
existantes ne sont **pas détruites**, et il existe un point de retour. C'est
réel et il faut le dire.

Ce qui restait possible : **injecter**. Un faux trade, une fausse entrée de
journal — dans le registre même qui sert à juger les décisions passées. Une
corruption discrète vaut mieux qu'une destruction bruyante, pour qui veut nuire.

## Pourquoi l'origine, et pas un jeton CSRF

Un jeton exige une session. Or **sans `VERTEX_CODE` il n'y a pas de session**,
et c'est la configuration par défaut. `SESSION_COOKIE_SAMESITE='Lax'` protège
le cookie — mais protéger un cookie qui n'existe pas ne protège rien.

Le navigateur, lui, **envoie toujours `Origin` sur un POST cross-origin**.
"""
from __future__ import annotations

import json
import time

import pytest

from vertex.app.origine import METHODES_ECRITURE, origine_etrangere


#  ═══════════  1. la règle, isolée  ═══════════════════════════════════════════

def test_une_ECRITURE_d_origine_etrangere_est_refusee():
    assert origine_etrangere(methode='POST',
                             origine='https://site-malveillant.example',
                             hote_servi='localhost:5002') is True


def test_une_ecriture_de_MEME_origine_passe():
    """Contre-épreuve : une protection qui bloque l'usage normal n'est pas une
    protection, c'est une panne."""
    assert origine_etrangere(methode='POST', origine='http://localhost:5002',
                             hote_servi='localhost:5002') is False


def test_une_LECTURE_n_est_JAMAIS_bloquee():
    """La protection viserait alors la simple consultation, et casserait les
    liens entrants."""
    for methode in ('GET', 'HEAD', 'OPTIONS'):
        assert origine_etrangere(methode=methode, origine='https://ailleurs.example',
                                 hote_servi='localhost:5002') is False


def test_une_ecriture_SANS_Origin_passe():
    """`curl`, les bancs et les appels serveur-à-serveur n'en envoient pas. Un
    navigateur, lui, ne PEUT PAS l'omettre sur un POST cross-origin :
    l'absence d'`Origin` n'est donc pas un contournement — c'est la marque d'un
    client qui n'est pas une page web."""
    assert origine_etrangere(methode='POST', origine='',
                             hote_servi='localhost:5002') is False
    assert origine_etrangere(methode='POST', origine=None,
                             hote_servi='localhost:5002') is False


def test_le_PORT_fait_partie_de_l_identite():
    """`localhost:5002` et `localhost:9999` sont deux origines différentes pour
    le navigateur. Les confondre rouvrirait la porte à une autre application
    locale."""
    assert origine_etrangere(methode='POST', origine='http://localhost:9999',
                             hote_servi='localhost:5002') is True


def test_le_SCHEMA_ne_fait_pas_l_identite():
    """`http://` et `https://` sur le même hôte sont la même origine pour cette
    protection : exiger le schéma casserait l'accès derrière un proxy TLS."""
    assert origine_etrangere(methode='POST', origine='https://localhost:5002',
                             hote_servi='localhost:5002') is False


def test_toutes_les_methodes_qui_MODIFIENT_sont_couvertes():
    """`POST` seul laisserait passer `PUT`, `PATCH` et `DELETE` le jour où une
    route en utilisera une."""
    assert METHODES_ECRITURE == {'POST', 'PUT', 'PATCH', 'DELETE'}
    for methode in METHODES_ECRITURE:
        assert origine_etrangere(methode=methode, origine='https://ailleurs.example',
                                 hote_servi='localhost:5002') is True


#  ═══════════  2. l'attaque réelle, sur le vrai produit  ══════════════════════

@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Client de test dont les ecritures vont dans un dossier TEMPORAIRE.

    Sans cette redirection, `test_la_synchro_NORMALE_...` ecrirait dans le VRAI
    `desk_data.json` — les donnees personnelles de l'utilisateur. C'est
    `test_desk_ecritures_lot387` qui l'a refuse, et il a eu raison : ma
    premiere version de ce banc touchait le bureau reel.
    """
    import os
    os.environ.setdefault('NO_IBKR', '1')
    os.environ.setdefault('START_ON_IMPORT', '0')
    from vertex.services import persist
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    import terminal
    return terminal.app.test_client()


def test_l_attaque_MESUREE_est_desormais_refusee(client):
    """La requête exacte qui écrivait : `text/plain` (pas de preflight) et une
    `Origin` étrangère."""
    charge = json.dumps({'ts': int(time.time()),
                         'data': {'trades': [{'sym': 'PWNED'}]}})
    r = client.post('/api/desk', data=charge, content_type='text/plain',
                    headers={'Origin': 'https://site-malveillant.example'})
    assert r.status_code == 403
    corps = r.get_json()
    assert corps['ok'] is False
    assert 'origine' in corps['err']


def test_le_refus_DIT_pourquoi(client):
    """403 et non 404 : l'utilisateur légitime qui tomberait dessus doit
    comprendre, et le journal doit pouvoir le compter."""
    r = client.post('/api/desk', json={'ts': 1, 'data': {}},
                    headers={'Origin': 'https://ailleurs.example'})
    assert r.status_code == 403
    assert 'ailleurs.example' in (r.get_json().get('origine') or '')


def test_la_synchro_NORMALE_du_bureau_marche_toujours(client):
    """Contre-épreuve sur le produit : sans elle, ce lot casserait la
    synchronisation entre appareils au lieu de la protéger."""
    r = client.post('/api/desk', json={'ts': int(time.time()),
                                       'data': {'vxJournal': '[]'}})
    assert r.status_code == 200 and r.get_json()['ok'] is True


def test_la_LECTURE_du_bureau_reste_ouverte(client):
    r = client.get('/api/desk', headers={'Origin': 'https://ailleurs.example'})
    assert r.status_code == 200


def test_la_garde_couvre_TOUTES_les_routes_d_ecriture(client):
    """Une protection d'écriture qui n'en couvre que certaines ne protège
    rien : c'est celle qu'on oublie qui sert de porte. Elle est posée dans la
    fabrique, avant les blueprints — ce banc le vérifie sur des routes de
    blueprints DIFFÉRENTS."""
    etrangere = {'Origin': 'https://ailleurs.example'}
    for chemin, charge in (('/api/desk', {'ts': 1, 'data': {}}),
                           ('/api/client-log', {'msg': 'x'}),
                           ('/api/pos-quotes', {'positions': []}),
                           ('/api/rescan', {})):
        r = client.post(chemin, json=charge, headers=etrangere)
        assert r.status_code == 403, '%s non protege (%s)' % (chemin, r.status_code)


def test_la_garde_est_posee_dans_la_FABRIQUE_et_pas_route_par_route():
    """Route par route, la quinzième s'écrira sans protection."""
    import pathlib
    src = (pathlib.Path(__file__).resolve().parents[1] / 'vertex' / 'app'
           / 'factory.py').read_text(encoding='utf-8')
    assert 'origine_etrangere' in src
    i = src.index('origine_etrangere')
    assert 'before_request' in src[max(0, i - 600):i]
