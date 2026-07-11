"""Gardiens de la migration Strategy OS : plus aucun nom personnel dans l'arbre,
plus d'ancien package legacy. Les motifs sont reconstruits dynamiquement pour
que ce fichier lui-même ne réintroduise pas d'occurrence littérale.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Motif « (el io|men des) » sans espaces — reconstruit pour rester introuvable
# par la recherche gardienne elle-même.
_FIRST = 'el' + 'io'
_LAST = 'men' + 'des'
PATTERN = re.compile(f'({_FIRST}|{_LAST})', re.IGNORECASE)

SKIP_DIRS = {'.git', 'venv', '.venv', '__pycache__', 'node_modules', '.pytest_cache'}
SKIP_SUFFIXES = {'.pyc', '.png', '.jpg', '.ico', '.woff', '.woff2', '.gz', '.zip'}


def _tracked_and_untracked_files():
    """Fichiers de l'arbre de travail (suivis + non suivis non ignorés)."""
    out = subprocess.run(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    for rel in out.splitlines():
        p = ROOT / rel
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in SKIP_SUFFIXES:
            continue
        yield p


def test_no_personal_name_in_current_tree():
    offenders = []
    for path in _tracked_and_untracked_files():
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if PATTERN.search(line):
                offenders.append(f'{path.relative_to(ROOT)}:{i}: {line.strip()[:120]}')
    assert not offenders, (
        'Noms personnels détectés dans l’arbre courant (exigence : zéro) :\n'
        + '\n'.join(offenders[:40]))


def test_no_legacy_personal_package():
    legacy_dir = ROOT / _FIRST
    assert not legacy_dir.exists(), (
        f'Le package legacy {legacy_dir.name}/ ne doit plus exister dans l’arbre.')


def test_no_legacy_imports_anywhere():
    """Aucun `import <ancien package>` ne doit subsister dans le code Python."""
    needle = re.compile(rf'(from|import)\s+{_FIRST}\b')
    offenders = []
    for path in _tracked_and_untracked_files():
        if path.suffix != '.py':
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        if needle.search(text):
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, f'Imports legacy restants : {offenders}'
