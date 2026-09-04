"""tests/test_import_full.py — SKYLER LOT 46 : restauration étendue.

Le lot 45 restaurait le ledger mémoire ; le périmètre disait honnêtement
« séances/journal au backlog ». Ce lot le complète : le MÊME bundle d'export
restaure aussi le log de séances datées et le journal de calibration, par
REJEU HONNÊTE — la donnée LOCALE gagne toujours : une séance (symbole, date)
déjà observée localement n'est JAMAIS remplacée par l'archive (le scan local
est l'observation de référence), une entrée de journal (symbol, as_of,
decision — le MÊME triple de dédup que `record`) déjà présente reste. Même
contrat d'empreinte (rien écrit si sha invalide). Stats par magasin.
"""
import json

import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import session_log as SL
from vertex.engines import skyler_journal as SJ
from vertex.engines import skyler_core as SK


# ─── session_log.merge_log — la clôture locale gagne ────────────────────────────

def test_merge_log_adds_absent_sessions_only():
    cur = SL.record_close(SL.empty_log(), 'AAA', '2026-08-01', 100.0)
    imported = {'schema': 1, 'symbols': {
        'AAA': [{'date': '2026-08-01', 'close': 999.0},     # locale gagne
                {'date': '2026-08-02', 'close': 101.0}],    # absente → ajoutée
        'BBB': [{'date': '2026-08-01', 'close': 50.0}]}}
    merged, stats = SL.merge_log(cur, imported)
    assert stats['added_sessions'] == 2
    assert stats['skipped_sessions'] == 1
    assert merged['symbols']['AAA'][0]['close'] == 100.0    # JAMAIS remplacée
    assert merged['symbols']['BBB'][0]['close'] == 50.0


def test_merge_log_corrupted_and_degenerate_counted():
    imported = {'schema': 1, 'symbols': {
        'AAA': [{'date': 'pasunedate', 'close': 1.0},
                {'date': '2026-08-01', 'close': -5.0},
                'nondict',
                {'date': '2026-08-02', 'close': 101.0}],
        'BAD': 'nonliste'}}
    merged, stats = SL.merge_log(SL.empty_log(), imported)
    assert stats['added_sessions'] == 1
    assert stats['corrupted_entries'] == 4
    for bad in (None, [], 'x', {'symbols': 'x'}):
        m, s = SL.merge_log(SL.empty_log(), bad)
        assert s['added_sessions'] == 0 and m['symbols'] == {}


# ─── skyler_journal.merge_journal — l'entrée locale gagne ───────────────────────

def test_merge_journal_adds_absent_entries_only():
    cur = [{'symbol': 'AAA', 'as_of': 't1', 'decision': 'ATTENDRE',
            'price': 100.0}]
    imported = [
        {'symbol': 'AAA', 'as_of': 't1', 'decision': 'ATTENDRE',
         'price': 999.0},                                    # locale gagne
        {'symbol': 'AAA', 'as_of': 't2', 'decision': 'ATTENDRE'},
        {'symbol': 'BBB', 'as_of': 't1', 'decision': 'REFUSER'}]
    merged, stats = SJ.merge_journal(cur, imported)
    assert stats['added_entries'] == 2 and stats['skipped_entries'] == 1
    assert merged[0]['price'] == 100.0                       # JAMAIS remplacée
    assert len(merged) == 3


def test_merge_journal_corrupted_and_degenerate_counted():
    imported = ['x', 42, {'as_of': 't'}, {'symbol': 'A', 'decision': 'ATTENDRE'}]
    merged, stats = SJ.merge_journal([], imported)
    assert stats['added_entries'] == 1                       # seul le complet
    assert stats['corrupted_entries'] == 3
    for bad in (None, 'x', {'pas': 'une liste'}):
        m, s = SJ.merge_journal([], bad)
        assert s['added_entries'] == 0 and m == []


# ─── Route : le même bundle restaure les TROIS magasins ─────────────────────────

@pytest.fixture()
def client(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    return terminal.app.test_client(), tmp_path


def _seed_all(tmp):
    d = {'symbol': 'FUL', 'as_of': 't', 'decision': 'ATTENDRE',
         'score': {'total': 20, 'level': 'REFUS_WATCH', 'insufficient_blocks': []},
         'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': []}
    r = DM.freeze(decision=d, packet={'schema_version': 1,
                                      'engine_version': SK.ENGINE_VERSION},
                  price=100.0, closes=None, portfolio_ctx=None, now=0,
                  session_date='2026-08-01')
    (tmp / 'skyler_memory.json').write_text(
        json.dumps(DM.append_decision(DM.empty_memory(), r)), encoding='utf-8')
    (tmp / SL.SESSIONS_FILE).write_text(
        json.dumps(SL.record_close(SL.empty_log(), 'FUL', '2026-08-01', 100.0)),
        encoding='utf-8')
    (tmp / SJ.JOURNAL_FILE).write_text(
        json.dumps(SJ.record([], d, price=100.0, now=0)), encoding='utf-8')
    return r


def test_import_restores_all_three_stores(client):
    c, tmp = client
    _seed_all(tmp)
    bundle = c.get('/api/skyler/memory/export').get_json()
    for name in ('skyler_memory.json', SL.SESSIONS_FILE, SJ.JOURNAL_FILE):
        (tmp / name).unlink()                               # sinistre simulé
    resp = c.post('/api/skyler/memory/import', json=bundle)
    assert resp.status_code == 200
    d = resp.get_json()
    assert d['stats']['added_decisions'] == 1
    assert d['stats']['sessions']['added_sessions'] == 1
    assert d['stats']['journal']['added_entries'] == 1
    assert 'backlog' not in d['note']                       # périmètre complet
    slog = json.loads((tmp / SL.SESSIONS_FILE).read_text(encoding='utf-8'))
    assert slog['symbols']['FUL'][0]['close'] == 100.0
    j = json.loads((tmp / SJ.JOURNAL_FILE).read_text(encoding='utf-8'))
    assert j and j[0]['symbol'] == 'FUL'


def test_import_local_session_close_wins_at_route_level(client):
    c, tmp = client
    _seed_all(tmp)
    bundle = c.get('/api/skyler/memory/export').get_json()
    # la même séance existe localement avec une AUTRE clôture (vérité locale)
    (tmp / SL.SESSIONS_FILE).write_text(
        json.dumps(SL.record_close(SL.empty_log(), 'FUL', '2026-08-01', 123.0)),
        encoding='utf-8')
    resp = c.post('/api/skyler/memory/import', json=bundle)
    assert resp.status_code == 200
    slog = json.loads((tmp / SL.SESSIONS_FILE).read_text(encoding='utf-8'))
    assert slog['symbols']['FUL'][0]['close'] == 123.0      # locale intacte


def test_import_tampered_checksum_writes_none_of_three(client):
    c, tmp = client
    _seed_all(tmp)
    bundle = c.get('/api/skyler/memory/export').get_json()
    for name in ('skyler_memory.json', SL.SESSIONS_FILE, SJ.JOURNAL_FILE):
        (tmp / name).unlink()
    bundle['sessions']['symbols']['FUL'][0]['close'] = 999.0   # falsification
    resp = c.post('/api/skyler/memory/import', json=bundle)
    assert resp.status_code == 400
    for name in ('skyler_memory.json', SL.SESSIONS_FILE, SJ.JOURNAL_FILE):
        assert not (tmp / name).exists()                    # RIEN écrit
