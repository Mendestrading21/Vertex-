"""CONTINUITY LOT 2 — gardiens du shell persistant & navigation client.

Progressive-enhancement : le document complet reste servi (deep link / refresh /
sans-JS), et une requête « fragment » ne renvoie QUE le contenu + métadonnées +
scripts de page (shell conservé côté client par vx-router.js). Ces tests verrouillent
les contrats statiques ; le comportement SPA lui-même est validé au navigateur
(voir le rapport de continuite 02 (archive, retiree du depot)).
"""
#  MARCHES EST FUSIONNE DANS LE DASHBOARD (Black Glass).
#
#  `/markets` ne sert plus de page : la route redirige 302 vers `/#…`
#  pour preserver les favoris. Les listes d'espaces ci-dessous ne le
#  citent donc plus, et les appels directs visent `/`, qui porte
#  desormais ce contenu. La couverture n'est pas perdue : elle a
#  simplement suivi le contenu.
import os
from pathlib import Path

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('DEMO', '1')

import pytest

import terminal

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / 'vertex' / 'static' / 'vertex' / 'js'

SPACES = ['/', '/opportunities', '/analysis', '/portfolio',
          '/journal', '/system']   # /options existe mais repli dur (external-only)


@pytest.fixture(scope='module')
def client():
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _read(*parts):
    return open(os.path.join(*parts), encoding='utf-8').read()


# ── Progressive-enhancement : document complet TOUJOURS servi ───────────────
def test_full_document_served_without_fragment_header(client):
    """Accès direct / deep link / refresh / sans-JS → document complet inchangé."""
    html = client.get('/').get_data(as_text=True)
    assert html.lstrip().lower().startswith('<!doctype')
    assert '<div class="vx-app"' in html
    assert 'id="vx-content"' in html


def test_fragment_mode_returns_fragment_not_document(client):
    """Requête fragment → PAS de document complet, seulement contenu + métadonnées."""
    frag = client.get('/', headers={'X-Vertex-Fragment': '1'}).get_data(as_text=True)
    assert '<!doctype' not in frag.lower()
    assert '<div class="vx-app"' not in frag          # shell NON reconstruit
    assert 'class="vx-fragment"' in frag
    assert 'template class="vx-frag-content"' in frag
    assert 'template class="vx-frag-mobile"' in frag


def test_fragment_query_flag_also_works(client):
    """Le drapeau ?__frag=1 déclenche aussi le fragment (diagnostic/tests)."""
    frag = client.get('/portfolio?__frag=1').get_data(as_text=True)
    assert 'class="vx-fragment"' in frag and '<!doctype' not in frag.lower()


def test_fragment_carries_navigation_metadata(client):
    """Le fragment porte tout ce qu'il faut au routeur pour remettre à jour le shell."""
    frag = client.get('/', headers={'X-Vertex-Fragment': '1'}).get_data(as_text=True)
    for attr in ('data-title=', 'data-active="markets"', 'data-space-label=',
                 'data-page-label='):
        assert attr in frag, attr


def test_every_space_serves_a_fragment(client):
    """Chaque espace (hors Options) est navigable en client : fragment + bon data-active."""
    ids = {'/': 'briefing', '/opportunities': 'opportunities',
           '/analysis': 'analysis', '/portfolio': 'portfolio',
           #  VERTEX 2.0 : le Journal est une sous-vue de Performance ; l'espace
           #  actif que porte /journal est donc « performance ».
           '/journal': 'performance',
           '/system': 'system'}
    for url, active in ids.items():
        frag = client.get(url, headers={'X-Vertex-Fragment': '1'}).get_data(as_text=True)
        assert 'class="vx-fragment"' in frag, url
        assert f'data-active="{active}"' in frag, url


# ── Shell : routeur inclus + police non bloquante ───────────────────────────
def test_router_script_included(client):
    html = client.get('/').get_data(as_text=True)
    assert '/static/vertex/js/vx-router.js' in html


def test_font_is_non_blocking(client):
    """Polices AUTO-HÉBERGÉES (lot 81) : fonts.css local + font-display:swap,
    plus aucune requête externe (le CDN Google a été retiré du shell)."""
    html = client.get('/').get_data(as_text=True)
    assert '/static/vertex/css/fonts.css' in html
    assert 'fonts.googleapis.com' not in html and 'fonts.gstatic.com' not in html
    css = open('vertex/static/vertex/css/fonts.css', encoding='utf-8').read()
    assert 'font-display: swap' in css, 'swap = rendu jamais bloqué par la police'


# ── Cycle de vie & store côté core ──────────────────────────────────────────
def test_core_exposes_lifecycle_and_store():
    core = _read(JS, 'vx-core.js')
    for needle in ('VX.page', '_teardown', 'onLeave', 'VX.store',
                   'VX.refresh._clearPage', 'VX.bus._clearPage', 'active_session_id',
                   'active_ticker', 'nav_history'):
        assert needle in core, needle


def test_refresh_and_bus_support_persistent_scope():
    core = _read(JS, 'vx-core.js')
    assert 'persistent' in core            # tâches/abonnements de shell survivent
    assert '_pageBus' in core              # abonnements de page purgeables


def test_shell_status_task_is_persistent():
    """La tâche de statut global (shell) doit survivre aux navigations client."""
    shell = _read(JS, 'vx-shell.js')
    assert "register(loadStatus, 90000, 'status', { persistent: true })" in shell


def test_router_falls_back_hard_on_external_only_and_errors():
    """Repli navigation dure : pages external-only + toute erreur → location.href."""
    router = _read(JS, 'vx-router.js')
    assert 'external-only' in router
    assert 'X-Vertex-Fragment' in router
    assert 'popstate' in router and 'pushState' in router
    assert 'hard(href)' in router          # repli présent
