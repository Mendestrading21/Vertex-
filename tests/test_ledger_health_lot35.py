"""tests/test_ledger_health_lot35.py — SKYLER LOT 35 : santé du ledger.

Après deux bumps de moteur (0.8.0 → 0.9.0) et les trouvailles fuzz des lots
31/34 (magasins corruptibles), le ledger multi-versions a besoin d'un
CONTRÔLE DE COHÉRENCE dit : `decision_memory.ledger_health(memory)` —
doublons de decision_id, outcomes orphelins (sans décision), outcomes dont
la version diffère de celle de leur décision (mélange interdit), entrées
corrompues (non-dict). Statut SAIN / ANOMALIES, comptes exacts, basis
lisible, déterministe. Servi dans /api/skyler/memory (`ledger_health`),
badge UI dans la carte Mémoire SEULEMENT si anomalie. SW v102 → v103.
"""
import re

import pytest

from vertex.engines import decision_memory as DM


def _rec(i, version='vH'):
    return {'decision_id': 'h%03d' % i, 'symbol': 'H%03d' % i,
            'engine_version': version, 'decision': 'ATTENDRE', 'level': 'A'}


def _out(decision_id, version='vH'):
    return {'decision_id': decision_id, 'engine_version': version,
            'sessions_observed': 5, 'horizons': {}}


# ─── Moteur : contrôle de cohérence honnête et déterministe ─────────────────────

def test_healthy_ledger_says_sain():
    mem = {'schema': 1, 'decisions': [_rec(1), _rec(2)],
           'outcomes': [_out('h001')]}
    h = DM.ledger_health(mem)
    assert h['status'] == 'SAIN'
    assert h['duplicate_decision_ids'] == 0
    assert h['orphan_outcomes'] == 0
    assert h['version_mismatches'] == 0
    assert h['corrupted_entries'] == 0
    assert h['basis']


def test_duplicate_ids_detected():
    """append_decision refuse les doublons — mais un magasin édité hors moteur
    peut en contenir : le contrôle les DIT (jamais réparés en silence)."""
    mem = {'schema': 1, 'decisions': [_rec(1), _rec(1), _rec(2)], 'outcomes': []}
    h = DM.ledger_health(mem)
    assert h['status'] == 'ANOMALIES' and h['duplicate_decision_ids'] == 1


def test_orphan_outcomes_detected():
    mem = {'schema': 1, 'decisions': [_rec(1)],
           'outcomes': [_out('h001'), _out('fantome')]}
    h = DM.ledger_health(mem)
    assert h['status'] == 'ANOMALIES' and h['orphan_outcomes'] == 1


def test_version_mismatch_detected():
    """Un outcome mesuré sous une AUTRE version que sa décision = mélange de
    versions interdit par la discipline du ledger — TOUJOURS dit."""
    mem = {'schema': 1, 'decisions': [_rec(1, version='0.8.0')],
           'outcomes': [_out('h001', version='0.9.0')]}
    h = DM.ledger_health(mem)
    assert h['status'] == 'ANOMALIES' and h['version_mismatches'] == 1


def test_corrupted_entries_counted_never_crash():
    mem = {'schema': 1, 'decisions': ['x', 42, None, _rec(1)],
           'outcomes': ['y', _out('h001')]}
    h = DM.ledger_health(mem)
    assert h['corrupted_entries'] == 4
    assert h['status'] == 'ANOMALIES'


def test_empty_and_degenerate_memory_honest():
    for mem in (None, {}, DM.empty_memory(),
                {'decisions': 'corrompu', 'outcomes': None}):
        h = DM.ledger_health(mem)
        assert h['status'] in ('SAIN', 'ANOMALIES') and 'basis' in h


def test_ledger_health_deterministic():
    mem = {'schema': 1, 'decisions': [_rec(1), _rec(1)], 'outcomes': [_out('z')]}
    assert DM.ledger_health(mem) == DM.ledger_health(mem)


# ─── Route : servi dans /api/skyler/memory ──────────────────────────────────────

def test_memory_route_serves_ledger_health(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    d = terminal.app.test_client().get('/api/skyler/memory').get_json()
    assert d['ledger_health']['status'] == 'SAIN'


# ─── UI : badge SEULEMENT si anomalie + SW v103 ─────────────────────────────────

def test_memory_card_wires_ledger_health_badge():
    import terminal
    body = terminal.app.test_client().get(
        '/journal', follow_redirects=True).get_data(as_text=True)
    assert 'ledger_health' in body
    assert 'ANOMALIES' in body                     # condition d'affichage du badge


def test_service_worker_bumped_to_at_least_v103():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 103
    assert 'td-shell-v102' not in body
