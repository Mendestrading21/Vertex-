"""Gardien lot 324 — terminal.py n'accumule plus d'imports orphelins.

Après la purge É1 (lot 323), 11 imports étaient devenus inutiles : leurs
consommateurs vivaient dans les 82 définitions retirées. Ce gardien empêche
la réapparition silencieuse d'imports morts dans le monolithe.

Sont tolérés (et eux seuls) : le ré-export explicite `import *` et les
lignes marquées `# noqa: F401`, qui déclarent l'intention de ré-exporter.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _orphan_imports():
    src = (ROOT / 'terminal.py').read_text(encoding='utf-8')
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

    orphans = []
    for name, lineno in imported.items():
        if name in used or name == '*':
            continue
        if 'noqa: F401' in lines[lineno - 1]:     # ré-export déclaré
            continue
        orphans.append(f'L{lineno}: {name}')
    return sorted(orphans)


def test_no_orphan_imports_in_terminal():
    orphans = _orphan_imports()
    assert not orphans, (
        'imports orphelins dans terminal.py (les retirer ou déclarer le '
        'ré-export avec « # noqa: F401 ») :\n  ' + '\n  '.join(orphans))
