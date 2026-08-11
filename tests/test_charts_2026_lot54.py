"""tests/test_charts_2026_lot54.py — SKYLER LOT 54 : prix & chandeliers 2026.

Suite de l'axe visuel « app 2026 » (lots 51-53). Deux modules satellites
rejoignent la signature (equity/drawdown héritent déjà via `C.area` —
vérifié, aucun changement nécessaire ; candlestick-lwc garde son moteur
LWC pro avec crosshair natif — inchangé, dit) :

- `price-chart.js` (graphique PRINCIPAL d'Analyse) : lissage monotone,
  ligne 2 px, dégradé 3 arrêts, glow, crosshair, pastille de dernier
  prix — la carte la plus vue du produit au niveau des aires 2026 ;
- `candlestick-chart.js` (repli Chart.js honnête) : corps de bougies
  ARRONDIS (`borderRadius`, `borderSkipped:false`), mèches FINES (1 px),
  visée verticale au survol (`C.crosshairPlugin`) ;
- palette : aucun littéral hex nouveau dans les deux fichiers touchés
  (inventaire exact pré-lot).

Shell visible (JS servi) → SW v110 → v111.
"""
import re

PRICE = 'vertex/static/vertex/js/charts/price-chart.js'
CANDLE = 'vertex/static/vertex/js/charts/candlestick-chart.js'


def _read(p):
    return open(p, encoding='utf-8').read()


def test_price_chart_full_2026_signature():
    src = _read(PRICE)
    assert "cubicInterpolationMode" in src and "'monotone'" in src
    assert src.count('addColorStop') >= 3          # dégradé riche 3 arrêts
    assert 'C.glowPlugin' in src
    assert 'C.crosshairPlugin' in src
    assert 'C.lastDotPlugin' in src                # pastille de dernier prix


def test_price_chart_keeps_levels_and_events():
    src = _read(PRICE)
    assert 'C.levelLines' in src                   # plan moteur conservé
    assert 'C.eventMarkers' in src                 # earnings conservés


def test_candles_rounded_bodies_thin_wicks():
    src = _read(CANDLE)
    assert 'borderRadius' in src
    assert 'borderSkipped: false' in src
    # mèche fine : 1 px (l'ancienne valeur 1.5 disparaît)
    assert 'maxBarThickness: 1,' in src
    assert 'maxBarThickness: 1.5' not in src


def test_candles_have_crosshair():
    src = _read(CANDLE)
    assert 'C.crosshairPlugin' in src


def test_candles_scale_fits_price_range():
    """Défaut réel attrapé en preuve navigateur : l'axe Y forcé à 0 écrasait
    les bougies (échelle 0-150 pour des prix ~100). L'axe doit épouser la
    plage réelle."""
    src = _read(CANDLE)
    assert 'beginAtZero: false' in src
    assert 'grace' in src


def test_no_new_color_literals_in_touched_files():
    """price-chart n'a qu'un secours '#DBE1E8' (déjà présent avant le lot),
    candlestick-chart n'a AUCUN littéral hex — le lot n'en ajoute aucun."""
    hexes_price = set(re.findall(r"#[0-9A-Fa-f]{6}\b", _read(PRICE)))
    assert hexes_price <= {'#DBE1E8'}, hexes_price
    hexes_candle = set(re.findall(r"#[0-9A-Fa-f]{6}\b", _read(CANDLE)))
    assert hexes_candle == set(), hexes_candle


def test_service_worker_bumped_to_at_least_v111():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 111
    assert 'td-shell-v110' not in body
