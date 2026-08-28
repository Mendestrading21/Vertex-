"""
tests/test_nav.py — La navigation a UNE source : la coque 2.0.

Historique : vertex/ui/nav.py alimentait les gabarits inline de terminal.py.
La couche pages est retirée (lot 36) et nav.py avec elle (lot 37) — la
navigation SERVIE appartient à vertex/ui/shell. Ce banc interdit toute
résurrection d'une nav inline côté terminal et garde les parcours cœur
navigables sur la coque réellement servie.
"""
import terminal


def test_terminal_ne_porte_plus_de_nav_inline():
    src = open('terminal.py', encoding='utf-8').read()
    assert 'var NAV=' not in src, (
        'terminal.py réintroduit une navigation inline — la nav servie '
        'appartient à la coque 2.0 (vertex/ui/shell)')


def test_core_workflows_navigables_sur_la_coque_servie():
    html = terminal.app.test_client().get('/').get_data(as_text=True)
    for path in ('/calendar', '/markets', '/opportunities', '/analysis',
                 '/options', '/simulator', '/portfolio', '/follow-up',
                 '/performance', '/system'):
        assert 'href="%s"' % path in html, path + ' absent de la coque'
