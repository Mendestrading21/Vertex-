"""Tests §3/§5/§14 — registre couleurs, chart_spec canonique, environnement options."""
import os
import re

from vertex.options import environment as env
from vertex.options import pulse as pu


# ─────────────────────────────────────────────── registre couleurs (§3)








def _js_series(src_lower):
    """Extrait le tableau `series: [...]` (liste de hex) du thème JS."""
    m = re.search(r'series\s*:\s*\[([^\]]*)\]', src_lower)
    assert m, 'tableau series introuvable dans le thème JS'
    return re.findall(r'#[0-9a-f]{6}', m.group(1))






# ─────────────────────────────────────────────── chart_spec canonique (§5)










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
