# -*- coding: utf-8 -*-
"""LOT 217 — gardien de l'invariant CLAUDE.md « scan_state muté en place —
ne JAMAIS réassigner » (vertex/app/state.py).

Lacune mesurée au lot 217 : l'invariant était documenté (state.py,
CLAUDE.md) mais épinglé par AUCUN test — on pouvait écrire
`state.scan_state = {...}` ou `scan_state = {...}` au niveau module et
casser silencieusement le partage de référence entre terminal.py et les
Blueprints (chacun garderait un objet différent).

Formes REFUSÉES dans le code produit (terminal.py + vertex/**) :
  - affectation au niveau module `scan_state = ...` (hors state.py,
    l'unique domicile) ;
  - affectation d'attribut `<obj>.scan_state = ...` (rebind du module) ;
  - `global scan_state` (préalable à une réassignation globale).
Forme LÉGITIME (constatée 5× au calibrage) : le rebind LOCAL d'un
paramètre de fonction (`scan_state = scan_state or {}`) — il ne touche
pas l'objet partagé.
"""
import ast
import glob
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOME = 'vertex/app/state.py'   # l'unique domicile de l'affectation


def _offenders_in(src, fname):
    out = []
    tree = ast.parse(src)

    def visit(node, in_func):
        for child in ast.iter_child_nodes(node):
            child_in_func = in_func or isinstance(
                child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))
            if isinstance(child, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                targets = child.targets if isinstance(child, ast.Assign) else [child.target]
                for t in targets:
                    if (isinstance(t, ast.Name) and t.id == 'scan_state'
                            and not in_func and fname != HOME):
                        out.append('%s:%d reassignation module-level' % (fname, child.lineno))
                    if isinstance(t, ast.Attribute) and t.attr == 'scan_state':
                        out.append('%s:%d affectation .scan_state' % (fname, child.lineno))
            if isinstance(child, ast.Global) and 'scan_state' in child.names:
                out.append('%s:%d global scan_state' % (fname, child.lineno))
            visit(child, child_in_func)

    visit(tree, False)
    return out


def _scan_production():
    files = [str(ROOT / 'terminal.py')] + glob.glob(str(ROOT / 'vertex' / '**' / '*.py'),
                                                    recursive=True)
    out = []
    for f in files:
        rel = pathlib.Path(f).relative_to(ROOT).as_posix()
        out.extend(_offenders_in(pathlib.Path(f).read_text(encoding='utf-8'), rel))
    return out


def test_scan_state_jamais_reassigne_dans_le_code_produit():
    off = _scan_production()
    assert off == [], ('scan_state doit être muté EN PLACE (référence partagée) : '
                       + ', '.join(off))


def test_le_domicile_unique_existe_et_definit_scan_state():
    src = (ROOT / HOME).read_text(encoding='utf-8')
    assert 'scan_state = {' in src            # la définition vit bien là
    assert 'jamais de réassignation' in src   # et la doctrine y est documentée


def test_le_scanner_detecte_bien_les_trois_formes_interdites():
    # Gardien du gardien : si le scan AST se cassait, il passerait à vide.
    mauvais = (
        'scan_state = {}\n'
        'state.scan_state = {}\n'
        'def f():\n'
        '    global scan_state\n'
        '    scan_state = {}\n'
    )
    off = _offenders_in(mauvais, 'exemple.py')
    assert len(off) == 3   # module-level + attribut + global (le rebind local est couvert par global)


def test_le_rebind_local_de_parametre_reste_legitime():
    ok = 'def f(scan_state=None):\n    scan_state = scan_state or {}\n    return scan_state\n'
    assert _offenders_in(ok, 'exemple.py') == []
