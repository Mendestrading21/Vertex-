"""Vertex Full Production — tests golden et propriétés des calculs financiers (§10-15).

Chaque calcul est vérifié contre des valeurs de référence documentées, des
propriétés mathématiques (grilles déterministes — pas d'aléa) et les règles
d'unités. Une donnée manquante ne devient JAMAIS zéro ni un chiffre inventé.
"""
import datetime as dt
import math

import pandas as pd
import pytest

from vertex.data_sources import provenance as P
from vertex.data_sources import models as M
from vertex.data_sources.rates import RateCurve
from vertex.engines import indicators
from vertex.engines.performance_ledger import PerformanceLedger
from vertex.options import scenario_pricer as sp
from vertex.options.legacy_engine import _bs_price, _greeks, _iv_from_price, gamma as bs_gamma
from vertex.options.models import UnderlyingSetup
from vertex.validation.probability_calibration import brier_score, log_loss

CURVE = RateCurve({30: 0.045, 365: 0.045}, source='TEST')


def call_contract(strike=100.0, dte=182, mid=10.0, iv=0.25):
    return {'symbol': 'TEST', 'right': 'C', 'strike': strike, 'dte': dte,
            'mid': mid, 'iv': iv, 'expiry': '2026-12-31'}


def setup(spot=100.0, stop=90.0, tp1=110.0, tp2=120.0, tp3=130.0, q=0.0):
    return UnderlyingSetup(symbol='TEST', spot=spot, invalidation=stop,
                           tp1=tp1, tp2=tp2, tp3=tp3, dividend_yield=q)


# ═════════════════════ Black-Scholes — valeurs golden ═════════════════
def test_bs_price_golden_atm_call():
    """Référence : S=100, K=100, T=1, σ=20 %, r=4.5 %, q=0.
    d1=0.325, d2=0.125 → C = 100·N(0.325) − 100·e^{-0.045}·N(0.125) ≈ 10.19."""
    price = sp.bs_price(100.0, 100.0, 1.0, 0.20, 0.045, 'C', 0.0)
    assert abs(price - 10.19) < 0.02, price


def test_bs_price_golden_put_via_parity():
    """Parité put-call : C - P = S - K·e^{-rT} (sans dividende)."""
    c = sp.bs_price(100.0, 100.0, 1.0, 0.20, 0.045, 'C', 0.0)
    p = sp.bs_price(100.0, 100.0, 1.0, 0.20, 0.045, 'P', 0.0)
    parity = c - p - (100.0 - 100.0 * math.exp(-0.045))
    assert abs(parity) < 1e-9, parity


def test_bs_deep_itm_call_close_to_forward_intrinsic():
    """CALL très ITM ≈ S·e^{-qT} - K·e^{-rT} (valeur temps quasi nulle)."""
    price = sp.bs_price(200.0, 100.0, 0.5, 0.20, 0.045, 'C', 0.0)
    expected = 200.0 - 100.0 * math.exp(-0.045 * 0.5)
    assert abs(price - expected) < 0.05


def test_option_intrinsic_value():
    """À expiration (T=0) : valeur = intrinsèque exacte, jamais autre chose."""
    assert sp.bs_price(105.0, 100.0, 0.0, 0.25, 0.045, 'C') == 5.0
    assert sp.bs_price(95.0, 100.0, 0.0, 0.25, 0.045, 'C') == 0.0
    assert sp.bs_price(95.0, 100.0, 0.0, 0.25, 0.045, 'P') == 5.0


def test_option_price_not_below_intrinsic():
    """Propriété : prix du CALL ≥ intrinsèque actualisée, sur toute une grille."""
    for s in (80.0, 95.0, 100.0, 110.0, 140.0):
        for t in (0.05, 0.25, 0.5, 1.0):
            for iv in (0.15, 0.35, 0.60):
                price = sp.bs_price(s, 100.0, t, iv, 0.045, 'C', 0.0)
                floor = max(0.0, s - 100.0 * math.exp(-0.045 * t))
                assert price >= floor - 1e-9, (s, t, iv)


