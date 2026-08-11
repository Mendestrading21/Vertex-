"""Gardien lots 324/325 — le dépôt n'accumule plus d'imports orphelins.

Lot 324 : après la purge É1, 11 imports de `terminal.py` étaient devenus
inutiles (leurs consommateurs vivaient dans les 82 définitions retirées).
Lot 325 : le même audit étendu à tout `vertex/` a sorti 11 imports morts de
plus, répartis dans 11 modules.

Sont tolérés (et eux seuls) :
- le ré-export explicite `import *` ;
- les lignes marquées `# noqa` (F401 = ré-export ou import-diagnostic
  assumé, comme `BROKER` dans services/startup.py où l'import EST le test) ;
- `from __future__ import annotations`, qui est une directive du compilateur
  et n'est jamais référencée par un nom ;
- les `__init__.py`, dont le rôle légitime est de ré-exporter.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _orphan_imports(path: Path):
    """Noms importés par `path` et jamais référencés dedans."""
    src = path.read_text(encoding='utf-8')
    lines = src.split('\n')
    tree = ast.parse(src)

    imported = {}          # nom lié -> ligne
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported[a.asname or a.name.split('.')[0]] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                imported[a.asname or a.name] = node.lineno

    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    for n in ast.walk(tree):                      # module.attribut → module utilisé
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name):
            used.add(n.value.id)
    for n in ast.walk(tree):                      # __all__ / globals()['NOM']
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            used.add(n.value)

    orphans = []
    for name, lineno in imported.items():
        if name in used or name in ('*', 'annotations'):
            continue
        if 'noqa' in lines[lineno - 1]:           # ré-export / diagnostic déclaré
            continue
        orphans.append(f'L{lineno}: {name}')
    return sorted(orphans)


def test_no_orphan_imports_in_terminal():
    orphans = _orphan_imports(ROOT / 'terminal.py')
    assert not orphans, (
        'imports orphelins dans terminal.py (les retirer ou déclarer le '
        'ré-export avec « # noqa: F401 ») :\n  ' + '\n  '.join(orphans))


def test_no_orphan_imports_in_vertex_package():
    offenders = []
    for path in sorted((ROOT / 'vertex').rglob('*.py')):
        if path.name == '__init__.py':            # ré-export : rôle légitime
            continue
        for orphan in _orphan_imports(path):
            offenders.append(f'{path.relative_to(ROOT).as_posix()} {orphan}')
    assert not offenders, (
        'imports orphelins dans vertex/ (les retirer, ou marquer « # noqa: F401 » '
        'si le ré-export / l\'effet de bord est voulu) :\n  '
        + '\n  '.join(offenders))
