"""Tests §18 — volatilité options : mesures pures, honnêteté des None."""
import math

from vertex.options import volatility as vol
from vertex.options import expected_move as em
from vertex.options import event_risk as ev


# ---------------------------------------------------------------- IV rank/pct
def test_iv_rank_bounds_and_midpoint():
    assert vol.iv_rank(0.30, 0.20, 0.40) == 50.0
    assert vol.iv_rank(0.40, 0.20, 0.40) == 100.0
    assert vol.iv_rank(0.20, 0.20, 0.40) == 0.0
    # au-dessus du haut → clampé à 100
    assert vol.iv_rank(0.55, 0.20, 0.40) == 100.0


def test_iv_rank_none_when_degenerate_or_missing():
    assert vol.iv_rank(0.3, 0.4, 0.4) is None      # couloir nul
    assert vol.iv_rank(None, 0.2, 0.4) is None
    assert vol.iv_rank(0.3, None, 0.4) is None


def test_iv_percentile_counts_strictly_below():
    hist = [0.2, 0.25, 0.3, 0.35, 0.4]
    # 0.32 dépasse 0.2/0.25/0.3 → 3/5 = 60 %
    assert vol.iv_percentile(0.32, hist) == 60.0
    assert vol.iv_percentile(0.2, hist) == 0.0
    assert vol.iv_percentile(0.5, hist) == 100.0
    assert vol.iv_percentile(0.3, None) is None


# ---------------------------------------------------------------- realized vol
def test_realized_vol_zero_when_flat():
    closes = [100.0] * 30
    assert vol.realized_vol(closes, window=20) == 0.0


def test_realized_vol_none_when_insufficient():
    assert vol.realized_vol([100, 101, 102], window=20) is None
    assert vol.realized_vol(None) is None


def test_realized_vol_matches_manual_formula():
    closes = [100, 102, 101, 103, 104, 102, 105]  # 6 returns
    r = vol.realized_vol(closes, window=6)
    rets = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]
    n = len(rets)
    mean = sum(rets) / n
    var = sum((x - mean) ** 2 for x in rets) / (n - 1)
    expected = round(math.sqrt(var) * math.sqrt(252), 4)
    assert r == expected


def test_iv_rv_premium_sign():
    assert vol.iv_rv_premium(0.30, 0.22) == 0.08
    assert vol.iv_rv_premium(0.20, 0.30) == -0.10
    assert vol.iv_rv_premium(None, 0.2) is None


def test_vol_regime_bands():
    assert vol.vol_regime(80) == 'ELEVEE'
    assert vol.vol_regime(60) == 'MOYENNE_HAUTE'
    assert vol.vol_regime(30) == 'MOYENNE_BASSE'
    assert vol.vol_regime(10) == 'BASSE'
    assert vol.vol_regime(None) is None


# ---------------------------------------------------------------- expected move
def test_expected_move_one_sigma():
    # spot 100, iv 40 %, 365 j → 1σ = 40
    assert em.expected_move(100, 0.40, 365) == 40.0
    # quart d'année
    assert abs(em.expected_move(100, 0.40, 91.25) - 20.0) < 0.01


def test_expected_move_none_on_bad_input():
    assert em.expected_move(None, 0.4, 30) is None
    assert em.expected_move(100, 0, 30) is None
    assert em.expected_move(100, 0.4, -5) is None


def test_expected_range_symmetric():
    lo, hi = em.expected_range(100, 0.40, 365)
    assert lo == 60.0 and hi == 140.0


def test_move_covers_target_ratio():
    # cible à +40 avec EM 40 → ratio 1.0
    assert em.move_covers_target(100, 0.40, 365, 140) == 1.0
    assert em.move_covers_target(100, 0.40, 365, 120) == 0.5
    assert em.move_covers_target(100, 0.40, 365, None) is None


# ---------------------------------------------------------------- event risk
def test_earnings_risk_levels():
    assert ev.earnings_risk(2, 30)[0] == ev.RISK_HIGH
    assert ev.earnings_risk(7, 30)[0] == ev.RISK_MODERATE
    assert ev.earnings_risk(40, 90)[0] == ev.RISK_LOW
    assert ev.earnings_risk(None, 30)[0] == ev.RISK_UNKNOWN


def test_earnings_risk_none_when_expiry_precedes_event():
    # échéance à 5 j, earnings à 10 j → pas de crush porté
    assert ev.earnings_risk(10, 5)[0] == ev.RISK_NONE


def test_dividend_risk_call_penalized():
    lvl, _ = ev.dividend_risk(3, 'CALL', 30)
    assert lvl == ev.RISK_MODERATE
    assert ev.dividend_risk(None, 'CALL', 30)[0] == ev.RISK_NONE


def test_combined_takes_worst():
    c = ev.combined(2, 3, 'CALL', 30)   # earnings HIGH, div MODERATE
    assert c['level'] == ev.RISK_HIGH
    assert c['earnings'] == ev.RISK_HIGH
    assert c['dividend'] == ev.RISK_MODERATE
