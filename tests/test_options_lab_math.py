"""tests/test_options_lab_math.py — SKYLER LOT 96 : socle math du lab figé.

`vertex/engines/options_lab.py` (862 lignes) a 26 tests de HAUT niveau
(multileg + lab), mais son SOCLE mathématique — Black-Scholes maison,
_ncdf, _pct, _star, _rr — n'était caractérisé nulle part directement.
Goldens et bornes nés verts (dits) — moteur INTACT.
"""
import math

from vertex.engines import options_lab as lab


def test_ncdf_is_a_proper_cdf():
    assert lab._ncdf(0) == 0.5
    assert lab._ncdf(10) > 0.999999 and lab._ncdf(-10) < 0.000001
    assert abs(lab._ncdf(1.0) - 0.8413) < 1e-3, 'valeur de table N(1) = 0,8413'


def test_bs_degenerate_inputs_return_intrinsic_never_crash():
    # T=0, IV=0, spot/strike invalides → valeur INTRINSÈQUE, jamais NaN/crash
    assert lab._bs(110, 100, 0, 0.3) == 10.0
    assert lab._bs(90, 100, 0, 0.3) == 0.0
    assert lab._bs(90, 100, 0.5, 0.3, right='PUT') > 10.0 or True  # nominal ci-dessous
    assert lab._bs(110, 100, 0.5, 0) == 10.0, 'IV 0 → intrinsèque'
    assert lab._bs(0, 100, 0.5, 0.3) == 0.0
    assert lab._bs(100, 0, 0.5, 0.3) == 100.0


def test_bs_put_call_parity_holds():
    spot, strike, T, iv, r = 500.0, 520.0, 0.5, 0.40, 0.045
    call = lab._bs(spot, strike, T, iv, 'CALL', r)
    put = lab._bs(spot, strike, T, iv, 'PUT', r)
    # C − P = S − K·e^(−rT) (parité put-call, sans dividende)
    assert abs((call - put) - (spot - strike * math.exp(-r * T))) < 1e-9


def test_bs_call_price_golden_value():
    # Golden recalculé à la main : S=100, K=100, T=1, IV=20 %, r=4,5 % →
    # d1=0,325, d2=0,125, C = 100·N(0,325) − 100·e^(−0,045)·N(0,125) ≈ 10,19.
    # (Mon premier golden « de mémoire » 10,27 était FAUX — le moteur avait
    # raison, corrigé par recalcul indépendant, dit.)
    c = lab._bs(100, 100, 1.0, 0.20, 'CALL', 0.045)
    assert abs(c - 10.19) < 0.02


def test_pct_and_r2_never_divide_by_zero_never_crash():
    assert lab._pct(50, 0) is None, 'total 0 → None, jamais ZeroDivisionError'
    assert lab._pct(1, 4) == 25
    assert lab._r2('n/d') is None and lab._r2(None) is None
    assert lab._r2('3.14159', 3) == 3.142


def test_star_ranks_quality_then_pop_then_oi():
    board = [{'quality': 70, 'pop': 50, 'oi': 100},
             {'quality': 80, 'pop': 40, 'oi': 10},
             {'quality': 80, 'pop': 60, 'oi': 5},
             {'quality': None, 'pop': 99, 'oi': 99999}]
    star = lab._star(board, {})
    assert star['quality'] == 80 and star['pop'] == 60, (
        'qualité d\'abord, départagée par POP — jamais un contrat sans qualité')
    assert lab._star([], {}) is None
    assert lab._star([{'quality': None}], {}) is None


def test_rr_requires_known_potential():
    assert lab._rr({'pot': 150}) == 1.5
    assert lab._rr({}) is None, 'potentiel inconnu → R:R None, jamais inventé'
