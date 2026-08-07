# -*- coding: utf-8 -*-
"""LOT 212 — gardien « aucun littéral couleur NU dans les pages ».

Pérennise le balayage des lots 211-212 : un hex quoté ('#xxxxxx') dans
vertex/ui/pages/*.py n'est toléré QUE comme repli d'un lookup de token
— les formes légitimes observées dans le code :
  var(--vx-…, #hex)          repli CSS
  cc('name', '#hex')         lookup VXCharts.colors avec repli
  col('name', '#hex')        idem
  cssv('--var', '#hex')      lecture de variable CSS avec repli
  … || '#hex'                repli canvas après lookup de token
Exemption DOCUMENTÉE : widget_lab.py — le Widget Lab est la
bibliothèque design FIGÉE, sa palette de mise en scène (_LIME, _MAG,
encres musée) est délibérée et hors périmètre produit.
"""
import re
import glob
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES_GLOB = str(ROOT / 'vertex' / 'ui' / 'pages' / '*.py')
EXEMPT = {'widget_lab.py'}

HEX = re.compile(r"['\"]#[0-9a-fA-F]{6}['\"]")
LEGIT_PREFIX = re.compile(
    r"(?:var\(--[\w-]+\s*,\s*"          # var(--token, #hex)
    r"|cc\(\s*'[\w-]+'\s*,\s*"          # cc('name', '#hex')
    r"|col\(\s*'[\w-]+'\s*,\s*"         # col('name', '#hex')
    r"|cssv\(\s*'--[\w-]+'\s*,\s*"      # cssv('--var', '#hex')
    r"|\|\|\s*)$"                        # lookup || '#hex' (repli canvas)
)


def _offenders():
    out = []
    for f in sorted(glob.glob(PAGES_GLOB)):
        name = pathlib.Path(f).name
        if name in EXEMPT:
            continue
        s = pathlib.Path(f).read_text(encoding='utf-8')
        for m in HEX.finditer(s):
            ctx = s[max(0, m.start() - 48):m.start()]
            if LEGIT_PREFIX.search(ctx):
                continue
            line = s.count('\n', 0, m.start()) + 1
            out.append(f'{name}:{line} {m.group(0)}')
    return out


def test_aucun_hex_nu_dans_les_pages():
    off = _offenders()
    assert not off, 'littéraux couleur NUS (utiliser les tokens VXCharts.colors ou un repli var()/cc()/col()/cssv()/||) : ' + ', '.join(off)


def test_les_deux_sites_du_lot_212_utilisent_les_tokens():
    mk = (ROOT / 'vertex' / 'ui' / 'pages' / 'markets_page.py').read_text(encoding='utf-8')
    op = (ROOT / 'vertex' / 'ui' / 'pages' / 'opportunities_page.py').read_text(encoding='utf-8')
    assert 'VXCharts.colors.muted' in mk           # étiquettes RRG
    assert "'#bab4ac'" not in mk
    assert 'VXCharts.colors.warning' in op          # bordure démo
    assert "'#FFC857'" not in op


def test_exemption_widget_lab_est_intentionnelle():
    # le Lab existe toujours et reste hors périmètre (bibliothèque figée)
    assert (ROOT / 'vertex' / 'ui' / 'pages' / 'widget_lab.py').exists()
    assert 'widget_lab.py' in EXEMPT
