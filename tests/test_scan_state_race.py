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
def test_scan_state_jamais_reassigne():
    offenders = []
    for path in _sources():
        rel = path.relative_to(ROOT)
        if rel.as_posix() == 'vertex/app/state.py':
            continue  # LE domicile : définition autorisée
        for i, line in enumerate(path.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
            if _REASSIGN.match(line) and not line.rstrip().endswith(','):  # ,=continuation kwarg
                offenders.append(f'{rel}:{i}: {line.strip()}')
    assert not offenders, (
        'scan_state réassigné (casse la référence partagée → course/lecteurs sur objet mort):\n'
        + '\n'.join(offenders))


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
    src = inspect.getsource(terminal.scan)
    start = src.index('def _analyse_one')
    end = src.index('_t_compute = time.monotonic()')   # fin des defs worker, début du dispatch //
    worker = src[start:end]
    assert 'def _analyse_one' in worker and 'def _safe_one' in worker
    assert 'scan_state' not in worker, (
        'un worker exécuté en parallèle référence scan_state — risque de course sur '
        'l\'état partagé ; les workers doivent rester purs (lecture snapshot, écriture locale)')
