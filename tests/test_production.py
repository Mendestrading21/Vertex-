"""
tests/test_production.py — Durcissement production (Ch. XV).

En-têtes de sécurité sur toutes les réponses, erreurs propres (JSON pour
l'API, page marquée pour l'utilisateur), limite de payload, et cohérence
de la couche de synchronisation (une seule liste de clés desk).
"""

import re

import terminal


def _client():
    return terminal.app.test_client()


def test_security_headers_on_every_response():
    r = _client().get('/healthz')
    assert r.headers['X-Content-Type-Options'] == 'nosniff'
    # SAMEORIGIN (pas DENY) : la Home embarque ses propres pages en iframe (?embed=1) —
    # DENY les bloquait silencieusement ; le clickjacking externe reste interdit.
    assert r.headers['X-Frame-Options'] == 'SAMEORIGIN'
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
    """L'ancre littérale des 17 clés de sync, comparée au JS RÉELLEMENT servi.

    Historique (lots 381/394/37) : les anciennes références (vx_kit.JS,
    journal.JS) n'étaient PAS servies — modules retirés au lot 37. La liste
    servie vit dans vx-entities.js (+ repli inline de system_page, égalité
    gardée par test_desk_keys_servies_lot381). Ici : l'ancre complète, clé à
    clé — retirer vxAlerts ou vxWatchlist de la liste servie MORD.
    """
    attendu = {'myTrades', 'myTradesClosed', 'myTradesEquity', 'myRecos',
               'myRecosClosed', 'myCapital', 'simCash', 'simStart', 'simTrades',
               'simClosed', 'myFavs', 'myNotes', 'vxJournal', 'myTradeLog',
               'vxVault', 'vxAlerts', 'vxWatchlist'}
    ent = open('vertex/static/vertex/js/vx-entities.js', encoding='utf-8').read()
    m = re.search(r"DESK_KEYS\s*=\s*\[([^\]]+)\]", ent)
    assert m, 'DESK_KEYS absent de vx-entities.js'
    servies = set(re.findall(r"'([^']+)'", m.group(1)))
    assert servies == attendu, servies ^ attendu
    # terminal.py ne doit pas ressusciter de liste de clés (source unique)
    src = open('terminal.py', encoding='utf-8').read()
    assert 'DESK_KEYS' not in src


def test_shell_has_accessibility_rules():
    #  La couche pages de terminal.py est retirée (lot 36) : les règles
    #  d'accessibilité vivent dans les feuilles réellement servies.
    base = open('vertex/static/vertex/css/base.css', encoding='utf-8').read()
    assert ':focus-visible' in base
    assert 'prefers-reduced-motion' in base
