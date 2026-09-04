"""tests/test_perf.py — SKYLER LOT 72 : audit PERFORMANCE (programme 100 %).

Mesures réelles (Playwright, cache froid, serveur démo) : DCL 224-1021 ms
(max = premier lancement navigateur), poids total par page 515-1116 kB,
0 doublon de chargement, 0 ressource en erreur, 16 CSS (118 kB) + 8-17 JS
(336-435 kB) par page, vendor lightweight-charts (160 kB) chargé UNIQUEMENT
sur /analysis. Verdict : SAIN — lot documentaire.

Gardiens PROSPECTIFS (nés verts, dits) : ils ferment la classe « dérive
de poids » — un fichier JS/CSS première partie qui enfle au-delà du budget
ou le vendor qui fuit dans le shell casseront ces tests.
"""
import os

BUDGET_JS_KB = 64      # plus gros actuel (recalibré lot 226) : chart-core 57 kB
                       # (89 % du budget — la tournée TV lots 189-213 a coûté
                       # +18 kB de builders ; prochain palier = discuter le
                       # budget AVANT de le crever, pas le monter en douce)
BUDGET_CSS_KB = 96     # plus gros actuel : vertex-2-0.css (~65 kB) — la COUCHE
                       # DE VÉRITÉ FINALE, qui absorbe les rapatriements des
                       # feuilles mortes (neon-glass.css 47 kB SUPPRIMÉE au
                       # lot 24 : le total CSS du dépôt baisse). Palier discuté
                       # et autorisé avec le lot 24, pas monté en douce ;
                       # prochain palier = même règle.


def _walk(ext, base='vertex/static'):
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.endswith(ext):
                yield os.path.join(root, f)


def test_vendor_lightweight_charts_only_on_analysis():
    shell = open('vertex/ui/shell/__init__.py', encoding='utf-8').read()
    assert 'lightweight-charts' not in shell, (
        'le vendor 160 kB ne doit jamais être dans le shell (toutes pages)')
    ana = open('vertex/ui/pages/analysis_page.py', encoding='utf-8').read()
    assert 'lightweight-charts' in ana, (
        'le vendor doit rester chargé par la seule page qui en a besoin')


def test_first_party_js_within_budget():
    fat = [p for p in _walk('.js')
           if os.sep + 'vendor' + os.sep not in p
           and os.path.getsize(p) > BUDGET_JS_KB * 1024]
    assert not fat, f'JS première partie au-delà de {BUDGET_JS_KB} kB : {fat}'


def test_css_within_budget():
    fat = [p for p in _walk('.css')
           if os.path.getsize(p) > BUDGET_CSS_KB * 1024]
    assert not fat, f'CSS au-delà de {BUDGET_CSS_KB} kB : {fat}'
