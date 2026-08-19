"""tests/test_desk_cycle_lot84.py — SKYLER LOT 84 : cycle desk bout-en-bout.

Audit navigateur (6 étapes, publiées) : push localStorage→serveur avec
marqueur, serveur le porte, pull le restitue, 3 backups listés,
restauration PAR LA ROUTE /api/desk/restore (jamais à la main), remise
en état par last-writer-wins — 6/6 OK, AUCUNE perte possible constatée.
Les 4 listes de clés desk sont alignées (gardien
test_desk_sync_keys_single_source_of_truth vert, 17 clés).

Gardien PROSPECTIF (né vert, dit) : le contrat API du cycle ne doit pas
se défaire — écrire/relire via les routes reste fidèle au bit près.
"""
import json
import time

import pytest

import terminal


@pytest.fixture()
def client():
    return terminal.app.test_client()


def test_desk_roundtrip_is_faithful(client):
    """⚠ Ce test écrit dans le VRAI desk de l'utilisateur (`myNotes` est une clé
    synchronisée : les notes par titre). La remise en état est OBLIGATOIREMENT
    dans un `finally` — lot 387 : sans lui, une assertion en échec laissait les
    notes du trader remplacées par le marqueur du test, définitivement. Prouvé
    par mutation ; le gardien `test_desk_ecritures_lot387` verrouille ce
    `finally`."""
    d0 = client.get('/api/desk').get_json()
    data = dict(d0.get('data') or {})
    marker = f'lot84-guard-{int(time.time())}'
    data['myNotes'] = json.dumps({'guard': marker})
    try:
        r = client.post('/api/desk', json={'ts': int(time.time() * 1000), 'data': data})
        assert r.status_code == 200
        d1 = client.get('/api/desk').get_json()
        assert (d1.get('data') or {}).get('myNotes') == data['myNotes'], (
            'le blob desk doit être restitué au bit près (données personnelles)')
    finally:
        # Remise en état honnête — quoi qu'il arrive au-dessus.
        #
        # #783/G2 : le serveur CONSERVE désormais une clé qu'il détient et que
        # le push n'envoie pas (un push partiel ne peut plus effacer). Si
        # `myNotes` n'existait pas avant ce test, l'omettre ici laisserait donc
        # le marqueur dans le desk RÉEL, définitivement. Sous le nouveau
        # contrat, supprimer se dit EXPLICITEMENT : on renvoie la clé vide.
        retour = dict(d0.get('data') or {})
        retour.setdefault('myNotes', '{}')
        client.post('/api/desk', json={'ts': int(time.time() * 1000) + 1,
                                       'data': retour})


def test_desk_backups_listed(client):
    r = client.get('/api/desk/backups')
    assert r.status_code == 200
    body = r.get_json()
    assert isinstance(body.get('backups'), list)
    #  DEUX familles depuis #783/G2 : le quotidien (avant la 1re sync du jour)
    #  et l'« avant-perte » (à la seconde, quand un push menaçait des clés).
    #  Rester sur `desk_backup_` ferait échouer ce test sur un filet ÉLARGI.
    for b in body['backups']:
        nom, famille = b.get('name', ''), b.get('type')
        assert nom.startswith(('desk_backup_', 'desk_avantperte_')), nom
        assert famille in ('quotidien', 'avant-perte'), (
            'un instantane sans famille declaree : %s' % b)
