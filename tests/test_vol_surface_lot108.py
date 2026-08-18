"""tests/test_vol_surface_lot108.py — SKYLER LOT 108 : surface de vol figée.

Trou réel de couverture : vertex/options/vol_surface.py (210 lignes)
n'avait que 3 tests d'INTÉGRATION (inversion+crush, honnêteté sans
historique, zones de valeur relative). Les formules internes —
realized_vol, ATM par proximité du spot, skew conditionnel, dislocations
nommées, IV rank/percentile, spike — n'étaient figées nulle part.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
import pytest

from vertex.options.vol_surface import _median, build_surface, realized_vol


def _rows(strike_ivs, expiry='2026-12-18', dte=180, right='C'):
    return [{'expiry': expiry, 'dte': dte, 'strike': k, 'right': right, 'iv': iv}
            for k, iv in strike_ivs]


def test_realized_vol_constant_prices_is_zero_and_short_series_none():
    assert realized_vol([100.0] * 30) == 0.0        # aucun mouvement = vol nulle
    assert realized_vol([100.0] * 20) is None       # < n+1 clôtures → None honnête
    assert _median([]) is None
    assert _median([1, 2, 3, 4]) == 2.5             # pair → moyenne des centraux


def test_invalid_spot_yields_empty_surface_with_note():
    surf = build_surface('TST', 0.0, _rows([(100, 0.30)]))
    assert surf.by_expiry == {} and any('spot invalide' in n for n in surf.notes)


def test_garbage_ivs_are_filtered_never_used():
    surf = build_surface('TST', 100.0, _rows(
        [(100, None), (100, 0.0), (100, -0.3), (100, 6.0)]))
    assert surf.by_expiry == {}, 'IV absente, nulle, négative ou > 500 % : ignorée'


def test_atm_iv_is_nearest_strike_and_expected_move_formula():
    surf = build_surface('TST', 100.0, _rows(
        [(90, 0.50), (101, 0.30), (120, 0.60)]), )
    exp = surf.by_expiry['2026-12-18']
    assert exp['atm_iv'] == 0.30                    # strike 101, le plus proche
    assert surf.expected_moves['2026-12-18'] == pytest.approx(
        0.30 * (180 / 365) ** 0.5 * 100, abs=0.01)  # ±21.07 % à 180 j


def test_surface_excludes_expiry_with_missing_or_conflicting_dte():
    missing = build_surface('TST', 100.0, _rows([(100, 0.30)], dte=None))
    assert missing.by_expiry == {}
    assert missing.term_structure == [] and missing.expected_moves == {}
    assert any('DTE indisponible ou contradictoire' in note for note in missing.notes)

    conflicting = build_surface('TST', 100.0,
                                _rows([(100, 0.30)], dte=90) + _rows([(101, 0.31)], dte=120))
    assert conflicting.by_expiry == {}
    assert any('DTE indisponible ou contradictoire' in note for note in conflicting.notes)


def test_skew_needs_a_put_near_10pct_otm():
    with_put = build_surface('TST', 100.0,
                             _rows([(100, 0.30)]) + _rows([(91, 0.38)], right='P'))
    assert with_put.skew_by_expiry['2026-12-18'] == pytest.approx(0.08)
    far_put = build_surface('TST', 100.0,
                            _rows([(100, 0.30)]) + _rows([(70, 0.45)], right='P'))
    assert far_put.skew_by_expiry == {}, (
        'put à 30 % du spot : trop loin du proxy 25-delta — pas de skew inventé')


def test_strike_dislocation_and_smile_discontinuity_are_named():
    surf = build_surface('TST', 100.0, _rows(
        [(90, 0.30), (100, 0.31), (110, 0.95)]))    # 0.95 ≈ 3× la médiane
    codes = [a.code for a in surf.anomalies]
    assert 'STRIKE_IV_DISLOCATION' in codes
    assert 'SMILE_DISCONTINUITY' in codes           # saut 0.31→0.95 > 35 %


def test_iv_rank_and_percentile_exact_on_linear_history():
    hist = [0.20 + 0.01 * i for i in range(21)]     # 0.20 → 0.40
    surf = build_surface('TST', 100.0, _rows([(100, 0.40)]), iv_history=hist)
    assert surf.iv_rank == 100.0 and surf.iv_percentile == 100.0
    mid = build_surface('TST', 100.0, _rows([(100, 0.30)]), iv_history=hist)
    assert mid.iv_rank == 50.0                      # (0.30−0.20)/(0.40−0.20)


def test_iv_spike_vs_recent_median_named_and_flat_history_no_rank():
    surf = build_surface('TST', 100.0, _rows([(100, 0.40)]),
                         iv_history=[0.20] * 25)
    codes = [a.code for a in surf.anomalies]
    assert 'IV_SPIKE' in codes                      # 0.40 > 1.3 × 0.20
    assert surf.iv_rank is None, 'historique plat (hi == lo) → rank None, pas 0'
    assert surf.iv_percentile == 100.0
