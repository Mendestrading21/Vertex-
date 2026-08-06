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
    d0 = client.get('/api/desk').get_json()
    data = dict(d0.get('data') or {})
    marker = f'lot84-guard-{int(time.time())}'
    data['myNotes'] = json.dumps({'guard': marker})
    r = client.post('/api/desk', json={'ts': int(time.time() * 1000), 'data': data})
    assert r.status_code == 200
    d1 = client.get('/api/desk').get_json()
    assert (d1.get('data') or {}).get('myNotes') == data['myNotes'], (
        'le blob desk doit être restitué au bit près (données personnelles)')
    # remise en état honnête
    client.post('/api/desk', json={'ts': int(time.time() * 1000) + 1,
                                   'data': d0.get('data') or {}})


def test_desk_backups_listed(client):
    r = client.get('/api/desk/backups')
    assert r.status_code == 200
    body = r.get_json()
    assert isinstance(body.get('backups'), list)
    for b in body['backups']:
        assert b.get('name', '').startswith('desk_backup_')
