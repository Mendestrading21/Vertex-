"""Tests §3/§5/§14 — registre couleurs, chart_spec canonique, environnement options."""
import os
import re

from vertex.visualization import palette as pal
from vertex.visualization.chart_spec import (
    chart_spec, empty_spec, is_valid_chart_spec, CHART_TYPES,
)
from vertex.options import environment as env
from vertex.options import pulse as pu


# ─────────────────────────────────────────────── registre couleurs (§3)
def test_palette_no_blue_identity():
    assert pal.audit_no_blue() == [], 'aucune couleur du registre ne doit être bleu dominant'


def test_palette_series_is_deterministic_and_brand_first():
    assert pal.series_color(0) == pal.BRAND
    # boucle sans arc-en-ciel : index modulo longueur
    assert pal.series_color(len(pal.SERIES)) == pal.SERIES[0]


def test_status_color_maps_all_statuses():
    from vertex.visualization.schemas import STATUSES
    for s in STATUSES:
        assert re.match(r'^#[0-9a-fA-F]{6}$', pal.status_color(s))


def test_is_bluish_flags_blue_but_not_green_or_violet():
    assert pal.is_bluish('#3b82f6') is True     # bleu franc
    assert pal.is_bluish(pal.POSITIVE) is False  # vert
    assert pal.is_bluish(pal.OPTION) is False    # violet option
    assert pal.is_bluish(pal.BRAND) is False     # orange


def test_js_theme_matches_python_palette():
    """Le thème graphique JS doit rester cohérent avec le registre central."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    js = os.path.join(root, 'vertex/static/vertex/js/charts/chart-theme-obsidian-copper.js')
    with open(js, encoding='utf-8') as fh:
        src = fh.read().lower()
    # les couleurs clés du registre doivent apparaître dans le thème JS
    for col in (pal.BRAND, pal.BEIGE, pal.OPTION):
        assert col.lower() in src, '%s absent du thème JS' % col
    # le thème JS ne doit contenir aucune couleur bleu-dominant en série
    hexes = re.findall(r'#[0-9a-f]{6}', src)
    blues = [h for h in hexes if pal.is_bluish(h)]
    assert blues == [], 'couleurs bleu dominant dans le thème JS : %s' % blues


# ─────────────────────────────────────────────── chart_spec canonique (§5)
def test_chart_spec_valid_and_complete():
    d = chart_spec('c.iv', 'IV vs RV', 'Les primes sont-elles chères ?', 'line',
                   series=[{'name': 'IV', 'color': pal.BRAND, 'points': [1, 2, 3]}],
                   source='IBKR', freshness='DELAYED', quality='MEDIUM',
                   dominant_reading='IV au-dessus de la réalisée', status='DEFAVORABLE',
                   confidence=0.6)
    assert is_valid_chart_spec(d)
    assert d['chart_type'] == 'line' and d['status'] == 'DEFAVORABLE'


def test_chart_spec_no_series_forces_unknown():
    d = chart_spec('c', 't', 'q', 'bar', series=[], dominant_reading='qqch',
                   status='FAVORABLE')
    assert d['status'] == 'INCONNU'


def test_chart_spec_bad_type_defaults_line():
    d = chart_spec('c', 't', 'q', 'hologram', series=[{'x': 1}],
                   dominant_reading='r', status='NEUTRE')
    assert d['chart_type'] == 'line'


def test_empty_spec_is_valid_and_missing():
    d = empty_spec('c', 't', 'q', 'heatmap', reason='pas de données')
    assert is_valid_chart_spec(d)
    assert d['status'] == 'INCONNU' and d['freshness'] == 'MISSING'
    assert 'pas de données' in d['uncertainties']


def test_all_chart_types_are_lowercase_slugs():
    for t in CHART_TYPES:
        assert re.match(r'^[a-z_]+$', t)


# ─────────────────────────────────────────────── environnement options (§14)
def _board():
    return [
        {'sym': 'AAPL', 'type': 'CALL', 'iv': 24.0, 'quality': 72, 'spread_pct': 1.5, 'dte': 45, 'theta_burn': 0.3},
        {'sym': 'MSFT', 'type': 'CALL', 'iv': 26.0, 'quality': 68, 'spread_pct': 2.0, 'dte': 30, 'theta_burn': 0.4},
        {'sym': 'XYZ', 'type': 'PUT', 'iv': 55.0, 'quality': 40, 'spread_pct': 6.5, 'dte': 60, 'theta_burn': 0.2},
    ]


def test_environment_score_bounded_and_dimensions_counted():
    r = env.score_environment(_board(), detail_by_sym={'AAPL': {'earnings_in_days': 40}})
    assert 0 <= r['score'] <= 100
    assert r['dimensions_total'] == 5
    assert r['dimensions_known'] >= 3
    from vertex.visualization.schemas import is_valid_interpretation
    assert is_valid_interpretation(r['interpretation'])


def test_environment_low_iv_is_favorable():
    board = [{'sym': 'A', 'type': 'CALL', 'iv': 20.0, 'quality': 80, 'spread_pct': 1.2, 'dte': 45}]
    r = env.score_environment(board)
    assert r['label'] in ('PORTEUR', 'MITIGE')
    assert r['score'] is not None


def test_environment_empty_board_is_unknown():
    r = env.score_environment([])
    assert r['score'] is None
    assert r['label'] == 'INCONNU'
    assert r['interpretation']['status'] == 'INCONNU'


def test_environment_missing_dimension_excluded_not_zeroed():
    # board sans spread ni quality → ces dimensions INCONNUES, exclues de la moyenne
    board = [{'sym': 'A', 'type': 'CALL', 'iv': 22.0}]
    r = env.score_environment(board)
    known = [d for d in r['dimensions'] if d['known']]
    assert all(d['score'] is not None for d in known)
    unknown = [d for d in r['dimensions'] if not d['known']]
    assert any(d['key'] in ('quality', 'liquidity') for d in unknown)


# ─────────────────────────────────────────────── pulses (§7)
def test_option_pulse_counts_and_ratio():
    p = pu.option_pulse(_board())
    assert p['calls'] == 2 and p['puts'] == 1
    assert p['call_put_ratio'] == 2.0
    assert p['avg_iv'] is not None


def test_option_pulse_empty():
    p = pu.option_pulse([])
    assert p['empty'] is True and p['calls'] == 0


def test_volatility_pulse_state():
    v = pu.volatility_pulse(_board())
    assert v['state'] in ('COMPRESSION', 'NORMALE', 'EXPANSION')
    assert v['median_iv'] is not None
    assert pu.volatility_pulse([])['state'] == 'INCONNU'