def test_call_value_increases_with_spot():
    """Propriété : à paramètres constants, CALL croissant / PUT décroissant en S."""
    spots = [70 + 5 * i for i in range(15)]
    calls = [sp.bs_price(s, 100.0, 0.5, 0.30, 0.045, 'C') for s in spots]
    puts = [sp.bs_price(s, 100.0, 0.5, 0.30, 0.045, 'P') for s in spots]
    assert all(b >= a - 1e-9 for a, b in zip(calls, calls[1:]))
    assert all(b <= a + 1e-9 for a, b in zip(puts, puts[1:]))


def test_gamma_non_negative_long_options():
    """Propriété : gamma ≥ 0 pour une option longue (grille de strikes/T)."""
    for k in (80.0, 100.0, 120.0):
        for t in (0.1, 0.5, 1.0):
            g = bs_gamma(100.0, k, t, 0.3)
            assert g is None or g >= 0, (k, t, g)


def test_legacy_and_new_bs_agree():
    """Les deux implémentations BS (héritée / scenario_pricer, q=0) convergent."""
    legacy = _bs_price(100.0, 100.0, 1.0, 0.20, True)   # r interne 0.045
    new = sp.bs_price(100.0, 100.0, 1.0, 0.20, 0.045, 'C', 0.0)
    assert abs(legacy - new) < 0.02, (legacy, new)


def test_iv_roundtrip():
    """IV inversée depuis un prix BS retombe sur l'IV d'origine (±1 pt)."""
    price = _bs_price(100.0, 105.0, 0.5, 0.35, True)
    iv = _iv_from_price(100.0, 105.0, 0.5, price, True)
    assert iv is not None and abs(iv - 0.35) < 0.01


def test_dividend_context():
    """Le rendement de dividende baisse le CALL et monte le PUT (q=3 %)."""
    c0 = sp.bs_price(100.0, 100.0, 1.0, 0.25, 0.045, 'C', 0.0)
    c3 = sp.bs_price(100.0, 100.0, 1.0, 0.25, 0.045, 'C', 0.03)
    p0 = sp.bs_price(100.0, 100.0, 1.0, 0.25, 0.045, 'P', 0.0)
    p3 = sp.bs_price(100.0, 100.0, 1.0, 0.25, 0.045, 'P', 0.03)
    assert c3 < c0 and p3 > p0


# ═════════════════ Simulateur — scénarios stop/objectifs ══════════════
def test_option_scenario_at_stop():
    """La valeur AU STOP vient du repricing à l'invalidation du sous-jacent —
    jamais un pourcentage forfaitaire."""
    sim = sp.simulate(call_contract(), setup(), rate_curve=CURVE)
    at_stop_now = sim['at_stop']['by_time_days'][0]
    manual = sp.bs_price(90.0, 100.0, 182 / 365, 0.25, 0.045, 'C', 0.0)
    assert abs(at_stop_now['value'] - manual) < 0.02
    assert sim['worst_planned_loss_pct'] < 0


def test_option_scenario_at_targets():
    sim = sp.simulate(call_contract(), setup(), rate_curve=CURVE)
    v_tp1 = sim['at_tp1']['by_time_days'][0]['value']
    v_tp2 = sim['at_tp2']['by_time_days'][0]['value']
    v_tp3 = sim['at_tp3']['by_time_days'][0]['value']
    assert v_tp1 < v_tp2 < v_tp3, 'objectifs croissants → valeurs croissantes'
    manual_tp1 = sp.bs_price(110.0, 100.0, 182 / 365, 0.25, 0.045, 'C', 0.0)
    assert abs(v_tp1 - manual_tp1) < 0.02


def test_option_time_scenarios():
    sim = sp.simulate(call_contract(), setup(), rate_curve=CURVE)
    days = [t['days'] for t in sim['time_decay']]
    assert days == [0, 3, 5, 10, 15, 20, 28]
    values = [t['value'] for t in sim['time_decay']]
    assert values == sorted(values, reverse=True), 'theta ronge la valeur au spot constant'


def test_option_iv_scenarios():
    sim = sp.simulate(call_contract(), setup(), rate_curve=CURVE)
    shifts = [s['iv_shift_pct'] for s in sim['iv_sensitivity']]
    assert shifts == [-20, -10, 0, 10, 20]
    values = [s['value'] for s in sim['iv_sensitivity']]
    assert values == sorted(values), 'vega positif : plus d’IV = plus de valeur'


