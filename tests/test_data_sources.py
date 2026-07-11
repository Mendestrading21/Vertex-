"""Couche données Strategy OS : provenance, routage, réconciliation, scheduler, taux."""
import datetime as dt

import pytest

from vertex.data_sources import models as M
from vertex.data_sources import provenance as P
from vertex.data_sources import quality as Q
from vertex.data_sources import reconciliation as R
from vertex.data_sources.source_router import SourceRouter
from vertex.data_sources.ibkr_scheduler import (
    IbkrScheduler, CircuitOpen, PRIO_OPEN_POSITIONS, PRIO_UNIVERSE,
    PRIO_WATCHLIST, CIRCUIT_OPEN_AFTER, STALE_REQUEST_S)
from vertex.data_sources.rates import RateCurve, FALLBACK_FLAT_RATE, rate_sensitivity
from vertex.data_sources import ibkr_gateway


NOW = dt.datetime(2026, 7, 11, 15, 0, 0, tzinfo=dt.timezone.utc)


# ── Provenance ────────────────────────────────────────────────────────
def test_stamp_exposes_full_provenance():
    pv = P.stamp(101.5, M.SOURCE_IBKR, M.MODE_LIVE,
                 timestamp='2026-07-11T14:59:50Z', now=NOW)
    d = pv.to_dict()
    for key in ('value', 'source', 'source_mode', 'timestamp', 'age_seconds',
                'quality', 'fallback_used'):
        assert key in d
    assert d['source'] == 'IBKR' and d['source_mode'] == 'LIVE'
    assert d['quality'] == 'FRESH' and d['fallback_used'] is False


def test_data_ages_and_degrades():
    old = P.stamp(101.5, M.SOURCE_IBKR, M.MODE_LIVE,
                  timestamp='2026-07-11T10:00:00Z', now=NOW)
    assert old.quality == 'EXPIRED'
    recent = P.stamp(101.5, M.SOURCE_IBKR, M.MODE_LIVE,
                     timestamp='2026-07-11T14:58:00Z', now=NOW)
    assert recent.quality == 'RECENT'


def test_missing_data_never_becomes_fake_data():
    pv = P.stamp(None, M.SOURCE_IBKR, M.MODE_LIVE)
    assert pv.value is None
    assert pv.quality == 'MISSING'
    assert not pv.usable


# ── Qualité paquet ────────────────────────────────────────────────────
def test_packet_quality_is_worst_of_critical():
    pkt = M.AnalyticsPacket('NVDA')
    pkt.set_source('spot', P.stamp(495.0, M.SOURCE_IBKR, M.MODE_LIVE,
                                   timestamp='2026-07-11T14:59:55Z', now=NOW))
    pkt.set_source('options', P.stamp([{'strike': 500}], M.SOURCE_IBKR, M.MODE_DELAYED,
                                      timestamp='2026-07-10T20:00:00Z', now=NOW))
    q = Q.grade_packet(pkt)
    assert q['overall'] in ('STALE', 'EXPIRED')
    assert q['actionable_allowed'] is False


def test_data_quality_is_exposed():
    pkt = M.AnalyticsPacket('NVDA')
    pkt.set_source('spot', P.stamp(495.0, M.SOURCE_IBKR, M.MODE_LIVE, now=NOW))
    pkt.set_source('options', P.stamp([{}], M.SOURCE_IBKR, M.MODE_DELAYED, now=NOW))
    Q.grade_packet(pkt)
    d = pkt.to_dict()
    assert 'as_of' in d and d['quality']['overall'] == 'FRESH'


# ── Routeur de sources ────────────────────────────────────────────────
def test_router_prefers_ibkr_live():
    router = SourceRouter()
    router.register(M.SOURCE_SECONDARY, M.MODE_DELAYED,
                    lambda: P.stamp(100.2, M.SOURCE_SECONDARY, M.MODE_DELAYED))
    router.register(M.SOURCE_IBKR, M.MODE_LIVE,
                    lambda: P.stamp(100.0, M.SOURCE_IBKR, M.MODE_LIVE))
    pv = router.fetch()
    assert pv.source == 'IBKR' and pv.fallback_used is False


def test_router_falls_back_and_flags_it():
    router = SourceRouter()
    router.register(M.SOURCE_IBKR, M.MODE_LIVE, lambda: None)
    router.register(M.SOURCE_FALLBACK_EOD, M.MODE_EOD,
                    lambda: P.stamp(99.5, M.SOURCE_FALLBACK_EOD, M.MODE_EOD))
    pv = router.fetch()
    assert pv.source == 'FALLBACK_EOD' and pv.fallback_used is True
    assert any('repli' in w for w in pv.warnings)


def test_router_honest_when_all_sources_fail():
    router = SourceRouter()
    router.register(M.SOURCE_IBKR, M.MODE_LIVE, lambda: (_ for _ in ()).throw(OSError('down')))
    pv = router.fetch()
    assert pv.value is None and pv.quality == 'MISSING'


# ── Réconciliation ────────────────────────────────────────────────────
def test_source_disagreement_blocks_actionable():
    rep = R.reconcile_spot('NVDA', [
        {'source': 'IBKR', 'price': 500.0, 'currency': 'USD'},
        {'source': 'SECONDARY', 'price': 512.0, 'currency': 'USD'}])
    assert rep.blocking and rep.max_decision == 'ATTENDRE'
    assert any(i.code == 'SOURCE_DISAGREEMENT' for i in rep.inconsistencies)


