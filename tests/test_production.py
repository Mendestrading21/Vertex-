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
    """Les listes de clés de sync de `vx_kit` et `journal` sont identiques.

    Depuis la purge É1, terminal.py n'héberge plus AUCUNE liste de clés :
    les copies qu'il portait vivaient dans le JS des pages mortes retirées.

    ⚠ PÉRIMÈTRE — corrigé au lot 394. Ce test compare `vx_kit.JS` et
    `journal.JS`, et **aucun des deux n'est servi** : le lot 381 a mesuré que
    `vx_kit.JS` (21 727 o) n'atteint aucune des 8 pages, et `journal.py` est un
    module mort. La phrase « la source de vérité servie est vx_kit (kit global,
    présent sur toutes les pages) » figurait ici et **était fausse**.

    Ce que les 8 pages chargent réellement, c'est
    `vertex/static/vertex/js/vx-entities.js`, plus le repli inline de
    `system_page.py`. Retirer une clé de l'un ou l'autre laisse CE test au vert
    (vérifié par mutation au lot 394) — c'est `tests/test_desk_keys_servies_lot381.py`
    qui garde les listes SERVIES. Les deux sont complémentaires : celui-ci
    verrouille l'ancre de comparaison, celui du 381 verrouille ce que le
    navigateur reçoit.
    """
    full = ("['myTrades','myTradesClosed','myTradesEquity','myRecos','myRecosClosed',"
            "'myCapital','simCash','simStart','simTrades','simClosed','myFavs','myNotes',"
            "'vxJournal','myTradeLog','vxVault','vxAlerts','vxWatchlist']")
    from vertex.ui import vx_kit
    src = open('terminal.py', encoding='utf-8').read()
    assert full in journal.JS                       # journal
    assert full in vx_kit.JS                        # kit global (DESK_KEYS)
    # terminal.py ne doit pas ressusciter de liste de clés (source unique)
    assert 'DESK_KEYS' not in src
    # aucune ancienne liste partielle ne subsiste dans le JS servi
    served = vx_kit.JS + journal.JS
    rest = served.replace(full, '')
    assert "'myNotes','myCapital']" not in rest
    assert "'myTradeLog','vxVault']" not in served  # liste SANS vxAlerts = perte d'alertes
    assert "'vxAlerts']" not in rest                # liste SANS vxWatchlist = perte watchlist


def test_shell_has_accessibility_rules():
    assert ':focus-visible' in terminal._VPAGE_CSS
    assert 'prefers-reduced-motion' in terminal._VPAGE_CSS
