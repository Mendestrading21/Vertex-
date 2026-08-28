"""
tests/test_nav.py — La navigation a UNE source par surface servie.

Historique : vertex/ui/nav.py était réinjecté dans les gabarits inline de
terminal.py. Cette couche pages est retirée (strangler, lot 36) — la
navigation SERVIE appartient à la coque 2.0 (vertex/ui/shell). nav.py reste
un module orphelin documenté (retrait = lot dédié avec ses preuves) ; ce banc
garde ses invariants de forme et interdit à terminal.py de ressusciter une
nav inline.
"""

from vertex.ui import nav


def test_items_wellformed_and_unique():
    for path, icon, label in nav.ITEMS:
        assert path.startswith('/') and icon and label
    paths = nav.paths()
    assert len(paths) == len(set(paths))       # aucun doublon de chemin


def test_terminal_ne_porte_plus_de_nav_inline():
    src = open('terminal.py', encoding='utf-8').read()
    assert 'var NAV=' not in src, (
        'terminal.py réintroduit une navigation inline — la nav servie '
        'appartient à la coque 2.0 (vertex/ui/shell)')


def test_core_workflows_are_in_nav():
    # La nav redessinée (design 2026-07-08) : les pages cœur restent navigables.
    for path in ('/', '/stocks', '/options', '/journal', '/settings'):
        assert path in nav.paths()