def test_split_mismatch_detection():
    rep = R.reconcile_spot('NVDA', [
        {'source': 'IBKR', 'price': 100.0},
        {'source': 'SECONDARY', 'price': 1000.0}])
    assert any(i.code == 'SPLIT_MISMATCH' and i.severity == 3
               for i in rep.inconsistencies)


def test_small_gap_warns_without_blocking():
    rep = R.reconcile_spot('NVDA', [
        {'source': 'IBKR', 'price': 500.0},
        {'source': 'SECONDARY', 'price': 503.5}])
    assert not rep.blocking
    assert rep.max_decision is None


def test_stale_option_chain_blocks_actionable():
    rep = R.reconcile_spot_vs_options('NVDA',
                                      spot_ts='2026-07-11T15:00:00Z',
                                      chain_ts='2026-07-10T20:00:00Z')
    assert rep.blocking and rep.max_decision == 'ATTENDRE'


def test_earnings_divergence_blocks():
    rep = R.reconcile_earnings_dates('NVDA', {'IBKR': '2026-08-20', 'SECONDARY': '2026-08-27'})
    assert rep.blocking


def test_contract_multiplier_and_mapping_checks():
    rep = R.reconcile_contract('NVDA', {'multiplier': 10, 'currency': 'EUR',
                                        'underlying': 'NVDL', 'bid': 5.2, 'ask': 5.0})
    codes = {i.code for i in rep.inconsistencies}
    assert {'MULTIPLIER_MISMATCH', 'CURRENCY_MISMATCH',
            'CONTRACT_MAPPING_ERROR', 'BID_ABOVE_ASK'} <= codes


# ── Scheduler IBKR ────────────────────────────────────────────────────
def test_scheduler_priority_order():
    s = IbkrScheduler()
    done = []
    s.submit('univers:AAA', PRIO_UNIVERSE, lambda: done.append('univers'))
    s.submit('watch:BBB', PRIO_WATCHLIST, lambda: done.append('watch'))
    s.submit('pos:CCC', PRIO_OPEN_POSITIONS, lambda: done.append('pos'))
    s.run_pending(budget=3)
    assert done == ['pos', 'watch', 'univers']


def test_scheduler_dedup_and_cache():
    s = IbkrScheduler()
    calls = []
    assert s.submit('spot:NVDA', PRIO_WATCHLIST, lambda: calls.append(1) or 495.0)
    assert not s.submit('spot:NVDA', PRIO_WATCHLIST, lambda: calls.append(1) or 495.0)
    s.run_pending()
    assert not s.submit('spot:NVDA', PRIO_WATCHLIST, lambda: calls.append(1) or 495.0), \
        'résultat en cache frais — pas de nouvelle requête'
    assert s.get_cached('spot:NVDA') == 495.0
    assert len(calls) == 1


def test_scheduler_circuit_breaker():
    s = IbkrScheduler(max_retries=1)
    def boom():
        raise OSError('TWS down')
    for i in range(CIRCUIT_OPEN_AFTER):
        s.submit(f'k{i}', PRIO_WATCHLIST, boom)
    s.run_pending(budget=CIRCUIT_OPEN_AFTER)
    assert s.circuit_open
    with pytest.raises(CircuitOpen):
        s.run_pending()


def test_scheduler_cancels_stale_requests():
    t = [1000.0]
    s = IbkrScheduler(clock=lambda: t[0])
    done = []
    s.submit('old', PRIO_WATCHLIST, lambda: done.append('old'))
    t[0] += STALE_REQUEST_S + 1
    s.submit('fresh', PRIO_WATCHLIST, lambda: done.append('fresh'))
    s.run_pending(budget=2)
    assert done == ['fresh']
    assert s.metrics['cancelled_stale'] == 1


# ── Taux par échéance ─────────────────────────────────────────────────
def test_rate_curve_interpolates_by_tenor():
    curve = RateCurve({30: 0.05, 90: 0.046, 365: 0.042}, source='TEST')
    q = curve.rate_for_tenor(60)
    assert q.fallback_used is False
    assert 0.046 < q.rate < 0.05
    assert curve.rate_for_tenor(30).rate != curve.rate_for_tenor(365).rate, \
        'fini le taux global unique: le taux dépend de l’échéance'


def test_rate_fallback_is_documented():
    q = RateCurve().rate_for_tenor(120)
    assert q.fallback_used is True
    assert q.rate == FALLBACK_FLAT_RATE
    assert q.notes and 'repli' in q.notes[0]


def test_rate_sensitivity_reported():
    sens = rate_sensitivity(lambda r: 100 * (1 + r), base_rate=0.045)
    assert sens['value_up'] > sens['value_base'] > sens['value_down']
    assert sens['sensitivity_per_bump'] is not None


# ── Sécurité passerelle IBKR ──────────────────────────────────────────
def test_ibkr_readonly():
    import inspect
    src = inspect.getsource(ibkr_gateway)
    assert 'readonly=True' in src
    assert ibkr_gateway.IbkrGateway.READONLY is True
    forbidden = ('placeOrder', 'place_order', 'submit_order', 'transmit_order',
                 'modify_order', 'cancel_order', 'exercise_option', 'whatIf')
    for name in forbidden:
        assert name not in src, f'{name} interdit dans la passerelle'
    gw = ibkr_gateway.IbkrGateway()
    assert gw.status()['order_execution'] == 'disabled-by-design'
