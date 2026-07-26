"""CONTINUITY LOT 5 — gardiens de la session atomique + bascule.

Manifest de session (session_id stable dérivé du cycle de scan, intégrité), endpoint,
et bascule atomique côté client (détection nouvelle session → notification discrète,
sans recalcul). READONLY, lecture seule.
"""
import os
from pathlib import Path

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('DEMO', '1')

import pytest

import terminal
from vertex.engines import session_snapshot

ROOT = Path(__file__).resolve().parents[1]
SHELL_JS = (ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'vx-shell.js').read_text(encoding='utf-8')
CORE_JS = (ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'vx-core.js').read_text(encoding='utf-8')


@pytest.fixture(scope='module')
def client():
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


# ── Manifest (moteur pur) ───────────────────────────────────────────────────
def test_empty_state_is_honest():
    m = session_snapshot.build({})
    assert m['session_id'] is None and m['status'] == 'analyzing'
    assert m['coverage_pct'] is None and m['quality_pct'] is None
    assert m['generator'] == 'deterministic'


def test_ready_manifest_reads_scan_state():
    import time
    m = session_snapshot.build({
        'rows': [{'symbol': 'A'}, {'symbol': 'B'}], 'detail': {'A': {'x': 1}, 'B': {'x': 1}},
        'scan_ts': time.time(), 'scanned_n': 20, 'universe_n': 517, 'updated': '10:32'})
    assert m['status'] == 'ready'
    assert m['session_id'] and m['session_id'].startswith('S')
    assert m['coverage_pct'] == round(100 * 20 / 517)   # 4
    assert m['quality_pct'] == 100                        # 2/2 couverts
    assert m['error'] is False


def test_session_id_is_stable_per_cycle():
    """Même scan_ts → même session_id (base de la cohérence multi-pages)."""
    assert session_snapshot.session_id_for(1700000000.7) == 'S1700000000'
    assert session_snapshot.session_id_for(1700000000.7) == session_snapshot.session_id_for(1700000000.1)
    assert session_snapshot.session_id_for(None) is None


def test_manifest_has_no_order_path():
    import json
    blob = json.dumps(session_snapshot.build(
        {'rows': [{'symbol': 'A'}], 'detail': {'A': {}}, 'scan_ts': 1.0})).lower()
    for w in ('place_order', 'submit_order', 'transmit', 'placeorder'):
        assert w not in blob


def test_manifest_endpoint(client):
    r = client.get('/api/session/manifest')
    assert r.status_code == 200
    j = r.get_json()
    for k in ('session_id', 'status', 'coverage_pct', 'quality_pct', 'error', 'generator'):
        assert k in j


# ── Bascule atomique côté client ────────────────────────────────────────────
def test_client_watches_session_and_switches():
    assert 'watchSession' in SHELL_JS
    assert "/api/session/manifest" in SHELL_JS
    assert "'session-watch'" in SHELL_JS and 'persistent: true' in SHELL_JS
    # bascule : store actif/précédent + événements + notification
    assert "active_session_id" in SHELL_JS and "previous_session_id" in SHELL_JS
    assert "vx:session-changed" in SHELL_JS
    assert 'Analyse mise à jour' in SHELL_JS


def test_switch_is_throttled_not_spammy():
    """La notification visible est throttlée (le scan republie ~toutes les 2 min)."""
    assert 'SESSION_NOTIFY_THROTTLE' in SHELL_JS


def test_store_tracks_sessions():
    assert 'previous_session_id' in CORE_JS and 'active_session_id' in CORE_JS
