"""LOT 623 — Options : contexte unique, hiérarchie graphique et détails."""
from __future__ import annotations

import re

from html.parser import HTMLParser
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'vertex/ui/pages/options_intel_page.py'
CONTEXT = ROOT / 'vertex/static/vertex/js/pages/options-context.js'
INTEL = ROOT / 'vertex/static/vertex/js/pages/options-intel.js'
SCANNER = ROOT / 'vertex/static/vertex/js/pages/options-scanner.js'
STRUCTURE = ROOT / 'vertex/static/vertex/js/pages/options-structure.js'
#  Lot 24 : la barre de contexte Options est régie par la couche SERVIE
#  (rapatriée au §24 de vertex-2-0.css) — neon-glass.css est supprimée.
THEME = ROOT / 'vertex/static/vertex/css/vertex-2-0.css'


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


def test_aucune_vue_servie_n_est_orpheline(client):
    """VERTEX 2.0 — la garantie est PLUS FORTE, pas plus faible.

    Trois vues — `overview`, `radar`, `scenarios` — étaient SERVIES (routes 200,
    contenu intact) mais **cachées de la barre d'onglets** : aucun chemin de
    l'interface n'y menait. Le banc d'origine se contentait de vérifier qu'elles
    empruntaient le contexte visuel de Structure, faute de mieux.

    Elles ont désormais chacune leur onglet, sous le nom du contrat — `radar`
    EST le Scanner qu'il réclame. Ce banc garde la propriété générale : toute
    vue servie est atteignable, et elle se marque courante quand on y est.
    """
    from vertex.ui.pages import options_intel_page as page
    for vid, label in page._ALL_VIEWS:
        html = _html(client, vid)
        assert 'data-view-tab="%s"' % vid in html, (
            '%s est servie mais n\'a aucun onglet : aucun chemin de '
            'l\'interface n\'y mène' % vid)
        #  Un seul onglet courant, et c'est le sien.
        courants = re.findall(r'aria-current="page"[^>]*>([^<]+)', html)
        assert courants == [label], (vid, courants)


def test_plus_aucune_vue_n_est_declaree_orpheline():
    """`_LEGACY_VIEWS` doit rester vide : une vue hors barre est inatteignable."""
    from vertex.ui.pages import options_intel_page as page
    assert page._LEGACY_VIEWS == (), (
        'une vue est de nouveau servie hors de la barre d\'onglets : '
        'elle serait inatteignable depuis l\'interface')
    assert page._VIEW_PARENT == {}, (
        'une vue emprunte de nouveau le contexte d\'une autre plutôt que '
        'd\'avoir le sien')

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
    #  Lot 24 : le contrat suit la feuille SERVIE. La grille est celle du §24
    #  (4 colonnes desktop), plus l'ancienne 3-colonnes de la feuille morte —
    #  qui n'a jamais été rendue à l'écran.
    css = THEME.read_text(encoding='utf-8')
    assert '#vx-content[data-space="options"] .vx-options-context' in css
    assert 'grid-template-columns:minmax(220px,1fr) minmax(180px,260px) auto auto' in css
    assert '@media (max-width:640px)' in css
    assert 'grid-template-columns:minmax(0,1fr)' in css
    bloc = css[css.find('24. La barre de contexte des Options'):]
    assert 'box-shadow:0 0' not in bloc, 'aucun glow dans le bloc options'
