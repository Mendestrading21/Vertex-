"""tests/test_import_ibkr_unique.py — contrôle 018 : UNE porte d'import.

Mesuré : 8 fichiers importaient ib_async directement. La frontière
market-data-only mérite une porte d'import unique — ibkr_gateway — par
laquelle toute classe ib_async est obtenue (import paresseux préservé :
l'app démarre sans la dépendance). Né ROUGE.
"""
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTORISE = os.path.join('vertex', 'data_sources', 'ibkr_gateway.py')


def _fichiers_py():
    for base in ('vertex', '.'):
        for root, dirs, files in os.walk(os.path.join(RACINE, base) if base != '.' else RACINE):
            dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', 'node_modules', 'tests')]
            if base == '.' and os.path.basename(root) != os.path.basename(RACINE):
                dirs[:] = []
                files = [f for f in files if f == 'terminal.py']
            for f in files:
                if f.endswith('.py'):
                    yield os.path.join(root, f)
        if base == '.':
            break


def test_seul_le_gateway_importe_ib_async():
    fautifs = []
    motif = re.compile(r'^\s*(?:from|import)\s+ib_async\b', re.M)
    vus = set()
    for chemin in _fichiers_py():
        if chemin in vus:
            continue
        vus.add(chemin)
        rel = os.path.relpath(chemin, RACINE)
        if rel == AUTORISE:
            continue
        src = open(chemin, encoding='utf-8', errors='ignore').read()
        if motif.search(src):
            fautifs.append(rel)
    assert not fautifs, ('ib_async importé hors de la porte unique '
                         '(ibkr_gateway.classe) : %s' % sorted(set(fautifs)))


def test_la_porte_rend_les_classes_et_reste_paresseuse():
    from vertex.data_sources import ibkr_gateway as gw
    assert callable(getattr(gw, 'classe', None)), (
        'ibkr_gateway.classe(nom) doit exister — la porte unique')
    #  paresseuse : l'appel n'a lieu qu'à la demande ; ici la dépendance est
    #  installée dans l'environnement de test, la classe doit se résoudre.
    Stock = gw.classe('Stock')
    assert Stock.__name__ == 'Stock'