def test_reward_risk_uses_repriced_premiums():
    """R:R = gain simulé à l'objectif / perte simulée au stop — pas le payoff max."""
    sim = sp.simulate(call_contract(), setup(), rate_curve=CURVE)
    rr = sim['reward_risk']
    assert rr is not None
    manual = sim['base_expected_gain_pct'] / abs(sim['worst_planned_loss_pct'])
    assert abs(rr - round(manual, 2)) < 0.02


def test_expired_option_scenarios_refused():
    sim = sp.simulate(call_contract(dte=0), setup(), rate_curve=CURVE)
    assert sim['reward_risk'] is None
    assert any('refusée' in l for l in sim['limitations'])


def test_option_multiplier():
    """Convention : mid = prime PAR ACTION ; contrat = ×100 ; jamais confondus."""
    sim = sp.simulate(call_contract(mid=10.0), setup(), rate_curve=CURVE)
    analysis = sp.capital_free_analysis(sim, call_contract(mid=10.0))
    assert analysis['cost_per_contract'] == 1000.0
    assert analysis['contracts'] is None, 'sans capital fourni, jamais de quantité inventée'
    assert sp.capital_free_analysis(sim, call_contract(mid=10.0),
                                    capital=3500)['contracts'] == 3


def test_model_source_labelled():
    sim = sp.simulate(call_contract(), setup(), rate_curve=CURVE)
    assert sim['model_source'] in ('MODEL_ESTIMATE', 'FALLBACK_ESTIMATE')
    assert any('américaines' in l for l in sim['limitations'])


# ═════════════════ Indicateurs actions — golden ═══════════════════════
def test_rsi_golden_monotonic_series():
    """Série strictement haussière → RSI proche de 100 ; baissière → proche de 0."""
    up = pd.Series([100 + i for i in range(30)], dtype=float)
    down = pd.Series([100 - i for i in range(30)], dtype=float)
    assert indicators.rsi(up).iloc[-1] > 95
    assert indicators.rsi(down).iloc[-1] < 5


def test_rsi_flat_series_is_neutral_not_zero():
    """Série plate : pas de mouvement — le RSI ne doit pas retomber à 0 par
    division masquée (0 = signal baissier extrême, PAS donnée absente)."""
    flat = pd.Series([100.0] * 30)
    val = indicators.rsi(flat).iloc[-1]
    assert not math.isnan(val) and 30 <= val <= 100


def test_atr_golden():
    """ATR d'une série au range constant (H-L=2, sans gaps) = 2 exactement."""
    df = pd.DataFrame({'High': [102.0] * 20, 'Low': [100.0] * 20,
                       'Close': [101.0] * 20})
    assert abs(indicators.atr(df).iloc[-1] - 2.0) < 1e-9


# ═════════════════ Performance — golden ═══════════════════════════════
def _ledger_with(returns):
    led = PerformanceLedger()
    for i, r in enumerate(returns):
        e = led.record('REAL_POSITION', f'S{i}')
        led.close(e['id'], {'return_pct': r})
    return led


def test_performance_metrics_golden():
    """5 trades : +10, +20, -5, -10, +5 → valeurs exactes documentées."""
    m = _ledger_with([10.0, 20.0, -5.0, -10.0, 5.0]).metrics('REAL_POSITION')
    assert m['win_rate'] == 0.6                      # 3/5
    assert m['expectancy_pct'] == 4.0                # moyenne
    assert m['profit_factor'] == 2.33   # 35/15 arrondi moteur à 2 décimales
    assert m['max_drawdown_pct'] < 0


def test_max_drawdown_golden():
    """Équité 1.10 → 1.32 → pertes -5 % puis -10 % → DD = 1 - 0.95×0.90 = -14.5 %."""
    m = _ledger_with([10.0, 20.0, -5.0, -10.0, 5.0]).metrics('REAL_POSITION')
    assert abs(m['max_drawdown_pct'] - (-14.5)) < 0.01


def test_small_sample_metrics_withheld():
    m = _ledger_with([50.0]).metrics('REAL_POSITION')
    assert 'win_rate' not in m and 'note' in m


