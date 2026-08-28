"""Lot 42 — publications ATOMIQUES et GÉNÉRATIONNÉES du scan (seconde dette
du lot 6 historique, dite aux rapports des lots 40/41).

Avant ce lot, `_scan_once` écrivait dans `scan_state` par petites touches
entre ses deux grandes publications (titres_en_echec, options démo,
analytics_packets, reconciliation_by_symbol, strat_tilt…) : un lecteur — les
routes Flask tournent sur d'autres threads — pouvait observer des `rows`
d'une génération et des dérivés d'une autre, sans aucun moyen de le savoir.

Après : TOUTE publication passe par `_publier(etat, phase, gen, bloc)` — un
SEUL `dict.update` C-level par phase (aucun entrelacement de bytecode
possible entre les clés d'un même bloc), estampillé `scan_gen` (génération
du scan) et `scan_phase` ('partiel' → 'complet', 'erreur' sinon). Un lecteur
sait désormais CE qu'il lit.
"""
import ast
import inspect
from pathlib import Path

import terminal

RACINE = Path(__file__).resolve().parent.parent


# ── Le helper lui-même ───────────────────────────────────────────────────────

def test_publier_estampille_generation_et_phase():
    etat = {}
    terminal._publier(etat, 'partiel', 7, {'rows': [1], 'breadth': 55})
    assert etat == {'rows': [1], 'breadth': 55, 'scan_gen': 7, 'scan_phase': 'partiel'}


def test_publier_ecrase_la_phase_precedente_de_la_meme_generation():
    etat = {}
    terminal._publier(etat, 'partiel', 3, {'rows': [1]})
    terminal._publier(etat, 'complet', 3, {'rows': [1], 'recommendations': []})
    assert etat['scan_phase'] == 'complet' and etat['scan_gen'] == 3


def test_generation_suit_l_etat_publie():
    assert terminal._generation({}) == 1
    assert terminal._generation({'scan_gen': 41}) == 42


# ── Gardien AST : plus AUCUNE écriture éparse dans _scan_once ────────────────

def _corps_scan_once():
    src = inspect.getsource(terminal._scan_once)
    return ast.parse('\n'.join(line[4:] if line.startswith('    ') else line
                               for line in src.splitlines()) if src.startswith('    ') else src)


def _est_scan_state(node):
    return isinstance(node, ast.Name) and node.id == 'scan_state'


def test_scan_once_ne_pose_plus_aucune_cle_a_l_unite():
    """`scan_state[...] = ...` dans _scan_once = écriture éparse — interdit."""
    arbre = _corps_scan_once()
    fautes = []
    for node in ast.walk(arbre):
        if isinstance(node, ast.Assign):
            for cible in node.targets:
                if isinstance(cible, ast.Subscript) and _est_scan_state(cible.value):
                    fautes.append(ast.dump(cible.slice)[:60])
    assert fautes == [], 'écritures éparses dans _scan_once : %r' % fautes


def test_scan_once_ne_contourne_pas_publier():
    """Même `scan_state.update(...)` direct est interdit : la publication passe
    par `_publier`, qui estampille génération et phase."""
    arbre = _corps_scan_once()
    directs = [node for node in ast.walk(arbre)
               if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
               and node.func.attr == 'update' and _est_scan_state(node.func.value)]
    assert directs == [], '%d update(s) direct(s) hors _publier' % len(directs)


def test_scan_once_publie_les_trois_phases():
    arbre = _corps_scan_once()
    phases = set()
    for node in ast.walk(arbre):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == '_publier':
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                phases.add(node.args[1].value)
    assert {'partiel', 'complet', 'erreur'} <= phases, phases


def test_les_derives_sont_publies_avec_le_bloc_complet():
    """analytics_packets / reconciliation_by_symbol / strat_tilt voyagaient
    seuls entre les deux publications — ils appartiennent au bloc complet."""
    src = inspect.getsource(terminal._scan_once)
    for cle in ('analytics_packets', 'reconciliation_by_symbol', 'strat_tilt'):
        assert "scan_state['%s']" % cle not in src, \
            '%s est encore posé à l’unité dans _scan_once' % cle
