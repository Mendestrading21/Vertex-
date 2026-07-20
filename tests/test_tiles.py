"""Tests — builder de tuiles KPI partagé (CMP-02).

Vérifie :
- `VX.tile` (metric/stat/kpi) est défini dans vx-core.js et émet le markup canonique
  (classes .vx-metric / .vx-stat / .vx-kpi stylées par premium.css/glass.css) ;
- le bug des tuiles non stylées est corrigé : les builders JS de page n'émettent plus
  `.vx-stat-label`/`.vx-stat-value` en dur ; et si un émetteur legacy subsiste, l'alias
  CSS existe (filet défensif) → aucune tuile ne rend nue.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = os.path.join(ROOT, 'vertex', 'static', 'vertex', 'js')
CSS = os.path.join(ROOT, 'vertex', 'static', 'vertex', 'css')


def _read(*parts):
    return open(os.path.join(ROOT, *parts), encoding='utf-8').read()


def test_vx_tile_builder_exists():
    src = _read('vertex', 'static', 'vertex', 'js', 'vx-core.js')
    assert 'VX.tile' in src, 'builder partagé absent'
    for needle in ('metric:', 'stat:', 'kpi:'):
        assert needle in src, needle
    # markup canonique attendu (stylé par premium.css/glass.css)
    for cls in ('vx-metric', 'vx-metric-k', 'vx-metric-v',
                'vx-stat"', 'vx-stat-k', 'vx-stat-v',
                'vx-card vx-card--compact vx-kpi', 'vx-kpi-label', 'vx-kpi-value'):
        assert cls in src, cls
    # absence honnête : les valeurs passent par VX.fmt.nd (— jamais 0)
    assert 'VX.fmt.nd' in src


def test_stat_tiles_are_styled_not_naked():
    """Les builders JS de page ne doivent plus émettre .vx-stat-label/.vx-stat-value
    en dur (classes jadis non définies → tuiles nues). Repli inline autorisé mais
    canonique (-k/-v)."""
    for page in ('tracking.js', 'options-intel.js'):
        src = _read('vertex', 'static', 'vertex', 'js', 'pages', page)
        assert 'class="vx-stat-label"' not in src, page + ' émet encore une tuile nue'
        assert 'class="vx-stat-value"' not in src, page + ' émet encore une tuile nue'


def test_css_alias_covers_legacy_stat_tiles():
    """Filet défensif : si un émetteur legacy utilise encore -label/-value, le CSS
    les style (alias = -k/-v)."""
    premium = _read('vertex', 'static', 'vertex', 'css', 'premium.css')
    assert '.vx-stat-label' in premium
    assert '.vx-stat-value' in premium
    glass = _read('vertex', 'static', 'vertex', 'css', 'glass.css')
    assert '.vx-stat-value' in glass
