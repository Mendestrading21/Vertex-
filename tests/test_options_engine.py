"""Desk Vertex Dynamic Options : pricer multi-scénarios, sélecteur CALL,
module PUT isolé, gestion des profits, earnings."""
import math

from vertex.data_sources.rates import RateCurve
from vertex.options import bearish_tactical, call_selector, chain_loader
from vertex.options import recommendation as reco
from vertex.options import scenario_pricer as sp
from vertex.options.models import UnderlyingSetup, CATEGORY_DYNAMIC
from vertex.catalysts import earnings_engine
from vertex.strategy import constitution as C

PROFILE = C.load_profile()
CURVE = RateCurve({30: 0.045, 180: 0.044, 365: 0.042}, source='TEST')


def setup_long(**kw):
    base = dict(symbol='NVDA', spot=500.0, invalidation=465.0, tp1=540.0,
                tp2=575.0, tp3=620.0, expected_move_pct=9.0,
                setup_quality='STANDARD', direction='LONG', dividend_yield=0.0)
    base.update(kw)
    return UnderlyingSetup(**base)


def call(strike, dte, delta, mid, iv=0.40, oi=4000, vol=600, spread=0.6, **kw):
    expiry = '2026-10-16'
    bid = round(mid - spread / 2, 2) if mid else None
    ask = round(mid + spread / 2, 2) if mid else None
    c = {'symbol': 'NVDA', 'underlying': 'NVDA', 'expiry': expiry, 'dte': dte,
         'strike': float(strike), 'right': 'C', 'bid': bid,
         'ask': ask, 'mid': mid, 'last': mid,
         'volume': vol, 'open_interest': oi, 'iv': iv, 'delta': delta,
         'gamma': 0.004, 'theta': -0.08, 'vega': 0.9,
         'greeks_source': 'BROKER_GREEKS', 'multiplier': '100', 'currency': 'USD'}
    c.update(kw)
    return c


def put(strike, dte, delta, mid, iv=0.42, oi=3000, vol=400, spread=0.5):
    c = call(strike, dte, delta, mid, iv=iv, oi=oi, vol=vol, spread=spread)
    c['right'] = 'P'
    return c


def liquid_chain():
    return [
        call(480, 130, 0.55, 48.0),   # BALANCED
        call(520, 130, 0.42, 32.0),   # BALANCED/DYNAMIC
        call(545, 130, 0.34, 24.0),   # DYNAMIC
        call(575, 160, 0.24, 15.0),   # ULTRA_CONVEX
        call(650, 160, 0.10, 4.0),    # trop OTM pour toute bande
        call(520, 30, 0.45, 14.0),    # DTE sous le minimum absolu (60)
        call(520, 400, 0.45, 60.0),   # DTE au-delà du maximum absolu (270)
        call(560, 130, 0.30, 18.0, oi=20, vol=1),  # illiquide
    ]


# ── Simulateur multi-scénarios ────────────────────────────────────────
def test_multihorizon_option_pricing():
    sim = sp.simulate(call(520, 130, 0.42, 32.0), setup_long(), rate_curve=CURVE)
    horizons = [t['days'] for t in sim['time_decay']]
    assert horizons == [0, 3, 5, 10, 15, 20, 28], \
        'les 7 horizons §6.5 doivent être simulés'
    assert sim['at_stop'] and sim['at_tp1'] and sim['at_tp2'] and sim['at_tp3']
    assert sim['worst_planned_loss_pct'] is not None and sim['worst_planned_loss_pct'] < 0
    assert sim['base_expected_gain_pct'] is not None
    assert sim['reward_risk'] is not None
    # theta : la valeur au spot inchangé décroît avec le temps
    values = [t['value'] for t in sim['time_decay']]
    assert values == sorted(values, reverse=True)


def test_iv_scenarios():
    sim = sp.simulate(call(520, 130, 0.42, 32.0), setup_long(), rate_curve=CURVE)
    shifts = [s['iv_shift_pct'] for s in sim['iv_sensitivity']]
    assert shifts == [-20, -10, 0, 10, 20]
    vals = [s['value'] for s in sim['iv_sensitivity']]
    assert vals == sorted(vals), 'plus d’IV = plus de valeur (vega positif)'


def test_dividend_in_pricing_context():
    no_div = sp.simulate(call(520, 130, 0.42, 32.0), setup_long(dividend_yield=0.0),
                         rate_curve=CURVE)
    with_div = sp.simulate(call(520, 130, 0.42, 32.0), setup_long(dividend_yield=0.03),
                           rate_curve=CURVE)
    v0 = no_div['time_decay'][0]['value']
    v1 = with_div['time_decay'][0]['value']
    assert v1 < v0, 'un rendement de dividende réduit la valeur théorique du CALL'


def test_model_is_labeled_estimate_never_broker_truth():
    sim = sp.simulate(call(520, 130, 0.42, 32.0), setup_long(), rate_curve=CURVE)
    assert sim['model_source'] in ('MODEL_ESTIMATE', 'FALLBACK_ESTIMATE')
    assert any('américaines' in l or 'ESTIMATION' in l for l in sim['limitations'])
    assert sim['rate']['source'] == 'TEST' and sim['rate']['fallback_used'] is False


