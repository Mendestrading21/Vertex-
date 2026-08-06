"""tests/test_research_backtest_lot115.py — SKYLER LOT 115 : backtest recherche figé.

Trou réel de couverture : vertex/research/backtest.py (§29 —
simple_backtest, la brique AVANT walk-forward) et
vertex/research/factory.apply_costs n'avaient AUCUN test direct. La
promesse « un backtest n'est jamais une preuve » (avertissement
systématique) et le modèle de coûts par rotation n'étaient figés nulle
part.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
import pytest

from vertex.research.backtest import simple_backtest
from vertex.research.factory import apply_costs


def test_flat_full_position_has_zero_turnover_and_zero_cost():
    r = simple_backtest([0.01] * 4, [1.0] * 4)
    assert r['turnover'] == 0.0
    assert r['net_mean'] == r['gross_mean'] == 0.01, (
        'position constante : aucune rotation, aucun coût')
    assert r['equity'] == [1.01, 1.0201, 1.030301, 1.040604]   # composition exacte


def test_position_switches_cost_exactly_per_turnover():
    # positions 1→0→1 : rotation 2.0 ; coût = (0.05+0.05)/100 · (2/3) par pas
    r = simple_backtest([0.01, -0.02, 0.03], [1.0, 0.0, 1.0])
    assert r['turnover'] == 2.0
    assert r['gross_mean'] == pytest.approx(0.0133333, abs=1e-6)
    assert r['net_mean'] == pytest.approx(0.0126667, abs=1e-6), (
        'chaque aller-retour se paie — jamais un backtest sans coûts')
    assert r['net_mean'] < r['gross_mean']


def test_zero_position_earns_nothing_but_pays_nothing():
    r = simple_backtest([0.05, -0.08, 0.02], [0.0, 0.0, 0.0])
    assert r['gross_mean'] == 0.0 and r['turnover'] == 0.0
    assert r['equity'] == [1.0, 1.0, 1.0]


def test_empty_series_is_honest_none_not_zero():
    r = simple_backtest([], [])
    assert r['gross_mean'] is None and r['net_mean'] is None
    assert r['equity'] == [] and r['turnover'] == 0


def test_warning_is_always_present_a_backtest_is_never_a_proof():
    for args in (([], []), ([0.01], [1.0]), ([0.01] * 9, [0.5] * 9)):
        assert 'walk-forward requis' in simple_backtest(*args)['warning'], (
            'l\'avertissement constitutionnel accompagne CHAQUE résultat')


def test_length_mismatch_truncates_to_shortest():
    r = simple_backtest([0.01, 0.02, 0.03, 0.04], [1.0, 1.0])
    assert len(r['equity']) == 2, 'aucun rendement sans position appariée'


def test_apply_costs_formula_exact_and_default_turnover_one():
    net = apply_costs([0.02, 0.02], spread_pct=0.05, slippage_pct=0.05)
    assert net == [pytest.approx(0.019), pytest.approx(0.019)], (
        '(0.05+0.05)/100 × turnover 1.0 = 10 bp retirés de chaque pas')
    free = apply_costs([0.02], 0.05, 0.05, turnover=0.0)
    assert free == [0.02]


def test_half_position_halves_exposure():
    full = simple_backtest([0.02, 0.02], [1.0, 1.0])
    half = simple_backtest([0.02, 0.02], [0.5, 0.5])
    assert half['gross_mean'] == pytest.approx(full['gross_mean'] / 2)
