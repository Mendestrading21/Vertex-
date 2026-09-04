"""Lot 36 — strangler : la couche pages morte de terminal.py est retirée.

Mesure au runtime (lot 35→36) : les 12 gabarits de pages de terminal.py
(5 bruts `PAGE_DAILY`…`PAGE_ENTREPRISES` + 7 `_vpage`) n'étaient renvoyés
par AUCUNE route — `/`, `/watchlist`, `/entreprises`, `/bordel`, `/review`,
`/research`, `/heatmap`, `/equipe`, `/settings`, `/health`, `/daily`,
`/options-desk` appartiennent tous à `vertex.app.routes.redesign` (pages 2.0
ou redirections 301). Zéro référence aux 46 noms de la couche depuis le code
vivant (AST, mesuré). Les « doubles écrivains » myRecos/myFavs/myNotes de
cette couche étaient donc du tissu mort : le seul écrivain SERVI est
vx-entities.js.

Ce banc fige le retrait : la couche ne doit pas ressusciter.
"""
import ast
import re

import terminal

_SRC = open('terminal.py', encoding='utf-8').read()
_ARBRE = ast.parse(_SRC)

_NOMS_MORTS = [
    'PAGE_DAILY', 'PAGE_WATCHLIST', 'PAGE_OPTIONS_DESK', 'PAGE_ME',
    'PAGE_ENTREPRISES', 'PAGE_SETTINGS', 'PAGE_REVIEW', 'PAGE_RESEARCH',
    'PAGE_HEALTH', 'PAGE_HEATMAP', 'PAGE_EQUIPE', 'PAGE_BORDEL',
    '_vpage', '_VPAGE_CSS', '_NAVJS_BLOCK', '_NAVCSS_BLOCK',
    '_SETTINGS_JS', '_HEATMAP_JS', '_hub_tabs',
]


def test_terminal_ne_porte_plus_la_couche_pages():
    survivants = [n for n in _NOMS_MORTS if hasattr(terminal, n)]
    assert not survivants, (
        'la couche pages morte ressuscite dans terminal.py : %s — les pages '
        'sont servies par vertex/ui/pages, jamais par terminal' % survivants)


def test_terminal_n_importe_plus_les_modules_de_la_couche():
    """nav, home_art, sync_center, vx_kit, design_system et recommendation
    n'alimentaient QUE les gabarits morts — l'import doit partir avec eux."""
    morts = ('vertex.ui.nav', 'vertex.ui.home_art', 'vertex.ui.sync_center',
             'vertex.ui.vx_kit', 'vertex.ui.design_system')
    fautes = []
    for n in ast.walk(_ARBRE):
        if isinstance(n, ast.ImportFrom) and n.module:
            for mod in morts:
                if (n.module + '.' + '.'.join(a.name for a in n.names)).startswith(mod) \
                        or n.module == mod \
                        or (n.module == 'vertex.ui' and any('vertex.ui.' + a.name in morts for a in n.names)):
                    fautes.append(ast.unparse(n))
    assert not fautes, 'imports morts revenus dans terminal.py : %s' % fautes


def test_les_routes_heritees_redirigent_toujours():
    c = terminal.app.test_client()
    for route in ('/bordel', '/review', '/research', '/heatmap', '/equipe',
                  '/settings', '/health', '/watchlist', '/entreprises', '/daily'):
        r = c.get(route)
        assert r.status_code in (301, 302, 308), (
            '%s ne redirige plus (HTTP %s) — une page héritée redeviendrait '
            'servie sans gabarit' % (route, r.status_code))


def test_les_douze_pages_servies_repondent():
    c = terminal.app.test_client()
    for page in ('/', '/calendar', '/markets', '/opportunities', '/analysis',
                 '/options', '/simulator', '/portfolio', '/follow-up',
                 '/performance', '/intelligence', '/system'):
        r = c.get(page)
        assert r.status_code == 200, '%s → HTTP %s' % (page, r.status_code)
        assert 'text/html' in (r.content_type or '')