def test_stop_derived_from_underlying():
    s = setup_long(invalidation=465.0)
    sim = sp.simulate(call(520, 130, 0.42, 32.0), s, rate_curve=CURVE)
    assert sim['at_stop']['spot'] == 465.0, \
        'le stop option dérive de l’invalidation du SOUS-JACENT'


def test_simulation_refuses_incomplete_data():
    sim = sp.simulate(call(520, 130, 0.42, None), setup_long(), rate_curve=CURVE)
    assert sim['reward_risk'] is None
    assert any('refusée' in l for l in sim['limitations'])


def test_capital_never_invented():
    sim = sp.simulate(call(520, 130, 0.42, 32.0), setup_long(), rate_curve=CURVE)
    analysis = sp.capital_free_analysis(sim, call(520, 130, 0.42, 32.0))
    assert analysis['contracts'] is None, 'pas de capital fourni → pas de nombre de contrats'
    assert analysis['estimated_gain_pct'] is not None
    assert analysis['cost_per_contract'] == 3200.0
    with_cap = sp.capital_free_analysis(sim, call(520, 130, 0.42, 32.0), capital=10000)
    assert with_cap['contracts'] == 3


# ── Sélecteur CALL ────────────────────────────────────────────────────
def test_selector_max_one_per_category_and_single_primary():
    res = call_selector.select_calls(liquid_chain(), setup_long(), PROFILE,
                                     rate_curve=CURVE)
    cats = res['per_category']
    assert set(cats) == {'BALANCED', 'DYNAMIC', 'ULTRA_CONVEX'}
    picked = [c for c in cats.values() if c]
    assert 1 <= len(picked) <= 3
    assert res['primary'] is not None
    assert res['primary']['category'] in ('BALANCED', 'DYNAMIC')


def test_dte_bounds_enforced():
    res = call_selector.select_calls(liquid_chain(), setup_long(), PROFILE,
                                     rate_curve=CURVE)
    for cat, sel in res['per_category'].items():
        if sel:
            assert 60 <= sel['contract']['dte'] <= 270
    rejected_dtes = [r['contract']['dte'] for r in res['rejected']]
    assert 30 in rejected_dtes and 400 in rejected_dtes


def test_ultra_convex_requirements():
    # setup STANDARD → pas d'ULTRA_CONVEX (rare_setup_only)
    res = call_selector.select_calls(liquid_chain(), setup_long(), PROFILE,
                                     rate_curve=CURVE)
    assert res['per_category']['ULTRA_CONVEX'] is None
    # setup EXCEPTIONNEL avec conviction forte → autorisé
    res2 = call_selector.select_calls(
        liquid_chain(), setup_long(setup_quality='EXCEPTIONAL', tp2=650.0, tp3=700.0),
        PROFILE, rate_curve=CURVE)
    ultra = res2['per_category']['ULTRA_CONVEX']
    if ultra:  # sélectionné seulement si la convexité simulée est réelle
        assert ultra['contract']['delta'] <= 0.30
        assert any('convexité' in r.lower() for r in ultra['reasons'])


def test_high_delta_no_longer_favored():
    """Fin du biais historique 0.70-0.88 : un delta 0.80 ne gagne pas d'office."""
    chain = liquid_chain() + [call(430, 130, 0.80, 82.0)]
    res = call_selector.select_calls(chain, setup_long(), PROFILE, rate_curve=CURVE)
    assert res['primary']['contract']['delta'] < 0.70, \
        'le delta 0.80 est hors bandes de catégories — jamais contrat principal'


def test_contract_not_selected_for_low_price_only():
    cheap = call(620, 130, 0.19, 0.05, oi=5000, vol=900, spread=0.02)
    chain = [cheap, call(545, 130, 0.34, 24.0)]
    res = call_selector.select_calls(chain, setup_long(setup_quality='EXCEPTIONAL'),
                                     PROFILE, rate_curve=CURVE)
    if res['primary']:
        assert res['primary']['contract']['mid'] != 0.05, \
            'une prime quasi nulle ne doit jamais faire gagner un contrat'


def test_call_is_primary_direction():
    """Le sélecteur CALL refuse un setup SHORT ; la reco route CALLS vs PUTS séparément."""
    import pytest
    with pytest.raises(AssertionError):
        call_selector.select_calls(liquid_chain(), setup_long(direction='SHORT'), PROFILE)
    r = reco.build_recommendation(liquid_chain(), setup_long(), PROFILE, rate_curve=CURVE)
    assert r['calls'] is not None and r['bearish'] is None


# ── Module PUT tactique isolé ─────────────────────────────────────────
def put_chain():
    return [put(460, 120, -0.40, 26.0), put(440, 120, -0.32, 19.0),
            put(480, 45, -0.45, 15.0)]


