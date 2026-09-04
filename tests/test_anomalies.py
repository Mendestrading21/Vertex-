"""Moteurs d'anomalies Strategy OS : données, actions, options, surface de vol."""
import datetime as dt
import math

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
