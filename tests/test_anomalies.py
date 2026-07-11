"""Moteurs d'anomalies Strategy OS : données, actions, options, surface de vol."""
import datetime as dt
import math

from vertex.anomalies import data_anomalies as DA
from vertex.anomalies import option_anomalies as OA
from vertex.anomalies.models import any_blocking, blocking_codes
from vertex.anomalies.stock_anomalies import detect_stock_anomalies
from vertex.options.vol_surface import build_surface, relative_value_zones

NOW = dt.datetime(2026, 7, 11, 15, 0, 0, tzinfo=dt.timezone.utc)


# ── Fixtures réalistes anonymisées ────────────────────────────────────
def make_bars(n=260, start=100.0, drift=0.0006, vol=0.012, volume=1_000_000, seed=7):
    """Série OHLCV déterministe (pseudo-aléa reproductible, aucun réseau)."""
    bars, price, s = [], start, seed
    base = dt.date(2025, 7, 1)
    d = base
    while len(bars) < n:
        if d.weekday() < 5:
            s = (s * 6364136223846793005 + 1442695040888963407) % (2 ** 63)
            shock = ((s / 2 ** 63) - 0.5) * 2 * vol
            o = price
            c = price * (1 + drift + shock)
            h = max(o, c) * 1.004
            l = min(o, c) * 0.996
            bars.append({'date': d.isoformat(), 'open': round(o, 2), 'high': round(h, 2),
                         'low': round(l, 2), 'close': round(c, 2), 'volume': volume})
            price = c
        d += dt.timedelta(days=1)
    return bars


def liquid_call(**kw):
    base = {'symbol': 'NVDA', 'underlying': 'NVDA', 'expiry': '2026-11-20',
            'strike': 520.0, 'right': 'C', 'bid': 24.0, 'ask': 24.8, 'mid': 24.4,
            'last': 24.5, 'volume': 800, 'open_interest': 5200, 'iv': 0.42,
            'delta': 0.38, 'gamma': 0.004, 'theta': -0.09, 'vega': 0.85,
            'greeks_source': 'BROKER_GREEKS', 'multiplier': '100', 'currency': 'USD'}
    base.update(kw)
    return base


# ── Anomalies de données ──────────────────────────────────────────────
def test_stale_quote_blocks():
    anomalies = DA.check_quote({'source': 'IBKR', 'price': 500.0,
                                'timestamp': '2026-07-11T10:00:00Z', 'mode': 'LIVE'}, now=NOW)
    assert 'STALE_DATA' in [a.code for a in anomalies]
    assert any_blocking(anomalies)


def test_crossed_and_locked_market_detection():
    crossed = DA.check_quote({'source': 'IBKR', 'price': 100, 'bid': 101.0, 'ask': 100.5,
                              'timestamp': NOW.isoformat()}, now=NOW)
    assert 'CROSSED_MARKET' in blocking_codes(crossed)
    locked = DA.check_quote({'source': 'IBKR', 'price': 100, 'bid': 100.5, 'ask': 100.5,
                             'timestamp': NOW.isoformat()}, now=NOW)
    assert 'LOCKED_MARKET' in [a.code for a in locked]


def test_impossible_ohlc_and_duplicates():
    bars = make_bars(40)
    bars[10]['high'] = bars[10]['low'] - 1          # OHLC impossible
    bars.append(dict(bars[-1]))                     # doublon de date
    anomalies = DA.check_bars(bars, source='TEST')
    codes = {a.code for a in anomalies}
    assert 'IMPOSSIBLE_OHLC' in codes and 'DUPLICATE_BARS' in codes
    assert any_blocking(anomalies)


def test_negative_and_zero_price_blocking():
    a1 = DA.check_quote({'source': 'X', 'price': -5, 'timestamp': NOW.isoformat()}, now=NOW)
    a2 = DA.check_quote({'source': 'X', 'price': 0, 'timestamp': NOW.isoformat()}, now=NOW)
    assert 'NEGATIVE_PRICE' in blocking_codes(a1)
    assert 'ZERO_PRICE' in blocking_codes(a2)


