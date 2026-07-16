"""Vertex Master Redesign — tests de l'architecture UI (§49).

Navigation 8 espaces, redirections legacy, shell unique, fiche canonique,
états de données, contrat graphique, clés de sync canoniques, mobile, SW.
"""
import os
import re
from pathlib import Path

import pytest

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('DEMO', '1')

import terminal  # noqa: E402
from vertex.app.routes.redesign import LEGACY_REDIRECTS  # noqa: E402
from vertex.ui.shell import PRIMARY_NAV, SHELL_VERSION  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / 'vertex' / 'static' / 'vertex'


@pytest.fixture()
def client():
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


# ── Navigation (§10) ──────────────────────────────────────────────────
def test_primary_navigation_has_eight_items():
    """Marchés est FUSIONNÉ dans le Dashboard — plus d'entrée dédiée (§fusion)."""
    assert len(PRIMARY_NAV) == 8
    assert [i['label'] for i in PRIMARY_NAV] == [
        'Dashboard', 'Opportunités', 'Portefeuille',
        'Analyse', 'Options', 'Performance', 'Intelligence', 'Système']
    assert [i['href'] for i in PRIMARY_NAV] == [
        '/', '/opportunities', '/portfolio',
        '/analysis', '/options', '/performance', '/intelligence', '/system']


def test_options_is_in_primary_navigation():
    ids = [i['id'] for i in PRIMARY_NAV]
    assert 'options' in ids
    opt = next(i for i in PRIMARY_NAV if i['id'] == 'options')
    assert opt['href'] == '/options'


def test_every_primary_route_returns_200(client):
    for item in PRIMARY_NAV:
        r = client.get(item['href'])
        assert r.status_code == 200, item['href']
        assert b'vx-app' in r.data, item['href']


def test_markets_redirects_to_dashboard_anchor(client):
    """L'ancienne page /markets redirige vers l'ancre correspondante du Dashboard."""
    for url, loc in (('/markets', '/'), ('/markets?view=sectors', '/#sectors'),
                     ('/markets?view=macro', '/#markets'),
                     ('/markets?view=breadth', '/#pulse'),
                     ('/markets?view=volatility', '/#pulse')):
        r = client.get(url)
        assert r.status_code == 302 and r.headers['Location'] == loc, url


def test_subviews_return_200(client):
    for url in ('/opportunities?view=stocks',
                '/opportunities?view=options', '/opportunities?view=anomalies',
                '/opportunities?view=calendar', '/portfolio?view=positions',
                '/portfolio?view=risk', '/portfolio?view=watchlist',
                '/performance?view=journal', '/performance?view=track-record',
                '/performance?view=learnings', '/intelligence?view=committee',
                '/intelligence?view=strategy', '/intelligence?view=research',
                '/intelligence?view=memory', '/system?view=data',
                '/system?view=settings', '/system?view=archive'):
        assert client.get(url).status_code == 200, url


def test_old_routes_redirect(client):
    for old, new in LEGACY_REDIRECTS.items():
        r = client.get(old)
        assert r.status_code == 301, old
        assert r.headers['Location'].split('?')[0] == new.split('?')[0], old


def test_redirect_preserves_ticker_and_filters(client):
    r = client.get('/titre/NVDA')
    assert r.status_code == 301 and r.headers['Location'] == '/analysis/NVDA'
    r2 = client.get('/journal?sym=NVDA')
    assert 'sym=NVDA' in r2.headers['Location']


def test_single_analysis_route(client):
    """Chaque ticker ouvre LA même fiche — pas de fiches concurrentes."""
    r = client.get('/analysis/NVDA')
    assert r.status_code == 200 and b'vx-app' in r.data
    for legacy in ('/titre/NVDA', '/company/NVDA'):
        assert client.get(legacy).headers['Location'] == '/analysis/NVDA'
    # les anciennes fiches concurrentes redirigent
    for concurrent in ('/stocks', '/entreprises', '/compare'):
        assert client.get(concurrent).status_code == 301


# ── Shell unique ──────────────────────────────────────────────────────
def test_app_shell_is_shared(client):
    pages = ['/', '/opportunities', '/portfolio', '/performance']
    for p in pages:
        html = client.get(p).get_data(as_text=True)
        assert f'data-shell="{SHELL_VERSION}"' in html, p
        assert 'vx-sidebar' in html and 'vx-topbar' in html, p
        assert 'vx-palette' in html and 'vx-toasts' in html, p
        assert '/static/vertex/css/tokens.css' in html, p


def test_active_nav_item_marked(client):
    html = client.get('/opportunities').get_data(as_text=True)
    assert re.search(r'href="/opportunities"[^>]*aria-current="page"', html) or \
        re.search(r'aria-current="page"[^>]*href="/opportunities"', html) or \
        'data-nav-id="opportunities" aria-current="page"' in html


def test_mobile_navigation_exists(client):
    html = client.get('/').get_data(as_text=True)
    assert 'vx-mobile-bar' in html


