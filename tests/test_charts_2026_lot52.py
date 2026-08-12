"""tests/test_charts_2026_lot52.py — SKYLER LOT 52 : crosshair app + harmonisation.

Suite de l'axe visuel « app 2026 » (lot 51). Livré CENTRALEMENT dans
`chart-core.js` :

- CROSSHAIR type app de courtage (plugin `vxCrosshair`) : ligne de visée
  VERTICALE pointillée au survol + point actif surligné — suit le point
  actif du tooltip (mode index), jamais dessinée hors survol ;
- câblé par défaut dans `C.area` (désactivable `{crosshair:false}`) ;
- HARMONISATION `C.multiLine` sur la signature 2026 du lot 51 : lissage
  monotone (jamais de faux extrêmes), ligne 2 px, crosshair ;
- palette : uniquement `C.colors` + suffixes alpha sur la couleur reçue —
  aucun littéral de couleur nouveau (même inventaire exact que lot 51).

Shell visible (JS servi) → SW v108 → v109.
"""
import re

CORE = 'vertex/static/vertex/js/charts/chart-core.js'


def _src():
    return open(CORE, encoding='utf-8').read()


def test_crosshair_plugin_present_and_dashed():
    src = _src()
    assert 'vxCrosshair' in src
    # ligne de visée pointillée (le plugin niveaux utilise déjà setLineDash,
    # on exige le motif DANS la section du plugin crosshair)
    section = src[src.index('C.crosshairPlugin ='):src.index('C.lastDotPlugin =')]
    assert 'setLineDash' in section
    assert 'getActiveElements' in section          # suit le survol réel


def test_area_wires_crosshair_by_default():
    src = _src()
    area = src[src.index('C.area ='):src.index('C.bars =')]
    assert 'crosshair' in area
    assert 'C.crosshairPlugin' in area


def test_multiline_harmonized_on_2026_signature():
    src = _src()
    ml = src[src.index('C.multiLine ='):src.index('C.levelLines =')]
    assert "cubicInterpolationMode: 'monotone'" in ml   # jamais de faux extrêmes
    assert 'borderWidth: 1.6' in ml                      # traits fins (lot 120)
    assert 'C.crosshairPlugin' in ml                     # même visée au survol
    assert 'C.endDotsPlugin(true)' in ml                 # point terminal + nom de série
    assert 'C.softGlowPlugin()' in ml                    # halo néon doux


def test_no_new_color_literals_outside_palette_and_fallbacks():
    """Même inventaire exact que le gardien du lot 51 — le lot 52 n'a le
    droit d'ajouter AUCUN littéral hex nouveau."""
    src = _src()
    hexes = set(re.findall(r"#[0-9A-Fa-f]{6}\b", src))
    allowed = {'#D28A54', '#E1A06E', '#45D6E8', '#9B7BFF', '#2BBE90', '#E9555F',
               '#D9BE3C', '#BABABA', '#8A8284', '#989092', '#c8bfae', '#151719',
               '#050505', '#0b0b0c', '#111315', '#817d77', '#b7b2aa',
               '#b7b3ad', '#f3f1ed', '#121214', '#F8F5F3'}
    assert hexes <= allowed, 'littéraux inattendus : %s' % (hexes - allowed)


def test_service_worker_bumped_to_at_least_v109():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 109
    assert 'td-shell-v108' not in body