# ── Anomalies actions ─────────────────────────────────────────────────
def test_return_zscore_and_volume_spike():
    bars = make_bars(200)
    last = bars[-1]
    last['close'] = round(bars[-2]['close'] * 1.09, 2)   # +9 % >> 3σ
    last['high'] = max(last['high'], last['close'] * 1.002)
    last['volume'] = 6_000_000                            # RVOL 6x
    found = {a.code for a in detect_stock_anomalies('TEST', bars)}
    assert 'RETURN_ZSCORE' in found
    assert 'OUTSIZED_ATR_MOVE' in found
    assert 'VOLUME_SPIKE' in found


def test_new_52w_high_detected():
    bars = make_bars(260, drift=0.002)
    found = {a.code for a in detect_stock_anomalies('TEST', bars)}
    assert 'NEW_52W_HIGH' in found


def test_failed_breakout_detected():
    bars = make_bars(200, drift=0.0)
    hi = max(b['high'] for b in bars[-61:-1])
    last = bars[-1]
    last['high'] = round(hi * 1.01, 2)     # dépasse en séance
    last['close'] = round(hi * 0.985, 2)   # clôture dessous
    last['low'] = min(last['low'], last['close'] * 0.99)
    found = {a.code for a in detect_stock_anomalies('TEST', bars)}
    assert 'FAILED_BREAKOUT' in found


def test_institutional_proxies_are_labeled_as_proxies():
    bars = make_bars(200)
    for i, b in enumerate(bars[-20:]):
        prev = bars[-21 + i]
        if b['close'] > prev['close']:
            b['volume'] = 2_400_000
        else:
            b['volume'] = 700_000
    anomalies = detect_stock_anomalies('TEST', bars)
    proxies = [a for a in anomalies if a.code in ('ACCUMULATION_PROXY', 'DISTRIBUTION_PROXY',
                                                  'VOLUME_SPIKE', 'OBV_DIVERGENCE')]
    for a in proxies:
        assert 'proxy' in a.impact.lower() or 'probable' in a.impact.lower(), \
            f'{a.code} doit être présenté comme proxy, jamais comme donnée certaine'


def test_fundamental_and_event_detectors_require_context():
    bars = make_bars(120)
    without = {a.code for a in detect_stock_anomalies('TEST', bars)}
    assert not ({'REVENUE_ACCELERATION', 'PRE_EARNINGS_RUNUP'} & without), \
        'sans contexte fourni, aucun détecteur fondamental/événement ne doit inventer'
    ctx = {'fundamentals': {'revenue_growth': 0.30, 'revenue_growth_prev': 0.10},
           'events': {'earnings_in_days': 5}}
    bars2 = make_bars(120, drift=0.008)
    with_ctx = {a.code for a in detect_stock_anomalies('TEST', bars2, ctx)}
    assert 'REVENUE_ACCELERATION' in with_ctx
    assert 'PRE_EARNINGS_RUNUP' in with_ctx


# ── Anomalies options ─────────────────────────────────────────────────
def test_zero_bid_blocks_contract():
    anomalies = OA.check_contract(liquid_call(bid=None, mid=None), spot=505.0)
    assert 'ZERO_BID' in blocking_codes(anomalies)


def test_crossed_market_blocks_contract():
    anomalies = OA.check_contract(liquid_call(bid=25.4, ask=24.2), spot=505.0)
    assert 'CROSSED_OPTION_MARKET' in blocking_codes(anomalies)


def test_wide_spread_detected():
    c = liquid_call(bid=20.0, ask=28.0, mid=24.0)
    codes = {a.code for a in OA.check_contract(c, spot=505.0)}
    assert 'WIDE_SPREAD' in codes


def test_negative_time_value_detected():
    # CALL strike 400, spot 505 → intrinsèque 105 ; mid 95 → valeur temps négative
    c = liquid_call(strike=400.0, bid=94.0, ask=96.0, mid=95.0)
    anomalies = OA.check_contract(c, spot=505.0)
    assert 'NEGATIVE_TIME_VALUE' in blocking_codes(anomalies)


