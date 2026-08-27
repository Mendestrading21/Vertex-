"""Bumpe la version du service worker ET tout ce qui l'épingle, d'un seul geste.

Le contrat du dépôt est explicite (`test_sw_cache_scope_lot361` le dit dans son
propre message d'échec) : un changement d'actif servi sous `/static` exige, DANS
LE MÊME COMMIT, un bump de `td-shell-vN` **et** la mise à jour des gardiens de
version et de l'empreinte. Le faire à la main en six endroits, c'est en oublier
un — ce qui est déjà arrivé une fois pendant cette refonte.

Usage :
    python tools/vertex_2_0_bump_sw.py "motif du bump, en une phrase"
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SW = RACINE / 'vertex' / 'app' / 'routes' / 'system.py'
EMPREINTE_TEST = RACINE / 'tests' / 'test_sw_cache_scope_lot361.py'
GARDIENS_BODY = ('tests/test_design_system_page_lot187.py',
                 'tests/test_production_guards_canonical.py',
                 'tests/test_redesign_ui.py',
                 'tests/test_ui_v3.py')
GARDIENS_SW = ('tests/test_reconstruction_today.py',)


def empreinte_static() -> tuple[str, int]:
    """Même calcul canonique que le gardien : chemins normalisés, CRLF → LF."""
    base = RACINE / 'vertex' / 'static'
    chemins = []
    for racine, _, noms in os.walk(base):
        chemins.extend(os.path.join(racine, n) for n in noms)
    chemins.sort()
    h = hashlib.sha256()
    for p in chemins:
        h.update(os.path.relpath(p, RACINE).replace(os.sep, '/').encode())
        with open(p, 'rb') as f:
            h.update(hashlib.sha256(f.read().replace(b'\r\n', b'\n')).digest())
    return h.hexdigest(), len(chemins)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    motif = ' '.join(sys.argv[1:]).strip()

    src = SW.read_text(encoding='utf-8')
    m = re.search(r"const CACHE='td-shell-v(\d+)';", src)
    if not m:
        print('version du service worker introuvable'); return 1
    ancienne = int(m.group(1))
    nouvelle = ancienne + 1

    src = src.replace(
        f"const CACHE='td-shell-v{ancienne}';",
        f"const CACHE='td-shell-v{nouvelle}';  // v{nouvelle} : {motif}", 1)
    SW.write_text(src, encoding='utf-8')

    for rel in GARDIENS_BODY:
        p = RACINE / rel
        p.write_text(p.read_text(encoding='utf-8').replace(
            f"td-shell-v{ancienne}' in body", f"td-shell-v{nouvelle}' in body"),
            encoding='utf-8')
    for rel in GARDIENS_SW:
        p = RACINE / rel
        p.write_text(p.read_text(encoding='utf-8').replace(
            f"td-shell-v{ancienne}' in sw", f"td-shell-v{nouvelle}' in sw"),
            encoding='utf-8')

    emp, n = empreinte_static()
    t = EMPREINTE_TEST.read_text(encoding='utf-8')
    t = re.sub(r"_EMPREINTE = '[a-f0-9]{64}'", f"_EMPREINTE = '{emp}'", t, count=1)
    t = re.sub(r'^_SW_VERSION = \d+$', f'_SW_VERSION = {nouvelle}', t,
               count=1, flags=re.M)
    EMPREINTE_TEST.write_text(t, encoding='utf-8')

    # Un .pyc périmé fait mentir le gardien d'empreinte : il sert l'ancienne
    # constante et l'on croit à tort que le bump n'a pas pris.
    for racine, dirs, _ in os.walk(RACINE / 'tests'):
        for d in list(dirs):
            if d == '__pycache__':
                import shutil
                shutil.rmtree(os.path.join(racine, d), ignore_errors=True)

    print(f'service worker v{ancienne} -> v{nouvelle}')
    print(f'empreinte /static : {emp}  ({n} fichiers)')
    print('gardiens de version et empreinte mis à jour')
    return 0


if __name__ == '__main__':
    sys.exit(main())
