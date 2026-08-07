"""
LOT 185 — Cartographie de mort de terminal.py, volet FONCTIONS
(complète les lots 183/184 — rien supprimé). Méthode PRUDENTE (un
doute = vivant) : sont racines VIVANTES toute fonction décorée, toute
fonction référencée au niveau module (threads de fond, assemblages),
toute vue Flask active du module et toute référence externe de
production ; la vie se propage par les références internes. CONSTAT :
29 fonctions top-niveau sont mortes (62 lignes) — presque toutes les
anciens stubs de vues des pages mortes du lot 183, plus _rail
(lot 184) et _legacy_pages_redirect (remplacé par redesign).
"""
import ast

import pytest

import terminal

_SRC = open('terminal.py', encoding='utf-8').read()

# Inventaire EXACT des fonctions mortes au moment du constat (lot 185).
_DEAD_FUNCS = {
    '_legacy_pages_redirect', '_rail', 'anomalies_page', 'bordel_page',
    'brief_page', 'catalysts_page', 'compare_page', 'decisions_page',
    'entreprises_page', 'equipe_page', 'health_page', 'heatmap_page',
    'home', 'journal_page', 'my_page', 'options_desk_alias',
    'options_desk_page', 'options_lab_page', 'research_page',
    'review_page', 'sectors_page', 'settings_page', 'stocks_page',
    'strategie_page', 'strategy_os_page', 'suivi_page', 'titre_page',
    'vault_page', 'watchlist_page'}

# Boucles de fond lancées au démarrage — DOIVENT rester classées vivantes
# (garde anti-faux-positif de la méthode).
_BACKGROUND = {'_loop', '_opt_loop', '_radar_loop', '_news_loop', '_cal_loop',
               '_fund_loop', '_edge_loop', '_weekly_loop', '_indices_loop'}


def _analyse():
    tree = ast.parse(_SRC)
    funcs = {n.name: n for n in tree.body
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

    def refs(node, exclude=None):
        out = set()
        for s in ast.walk(node):
            if isinstance(s, ast.Name) and s.id in funcs and s.id != exclude:
                out.add(s.id)
            if isinstance(s, ast.Attribute) and s.attr in funcs:
                out.add(s.attr)
        return out

    roots = set()
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if n.decorator_list:                    # décorée = potentiellement branchée
                roots.add(n.name)
            continue
        roots |= refs(n)                            # référencée au niveau module
    for rule in terminal.app.url_map.iter_rules():  # vue Flask ACTIVE
        fn = terminal.app.view_functions[rule.endpoint]
        if getattr(fn, '__module__', '') == 'terminal':
            roots.add(fn.__name__)
    alive, stack = set(), list(roots)
    while stack:
        f = stack.pop()
        if f in alive or f not in funcs:
            continue
        alive.add(f)
        stack.extend(refs(funcs[f], exclude=f) - alive)
    return funcs, alive


def test_inventaire_exact_des_fonctions_mortes():
    funcs, alive = _analyse()
    assert set(funcs) - alive == _DEAD_FUNCS
    # Ressusciter (référencer/router) ou supprimer = mise à jour explicite.


def test_les_boucles_de_fond_restent_vivantes():
    # Garde anti-faux-positif : les boucles lancées au démarrage (threads)
    # sont bien classées vivantes par la méthode — la cartographie ne
    # condamne jamais un travailleur de fond.
    funcs, alive = _analyse()
    assert _BACKGROUND <= set(funcs)
    assert _BACKGROUND <= alive


def test_les_mortes_sont_les_stubs_des_pages_mortes():
    # Cohérence avec le lot 183 : hormis _rail et _legacy_pages_redirect,
    # chaque fonction morte est un stub de vue legacy (≤ 3 lignes) qui
    # retourne une PAGE_* morte ou une redirection — jamais de la logique.
    tree = ast.parse(_SRC)
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name in _DEAD_FUNCS:
            assert (n.end_lineno - n.lineno + 1) <= 4, n.name
    from tests.test_legacy_pages_life_lot183 import _DEAD_PAGES
    stubs = _DEAD_FUNCS - {'_rail', '_legacy_pages_redirect'}
    src_by = {n.name: ast.get_source_segment(_SRC, n) for n in tree.body
              if isinstance(n, ast.FunctionDef) and n.name in stubs}
    for name, seg in src_by.items():
        assert (('return PAGE_' in seg and any(p in seg for p in _DEAD_PAGES))
                or 'redirect(' in seg
                or 'render_page()' in seg), name    # page migrée vers redesign


def test_aucune_fonction_morte_n_est_exposee_par_une_route():
    # Recoupement : aucune morte n'est un endpoint actif (croisement inverse
    # de la racine « vue Flask » — si ce test casse, la méthode a un trou).
    actives = {terminal.app.view_functions[r.endpoint].__name__
               for r in terminal.app.url_map.iter_rules()
               if getattr(terminal.app.view_functions[r.endpoint],
                          '__module__', '') == 'terminal'}
    assert actives & _DEAD_FUNCS == set()


def test_poids_mort_des_fonctions_borne():
    # Le volet « fonctions » du poids mort est PETIT (62 lignes de stubs) —
    # l'essentiel du poids mort reste les blobs (lots 183/184). Ce test
    # chiffre le constat ; s'il casse, le paysage a changé : re-cartographier.
    tree = ast.parse(_SRC)
    total = sum(n.end_lineno - n.lineno + 1 for n in tree.body
                if isinstance(n, ast.FunctionDef) and n.name in _DEAD_FUNCS)
    assert total == 62
