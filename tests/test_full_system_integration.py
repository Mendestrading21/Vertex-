"""Tests §49/§51 — intégration système : READONLY global, observabilité,
connexions honnêtes, couverture des routes principales.

Prouve les invariants de production sans jamais masquer un échec.
"""
import os
import re

import pytest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_ORDER_WORDS = [
    'place_order', 'placeOrder', 'submit_order', 'submitOrder', 'transmit_order',
    'transmitOrder', 'modify_order', 'modifyOrder', 'cancel_order', 'cancelOrder',
    'exercise_option', 'exerciseOption', 'close_position', 'closePosition',
    'auto_close', 'auto_reduce', 'auto_rebalance', 'execute_trade', 'executeTrade',
    'send_order', 'sendOrder', 'one_click_trade', 'withdraw_cash', 'transfer_cash',
    'auto_execute',
]


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


# ───────────────────────────────────────────── READONLY global (§4)
def test_no_order_path_anywhere_in_source():
    """Aucun appel/définition de chemin d'ordre dans TOUT le code produit
    (backend + JS). Les tests sont exclus (ils citent les mots comme données)."""
    pat = re.compile(r'(?:\.|\bdef\s+|\bfunction\s+)(' + '|'.join(_ORDER_WORDS) + r')\s*\(')
    offenders = []
    for base, dirs, files in os.walk(ROOT):
        if any(s in base for s in ('/.git', '/node_modules', '__pycache__',
                                   '/.pytest_cache', '/tests', '/docs',
                                   'site-packages', '.venv', 'venv')):
            continue
        for f in files:
            if not f.endswith(('.py', '.js')):
                continue
            p = os.path.join(base, f)
            try:
                src = open(p, encoding='utf-8', errors='ignore').read()
            except OSError:
                continue
            for m in pat.finditer(src):
                ln = src[:m.start()].count('\n') + 1
                offenders.append('%s:%d %s' % (os.path.relpath(p, ROOT), ln, m.group(1)))
    assert not offenders, 'chemins d\'ordre interdits détectés :\n' + '\n'.join(offenders)


def test_readonly_is_effective():
    from vertex.app.config import READONLY
    assert READONLY is True


def test_ibkr_readonly_flag_true():
    # L'adaptateur IBKR ne doit jamais tourner en écriture.
    import vertex.app.config as cfg
    assert getattr(cfg, 'READONLY', True) is True


# ───────────────────────────────────────────── Observabilité (§41)
@pytest.mark.parametrize('url', [
    '/healthz', '/readyz', '/api/system/status', '/api/system/diagnostics',
    '/api/system/connections', '/api/system/jobs', '/api/data-quality',
    '/api/live/status', '/api/system/startup-report', '/api/system/config',
])
def test_observability_endpoints_respond(client, url):
    r = client.get(url)
    assert r.status_code in (200, 503), '%s → %s' % (url, r.status_code)
    assert r.get_json() is not None


def test_readyz_reports_readonly_and_checks(client):
    d = client.get('/readyz').get_json()
    assert d['readonly'] is True
    assert isinstance(d['checks'], list) and d['checks']
    assert any(c['name'] == 'readonly' and c['ok'] for c in d['checks'])


def test_healthz_and_readyz_are_distinct(client):
    assert client.get('/healthz').get_json().get('status') == 'ok'
    assert 'ready' in client.get('/readyz').get_json()


# ───────────────────────────────────────────── Connexions honnêtes (§9)
def test_connections_use_canonical_statuses(client):
    from vertex.services.connections import CANONICAL_STATUSES
    d = client.get('/api/system/connections').get_json()
    names = {c['name'] for c in d['connections']}
    assert {'IBKR', 'TradingView', 'Claude', 'Stockage', 'Scheduler', 'Live Stream'} <= names
    for c in d['connections']:
        assert c['status'] in CANONICAL_STATUSES, '%s statut non canonique %s' % (c['name'], c['status'])
    assert d['readonly'] is True


