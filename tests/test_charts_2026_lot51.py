"""tests/test_charts_2026_lot51.py — SKYLER LOT 51 : graphiques niveau app 2026.

Direction utilisateur : élever le visuel des graphiques au niveau d'une app
de courtage moderne (esprit IBKR app). Livré CENTRALEMENT dans
`chart-core.js` (toutes les cartes `areaCard` du produit en bénéficient,
zéro fork de renderer) :

- courbe LISSE monotone (`cubicInterpolationMode: 'monotone'` — jamais de
  dépassement au-delà des données réelles, les points restent exacts) ;
- dégradé d'aire RICHE (3 arrêts, fondu profond vers transparent) ;
- GLOW subtil de la ligne (plugin `vxGlow`, ombre portée douce) ;
- PASTILLE DE DERNIER PRIX (plugin `vxLastDot`) : point + halo + pilule de
  prix au bord droit — la signature visuelle des apps de courtage ;
- palette : uniquement `C.colors` + suffixes alpha sur la couleur reçue
  (même idiome que l'existant — aucun littéral de couleur nouveau hors
  motif de secours déjà présent dans le fichier).

Shell visible (JS servi) → SW v107 → v108.
"""
import re

CORE = 'vertex/static/vertex/js/charts/chart-core.js'


def _src():
    return open(CORE, encoding='utf-8').read()


def test_area_uses_monotone_smoothing_never_overshoot():
    src = _src()
    assert "cubicInterpolationMode" in src
    assert "'monotone'" in src                    # jamais de faux extrêmes


def test_area_gradient_has_three_stops():
    src = _src()
    # trois addColorStop dans le dégradé de C.area (0 / médian / 1)
    area = src[src.index('C.area ='):src.index('C.bars =')]
    assert area.count('addColorStop') >= 3


def test_glow_plugin_present_and_subtle():
    src = _src()
    assert 'vxGlow' in src
    assert 'shadowBlur' in src


def test_last_price_dot_and_pill():
    src = _src()
    assert 'vxLastDot' in src
    assert 'lastValueLabel' in src or 'pilule' in src or 'pill' in src


def test_no_new_color_literals_outside_palette_and_fallbacks():
    """Aucune couleur hex nouvelle hors du bloc C.colors et des motifs de
    secours déjà présents (#151719 du tooltip). Les plugins utilisent
    C.colors ou la couleur reçue + suffixe alpha."""
    src = _src()
    hexes = set(re.findall(r"#[0-9A-Fa-f]{6}\b", src))
    # inventaire EXISTANT du fichier avant ce lot (palette + secours theme) —
    # le lot n'a le droit d'en ajouter AUCUN
    allowed = {'#DBE1E8', '#45D6E8', '#9B7BFF', '#2BBE90', '#E9555F',
               '#D9BE3C', '#BABABA', '#8A8284', '#c8bfae', '#151719',
               '#050505', '#0b0b0c', '#111315', '#817d77', '#b7b2aa',
               '#b7b3ad', '#f3f1ed'}
    assert hexes <= allowed, 'littéraux inattendus : %s' % (hexes - allowed)


def test_service_worker_bumped_to_at_least_v108():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 108
    assert 'td-shell-v107' not in body
