"""
tests/test_production.py — Durcissement production (Ch. XV).

En-têtes de sécurité sur toutes les réponses, erreurs propres (JSON pour
l'API, page marquée pour l'utilisateur), limite de payload, et cohérence
de la couche de synchronisation (une seule liste de clés desk).
"""

import re

import terminal
from vertex.ui import journal


def _client():
    return terminal.app.test_client()


def test_security_headers_on_every_response():
    r = _client().get('/healthz')
    assert r.headers['X-Content-Type-Options'] == 'nosniff'
    assert r.headers['X-Frame-Options'] == 'DENY'
    assert 'strict-origin' in r.headers['Referrer-Policy']
    assert 'camera=()' in r.headers['Permissions-Policy']


def test_hsts_only_behind_https():
    c = _client()
    assert 'Strict-Transport-Security' not in c.get('/healthz').headers
    r = c.get('/healthz', headers={'X-Forwarded-Proto': 'https'})
    assert 'max-age=31536000' in r.headers['Strict-Transport-Security']


def test_api_404_is_json():
    r = _client().get('/api/nexiste-pas')
    assert r.status_code == 404
    assert r.get_json()['error'] == 'not_found'


def test_page_404_is_branded_html():
    r = _client().get('/page-fantome')
    assert r.status_code == 404
    assert b'404' in r.data and 'Market Overview'.encode() in r.data


def test_payload_cap_is_set():
    assert terminal.app.config['MAX_CONTENT_LENGTH'] == 2 * 1024 * 1024


def test_oversized_desk_payload_is_rejected():
    c = _client()
    blob = {'ts': 1, 'data': {'x': 'a' * (3 * 1024 * 1024)}}
    import json as _json
    r = c.post('/api/desk', data=_json.dumps(blob), content_type='application/json')
    assert r.status_code == 413


def test_desk_sync_keys_single_source_of_truth():
    """Toutes les listes de clés de sync (desk, journal, watchlist) sont identiques."""
    full = ("['myTrades','myTradesClosed','myTradesEquity','myRecos','myRecosClosed',"
            "'myCapital','simCash','simStart','simTrades','simClosed','myFavs','myNotes',"
            "'vxJournal','myTradeLog','vxVault','vxAlerts']")
    src = open('terminal.py', encoding='utf-8').read()
    assert full in journal.JS                       # journal
    assert src.count(full) >= 3                     # desk (__DESK_KEYS) + suivi push/pull
    # aucune ancienne liste partielle ne subsiste
    assert "'myNotes','myCapital']" not in src.replace(full, '')
    assert "'myTradeLog','vxVault']" not in src     # liste SANS vxAlerts = perte d'alertes
    # le kit global (vx_kit) référence les mêmes clés + vxAlerts
    from vertex.ui import vx_kit
    assert "'vxAlerts'" in vx_kit.JS


def test_shell_has_accessibility_rules():
    assert ':focus-visible' in terminal._VPAGE_CSS
    assert 'prefers-reduced-motion' in terminal._VPAGE_CSS
