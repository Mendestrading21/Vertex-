"""LOT 623 — Options : contexte unique, hiérarchie graphique et détails."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'vertex/ui/pages/options_intel_page.py'
CONTEXT = ROOT / 'vertex/static/vertex/js/pages/options-context.js'
INTEL = ROOT / 'vertex/static/vertex/js/pages/options-intel.js'
SCANNER = ROOT / 'vertex/static/vertex/js/pages/options-scanner.js'
STRUCTURE = ROOT / 'vertex/static/vertex/js/pages/options-structure.js'
THEME = ROOT / 'vertex/static/vertex/css/neon-glass.css'


class _Ids(HTMLParser):
    def __init__(self, source: str):
        super().__init__()
        self.ids: list[str] = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])


@pytest.fixture(scope='module')
def client():
    import terminal
    return terminal.app.test_client()


def _html(client, view: str) -> str:
    response = client.get('/options?view=' + view)
    assert response.status_code == 200
    return response.get_data(as_text=True)


def test_every_options_view_has_one_global_symbol_context(client):
    for view in ('structure', 'positioning', 'leaps', 'positions', 'volatility',
                 'events', 'overview', 'radar', 'scenarios'):
        html = _html(client, view)
        assert _Ids(html).ids.count('vx-options-symbol') == 1, view
        assert 'Analyse uniquement · aucun ordre' in html
        assert '/static/vertex/js/pages/options-context.js' in html


def test_legacy_views_are_visually_attached_to_structure(client):
    for view in ('overview', 'radar', 'scenarios'):
        html = _html(client, view)
        assert 'data-view-tab="structure"' in html
        assert 'data-view-tab="structure">Structure</a>' in html
        # Structure est le seul tab actif, pas un écran sans contexte sélectionné.
        prefix = html.split('data-view-tab="structure"')[0]
        #  VERTEX 2.0 : les onglets sont de VRAIS liens dans un `<nav>`, pas un
        #  `role="tablist"`. L'attribut correct pour « la page courante » est
        #  alors `aria-current="page"` ; `aria-selected` n'a de sens que sur un
        #  onglet ARIA. L'exigence est la meme : Structure est le seul actif.
        assert 'aria-current="page"' in prefix[-160:]


def test_options_removed_embedded_style_and_implementation_language():
    source = PAGE.read_text(encoding='utf-8')
    assert '_STYLE = ""' in source
    assert '<style>' not in source
    assert 'Domicile canonique' not in source
    assert 'Constitution §18' not in source
    assert 'Règle de sécurité' in STRUCTURE.read_text(encoding='utf-8')


def test_structure_and_volatility_have_one_visible_hero_plus_progressive_detail(client):
    structure = _html(client, 'structure')
    assert 'class="vx-hero-grid vx-mt3"' in structure
    assert 'Comparer les contrats et voir la méthode' in structure
    volatility = _html(client, 'volatility')
    assert 'class="vx-hero-grid vx-mt3"' in volatility
    assert 'Cône estimé, intérêt ouvert et smile' in volatility
    assert 'id="vx-opt-term"' in volatility


def test_volatility_charts_expose_axes_spot_and_no_smoothing():
    source = INTEL.read_text(encoding='utf-8')
    for label in ('Échéance (DTE)', 'Volatilité implicite (%)',
                  'Open interest (contrats)', 'Strike'):
        assert label in source
    assert 'spotLinePlugin' in source
    assert "tension: 0" in source
    assert "variant: 'hero'" in source
    assert 'Estimation lognormale' in source


def test_options_tables_keep_essential_columns_and_open_details_in_drawer():
    scanner = SCANNER.read_text(encoding='utf-8')
    positions = STRUCTURE.read_text(encoding='utf-8')
    assert 'data-candidate=' in scanner and 'vx-row-open' in scanner
    assert "openDrawer((c.sym || 'Contrat')" in scanner
    assert 'data-option-position=' in positions and 'vx-row-open' in positions
    assert "openDrawer(esc(t.sym) + ' · position option'" in positions
    assert '<th class="vx-num">Coût</th>' not in positions
    assert '<th class="vx-num">Invalidation</th>' not in positions


def test_options_context_propagates_symbol_and_never_executes():
    source = CONTEXT.read_text(encoding='utf-8')
    assert "VX.store.set('active_ticker', sym)" in source
    assert "page.searchParams.set('sym', sym)" in source
    assert 'button.click()' in source
    for forbidden in ('/order', '/trade', '/execute', 'BUY', 'SELL'):
        assert forbidden not in source


def test_options_css_uses_shared_tokens_and_mobile_single_column():
    css = THEME.read_text(encoding='utf-8')
    assert '.vx-content[data-space="options"] .vx-options-context' in css
    assert 'grid-template-columns:minmax(220px,1fr) minmax(180px,260px) auto' in css
    assert '@media (max-width:640px)' in css
    assert 'grid-template-columns:minmax(0,1fr)' in css
    assert 'box-shadow:0 0' not in css[css.rfind('/* ══ OPTIONS'):]