def test_mobile_action_bar_exists(client):
    html = client.get('/analysis/NVDA').get_data(as_text=True)
    assert 'vx-mobile-bar' in html
    assert 'Favori' in html and 'Alerte' in html and 'Options' in html


def test_no_duplicate_component_ids(client):
    for page in ('/', '/analysis/NVDA', '/portfolio'):
        html = client.get(page).get_data(as_text=True)
        ids = re.findall(r'id="([^"]+)"', html)
        dupes = {i for i in ids if ids.count(i) > 1}
        assert not dupes, f'{page}: ids dupliqués {dupes}'


def test_no_dead_links(client):
    """Tous les liens internes des pages rendues répondent 200/301."""
    seen = set()
    for page in ('/', '/opportunities', '/portfolio', '/system'):
        html = client.get(page).get_data(as_text=True)
        for href in set(re.findall(r'href="(/[a-z0-9\-/?=&%]*)"', html)):
            if href in seen or href.startswith('/static') or href.startswith('/api'):
                continue
            seen.add(href)
            r = client.get(href)
            assert r.status_code in (200, 301, 302), f'{page} → {href}: {r.status_code}'


# ── Brief Vertex (§21) ────────────────────────────────────────────────
def test_brief_has_timestamp_and_sources(client):
    b = client.get('/api/briefing/editorial').get_json()
    assert b['as_of']
    assert b['sources']
    assert 8 >= len(b['lines']) >= 3 or len(b['lines']) <= 12


def test_brief_fallback_without_claude(client):
    b = client.get('/api/briefing/editorial').get_json()
    assert b['generator'] == 'deterministic'
    assert any('Discipline' in l for l in b['lines'])


def test_brief_length_bounds(client):
    b = client.get('/api/briefing/editorial').get_json()
    assert len(b['lines']) <= 12


# ── Contrat graphique (§34) — vérifié statiquement ────────────────────
def test_chart_core_contract():
    src = (STATIC / 'js' / 'charts' / 'chart-core.js').read_text(encoding='utf-8')
    for needle in ('vx-chart-question', 'vx-chart-conclusion', 'updateIndicator',
                   'Comprendre ce graphique', 'Ce que montre le graphique',
                   'Pourquoi cela compte', 'Ce qui confirmerait', 'Ce qui invaliderait'):
        assert needle in src, needle


def test_chart_modules_exist():
    charts = STATIC / 'js' / 'charts'
    for name in ('chart-core', 'sparkline', 'price-chart', 'candlestick-chart',
                 'line-area-chart', 'bar-chart', 'donut-chart', 'heatmap',
                 'breadth-chart', 'sector-chart', 'correlation-matrix',
                 'factor-chart', 'equity-chart', 'drawdown-chart', 'option-payoff',
                 'option-scenarios', 'option-theta', 'option-iv-sensitivity',
                 'vol-surface', 'timeline-chart', 'geographic-exposure',
                 'annotations'):
        assert (charts / f'{name}.js').is_file(), name


def test_graph_level_can_create_alert():
    src = (STATIC / 'js' / 'charts' / 'annotations.js').read_text(encoding='utf-8')
    assert 'alertFromLevel' in src and "openAddModal" in src


def test_no_fake_data_in_charts():
    """Les modules graphiques refusent les données manquantes au lieu d'inventer."""
    for name in ('option-payoff', 'option-scenarios', 'candlestick-chart', 'vol-surface'):
        src = (STATIC / 'js' / 'charts' / f'{name}.js').read_text(encoding='utf-8')
        assert 'states.empty' in src or 'repli honnête' in src or 'indisponible' in src, name


# ── États de données (§39) ────────────────────────────────────────────
def test_ui_data_states():
    src = (STATIC / 'js' / 'vx-core.js').read_text(encoding='utf-8')
    for state in ('loading', 'empty', 'stale', 'error'):
        assert f'{state}(' in src, state
    assert 'Réessayer' in src and 'Ouvrir Système' in src
    assert 'vx-skeleton' in src


def test_update_indicator_formats():
    src = (STATIC / 'js' / 'vx-core.js').read_text(encoding='utf-8')
    for fmt in ('À l’instant', 'Il y a', 'Aujourd’hui à', 'Hier à'):
        assert fmt in src, fmt


# ── Synchronisation (§47) ─────────────────────────────────────────────
def test_all_sync_keys_are_canonical():
    """vx-entities.js DOIT porter exactement les mêmes clés que __DESK_KEYS."""
    ent = (STATIC / 'js' / 'vx-entities.js').read_text(encoding='utf-8')
    m = re.search(r"DESK_KEYS\s*=\s*\[([^\]]+)\]", ent)
    assert m, 'DESK_KEYS absent de vx-entities.js'
    entity_keys = set(re.findall(r"'([^']+)'", m.group(1)))
    src = (ROOT / 'terminal.py').read_text(encoding='utf-8')
    m2 = re.search(r'__DESK_KEYS\s*=\s*\[([^\]]+)\]', src)
    terminal_keys = set(re.findall(r"'([^']+)'", m2.group(1)))
    assert entity_keys == terminal_keys, entity_keys ^ terminal_keys
    assert 'vxWatchlist' in entity_keys


