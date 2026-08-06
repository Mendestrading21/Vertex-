"""tests/test_polish_lot63.py — SKYLER LOT 63 : sparkArea de Marchés lissé.

Écart de cohérence RÉEL constaté en capture (lot 56) : les mini-aires des
cartes d'indices (`sparkArea`, SVG local de markets_page.py) sont des
POLYLIGNES anguleuses rendues juste au-dessus du grand graphique `C.area`
lissé monotone — deux langages visuels sur la même page. Harmonisé :

- `sparkArea` trace désormais un chemin lissé MONOTONE (Fritsch-Carlson,
  même principe que `cubicInterpolationMode 'monotone'` de Chart.js) —
  la courbe ne dépasse JAMAIS les données réelles, les points restent
  exacts, le calcul est déterministe (aucun aléatoire) ;
- le dégradé de remplissage et le point actif final sont conservés ;
- `sparkSvg` (l'ancien mini-trait) : AUCUN consommateur dans tout le
  dépôt (vérifié par grep) — code mort SUPPRIMÉ.

Shell visible → SW v118 → v119.
"""
import re

PAGE = 'vertex/ui/pages/markets_page.py'


def _src():
    return open(PAGE, encoding='utf-8').read()


def _spark_section(src):
    return src[src.index('function sparkArea'):src.index('const MONO=')]


def test_spark_area_uses_monotone_path():
    sec = _spark_section(_src())
    assert 'monotone' in sec.lower()
    assert '<path' in sec                       # chemin lissé, plus une polyligne
    assert '<polyline' not in sec
    assert '<polygon' not in sec                # l'aire suit le même chemin lissé


def test_spark_area_keeps_gradient_and_last_dot():
    sec = _spark_section(_src())
    assert 'linearGradient' in sec
    assert '<circle' in sec                     # point actif final conservé


def test_spark_area_no_randomness():
    sec = _spark_section(_src())
    assert 'Math.random' not in sec


def test_dead_spark_svg_removed():
    assert 'sparkSvg' not in _src()


def test_service_worker_bumped_to_at_least_v119():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 119
    assert 'td-shell-v118' not in body
