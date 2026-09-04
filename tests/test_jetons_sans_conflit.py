"""tests/test_jetons_sans_conflit.py — LOT 25 : VX2-DESIGN-02.

Mesuré : 12 jetons `--vx-*` étaient définis avec DEUX valeurs différentes
hors contexte media — tokens.css portait encore la marque verte abandonnée
(#84aa31…), glass.css la corrigeait par cascade. La cascade rendait la
bonne couleur, mais tokens.css MENTAIT à quiconque le lisait comme source.
Cible : hors surcharges media (responsive volontaire) et hors couche
finale (vertex-2-0.css, qui arbitre par conception), un jeton n'a qu'UNE
valeur. Né ROUGE.
"""
import collections
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(RACINE, 'vertex', 'static', 'vertex', 'css')


def _defs_root(path):
    """Définitions --vx-* dans les blocs `:root{…}` HORS media — le vrai
    « propriétaire de jeton ». Une redéfinition scopée (`.vx-theme-x{…}`)
    est un thème local légitime, pas un conflit."""
    src = open(path, encoding='utf-8').read()
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    defs = []
    for m in re.finditer(r'(?:^|\})\s*:root\s*\{([^}]*)\}', src):
        avant = src[:m.start()]
        if avant.count('@media') and avant.rfind('@media') > avant.rfind('}}'):
            continue          # :root dans un @media : surcharge responsive
        defs += re.findall(r'(--vx[a-z0-9-]*)\s*:\s*([^;}]+)[;}]', m.group(1))
    return defs


def test_un_jeton_une_valeur_hors_couche_finale():
    defs = collections.defaultdict(set)
    for f in sorted(os.listdir(CSS)):
        if not f.endswith('.css') or f == 'vertex-2-0.css':
            continue
        for name, val in _defs_root(os.path.join(CSS, f)):
            defs[name].add((f, val.strip()))
    conflits = {k: sorted(v) for k, v in defs.items()
                if len({val for _, val in v}) > 1}
    assert not conflits, (
        'jetons définis avec plusieurs valeurs (hors media, hors couche '
        'finale) : %s' % conflits)