def bearish_setup():
    return setup_long(direction='SHORT', invalidation=530.0, tp1=460.0,
                      tp2=430.0, tp3=400.0)


def test_rare_put_is_isolated():
    """Un régime défavorable SEUL ne produit jamais un PUT (§6.4/§10)."""
    res = bearish_tactical.select_put(put_chain(), bearish_setup(),
                                      {'regime_unfavorable': True}, PROFILE,
                                      rate_curve=CURVE)
    assert res['selected'] is None
    assert not res['evidence']['converges']
    # même avec 2 preuves : toujours rien
    res2 = bearish_tactical.select_put(
        put_chain(), bearish_setup(),
        {'regime_unfavorable': True, 'support_broken': True}, PROFILE, rate_curve=CURVE)
    assert res2['selected'] is None


def test_put_selected_with_converging_evidence():
    evidence = {'regime_unfavorable': True, 'relative_weakness': True,
                'downtrend_confirmed': True, 'support_broken': True}
    res = bearish_tactical.select_put(put_chain(), bearish_setup(), evidence,
                                      PROFILE, rate_curve=CURVE)
    sel = res['selected']
    assert sel is not None
    assert sel['contract']['right'] == 'P'
    assert 0.30 <= abs(sel['contract']['delta']) <= 0.55
    assert sel['scenarios']['reward_risk'] >= 1.5


def test_max_one_bearish_position():
    evidence = {'regime_unfavorable': True, 'relative_weakness': True,
                'downtrend_confirmed': True}
    res = bearish_tactical.select_put(put_chain(), bearish_setup(), evidence,
                                      PROFILE, open_bearish_positions=1,
                                      rate_curve=CURVE)
    assert res['selected'] is None
    assert any('maximum' in n for n in res['notes'])


def test_bearish_module_never_sells_options():
    import inspect
    src = inspect.getsource(bearish_tactical)
    for forbidden in ('sell_option', 'short_option', 'covered_call',
                      'credit_spread', 'naked'):
        assert forbidden not in src


# ── Maximum 3 options ─────────────────────────────────────────────────
def test_max_three_options():
    r = reco.build_recommendation(liquid_chain(), setup_long(), PROFILE,
                                  open_options_count=3, rate_curve=CURVE)
    assert r['blocked'] is True and r['calls'] is None
    r2 = reco.build_recommendation(liquid_chain(), setup_long(), PROFILE,
                                   open_options_count=2, rate_curve=CURVE)
    assert r2['blocked'] is False


# ── Gestion des profits (§11) ─────────────────────────────────────────
def test_profit_management_at_50pct():
    plan = reco.profit_management_plan(current_gain_pct=55, sessions_in_trade=6)
    assert plan['action'] == 'PARTIAL_EXIT'
    assert plan['secure_share_pct'] == [60, 70]
    assert plan['runner_share_pct'] == [30, 40]
    assert plan['raise_invalidation'] is True


def test_runner_never_mandatory():
    plan = reco.profit_management_plan(current_gain_pct=60, sessions_in_trade=6,
                                       conditions={'momentum_broken': True})
    assert plan['action'] == 'FULL_EXIT'
    assert plan['runner_share_pct'] is None


def test_time_stop():
    plan = reco.profit_management_plan(current_gain_pct=-3, sessions_in_trade=8)
    assert plan['time_stop_triggered'] is True
    assert plan['action'] == 'REEVALUATE_OR_EXIT'


# ── Entonnoir de chargement ───────────────────────────────────────────
def test_funnel_never_loads_everything():
    import datetime as dt
    today = dt.date(2026, 7, 11)
    expirations = [(today + dt.timedelta(days=d)).isoformat()
                   for d in (7, 21, 45, 75, 100, 130, 160, 200, 240, 300, 400)]
    strikes = {e: [k * 10.0 for k in range(20, 100)] for e in expirations}
    plan = chain_loader.funnel_plan(expirations, strikes, 500.0, PROFILE, today=today)
    assert 0 < len(plan) <= chain_loader.MAX_EXPIRIES
    for leg in plan:
        assert 60 <= leg['dte'] <= 270
        assert len(leg['strikes']) <= chain_loader.MAX_STRIKES_PER_EXPIRY
        assert all(325 <= k <= 675 for k in leg['strikes'])


# ── Earnings ──────────────────────────────────────────────────────────
def test_hold_through_earnings_requires_full_dossier():
    plan = earnings_engine.evaluate_earnings_plan(5, hold_through_dossier={})
    assert plan['hold_through_allowed'] is False
    assert plan['exit_before_announcement'] is True
    assert plan['missing_requirements']
    full = {k: True for k in earnings_engine.HOLD_THROUGH_REQUIRED}
    plan2 = earnings_engine.evaluate_earnings_plan(5, hold_through_dossier=full)
    assert plan2['hold_through_allowed'] is True


def test_no_certainty_language():
    text = earnings_engine.sanitize_language('Ce trade est garanti et sans risque')
    assert 'garanti' not in text and 'sans risque' not in text
