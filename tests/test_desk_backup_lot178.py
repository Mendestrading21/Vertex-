"""
LOT 178 — Caractérisation du FILET DE SÉCURITÉ du desk
(`vertex/app/routes/desk.py` — backup quotidien + /api/desk/restore).
Le round-trip push/pull est couvert (desk_routes, cycle lot 84) ; la
lacune était la chaîne de SAUVEGARDE : snapshot quotidien avant
écrasement (filet contre le last-writer-wins — règle critique n°6),
rotation à 7 jours, et la validation STRICTE du restore (surface de
sécurité : le nom vient du client).
"""
import glob
import json
import os
import time

import pytest

import terminal
from vertex.services import persist


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    yield terminal.app.test_client()


def _push(client, ts, notes):
    return client.post('/api/desk', json={'ts': ts, 'data': {'myNotes': notes}})


def _today():
    return time.strftime('%Y%m%d')


# ── Snapshot quotidien : le filet contre le last-writer-wins ─────────────────

def test_backup_cree_au_premier_ecrasement_du_jour(client, tmp_path):
    _push(client, 1000, 'v1')                       # rien à sauvegarder encore
    assert not glob.glob(str(tmp_path / 'desk_backup_*.json'))
    _push(client, 2000, 'v2')                       # écrase v1 → v1 sauvegardée AVANT
    bk = tmp_path / ('desk_backup_%s.json' % _today())
    assert bk.exists()
    assert json.loads(bk.read_text())['data'] == {'myNotes': 'v1'}


def test_backup_du_jour_jamais_ecrase_par_les_pushs_suivants(client, tmp_path):
    # Le snapshot du MATIN protège toute la journée : les pushs suivants ne le
    # réécrivent pas — on peut toujours revenir à l'état d'avant la 1re sync.
    _push(client, 1000, 'v1')
    _push(client, 2000, 'v2')
    _push(client, 3000, 'v3')
    bk = tmp_path / ('desk_backup_%s.json' % _today())
    assert json.loads(bk.read_text())['data'] == {'myNotes': 'v1'}


def test_rotation_conserve_7_snapshots(client, tmp_path):
    for i in range(1, 9):                           # 8 anciens jours
        (tmp_path / ('desk_backup_2026010%d.json' % i)).write_text(
            json.dumps({'ts': i, 'data': {'myNotes': 'ancien'}}))
    _push(client, 1000, 'v1')
    _push(client, 2000, 'v2')                       # crée le backup du jour + rotation
    restants = sorted(os.path.basename(p)
                      for p in glob.glob(str(tmp_path / 'desk_backup_*.json')))
    assert len(restants) == 7                       # BACKUP_KEEP
    assert restants[-1] == 'desk_backup_%s.json' % _today()
    assert 'desk_backup_20260101.json' not in restants   # les plus vieux purgés


# ── /api/desk/restore : validation stricte (le nom vient du client) ──────────

def test_restore_refuse_traversal_et_noms_hors_motif(client):
    for bad in ('../../etc/passwd', 'desk_backup_2026.json',
                'desk_backup_20260807.json.bak', 'autre.json', ''):
        r = client.post('/api/desk/restore', json={'name': bad})
        assert r.status_code == 400, bad
        assert r.get_json() == {'ok': False, 'err': 'nom invalide'}


def test_restore_introuvable_404(client):
    r = client.post('/api/desk/restore', json={'name': 'desk_backup_19990101.json'})
    assert r.status_code == 404
    assert r.get_json() == {'ok': False, 'err': 'backup introuvable'}


def test_restore_illisible_500_sans_toucher_le_desk(client, tmp_path):
    _push(client, 1000, 'courant')
    (tmp_path / 'desk_backup_19990102.json').write_text('null')   # nom valide, contenu mort
    r = client.post('/api/desk/restore', json={'name': 'desk_backup_19990102.json'})
    assert r.status_code == 500
    assert r.get_json()['err'] == 'backup illisible'
    assert client.get('/api/desk').get_json()['data'] == {'myNotes': 'courant'}


def test_restore_reussi_donnees_restaurees_et_ts_neuf(client, tmp_path):
    # Le restore réécrit desk_data avec un ts DE MAINTENANT : dans le modèle
    # last-writer-wins, tous les appareils re-tireront la version restaurée.
    _push(client, 1000, 'v1')
    _push(client, 2000, 'v2')
    bk = 'desk_backup_%s.json' % _today()
    r = client.post('/api/desk/restore', json={'name': bk})
    assert r.status_code == 200
    assert r.get_json() == {'ok': True, 'restored': bk}
    d = client.get('/api/desk').get_json()
    assert d['data'] == {'myNotes': 'v1'}           # contenu du snapshot
    assert d['ts'] > 2000                           # ts neuf → gagne le LWW partout


# ── Contrat de la liste ──────────────────────────────────────────────────────

def test_backups_listes_du_plus_recent_au_plus_ancien(client, tmp_path):
    for day in ('20260101', '20260103', '20260102'):
        (tmp_path / ('desk_backup_%s.json' % day)).write_text(
            json.dumps({'ts': 1, 'data': {}}))
    j = client.get('/api/desk/backups').get_json()
    assert [b['date'] for b in j['backups']] == ['20260103', '20260102', '20260101']
    assert j['keep'] == 7
