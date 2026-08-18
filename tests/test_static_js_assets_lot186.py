"""
LOT 186 — Gardien des JS STATIQUES et des liens d'assets (extension du
lot 182 : le sweep validait les blocs <script> INLINE des pages —
les fichiers chargés par src= n'étaient PAS couverts). Figé : les 31
fichiers JS du produit (hors vendor) parsent tous (node --check),
chaque asset référencé par les pages servies résout en 200 (aucun
lien mort), aucun script externe (autonomie hors-ligne), et chaque
builder de charts s'enregistre sur son espace de noms.
"""
import functools
import glob
import re
import subprocess

import pytest

import terminal

_ROUTES = ('/', '/markets', '/opportunities', '/portfolio', '/journal',
           '/options', '/system', '/tracking', '/intelligence',
           '/analysis', '/titre/AAPL', '/analysis/AAPL', '/widget-lab',
           '/design-system')
# `/analysis` (index) ajouté au lot 359 — ses liens d'assets n'étaient couverts
# ni ici ni par le lot 182 (voir SKYLER-LOT-359.md).


def _js_files():
    return sorted(f for f in glob.glob('vertex/static/**/*.js', recursive=True)
                  if '/vendor/' not in f)


# ── Syntaxe : chaque fichier JS du produit parse ─────────────────────────────

def test_tous_les_fichiers_js_du_produit_parsent():
    fichiers = _js_files()
    assert len(fichiers) >= 30                      # anti-vide : le gardien contrôle
    erreurs = []
    for f in fichiers:
        r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
        if r.returncode != 0:
            erreurs.append((f, (r.stderr.strip().splitlines() or ['?'])[-1]))
    assert erreurs == []


def test_seul_vendor_est_exclu_du_gardien():
    # Le seul JS non contrôlé est la bibliothèque tierce minifiée (chandeliers).
    vendor = [f for f in glob.glob('vertex/static/**/*.js', recursive=True)
              if '/vendor/' in f]
    assert vendor == ['vertex/static/vertex/js/vendor/'
                      'lightweight-charts.standalone.production.js']


# ── Liens d'assets : rien de mort, rien d'externe ────────────────────────────

@functools.lru_cache(maxsize=1)
def _assets():
    c = terminal.app.test_client()
    srcs = set()
    for r in _ROUTES:
        html = c.get(r, follow_redirects=True).get_data(as_text=True)
        srcs |= set(re.findall(r'<script[^>]*\bsrc="([^"]+)"', html))
        srcs |= set(re.findall(r'<link[^>]*\bhref="([^"]+\.css[^"]*)"', html))
    return srcs


def test_aucun_asset_reference_n_est_mort():
    c = terminal.app.test_client()
    assert len(_assets()) >= 40                     # anti-vide
    morts = [s for s in _assets()
             if not s.startswith('http')
             and c.get(s.split('?')[0]).status_code != 200]
    assert morts == []


def test_aucun_script_ni_style_externe():
    # Autonomie hors-ligne (acquis lots 81-85 : polices auto-hébergées) :
    # aucune page ne référence un asset http(s) externe.
    assert [s for s in _assets() if s.startswith('http')] == []


# ── Espaces de noms des builders ─────────────────────────────────────────────

def test_chaque_builder_charts_s_enregistre_sur_son_namespace():
    # Les builders s'attachent à VXCharts ; seule exception : le thème,
    # chargé AVANT chart-core, qui expose VXChartTheme (miroir de palette.py,
    # gardé par test_js_theme_matches_python_palette).
    for f in sorted(glob.glob('vertex/static/vertex/js/charts/*.js')):
        src = open(f, encoding='utf-8').read()
        if f.endswith('chart-theme.js'):
            assert 'VXChartTheme' in src
        else:
            assert 'VXCharts' in src, f
