"""tests/test_charts_2026_lot53.py — SKYLER LOT 53 : sparkline/bars/donut 2026.

Suite de l'axe visuel « app 2026 » (lots 51-52). Les trois primitives
restantes de `chart-core.js` rejoignent la signature :

- `C.sparkline` : lissage monotone (jamais de faux extrêmes) + mini-aire
  en dégradé (fondu vers transparent) — le rendu watchlist des apps de
  courtage ;
- `C.bars` : coins arrondis complets (`borderSkipped:false`), barres
  légèrement translucides qui deviennent pleines au survol
  (`hoverBackgroundColor`) — l'alpha n'est appliqué qu'aux hex 6 digits
  (les couleurs non-hex passent inchangées, jamais corrompues) ;
- `C.donut` : arcs arrondis (`borderRadius`) espacés (`spacing`) +
  `hoverOffset` — donut 2026 ;
- palette : uniquement `C.colors` + suffixes alpha — aucun littéral de
  couleur nouveau (même inventaire exact que lots 51-52).

Shell visible (JS servi) → SW v109 → v110.
"""
import re

CORE = 'vertex/static/vertex/js/charts/chart-core.js'


def _src():
    return open(CORE, encoding='utf-8').read()


def _section(src, start, end):
    return src[src.index(start):src.index(end)]


def test_sparkline_monotone_with_gradient_fill():
    src = _src()
    spark = _section(src, 'C.sparkline =', 'C.glowPlugin =')
    assert "cubicInterpolationMode: 'monotone'" in spark
    assert 'addColorStop' in spark                # mini-aire en dégradé
    assert 'tooltip: { enabled: false }' in spark  # reste muet (primitive)


def test_bars_rounded_and_hover_full():
    src = _src()
    bars = _section(src, 'C.bars =', 'C.donut =')
    assert 'borderSkipped: false' in bars          # coins arrondis complets
    assert 'hoverBackgroundColor' in bars          # pleine couleur au survol
    # l'alpha n'est appliqué qu'aux hex 6 digits — jamais de couleur corrompue
    assert re.search(r'#\[0-9A-Fa-f\]\{6\}|\[0-9A-Fa-f\]\{6\}', bars)


def test_donut_rounded_spaced_hover():
    src = _src()
    donut = _section(src, 'C.donut =', 'C.multiLine =')
    assert 'borderRadius' in donut
    assert 'spacing' in donut
    assert 'hoverOffset' in donut


def test_no_new_color_literals_outside_palette_and_fallbacks():
    """Même inventaire exact que les gardiens des lots 51-52 — le lot 53
    n'a le droit d'ajouter AUCUN littéral hex nouveau."""
    src = _src()
    hexes = set(re.findall(r"#[0-9A-Fa-f]{6}\b", src))
    allowed = {'#DBE1E8', '#45D6E8', '#9B7BFF', '#2BBE90', '#E9555F',
               '#D9BE3C', '#BABABA', '#8A8284', '#c8bfae', '#151719',
               '#050505', '#0b0b0c', '#111315', '#817d77', '#b7b2aa',
               '#b7b3ad', '#f3f1ed', '#121214', '#F8F5F3'}
    assert hexes <= allowed, 'littéraux inattendus : %s' % (hexes - allowed)


def test_service_worker_bumped_to_at_least_v110():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 110
    assert 'td-shell-v109' not in body
