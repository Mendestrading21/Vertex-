"""Desk Vertex Dynamic Options : pricer multi-scénarios, sélecteur CALL,
module PUT isolé, gestion des profits, earnings."""
import math

from vertex.data_sources.rates import RateCurve
from vertex.options import scenario_pricer as sp
from vertex.options.models import UnderlyingSetup, CATEGORY_DYNAMIC
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












# ── Module PUT tactique isolé ─────────────────────────────────────────
def put_chain():
    return [put(460, 120, -0.40, 26.0), put(440, 120, -0.32, 19.0),
            put(480, 45, -0.45, 15.0)]


def bearish_setup():
    return setup_long(direction='SHORT', invalidation=522.0, tp1=440.0,
                      tp2=410.0, tp3=380.0)












# ── Maximum 3 options ─────────────────────────────────────────────────


# ── Gestion des profits (§11) ─────────────────────────────────────────






# ── Entonnoir de chargement ───────────────────────────────────────────


# ── Earnings ──────────────────────────────────────────────────────────




