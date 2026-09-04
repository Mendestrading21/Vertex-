"""tests/test_export_integrity.py — SKYLER LOT 42 : intégrité de l'export.

L'export souverain (lot 29) est la sauvegarde de la donnée la plus précieuse
du desk — il gagne deux propriétés d'ARCHIVE :

- `ledger_health` embarqué : l'archive dit ELLE-MÊME si le ledger était
  cohérent au moment de l'export (lot 35, calculé à l'export) ;
- `content_sha256` : empreinte sha256 du JSON CANONIQUE du bundle (clés
  triées, séparateurs compacts, contenu SANS le champ d'empreinte) —
  vérifiable HORS LIGNE par quiconque détient le fichier, sans le serveur.

Toujours strictement lecture seule (octets identiques avant/après).
"""
import hashlib
import json

import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import skyler_core as SK


def _canonical(d):
    """Recette de vérification HORS LIGNE (lots 42/47) : clés triées,
    séparateurs compacts, flottants entiers normalisés (100.0 ≡ 100 — stable
    au round-trip JSON.stringify des navigateurs)."""
    def norm(o):
        if isinstance(o, float) and o.is_integer():
            return int(o)
        if isinstance(o, dict):
            return {k: norm(v) for k, v in o.items()}
        if isinstance(o, list):
            return [norm(v) for v in o]
        return o
    return json.dumps(norm(d), sort_keys=True, ensure_ascii=False,
                      separators=(',', ':'))


def _seed(tmp_path, monkeypatch, with_orphan=False):
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    d = {'symbol': 'INT', 'as_of': 't', 'decision': 'ATTENDRE',
         'score': {'total': 20, 'level': 'REFUS_WATCH', 'insufficient_blocks': []},
         'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': []}
    r = DM.freeze(decision=d, packet={'schema_version': 1,
                                      'engine_version': SK.ENGINE_VERSION},
                  price=100.0, closes=None, portfolio_ctx=None, now=0,
                  session_date='2026-08-01')
    mem = DM.append_decision(DM.empty_memory(), r)
    if with_orphan:
        mem['outcomes'].append({'decision_id': 'fantome',
                                'engine_version': SK.ENGINE_VERSION,
                                'sessions_observed': 5, 'horizons': {}})
    persist.save_json(DM.MEMORY_FILE, mem)
    return persist


def _export(tmp_path, monkeypatch, **kw):
    import terminal
    _seed(tmp_path, monkeypatch, **kw)
    return terminal.app.test_client().get('/api/skyler/memory/export')


def test_export_embeds_ledger_health_sain(tmp_path, monkeypatch):
    d = _export(tmp_path, monkeypatch).get_json()
    assert d['ledger_health']['status'] == 'SAIN'
    assert d['ledger_health']['n_decisions'] == 1


def test_export_embeds_ledger_health_anomalies_honest(tmp_path, monkeypatch):
    """Un export d'un ledger incohérent le DIT dans l'archive elle-même —
    jamais une archive silencieusement présentée comme saine."""
    d = _export(tmp_path, monkeypatch, with_orphan=True).get_json()
    assert d['ledger_health']['status'] == 'ANOMALIES'
    assert d['ledger_health']['orphan_outcomes'] == 1


def test_export_checksum_verifiable_offline(tmp_path, monkeypatch):
    """La vérification n'exige QUE le fichier : sha256 du JSON canonique
    (clés triées, séparateurs compacts) du bundle SANS content_sha256."""
    body = _export(tmp_path, monkeypatch).get_data(as_text=True)
    d = json.loads(body)
    claimed = d.pop('content_sha256')
    assert claimed == hashlib.sha256(_canonical(d).encode('utf-8')).hexdigest()


def test_export_note_documents_verification(tmp_path, monkeypatch):
    d = _export(tmp_path, monkeypatch).get_json()
    assert 'sha256' in d['note']


def test_export_still_strictly_readonly(tmp_path, monkeypatch):
    import os
    import terminal
    _seed(tmp_path, monkeypatch)
    before = {f: open(str(tmp_path / f), 'rb').read()
              for f in os.listdir(str(tmp_path))}
    assert terminal.app.test_client().get(
        '/api/skyler/memory/export').status_code == 200
    after = {f: open(str(tmp_path / f), 'rb').read()
             for f in os.listdir(str(tmp_path))}
    assert before == after


def test_export_corrupted_store_checksum_still_valid(tmp_path, monkeypatch):
    """Même sur magasin corrompu (servi tel quel, lot 31), l'empreinte reste
    exacte — l'archive corrompue est fidèlement empreintée, jamais maquillée."""
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    (tmp_path / 'skyler_memory.json').write_text(
        '{"decisions": [1, "x"], "outcomes": null}', encoding='utf-8')
    body = terminal.app.test_client().get(
        '/api/skyler/memory/export').get_data(as_text=True)
    d = json.loads(body)
    claimed = d.pop('content_sha256')
    assert claimed == hashlib.sha256(_canonical(d).encode('utf-8')).hexdigest()
    assert d['ledger_health']['status'] == 'ANOMALIES'
