"""
LOT 184 — Extension de l'inventaire de vie/mort (lot 183) aux COUCHES
JS/CSS de terminal.py. CONSTAT (documenté, rien supprimé) : les 35
chaînes de couche (_*_JS/_*_CSS) du monolithe ne nourrissent QUE les
25 pages mortes — leurs seules cibles d'assemblage sont des PAGE_*
(mortes, lot 183) ou d'autres couches ; les deux seuls helpers qui
les touchent (_vpage, _rail) ne sont appelés qu'au niveau module pour
construire des PAGE_* mortes. Recoupement EMPIRIQUE : les marqueurs
de ces couches n'apparaissent dans AUCUNE page réellement servie.
"""
import ast
import re

import pytest

import terminal
from tests.test_legacy_pages_life_lot183 import _DEAD_PAGES

_SRC = open('terminal.py', encoding='utf-8').read()
_LAYER_RE = r'^(_[A-Z][A-Z0-9_]*(?:_JS|_CSS|_HTML))\s*='

# Inventaire EXACT des 35 couches au moment du constat (lot 184).
_LAYERS = {
    '_BASE_CSS', '_BASE_JS', '_BORDEL_JS', '_BORDEL_MARKET_JS', '_BRIEF_JS',
    '_CAT_JS', '_COMPARE_JS', '_DECJ_JS', '_DESK_COCKPIT_JS', '_HEALTH_JS',
    '_HEATMAP_JS', '_OPP_BRIEF_JS', '_OV_EXTRA_JS', '_PLAYBOOK_CSS',
    '_PLAYBOOK_JS', '_PORTSIM_JS', '_RAIL_CSS', '_READ_CSS', '_RECO_JS',
    '_RESEARCH_JS', '_REVIEW_JS', '_SCATTER_HELP_JS', '_SECT_JS',
    '_SETTINGS_JS', '_SI_CSS', '_SI_JS', '_STOCKS_JS', '_STRATTOP_JS',
    '_STRAT_EMBED_JS', '_STRAT_PAGE_CSS', '_SUIVI_JS', '_TRADES_JS',
    '_VPAGE_CSS', '_VXSCATTER_JS', '_WEEKLY_CSS'}


def test_inventaire_exact_des_35_couches():
    assert set(re.findall(_LAYER_RE, _SRC, re.M)) == _LAYERS


def test_aucune_couche_utilisee_dans_une_fonction_sauf_les_assembleurs():
    # Si une couche apparaissait dans une VUE, elle serait vivante — seuls les
    # deux helpers d'assemblage (_vpage, _rail) y touchent.
    tree = ast.parse(_SRC)
    porteurs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id in _LAYERS:
                    porteurs.add(node.name)
    assert porteurs == {'_vpage', '_rail'}


def test_toutes_les_cibles_d_assemblage_sont_mortes():
    # Chaque assignation module-niveau consommant une couche vise une PAGE_*
    # morte (lot 183) ou une autre couche — jamais autre chose.
    tree = ast.parse(_SRC)
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AugAssign)):
            used = {n.id for n in ast.walk(node)
                    if isinstance(n, ast.Name) and n.id in _LAYERS}
            if not used:
                continue
            tgt = node.targets[0] if isinstance(node, ast.Assign) else node.target
            name = getattr(tgt, 'id', None)
            assert name in _DEAD_PAGES or name in _LAYERS, (name, used)


def test_vpage_appele_au_module_seulement_vers_des_pages_mortes():
    cibles = re.findall(r'^(\w+)\s*=\s*_vpage\(', _SRC, re.M)
    assert len(cibles) == 20
    assert set(cibles) <= _DEAD_PAGES
    # _rail n'est appelé NULLE PART : le helper lui-même est mort (sa CSS,
    # _RAIL_CSS, n'est appliquée que directement sur PAGE_DAILY morte).
    tree = ast.parse(_SRC)
    appels = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
              and n.func.id == '_rail']
    assert appels == []


def test_recoupement_empirique_marqueurs_absents_des_pages_servies():
    # Les identifiants signés des couches mortes (heatmap du vault, tableau
    # artistique de l'ancien accueil) n'apparaissent dans AUCUNE page servie.
    routes = ('/', '/markets', '/opportunities', '/portfolio', '/journal',
              '/options', '/system', '/tracking', '/intelligence',
              '/titre/AAPL', '/analysis/AAPL')
    c = terminal.app.test_client()
    for r in routes:
        html = c.get(r, follow_redirects=True).get_data(as_text=True)
        assert 'hmHost' not in html, r                   # _HEATMAP_JS (vault mort)
        assert 'artBoard' not in html, r                 # home_art sur PAGE_DAILY morte
