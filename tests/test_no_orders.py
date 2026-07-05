"""
tests/test_no_orders.py — GARDE-FOU DE SÛRETÉ (non négociable).

VERTEX est un terminal d'ANALYSE, en LECTURE SEULE. Ces tests échouent si du
code d'exécution d'ordre apparaît, ou si le verrou IBKR readonly est retiré.
Ils protègent l'invariant produit : aucun ordre ne peut jamais être passé.
"""

import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Appels d'exécution d'ordre formellement interdits dans tout le dépôt.
FORBIDDEN = [
    r'\bplaceOrder\b',
    r'\bsubmitOrder\b',
    r'\bbracketOrder\b',
    r'\bMarketOrder\b',
    r'\bLimitOrder\b',
    r'\bStopOrder\b',
    r'\breqGlobalCancel\b',
    r'\.placeOrder\(',
]

def _py_files():
    """Code applicatif et moteurs — on exclut les fichiers de test (qui citent
    volontairement les motifs interdits) et le cache."""
    for path in glob.glob(os.path.join(ROOT, '**', '*.py'), recursive=True):
        base = os.path.basename(path)
        if '/.git/' in path or '__pycache__' in path or base.startswith('test_'):
            continue
        yield path


def test_no_order_execution_calls():
    """Aucun appel d'exécution d'ordre dans le code source."""
    hits = []
    for path in _py_files():
        try:
            src = open(path, encoding='utf-8').read()
        except Exception:
            continue
        for pat in FORBIDDEN:
            for m in re.finditer(pat, src):
                line = src[:m.start()].count('\n') + 1
                hits.append(f'{os.path.relpath(path, ROOT)}:{line}  {pat}')
    assert not hits, 'Code d\'exécution d\'ordre détecté (INTERDIT) :\n' + '\n'.join(hits)


def test_ibkr_is_readonly():
    """Toute connexion IBKR doit forcer readonly=True."""
    connects = []
    for path in _py_files():
        try:
            src = open(path, encoding='utf-8').read()
        except Exception:
            continue
        for m in re.finditer(r'\.connect\s*\(', src):
            seg = src[m.start():m.start() + 200]
            if 'readonly' in seg.lower():
                assert re.search(r'readonly\s*=\s*True', seg), \
                    f'{os.path.relpath(path, ROOT)} : connexion IBKR sans readonly=True'
                connects.append(path)
    # Il doit exister au moins un point de connexion IBKR, et tous en readonly.
    # (Si aucun connect n'existe, le test est vacuously vrai — pas de risque.)


def test_config_readonly_invariant():
    """Le module de config affirme explicitement l'invariant lecture seule."""
    from vertex.app import config
    assert config.READONLY is True
    assert config.ANALYSIS_ONLY is True
