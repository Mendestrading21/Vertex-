"""tests/test_memory_export_lot29.py — SKYLER LOT 29 : export souverain.

`GET /api/skyler/memory/export` : sauvegarde LECTURE SEULE de tout l'état
runtime Skyler du trader — mémoire décisionnelle, log de séances datées,
journal de calibration — avec les versions, servie en téléchargement
(Content-Disposition). Les fichiers runtime sont gitignorés et périssables :
l'export rend la donnée la plus précieuse (l'historique des décisions)
SOUVERAINE. Aucun effet de bord ; magasins vides = vides honnêtes.
Bouton « Exporter » dans la carte Mémoire → SW v100 → v101.
"""
import json

import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import session_log as SL
from vertex.engines import skyler_journal as SJ
from vertex.engines import skyler_core as SK


def _seed(tmp_path, monkeypatch):
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    d = {'symbol': 'EXP', 'as_of': 't', 'decision': 'ATTENDRE',
         'score': {'total': 20, 'level': 'REFUS_WATCH', 'insufficient_blocks': []},
         'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': []}
    r = DM.freeze(decision=d, packet={'schema_version': 1,
                                      'engine_version': SK.ENGINE_VERSION},
                  price=100.0, closes=None, portfolio_ctx=None, now=0,
                  session_date='2026-08-01')
    persist.save_json(DM.MEMORY_FILE, DM.append_decision(DM.empty_memory(), r))
    persist.save_json(SL.SESSIONS_FILE,
                      SL.record_close(SL.empty_log(), 'EXP', '2026-08-01', 100.0))
    persist.save_json(SJ.JOURNAL_FILE,
                      SJ.record([], {'symbol': 'EXP', 'as_of': 't',
                                     'decision': 'ATTENDRE', 'score': {'total': 20}},
                                price=100.0, now=0))
    return persist


def test_export_bundles_all_runtime_stores(tmp_path, monkeypatch):
    import terminal
    _seed(tmp_path, monkeypatch)
    resp = terminal.app.test_client().get('/api/skyler/memory/export')
    assert resp.status_code == 200
    d = resp.get_json()
    assert d['versions']['decision_engine'] == SK.ENGINE_VERSION
    assert d['versions']['memory_schema'] == DM.MEMORY_SCHEMA_VERSION
    assert d['memory']['decisions'][0]['symbol'] == 'EXP'
    assert d['sessions']['symbols']['EXP'][0]['close'] == 100.0
    assert d['journal'][0]['symbol'] == 'EXP'
    assert d['exported_at']                                # horodatage réel
    assert 'jamais' in d['note'] or 'lecture seule' in d['note'].lower()


def test_export_download_header(tmp_path, monkeypatch):
    import terminal
    _seed(tmp_path, monkeypatch)
    resp = terminal.app.test_client().get('/api/skyler/memory/export')
    cd = resp.headers.get('Content-Disposition', '')
    assert 'attachment' in cd and 'skyler_export' in cd and cd.endswith('.json"')


def test_export_empty_stores_honest(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    d = terminal.app.test_client().get('/api/skyler/memory/export').get_json()
    assert d['memory']['decisions'] == []
    assert d['sessions']['symbols'] == {}
    assert d['journal'] == []


def test_export_is_strictly_readonly(tmp_path, monkeypatch):
    """L'export ne modifie AUCUN fichier runtime (ni création ni mutation)."""
    import os
    import terminal
    persist = _seed(tmp_path, monkeypatch)
    before = {f: open(str(tmp_path / f), 'rb').read()
              for f in os.listdir(str(tmp_path))}
    assert terminal.app.test_client().get('/api/skyler/memory/export').status_code == 200
    after = {f: open(str(tmp_path / f), 'rb').read()
             for f in os.listdir(str(tmp_path))}
    assert before == after


def test_export_json_roundtrip(tmp_path, monkeypatch):
    import terminal
    _seed(tmp_path, monkeypatch)
    body = terminal.app.test_client().get('/api/skyler/memory/export').get_data(as_text=True)
    assert json.loads(body)                                # JSON strictement valide


# ─── Surfaçage : bouton d'export dans la carte Mémoire, SW v101 ─────────────────

def test_memory_card_has_export_button():
    import terminal
    body = terminal.app.test_client().get('/journal', follow_redirects=True).get_data(as_text=True)
    assert '/api/skyler/memory/export' in body
    assert 'Exporter' in body


def test_service_worker_bumped_to_at_least_v101():
    import re
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 101
    assert 'td-shell-v100' not in body
