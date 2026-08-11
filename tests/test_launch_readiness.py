"""VERTEX — Contrôle de mise en route (« demain, tout marche à 100 % »).

Porte de vérification unique qui valide TOUT ce que la refonte CONTINUITY a modifié,
sans navigateur (client Flask), donc exécutable partout :

    python -m pytest tests/test_launch_readiness.py -q

Couvre : rendu des 8 espaces (document complet + fragment), endpoints de session,
mécaniques client (routeur, store, cache/SWR, préchargement, fraîcheur, prix, offline),
badges de fraîcheur dans les pages, invariant READONLY, cohérence du Service Worker.
Tout doit être vert avant un lancement.
"""
import os
import re
from pathlib import Path

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('DEMO', '1')

import pytest

import terminal

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / 'vertex' / 'static' / 'vertex' / 'js'
CSS = ROOT / 'vertex' / 'static' / 'vertex' / 'css'
PAGES = ROOT / 'vertex' / 'ui' / 'pages'

SPACES = {'/': 'briefing', '/markets': 'markets', '/opportunities': 'opportunities',
          '/analysis': 'analysis', '/portfolio': 'portfolio', '/options': 'options',
          '/journal': 'journal', '/system': 'system'}


@pytest.fixture(scope='module')
def client():
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _read(*p):
    return open(os.path.join(*p), encoding='utf-8').read()


# ══ 1. Les 8 espaces répondent (document complet — accès direct / refresh / sans-JS) ══
def test_all_eight_spaces_return_full_document(client):
    for url, active in SPACES.items():
        r = client.get(url)
        assert r.status_code == 200, url
        html = r.get_data(as_text=True)
        assert html.lstrip().lower().startswith('<!doctype'), url
        assert 'id="vx-content"' in html and f'data-space="{active}"' in html, url


def test_fiche_ticker_and_key_subviews_ok(client):
    for url in ('/analysis/NVDA', '/markets?view=breadth', '/opportunities?view=stocks',
                '/portfolio?view=risk', '/journal?view=journal', '/system?view=data'):
        assert client.get(url).status_code == 200, url


# ══ 2. Rendu de FRAGMENT (shell persistant / navigation continue) ══
def test_every_space_serves_a_fragment(client):
    for url, active in SPACES.items():
        frag = client.get(url, headers={'X-Vertex-Fragment': '1'}).get_data(as_text=True)
        assert '<!doctype' not in frag.lower(), url            # PAS de shell
        assert 'class="vx-fragment"' in frag, url
        assert f'data-active="{active}"' in frag, url
        assert 'template class="vx-frag-content"' in frag, url


# ══ 3. Endpoints de session (digest, manifest) ══
def test_session_endpoints(client):
    dg = client.get('/api/session/digest')
    assert dg.status_code == 200 and 'state' in dg.get_json()
    mf = client.get('/api/session/manifest')
    assert mf.status_code == 200
    j = mf.get_json()
    for k in ('session_id', 'status', 'coverage_pct', 'quality_pct', 'generator'):
        assert k in j, k


def test_health_and_ready(client):
    assert client.get('/healthz').status_code == 200
    assert client.get('/readyz').json['readonly'] is True


# ══ 4. Mécaniques client livrées (assets servis + contenu) ══
def test_shell_loads_continuity_scripts(client):
    html = client.get('/').get_data(as_text=True)
    for src in ('/static/vertex/js/vx-core.js', '/static/vertex/js/vx-router.js',
                '/static/vertex/js/vx-shell.js'):
        assert src in html, src


def test_client_core_has_all_mechanisms():
    core = _read(JS, 'vx-core.js')
    for feat in ('VX.store', 'VX.page', 'VX.swr', 'VX.fetch.invalidate', 'VX.fetch.peek',
                 'VX.fetch.stats', 'VX.freshness', 'VX.prices', 'vxDataCache', 'active_session_id'):
        assert feat in core, feat


def test_router_has_spa_and_prefetch():
    router = _read(JS, 'vx-router.js')
    for feat in ('X-Vertex-Fragment', 'pushState', 'popstate', 'function prefetch',
                 'takeFragment', 'hard(href)'):
        assert feat in router, feat


def test_shell_has_offline_and_session_watch():
    shell = _read(JS, 'vx-shell.js')
    for feat in ('setNet', "addEventListener('offline'", "addEventListener('online'",
                 'watchSession', 'Analyse mise à jour', 'Hors ligne', 'Reconnecté'):
        assert feat in shell, feat


# ══ 5. Badges de fraîcheur présents dans les pages de décision (§8) ══
def test_freshness_badges_in_pages():
    assert 'an-fresh' in _read(PAGES, 'analysis_page.py')
    assert 'VX.prices.setLive' in _read(PAGES, 'analysis_page.py')       # prix central (§9)
    assert 'vx-mk-fresh' in _read(PAGES, 'markets_page.py')
    assert 'pf-fresh' in _read(PAGES, 'portfolio_page.py')
    assert 'op-fresh' in _read(PAGES, 'opportunities_page.py')
    assert '.vx-fresh-chip' in _read(CSS, 'states.css')


def test_swr_paint_from_cache_wired():
    """Aujourd'hui + Marchés peignent depuis le cache avant de revalider (SWR)."""
    assert "VX.fetch.peek('/api/market/summary')" in _read(PAGES, 'briefing.py')
    assert "VX.fetch.peek('/scan')" in _read(PAGES, 'markets_page.py')


# ══ 6. Invariant absolu : READONLY (aucun ordre) ══
def test_readonly_invariant():
    from vertex.app.config import READONLY
    assert READONLY is True
    # aucune route ne doit exposer un chemin d'ordre
    rules = ' '.join(str(r) for r in terminal.app.url_map.iter_rules()).lower()
    for forbidden in ('place_order', 'placeorder', 'submitorder', 'transmit_order'):
        assert forbidden not in rules, forbidden


# ══ 7. Service Worker : version cohérente entre shell et gardiens ══
def test_service_worker_version_consistent(client):
    sw = client.get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", sw)
    assert m, 'version SW introuvable'
    assert int(m.group(1)) >= 70, 'SW doit être au moins v70 (CONTINUITY)'


# ══ 8. Pas de valeur invalide visible sur les pages clés ══
def test_no_broken_values_on_key_pages(client):
    for url in ('/', '/markets', '/system?view=data'):
        html = re.sub(r'<script.*?</script>', '', client.get(url).get_data(as_text=True), flags=re.S)
        for bad in ('[object Object]', '>undefined<', '>NaN<', '>Infinity<'):
            assert bad not in html, f'{url}: {bad}'