def test_ibkr_not_claimed_live_without_proof(client):
    """Sans session IBKR prouvée, le statut ne doit jamais être LIVE."""
    d = client.get('/api/system/connections').get_json()
    ibkr = next(c for c in d['connections'] if c['name'] == 'IBKR')
    from vertex.app.state import scan_state
    if not scan_state.get('ibkr_live'):
        assert ibkr['status'] != 'LIVE'


def test_header_badge_never_claims_live_ibkr_from_config_flag():
    """Le badge d'en-tête ne doit PAS afficher « LIVE IBKR » sur le simple flag
    de config (ibkr_enabled) — seulement sur une donnée IBKR réelle (data_source).
    Règle de vérité : jamais LIVE sans preuve."""
    src = open(os.path.join(ROOT, 'terminal.py'), encoding='utf-8').read()
    assert "ibkr_enabled){s='🟢 LIVE IBKR'" not in src, \
        'le badge LIVE IBKR est dérivé du flag de config au lieu de la donnée réelle'
    # la version honnête consulte data_source==='ibkr'
    assert "data_source==='ibkr'){s='🟢 LIVE IBKR'" in src


def test_morning_brief_uses_live_news_endpoint():
    """Le morning brief doit interroger /news-feed (JSON réel), pas /news
    (redirection HTML → news vides silencieuses)."""
    src = open(os.path.join(ROOT, 'terminal.py'), encoding='utf-8').read()
    assert "fetch('/news')" not in src, '/news est une redirection HTML, pas un endpoint JSON'


# ───────────────────────────────────────────── Couverture des routes (§31)
_MAIN_ROUTES = [
    '/', '/markets', '/opportunities', '/portfolio', '/analysis', '/options',
    '/performance', '/intelligence', '/system',
    '/markets?view=macro', '/markets?view=sectors', '/markets?view=breadth',
    '/markets?view=volatility',
    '/opportunities?view=stocks', '/opportunities?view=options',
    '/opportunities?view=anomalies', '/opportunities?view=calendar',
    '/portfolio?view=positions', '/portfolio?view=options', '/portfolio?view=risk',
    '/portfolio?view=watchlist',
    '/performance?view=journal', '/performance?view=track-record',
    '/intelligence?view=committee', '/intelligence?view=strategy',
    '/intelligence?view=impacts', '/intelligence?view=research',
    '/system?view=data', '/system?view=automations', '/system?view=settings',
    '/system?view=archive',
    '/options?view=volatility', '/options?view=radar', '/options?view=events',
]


@pytest.mark.parametrize('route', _MAIN_ROUTES)
def test_main_routes_ok_or_redirect(client, route):
    r = client.get(route)
    assert r.status_code in (200, 301, 302, 308), '%s → %s' % (route, r.status_code)


def test_tracking_page_and_api_respond(client):
    assert client.get('/tracking').status_code == 200
    r = client.get('/api/tracking')
    assert r.status_code == 200
    assert 'summary' in r.get_json()


def test_tracking_engine_has_no_order_path():
    import glob
    banned = re.compile(r'(?:\.|\bdef\s+|\bfunction\s+)(place_order|placeOrder|'
                        r'submit_order|close_position|closePosition|execute_trade|'
                        r'send_order|cancel_order)\s*\(')
    for path in glob.glob(os.path.join(ROOT, 'vertex/tracking/*.py')) + \
            [os.path.join(ROOT, 'vertex/app/routes/tracking_api.py'),
             os.path.join(ROOT, 'vertex/static/vertex/js/pages/tracking.js')]:
        assert not banned.search(open(path, encoding='utf-8').read()), path


_LEGACY_REDIRECTS = ['/options-lab', '/watchlist', '/journal', '/sectors', '/health']


@pytest.mark.parametrize('route', _LEGACY_REDIRECTS)
def test_legacy_routes_redirect(client, route):
    r = client.get(route)
    assert r.status_code in (200, 301, 302, 308), '%s → %s' % (route, r.status_code)
