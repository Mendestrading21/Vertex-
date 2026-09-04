"""Lot 44 — la TAILLE des graphiques est gérée, plus improvisée.

Avant : chaque page inventait ses pixels (140, 150, 220, 230, 240, 260,
320, 360…) et les corps de graphique portaient un `height` inline que la
feuille ne pouvait pas moduler — en mobile, une carte « hero » de 360 px
avalait tout l'écran d'un téléphone.

Après :

- `C.TAILLES` — l'échelle NOMMÉE (xs/s/m/l/xl/hero) ; `C.card` accepte
  `size:` et garde `height:` numérique en compat ;
- le corps émet `--vx-chart-h` et lit sa hauteur DE la variable : le pixel
  desktop ne bouge pas, mais la feuille reprend la main ;
- en mobile (≤ 640 px), `charts.css` borne toute hauteur à ~58 % de la
  largeur d'écran — politique d'écran, pas choix de page.
"""
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CORE = (RACINE / 'vertex/static/vertex/js/charts/chart-core.js').read_text(encoding='utf-8')
CSS = (RACINE / 'vertex/static/vertex/css/charts.css').read_text(encoding='utf-8')
INTEL = (RACINE / 'vertex/static/vertex/js/pages/options-intel.js').read_text(encoding='utf-8')


def test_l_echelle_des_tailles_est_declaree():
    assert 'C.TAILLES' in CORE, 'l’échelle nommée des hauteurs n’existe pas'
    for gabarit in ('xs:', 's:', 'm:', 'l:', 'xl:', 'hero:'):
        assert gabarit in CORE.split('C.TAILLES')[1][:120], gabarit


def test_le_resolveur_de_hauteur_existe():
    assert 'C.hauteur' in CORE, \
        'card() doit résoudre size/height par un chemin unique'


def test_le_corps_de_carte_emet_la_variable_de_hauteur():
    assert '--vx-chart-h' in CORE, \
        'le corps doit émettre --vx-chart-h pour rendre la main à la feuille'
    assert 'height:${opts.height || 200}px' not in CORE, \
        'le pixel inline nu est toujours là — la feuille ne peut pas moduler'


def test_le_site_manuel_d_options_intel_suit_le_meme_contrat():
    assert '--vx-chart-h' in INTEL, \
        'le vx-chart-body posé à la main doit émettre la même variable'
    assert 'style="height:320px"' not in INTEL


def test_la_feuille_borne_les_hauteurs_en_mobile():
    assert '--vx-chart-h' in CSS, 'charts.css ignore la variable de hauteur'
    assert '58vw' in CSS and 'max-width:640px' in CSS.replace(' ', ''), \
        'aucune borne mobile : un hero de 360 px avale l’écran d’un téléphone'
    #  max-height, pas height : dans une carte flex, seul un min/max borne la
    #  taille servie par l’algorithme flex (mesuré au navigateur, lot 44).
    assert 'max-height:min(var(--vx-chart-h),58vw)' in CSS.replace(' ', ''), \
        'la borne doit être un max-height — un height ne plafonne pas un item flex'
    #  Scopé aux corps OPTÉS : les corps sans variable (#an-chart, 260 px
    #  épinglés au lot 620) gardent leur contrat.
    assert '[style*="--vx-chart-h"]' in CSS, \
        'borne non scopée — elle écraserait les hauteurs épinglées par id'


def test_le_plein_ecran_garde_la_main():
    #  Le mode plein écran (vx-chart-fs) pose height:auto!important avec une
    #  spécificité supérieure : la borne mobile ne doit PAS l'écraser.
    assert 'vx-chart-fs.vx-chart-body{height:auto!important' in CSS.replace(' ', '')