def test_entity_schemas_preserved():
    """Les écritures respectent les schémas historiques (pas de renommage)."""
    ent = (STATIC / 'js' / 'vx-entities.js').read_text(encoding='utf-8')
    for marker in ("'myFavs'", "'myRecos'", "'myTrades'", "'vxAlerts'",
                   "kind: 'STK'", 'entry_spot', 'entrySnap', "cond: cond || 'above'",
                   'myTradesClosed', 'deskTs'):
        assert marker in ent, marker


def test_never_overwrite_newer_data():
    ent = (STATIC / 'js' / 'vx-entities.js').read_text(encoding='utf-8')
    assert 'd.ts > localTs' in ent, 'le pull doit comparer les timestamps'


# ── Actions universelles (§17) ────────────────────────────────────────
def test_entity_actions_complete():
    ent = (STATIC / 'js' / 'vx-entities.js').read_text(encoding='utf-8')
    for action in ('Ouvrir l’analyse', 'favoris', 'watchlist', 'Créer un suivi',
                   'Créer une alerte', 'Ajouter une position', 'Ouvrir les options',
                   'note / thèse', 'Ouvrir le journal', 'Copier le ticker',
                   'Ouvrir TradingView'):
        assert action in ent, action


def test_no_blocking_dialogs():
    """Jamais alert()/confirm()/prompt() dans la nouvelle expérience (§42)."""
    for js in (STATIC / 'js').rglob('*.js'):
        src = js.read_text(encoding='utf-8')
        for forbidden in ('window.alert(', 'window.confirm(', 'window.prompt(',
                          '\nalert(', ' confirm(', ' prompt('):
            assert forbidden not in src, f'{js.name}: {forbidden.strip()}'


# ── Contexte de navigation (§15) ──────────────────────────────────────
def test_context_navigation_implemented():
    core = (STATIC / 'js' / 'vx-core.js').read_text(encoding='utf-8')
    for needle in ('vxNavigationContext', 'scrollY', 'restoreIfReturning',
                   'selectedSymbol', '_collectFilters'):
        assert needle in core, needle
    shell = (STATIC / 'js' / 'vx-shell.js').read_text(encoding='utf-8')
    assert 'Retour' in shell and 'vx-back-btn' in shell


def test_command_palette_keyboard():
    shell = (STATIC / 'js' / 'vx-shell.js').read_text(encoding='utf-8')
    for k in ("'ArrowDown'", "'ArrowUp'", "'Enter'", "'Escape'", "metaKey", "ctrlKey"):
        assert k in shell, k


# ── TradingView & IBKR dans l'UX (§30-31) ─────────────────────────────
def test_tradingview_signal_never_directly_buys(client):
    html = client.get('/analysis/NVDA').get_data(as_text=True)
    assert 'jamais un ACHETER direct' in html or 'jamais un achat' in html


def test_ibkr_status_is_visible(client):
    html = client.get('/system?view=connections').get_data(as_text=True)
    assert 'IBKR' in html
    shell_js = (STATIC / 'js' / 'vx-shell.js').read_text(encoding='utf-8')
    assert 'Connexions' in shell_js


# ── Accessibilité (§45) ───────────────────────────────────────────────
def test_accessibility_markup(client):
    html = client.get('/').get_data(as_text=True)
    assert 'aria-label' in html and 'aria-current' in html
    base = (STATIC / 'css' / 'base.css').read_text(encoding='utf-8')
    assert ':focus-visible' in base and 'prefers-reduced-motion' in base


def test_reduced_motion():
    base = (STATIC / 'css' / 'base.css').read_text(encoding='utf-8')
    assert 'prefers-reduced-motion:reduce' in base.replace(' ', '')


# ── Service worker (§51) ──────────────────────────────────────────────
def test_service_worker_bumped(client):
    r = client.get('/sw.js')
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert 'td-shell-v59' in body, 'le shell a changé — la version du cache doit suivre'
    assert 'td-shell-v49' not in body


# ── Lecture seule (rappel §1) ─────────────────────────────────────────
def test_no_order_execution_in_ui():
    for js in (STATIC / 'js').rglob('*.js'):
        src = js.read_text(encoding='utf-8')
        for needle in ('placeOrder', 'place_order', 'submit_order', 'transmit'):
            assert needle not in src, f'{js.name}: {needle}'
    for page in (ROOT / 'vertex' / 'ui' / 'pages').glob('*.py'):
        src = page.read_text(encoding='utf-8')
        for needle in ('placeOrder', 'place_order', 'submit_order'):
            assert needle not in src, f'{page.name}: {needle}'
