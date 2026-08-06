"""tests/test_contract_scorer_lot106.py — SKYLER LOT 106 : score contextuel figé.

Trou réel de couverture : vertex/options/contract_scorer.py (§20 — le
score qui classe les contrats candidats) n'avait qu'UNE assertion de
constante (MIN_REWARD_RISK == 2.0 dans test_obsidian_theme). Les
principes anti-défauts du module — multiplicatif, aucun facteur ne
rachète un défaut fatal — n'étaient figés nulle part.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
import pytest

from vertex.options import contract_scorer as cs
from vertex.options.models import UnderlyingSetup
from vertex.strategy import constitution as C

PROFILE = C.load_profile()          # DYNAMIC : DTE préféré 90-210, perte 25-35


def _setup(quality='STANDARD'):
    return UnderlyingSetup(symbol='TEST', spot=100.0, setup_quality=quality)


def _contract(**kw):
    base = {'dte': 150, 'mid': 5.0, '_liquidity': {'score': 100.0}}
    base.update(kw)
    return base


def _sim(rr=2.5, loss=-30.0, gain=60.0, **kw):
    d = {'reward_risk': rr, 'worst_planned_loss_pct': loss,
         'base_expected_gain_pct': gain}
    d.update(kw)
    return d


def test_good_rr_scores_high_with_named_reasons():
    r = cs.score_contract(_contract(), 'DYNAMIC', _sim(), PROFILE, _setup())
    assert r.score == 90.0            # base 55+35 (R:R 2.5) × multiplicateurs 1
    assert any('R:R simulé' in x for x in r.reasons)
    assert any('DYNAMIC' in x for x in r.reasons)


def test_rr_below_minimum_is_capped_and_named():
    r = cs.score_contract(_contract(), 'DYNAMIC', _sim(rr=1.0), PROFILE, _setup())
    assert r.score == 10.0            # 20·(1/2) — un OI élevé ne rachète pas
    assert any('ne rachètera pas' in p for p in r.penalties)


def test_uncomputable_rr_is_floor_5():
    r = cs.score_contract(_contract(), 'DYNAMIC', _sim(rr=None), PROFILE, _setup())
    assert r.score == 5.0
    assert any('non calculable' in p for p in r.penalties)


def test_liquidity_is_a_multiplier_that_never_exceeds_1():
    perfect = cs.score_contract(_contract(), 'DYNAMIC', _sim(), PROFILE, _setup())
    mediocre = cs.score_contract(_contract(_liquidity={'score': 50.0}),
                                 'DYNAMIC', _sim(), PROFILE, _setup())
    assert perfect.score == 90.0
    assert mediocre.score == pytest.approx(58.5)   # 90 × (0.3 + 0.7·0.5) — non arrondi (réalité figée)
    assert any('liquidité moyenne' in p for p in mediocre.penalties)


def test_dte_fit_degrades_outside_preferred_window():
    inside = cs.score_contract(_contract(dte=150), 'DYNAMIC', _sim(), PROFILE, _setup())
    edge = cs.score_contract(_contract(dte=60), 'DYNAMIC', _sim(), PROFILE, _setup())
    assert inside.score == 90.0
    assert edge.score == 67.5         # 90 × 0.75 (minimum absolu, hors préféré)
    assert any('hors fenêtre préférée' in p for p in edge.penalties)


def test_expensive_iv_taxes_even_long_dte():
    r = cs.score_contract(_contract(dte=200), 'DYNAMIC', _sim(),
                          PROFILE, _setup(), surface_context={'iv_rank': 90})
    assert r.score == 54.0            # 90 × 0.6 — « DTE long ou pas »
    assert any('payer la peur' in p for p in r.penalties)


def test_ultra_convex_requires_exceptional_setup_else_zero():
    std = cs.score_contract(_contract(dte=150), 'ULTRA_CONVEX',
                            _sim(extended_gain_pct=120.0), PROFILE, _setup())
    assert std.score == 0.0, 'rare_setup_only : STANDARD → score nul, sans appel'
    exc = cs.score_contract(_contract(dte=150), 'ULTRA_CONVEX',
                            _sim(extended_gain_pct=120.0), PROFILE,
                            _setup('EXCEPTIONAL'))
    assert exc.score > 0
    assert any('convexité réelle' in x for x in exc.reasons)
    weak = cs.score_contract(_contract(dte=150), 'ULTRA_CONVEX',
                             _sim(extended_gain_pct=40.0), PROFILE,
                             _setup('EXCEPTIONAL'))
    assert weak.score == exc.score / 2, 'convexité simulée < 80 % → moitié'


def test_tiny_premium_is_never_a_buy_argument():
    r = cs.score_contract(_contract(mid=0.05), 'DYNAMIC', _sim(), PROFILE, _setup())
    assert r.score == 27.0            # 90 × 0.3 — le prix bas n'est pas un argument
    assert any('prime quasi nulle' in p for p in r.penalties)