def test_greek_sign_error_blocks():
    anomalies = OA.check_contract(liquid_call(delta=-0.4), spot=505.0)
    assert 'GREEK_SIGN_ERROR' in blocking_codes(anomalies)


def test_stale_option_quote_blocks():
    anomalies = OA.check_contract(liquid_call(), spot=505.0, quote_age_s=7200)
    assert 'STALE_QUOTE' in blocking_codes(anomalies)


def test_put_call_parity_warning():
    # C - P doit ≈ S - K·e^{-rT}. spot 500, K 500, C 40, P 5 → écart ~35 : alerte.
    call = liquid_call(strike=500.0, mid=40.0)
    anomalies = OA.check_economics(call, spot=500.0, dte=180, rate=0.045,
                                   counterpart_mid=5.0)
    assert 'PUT_CALL_PARITY_WARNING' in {a.code for a in anomalies}


def test_premium_too_cheap_never_a_reason_to_buy():
    c = liquid_call(strike=900.0, bid=0.02, ask=0.04, mid=0.03)
    anomalies = OA.check_economics(c, spot=505.0, expected_move_pct=12.0, dte=120)
    codes = {a.code for a in anomalies}
    assert 'PREMIUM_TOO_CHEAP_TO_BE_TRUSTED' in codes
    assert 'BREAKEVEN_UNREALISTIC' in codes


def test_activity_never_called_institutional_buying():
    c = liquid_call(volume=30000, open_interest=2000)
    anomalies = OA.check_activity(c, avg_volume=1500, prev_open_interest=900, dte=120)
    assert anomalies
    for a in anomalies:
        text = (a.impact + str(a.observed)).lower()
        assert 'achat institutionnel' not in text
        assert 'proxy' in text or 'confirmer' in text or 'inconnu' in text


# ── Surface de volatilité ─────────────────────────────────────────────
def surface_contracts(front_iv=0.75, back_iv=0.42):
    """Chaîne synthétique de test : front month gonflé (événement pricé)."""
    rows = []
    for expiry, dte, base_iv in (('2026-07-24', 13, front_iv), ('2026-10-16', 97, back_iv),
                                 ('2027-01-15', 188, back_iv * 0.98)):
        for strike in (420, 460, 500, 540, 580):
            skew = 0.05 * max(0, (500 - strike)) / 80
            rows.append({'expiry': expiry, 'dte': dte, 'strike': float(strike),
                         'right': 'C', 'iv': base_iv + skew, 'volume': 300,
                         'open_interest': 2000})
            rows.append({'expiry': expiry, 'dte': dte, 'strike': float(strike),
                         'right': 'P', 'iv': base_iv + skew + 0.03, 'volume': 250,
                         'open_interest': 1800})
    return rows


def test_vol_surface_outlier_detection():
    closes = [500 * (1 + 0.001 * math.sin(i / 3)) for i in range(60)]
    surf = build_surface('NVDA', 500.0, surface_contracts(),
                         closes=closes, iv_history=[0.30 + 0.005 * i for i in range(40)])
    codes = {a.code for a in surf.anomalies}
    assert 'TERM_STRUCTURE_INVERSION' in codes
    assert 'IV_CRUSH_RISK' in codes
    assert surf.iv_percentile is not None and surf.iv_rank is not None
    assert surf.expected_moves, 'expected move par expiration attendu'


def test_vol_surface_honest_without_history():
    surf = build_surface('NVDA', 500.0, surface_contracts(), iv_history=[0.4] * 5)
    assert surf.iv_percentile is None and surf.iv_rank is None
    assert any('insuffisant' in n for n in surf.notes)


def test_relative_value_prefers_compromise_not_cheapest():
    surf = build_surface('NVDA', 500.0, surface_contracts())
    zones = relative_value_zones(surf, preferred_dte=(90, 210))
    assert zones['preferred'], 'une expiration 90-210 DTE sous la médiane doit ressortir'
    preferred_dtes = [d for d, _ in zones['preferred']]
    assert all(90 <= d <= 210 for d in preferred_dtes)
    assert 13 not in preferred_dtes, 'le front month gonflé ne doit pas être préféré'
