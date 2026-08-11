# -*- coding: utf-8 -*-
"""LOT 213 — gardien « aucun hex nu » étendu aux builders JS statiques.

Extension du gardien lot 212 (pages Python) aux fichiers
vertex/static/vertex/js/charts/*.js et pages/*.js. Un hex quoté n'est
toléré que :
  - comme repli d'un lookup de token : var(--…, #hex) ·
    fn('name', '#hex') · fn(obj, 'name', '#hex') · lookup || '#hex' ;
  - dans les DÉFINITIONS de palette (la source des tokens doit bien
    porter les hex quelque part) : chart-theme-obsidian-copper.js
    (le thème entier) et le bloc `C.colors = Object.assign({...})`
    de chart-core.js — exemptions DOCUMENTÉES et bornées.
Calibré contre l'état réel au lot 213 : 49 occurrences → 1 littéral
réellement nu (texte des tuiles treemap, soldé dans ce lot) + 48
légitimes.
"""
import re
import glob
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
JS_GLOBS = [
    str(ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'charts' / '*.js'),
    str(ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'pages' / '*.js'),
]
EXEMPT_FILES = {'chart-theme-obsidian-copper.js'}   # définition du thème

HEX = re.compile(r"['\"]#[0-9a-fA-F]{3,6}['\"]")
LEGIT_PREFIX = re.compile(
    r"(?:var\(--[\w-]+\s*,\s*"                       # var(--token, #hex)
    r"|\w+\(\s*'[\w-]+'\s*,\s*"                      # fn('name', '#hex')
    r"|\w+\(\s*\w+\s*,\s*'[\w-]+'\s*,\s*"            # fn(obj, 'name', '#hex')
    r"|\w+\(\s*'--[\w-]+'\s*,\s*"                    # cssv('--var', '#hex')
    r"|\|\|\s*)$"                                     # lookup || '#hex'
)


def _strip_palette_block(name, s):
    """chart-core : le bloc C.colors = Object.assign({...}, THEME.colors)
    est LA définition de la palette — exclu du scan, borné précisément."""
    if name != 'chart-core.js':
        return s
    start = s.index('C.colors = Object.assign(')
    end = s.index('}, THEME.colors);', start)
    return s[:start] + s[end:]


def _offenders():
    out = []
    for pattern in JS_GLOBS:
        for f in sorted(glob.glob(pattern)):
            name = pathlib.Path(f).name
            if name in EXEMPT_FILES:
                continue
            s = pathlib.Path(f).read_text(encoding='utf-8')
            s = _strip_palette_block(name, s)
            for m in HEX.finditer(s):
                ctx = s[max(0, m.start() - 64):m.start()]
                if LEGIT_PREFIX.search(ctx):
                    continue
                line = s.count('\n', 0, m.start()) + 1
                out.append(f'{name}:~{line} {m.group(0)}')
    return out


def test_aucun_hex_nu_dans_les_builders_js():
    off = _offenders()
    assert not off, 'littéraux couleur NUS dans les builders (tokens/var()/fallback attendus) : ' + ', '.join(off)


def test_le_treemap_utilise_le_token_texte():
    src = (ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'charts' / 'chart-core.js').read_text(encoding='utf-8')
    assert 'var(--vx-text-primary,#F8F5F3)' in src   # texte des tuiles (lot 213)
    assert '"#f3f1ed"' not in src


def test_les_exemptions_restent_bornees():
    # le thème existe (source des tokens) et le bloc palette de chart-core
    # est présent avec ses bornes exactes (sinon _strip_palette_block casse)
    theme = ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'charts' / 'chart-theme-obsidian-copper.js'
    core = (ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'charts' / 'chart-core.js').read_text(encoding='utf-8')
    assert theme.exists()
    assert 'C.colors = Object.assign(' in core
    assert '}, THEME.colors);' in core
