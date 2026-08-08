"""
LOT 362 — Règle n°6 passée à la question « la règle écrite décrit-elle le code
servi ? ». Elle dit : « `desk_data.json` : ne jamais l'écraser à la main ; en
cas de doute, backups `desk_backup_*.json` + `/api/desk/restore` ».

La chaîne de sauvegarde est SAINE et déjà gardée (lot 178 : snapshot quotidien,
rotation à 7, validation stricte du restore). Ce fichier fige ce que la règle
ne dit pas — trois faits mesurés qui bornent ce que « en cas de doute, les
backups » promet réellement :

  1. le serveur accepte un push de desk **vide** (`data: {}`) et remplace le
     blob — l'écrasement redouté n'a pas besoin d'être « à la main » ;
  2. un push **partiel** remplace le blob ENTIER (last-writer-wins total, pas
     clé par clé) : les clés absentes du push disparaissent côté serveur ;
  3. aucun snapshot supplémentaire n'est pris à ce moment-là — le point de
     restauration reste l'état d'**avant la première sync du jour**, donc un
     restore fait perdre tout le travail de la journée.

Le client, lui, se protège bien (`vertex/ui/vx_kit.py`) : il ne pousse
qu'après une hydratation réussie (`_bootDone`), s'abstient si `bootSync`
échoue, et recharge toute clé absente en local. Le scénario résiduel est un
navigateur dont l'écriture localStorage échoue silencieusement (navigation
privée, quota) : l'hydratation ne persiste rien, et le push suivant envoie
`{}`.

⚠️ Ce sont des tests de CARACTÉRISATION : ils décrivent le contrat actuel, ils
ne le bénissent pas. Si le serveur est un jour durci (refus d'un push qui vide
un desk non vide, ou snapshot supplémentaire avant perte), ces tests DOIVENT
être mis à jour — c'est précisément leur rôle d'alerte.

Tout passe par un dossier temporaire : le vrai `desk_data.json` n'est jamais
touché.
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


PLEIN = {'myTrades': '[{"symbol":"ACN"}]',
         'vxJournal': '[{"note":"these"}]',
         'myFavs': '["ACN","ABT"]'}


def _push(client, ts, data):
    return client.post('/api/desk', json={'ts': ts, 'data': data})


def _desk(client):
    return client.get('/api/desk').get_json()


def _snapshots(tmp_path):
    return sorted(os.path.basename(p)
                  for p in glob.glob(str(tmp_path / 'desk_backup_*.json')))


# ── 1. Un desk vide est accepté et remplace tout ─────────────────────────────

def test_un_push_vide_est_accepte_et_vide_le_desk_serveur(client):
    _push(client, 1000, PLEIN)
    r = _push(client, 2000, {})
    assert r.status_code == 200 and r.get_json()['ok'] is True
    assert _desk(client)['data'] == {}, \
        'le serveur refuse désormais un push vide — mettre à jour ce gardien'


def test_seul_un_data_non_dict_ou_un_ts_absent_est_refuse(client):
    # La validation porte sur le TYPE, jamais sur le contenu : {} est un dict.
    assert _push(client, 1000, None).status_code == 400
    assert _push(client, 1000, []).status_code == 400
    assert client.post('/api/desk', json={'data': {}}).status_code == 400   # ts absent
    assert _push(client, 1000, {}).status_code == 200                       # {} passe


# ── 2. Le last-writer-wins est TOTAL, pas clé par clé ────────────────────────

def test_un_push_partiel_efface_les_cles_absentes(client):
    _push(client, 1000, PLEIN)
    _push(client, 2000, {'myFavs': '["ACN"]'})
    d = _desk(client)['data']
    assert sorted(d) == ['myFavs']
    assert 'myTrades' not in d and 'vxJournal' not in d


# ── 3. Le point de restauration ne bouge pas — le jour est perdu ─────────────

def test_le_restore_remonte_avant_la_premiere_sync_du_jour(client, tmp_path):
    _push(client, 1000, PLEIN)                       # 1re sync : rien à sauvegarder
    _push(client, 2000, dict(PLEIN,
                             vxJournal='[{"note":"these"},{"note":"ajout du jour"}]'))
    snaps = _snapshots(tmp_path)
    assert snaps == ['desk_backup_%s.json' % time.strftime('%Y%m%d')]

    _push(client, 3000, {})                          # perte
    assert _snapshots(tmp_path) == snaps, \
        'un snapshot supplémentaire est désormais pris — mettre à jour ce gardien'

    client.post('/api/desk/restore', json={'name': snaps[0]})
    restaure = _desk(client)['data']
    assert restaure['vxJournal'] == PLEIN['vxJournal']       # état d'avant la 1re sync
    assert 'ajout du jour' not in restaure['vxJournal']      # le jour est perdu


def test_le_filet_couvre_au_plus_sept_jours(client, tmp_path):
    # BACKUP_KEEP=7 : au-delà, aucun retour en arrière possible.
    from vertex.app.routes import desk as _desk_mod
    assert _desk_mod.BACKUP_KEEP == 7
    for j in range(1, 10):
        (tmp_path / ('desk_backup_2026010%d.json' % j)).write_text(
            json.dumps({'ts': j, 'data': PLEIN}))
    _push(client, 1000, PLEIN)
    _push(client, 2000, PLEIN)                       # déclenche rotation
    assert len(_snapshots(tmp_path)) == 7
