"""Tests §15 — jeux de données des graphiques options (term/cone/OI/smile)."""
import math

from vertex.options import vol_charts as vc
from vertex.visualization.schemas import is_valid_interpretation


def _board():
    # AAPL : spot 200, deux échéances, calls + puts
    return [
        {'sym': 'AAPL', 'type': 'CALL', 'dte': 30, 'strike': 200, 'spot': 200, 'iv': 25.0, 'oi': 5000},
        {'sym': 'AAPL', 'type': 'CALL', 'dte': 30, 'strike': 210, 'spot': 200, 'iv': 27.0, 'oi': 3000},
        {'sym': 'AAPL', 'type': 'PUT', 'dte': 30, 'strike': 190, 'spot': 200, 'iv': 30.0, 'oi': 4000},
        {'sym': 'AAPL', 'type': 'CALL', 'dte': 180, 'strike': 205, 'spot': 200, 'iv': 28.0, 'oi': 1500},
        {'sym': 'AAPL', 'type': 'PUT', 'dte': 180, 'strike': 195, 'spot': 200, 'iv': 32.0, 'oi': 1200},
        {'sym': 'MSFT', 'type': 'CALL', 'dte': 45, 'strike': 420, 'spot': 420, 'iv': 22.0, 'oi': 900},
    ]


def test_term_structure_picks_atm_and_sorts_by_dte():
    c = [x for x in _board() if x['sym'] == 'AAPL']
    ts = vc.term_structure(c, 200)
    dtes = [p['dte'] for p in ts['points']]
    assert dtes == sorted(dtes)
    # à 30j l'ATM (strike 200) est retenu → IV 0.25
    p30 = next(p for p in ts['points'] if p['dte'] == 30)
    assert abs(p30['iv'] - 0.25) < 1e-9
    assert ts['slope'] is not None


def test_expected_move_cone_bands_are_ordered():
    c = [x for x in _board() if x['sym'] == 'AAPL']
    cone = vc.expected_move_cone(c, 200)
    for p in cone['points']:
        assert p['lo2'] <= p['lo1'] <= p['mid'] <= p['hi1'] <= p['hi2']
    # 1σ à 30j = 200 * 0.25 * sqrt(30/365)
    p30 = next(p for p in cone['points'] if p['dte'] == 30)
    em = 200 * 0.25 * math.sqrt(30 / 365.0)
    assert abs(p30['hi1'] - (200 + em)) < 0.05


def test_oi_by_strike_separates_calls_puts():
    c = [x for x in _board() if x['sym'] == 'AAPL']
    oi = vc.oi_by_strike(c, 200)
    row200 = next(r for r in oi['rows'] if r['strike'] == 200)
    assert row200['call'] == 5000 and row200['put'] == 0
    row190 = next(r for r in oi['rows'] if r['strike'] == 190)
    assert row190['put'] == 4000


def test_iv_smile_splits_calls_puts_for_expiry():
    c = [x for x in _board() if x['sym'] == 'AAPL']
    sm = vc.iv_smile(c, 200, expiry=30)
    assert sm['dte'] == 30
    assert all(r['strike'] for r in sm['calls'])
    assert any(abs(r['iv'] - 0.30) < 1e-9 for r in sm['puts'])


def test_build_full_payload_and_interpretation():
    d = vc.build(_board(), 'AAPL', as_of='2026-07-12T00:00:00')
    assert d['empty'] is False
    assert d['spot'] == 200
    assert d['term_structure']['points']
    assert d['expected_move_cone']['points']
    assert d['oi_by_strike']['rows']
    assert d['iv_smile']['calls'] or d['iv_smile']['puts']
    assert is_valid_interpretation(d['interpretation'])


def test_build_unknown_symbol_is_empty_and_honest():
    d = vc.build(_board(), 'NOPE')
    assert d['empty'] is True
    assert d['spot'] is None
    assert d['interpretation']['status'] == 'INCONNU'


def test_term_structure_missing_data_no_crash():
    # contrats sans strike/iv → ignorés, pas d'exception
    board = [{'sym': 'X', 'type': 'CALL', 'dte': 30, 'spot': 100}]
    d = vc.build(board, 'X')
    assert d['term_structure']['points'] == []
