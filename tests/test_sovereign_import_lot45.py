"""tests/test_sovereign_import_lot45.py — SKYLER LOT 45 : restauration souveraine.

L'export (lots 29/42) est une sauvegarde SANS chemin de retour — une archive
qu'on ne peut pas restaurer n'est souveraine qu'à moitié. La restauration se
fait par REJEU APPEND-ONLY : chaque décision repasse par `append_decision`
(un decision_id existant n'est JAMAIS remplacé — l'historique local gagne),
chaque outcome par `append_outcome` (monotone). L'empreinte `content_sha256`
du bundle est VÉRIFIÉE avant toute écriture — archive altérée → 400 dit,
rien n'est touché. Périmètre : le ledger mémoire (la donnée précieuse) ;
séances/journal restent au backlog, dit dans la note de réponse.
"""
import hashlib
import json

import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import skyler_core as SK


def _rec(i, version='vI'):
    d = {'symbol': 'I%03d' % i, 'as_of': str(i), 'decision': 'ATTENDRE',
         'score': {'total': 20, 'level': 'REFUS_WATCH', 'insufficient_blocks': []},
         'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': []}
    return DM.freeze(decision=d, packet={'schema_version': 1,
                                         'engine_version': version},
                     price=100.0 + i, closes=None, portfolio_ctx=None, now=i,
                     session_date='2026-08-01')


def _out(decision_id, sessions=5, version='vI'):
    return {'decision_id': decision_id, 'engine_version': version,
            'symbol': 'X', 'sessions_observed': sessions,
            'horizons': {'H5': {'status': 'MESURE', 'sessions': 5,
                                'return_pct': 1.0, 'basis': 't'}},
            'mfe_pct': None, 'mae_pct': None}


# ─── Moteur : merge_memory = rejeu append-only ──────────────────────────────────

def test_merge_adds_new_and_never_rewrites_existing():
    r1, r2 = _rec(1), _rec(2)
    current = DM.append_decision(DM.empty_memory(), r1)
    r1_altered = dict(r1, thesis='RÉÉCRITURE HOSTILE')
    imported = {'schema': 1, 'decisions': [r1_altered, r2], 'outcomes': []}
    merged, stats = DM.merge_memory(current, imported)
    assert stats['added_decisions'] == 1                 # r2 seulement
    assert stats['skipped_decisions'] == 1               # r1 existant GAGNE
    kept = DM.find_decision(merged, r1['decision_id'])
    assert kept.get('thesis') != 'RÉÉCRITURE HOSTILE'    # jamais réécrit


def test_merge_outcomes_monotone():
    r1 = _rec(1)
    current = DM.append_outcome(DM.append_decision(DM.empty_memory(), r1),
                                _out(r1['decision_id'], sessions=10))
    imported = {'schema': 1, 'decisions': [],
                'outcomes': [_out(r1['decision_id'], sessions=5),
                             _out(r1['decision_id'], sessions=20)]}
    merged, stats = DM.merge_memory(current, imported)
    o = DM.find_outcome(merged, r1['decision_id'])
    assert o['sessions_observed'] == 20                  # seul le PLUS long gagne


def test_merge_corrupted_entries_counted_never_crash():
    imported = {'schema': 1, 'decisions': ['x', 42, None, _rec(1)],
                'outcomes': ['y', 7]}
    merged, stats = DM.merge_memory(DM.empty_memory(), imported)
    assert stats['added_decisions'] == 1
    assert stats['corrupted_entries'] == 5
    assert len(merged['decisions']) == 1


def test_merge_degenerate_import_refused():
    for bad in (None, [], 'x', {'decisions': 'x', 'outcomes': None}):
        merged, stats = DM.merge_memory(DM.empty_memory(), bad)
        assert stats['added_decisions'] == 0 and merged['decisions'] == []


# ─── Route : empreinte vérifiée AVANT toute écriture ────────────────────────────

@pytest.fixture()
def client(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    return terminal.app.test_client(), tmp_path


def _bundle(client_tuple):
    """Un bundle d'export RÉEL (empreinte exacte) contenant 1 décision."""
    c, tmp = client_tuple
    r = _rec(7, version=SK.ENGINE_VERSION)
    mem = DM.append_decision(DM.empty_memory(), r)
    (tmp / 'skyler_memory.json').write_text(json.dumps(mem), encoding='utf-8')
    bundle = c.get('/api/skyler/memory/export').get_json()
    (tmp / 'skyler_memory.json').unlink()                # magasin remis à vide
    return bundle, r


def test_import_restores_from_real_export(client):
    c, tmp = client
    bundle, r = _bundle(client)
    resp = c.post('/api/skyler/memory/import', json=bundle)
    assert resp.status_code == 200
    d = resp.get_json()
    assert d['ok'] is True and d['stats']['added_decisions'] == 1
    assert d['ledger_health']['status'] == 'SAIN'
    assert 'séances' in d['note'] or 'sessions' in d['note']   # périmètre dit
    stored = json.loads((tmp / 'skyler_memory.json').read_text(encoding='utf-8'))
    assert DM.find_decision(stored, r['decision_id']) is not None


def test_import_tampered_checksum_refused_nothing_written(client):
    c, tmp = client
    bundle, _ = _bundle(client)
    bundle['memory']['decisions'][0]['thesis'] = 'ALTÉRÉ'    # falsification
    resp = c.post('/api/skyler/memory/import', json=bundle)
    assert resp.status_code == 400
    d = resp.get_json()
    assert d['ok'] is False and 'empreinte' in d['error']
    assert not (tmp / 'skyler_memory.json').exists()          # RIEN écrit


def test_import_missing_checksum_refused(client):
    c, _ = client
    bundle, _ = _bundle(client)
    bundle.pop('content_sha256')
    resp = c.post('/api/skyler/memory/import', json=bundle)
    assert resp.status_code == 400 and resp.get_json()['ok'] is False


def test_import_garbage_bodies_never_500(client):
    c, _ = client
    for body, kw in (('nonjson', {'data': 'pas du json', 'content_type': 'application/json'}),
                     (None, {'json': {}}),
                     (None, {'json': []}),
                     (None, {'json': {'content_sha256': 'x' * 64}})):
        resp = c.post('/api/skyler/memory/import', **kw)
        assert resp.status_code in (400, 415) and resp.status_code != 500


def test_import_into_populated_store_existing_wins(client):
    c, tmp = client
    bundle, r = _bundle(client)
    local = dict(r, thesis='VÉRITÉ LOCALE')
    (tmp / 'skyler_memory.json').write_text(
        json.dumps(DM.append_decision(DM.empty_memory(), local)),
        encoding='utf-8')
    resp = c.post('/api/skyler/memory/import', json=bundle)
    assert resp.status_code == 200
    stored = json.loads((tmp / 'skyler_memory.json').read_text(encoding='utf-8'))
    assert DM.find_decision(stored, r['decision_id'])['thesis'] == 'VÉRITÉ LOCALE'