def test_brier_and_logloss_golden():
    """Prévision parfaite → Brier 0 ; prévision 0.5 constante → Brier 0.25."""
    assert brier_score([1.0, 0.0, 1.0], [1, 0, 1]) == 0.0
    assert brier_score([0.5] * 10, [1, 0] * 5) == 0.25
    assert abs(log_loss([0.5] * 4, [1, 0, 1, 0]) - math.log(2)) < 1e-4  # arrondi moteur 4 déc.


# ═════════════════ Unités, zéros et conventions ═══════════════════════
def test_percentage_conventions():
    """IV décimale (0.42) et IV pourcentage (42) ne se confondent jamais :
    l'API de simulation normalise et le note explicitement."""
    import terminal  # noqa: F401 — l'app expose /api/options/simulate
    c = terminal.app.test_client()
    r = c.get('/api/options/simulate?sym=TEST&strike=100&dte=182&mid=1000&iv=42'
              '&right=C&spot=100')
    d = r.get_json()
    assert r.status_code == 200
    assert d['contract']['iv'] == 0.42
    assert d['contract']['mid'] == 10.0
    assert any('convertie' in n for n in d['sim']['limitations'])


def test_missing_data_never_becomes_zero():
    """Donnée absente = None/MISSING partout — jamais 0."""
    pv = P.stamp(None, M.SOURCE_IBKR, M.MODE_LIVE)
    assert pv.value is None and pv.quality == 'MISSING'
    sim = sp.simulate(call_contract(mid=None), setup(), rate_curve=CURVE)
    assert sim['reward_risk'] is None
    assert sim['base_expected_gain_pct'] is None
    led = PerformanceLedger()
    e = led.record('SIGNAL', 'X')
    led.close(e['id'], {'return_pct': None})
    m = led.metrics('SIGNAL')
    assert m.get('expectancy_pct') is None or 'note' in m, \
        'un rendement inconnu ne compte pas comme 0'


def test_timezone_handling():
    """Les âges de données acceptent naïf (supposé UTC) et timezone-aware,
    et un timestamp futur ne donne jamais un âge négatif."""
    now = dt.datetime(2026, 7, 11, 15, 0, 0, tzinfo=dt.timezone.utc)
    naive = P.age_seconds('2026-07-11T14:59:00', now=now)
    aware = P.age_seconds('2026-07-11T14:59:00+00:00', now=now)
    assert naive == aware == 60.0
    future = P.age_seconds('2026-07-11T15:05:00Z', now=now)
    assert future == 0.0, 'âge jamais négatif'


def test_stock_split_handling():
    """Un ratio de prix 10:1 entre sources = split non appliqué → bloquant."""
    from vertex.data_sources.reconciliation import reconcile_spot
    rep = reconcile_spot('TEST', [{'source': 'IBKR', 'price': 50.0},
                                  {'source': 'SECONDARY', 'price': 500.0}])
    assert any(i.code == 'SPLIT_MISMATCH' for i in rep.inconsistencies)
    assert rep.max_decision == 'ATTENDRE'


def test_negative_time_and_spread_invariants():
    """Le temps restant et le spread % ne peuvent être négatifs."""
    from vertex.options.liquidity import assess
    liq = assess({'bid': 10.0, 'ask': 10.4, 'mid': 10.2,
                  'open_interest': 1000, 'volume': 100})
    assert liq['spread_pct'] >= 0
    sim = sp.simulate(call_contract(dte=-5), setup(), rate_curve=CURVE)
    assert sim['reward_risk'] is None, 'DTE négatif = contrat expiré, simulation refusée'


def test_broker_model_divergence_warning():
    from vertex.anomalies.option_anomalies import check_contract
    anomalies = check_contract(
        {'symbol': 'T', 'expiry': 'e', 'strike': 100.0, 'right': 'C',
         'bid': 5.0, 'ask': 5.2, 'mid': 5.1, 'delta': 0.50,
         'model_greeks': {'delta': 0.30}}, spot=100.0)
    assert 'BROKER_MODEL_GREEK_DIVERGENCE' in [a.code for a in anomalies]
