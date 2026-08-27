"""PRF-04 — absence de course sur `scan_state` (mutation en place, jamais réassignée).

`scan_state` (`vertex/app/state.py`) est LE dict vivant partagé : terminal.py et les
Blueprints importent le MÊME objet. L'invariant qui garantit l'absence de course :
1. il n'est JAMAIS réassigné (sinon la référence partagée casse et des lecteurs voient
   un objet mort) — seulement muté en place (`state['x']=…`, `.update`, `.pop`) ;
2. tous les modules partagent la même identité d'objet ;
3. le scan PARALLÈLE (`ThreadPoolExecutor`) suit un modèle map-and-collect : les workers
   sont PURS (lisent un snapshot en lecture seule, écrivent des objets locaux, renvoient
   un tuple) et n'écrivent JAMAIS `scan_state` — l'assemblage se fait sur le thread
   principal. Donc aucune écriture concurrente sur l'état partagé.

Régression (une réassignation, un module qui shadow l'objet, une écriture `scan_state`
glissée dans le worker parallèle) = test rouge.
"""
import inspect
import re
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Réassignation `scan_state = …` en début d'instruction : espaces AUTOUR du `=` (style
# affectation), hors `==`. Exclut les kwargs `scan_state=scan_state` (sans espaces) et les
# continuations d'appel se terminant par une virgule.
_REASSIGN = re.compile(r'^\s*scan_state\s+=\s+(?!=)')


def _sources():
    yield ROOT / 'terminal.py'
    for p in (ROOT / 'vertex').rglob('*.py'):
        yield p


# ── 1. jamais de réassignation hors sa définition canonique (state.py) ─────
def _cible_scan_state(noeud) -> bool:
    return any(isinstance(t, ast.Name) and t.id == 'scan_state'
               for t in getattr(noeud, 'targets', []))


def _reassignations(arbre, rel):
    """Les seules réassignations qui cassent la référence partagée.

    a) au niveau du **module** : l'affectation rebranche le global ;
    b) dans une fonction qui a déclaré `global scan_state` : idem.

    Tout le reste est local et ne peut rien casser.
    """
    out = []
    for n in arbre.body:
        if isinstance(n, ast.Assign) and _cible_scan_state(n):
            out.append('%s:%d: affectation au niveau module' % (rel, n.lineno))
    for n in ast.walk(arbre):
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not any(isinstance(g, ast.Global) and 'scan_state' in g.names
                   for g in ast.walk(n)):
            continue
        for x in ast.walk(n):
            if isinstance(x, ast.Assign) and _cible_scan_state(x):
                out.append('%s:%d: `global scan_state` puis affectation dans %s'
                           % (rel, x.lineno, n.name))
    return out


def test_scan_state_jamais_reassigne():
    """Le global partagé ne doit jamais être rebranché sur un autre objet.

    La version par expression régulière accusait sept fonctions qui écrivent
    `scan_state = scan_state or {}` — l'idiome de normalisation d'un
    PARAMÈTRE. Vérifié à l'AST : dans les sept, `scan_state` est un argument
    de la fonction et aucune ne déclare `global scan_state`. Le rebranchement
    y est purement local ; l'objet partagé n'est pas touché.

    Le détecteur lit donc désormais l'arbre. C'est strictement plus précis que
    le texte, et la contre-épreuve ci-dessous le prouve dans les deux sens.
    """
    offenders = []
    for path in _sources():
        rel = path.relative_to(ROOT).as_posix()
        if rel == 'vertex/app/state.py':
            continue  # LE domicile : définition autorisée
        try:
            arbre = ast.parse(path.read_text(encoding='utf-8', errors='ignore'))
        except SyntaxError:
            continue
        offenders += _reassignations(arbre, rel)
    assert not offenders, (
        'scan_state réassigné (casse la référence partagée → course/lecteurs '
        'sur objet mort):\n' + '\n'.join(offenders))


def test_le_detecteur_voit_une_VRAIE_reassignation():
    """Contre-épreuve dans les deux sens. Un détecteur qui ne verrait plus
    rien serait pire que celui qui voyait trop."""
    innocent = ast.parse('def f(scan_state=None):\n'
                         '    scan_state = scan_state or {}\n'
                         '    return scan_state\n')
    assert _reassignations(innocent, 'x.py') == []

    coupable = ast.parse('scan_state = {}\n'
                         'def g():\n'
                         '    global scan_state\n'
                         '    scan_state = {}\n')
    assert len(_reassignations(coupable, 'x.py')) == 2


# ── 2. identité partagée entre modules (même objet vivant) ─────────────────
def test_scan_state_identite_partagee():
    import terminal
    from vertex.app import state
    assert terminal.scan_state is state.scan_state, 'terminal shadow scan_state (référence divergente)'


def test_mutation_en_place_visible_partout():
    import terminal
    from vertex.app import state
    sentinel = '__prf04_probe__'
    assert sentinel not in state.scan_state
    state.scan_state[sentinel] = 42            # mutation via un import…
    try:
        assert terminal.scan_state.get(sentinel) == 42   # …visible via l'autre (même objet)
    finally:
        state.scan_state.pop(sentinel, None)


# ── 3. le worker du scan parallèle ne touche JAMAIS scan_state ─────────────
def test_worker_parallele_ne_mute_pas_scan_state():
    import terminal
    #  Le worker parallele vit dans `_scan_once` ; `terminal.scan` est
    #  l enveloppe publique et ne porte plus les defs du worker.
    src = inspect.getsource(terminal._scan_once)
    start = src.index('def _analyse_one')
    end = src.index('_t_compute = time.monotonic()')   # fin des defs worker, début du dispatch //
    worker = src[start:end]
    assert 'def _analyse_one' in worker and 'def _safe_one' in worker
    assert 'scan_state' not in worker, (
        'un worker exécuté en parallèle référence scan_state — risque de course sur '
        'l\'état partagé ; les workers doivent rester purs (lecture snapshot, écriture locale)')
