"""
tests/test_nav.py — La navigation a UNE source (Ch. II, loi anti-duplication).

vertex/ui/nav.py est la vérité ; terminal.py la réinjecte dans toutes les pages.
Ce test échoue si une page réintroduit sa propre copie divergente.
"""

import terminal  # noqa: E402  (conftest a déjà neutralisé IBKR/gate)
from vertex.ui import nav


_INLINE_PAGES = ['PAGE_DAILY', 'PAGE_WATCHLIST', 'PAGE_OPTIONS_DESK',
                 'PAGE_ME', 'PAGE_ENTREPRISES', 'PAGE_TITRE']


def test_items_wellformed_and_unique():
    for path, icon, label in nav.ITEMS:
        assert path.startswith('/') and icon and label
    paths = nav.paths()
    assert len(paths) == len(set(paths))       # aucun doublon de chemin


def test_every_inline_page_uses_the_single_source():
    want = 'var NAV=' + nav.nav_array_js()
    for pg in _INLINE_PAGES:
        src = getattr(terminal, pg)
        assert want in src, pg + ' ne référence pas la nav source unique'
        assert src.count('var NAV=') == 1       # pas de copie résiduelle


def test_shell_pages_inherit_single_source():
    # Les pages _vpage tirent leur nav du bloc extrait de PAGE_DAILY.
    assert nav.nav_array_js() in terminal._NAVJS_BLOCK


def test_core_workflows_are_in_nav():
    # La nav redessinée (design 2026-07-08) : les pages cœur restent navigables.
    for path in ('/', '/stocks', '/options', '/journal', '/settings'):
        assert path in nav.paths()
