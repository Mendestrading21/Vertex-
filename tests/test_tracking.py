"""Tests §34 — VERTEX TRACKING ENGINE (suivi analytique hypothétique).

Couvre : abonnement horodaté, prix de référence honnête, rendement/alpha/
MAE/MFE/drawdown, options (mid/mark, expiration), arrêt (gel + historique),
réactivation (nouvel id), invariant lecture seule, étiquette hypothétique.
Le stockage est isolé en mémoire (monkeypatch persist).
"""
import re
import pytest

from vertex.tracking import models, reference_price as refp, returns as R, benchmark as B
from vertex.tracking import performance as perf
from vertex.tracking import repository as repo


@pytest.fixture(autouse=True)
def _isolated_store(monkeypatch):
    store = {}

    def _load(name, default):
        return store.get(name, default)

    def _save(name, obj):
        store[name] = obj
    monkeypatch.setattr('vertex.services.persist.load_json', _load)
    monkeypatch.setattr('vertex.services.persist.save_json', _save)
    yield store


TS = '2026-07-12T15:42:00-04:00'


# ─────────────────────────────────────────── abonnement (§14)
def test_follow_creates_timestamped_tracking(_isolated_store):
    t = repo.create(tracking_id='t1', entity_type='STOCK', symbol='NVDA',
                    quote={'bid': 100, 'ask': 100.4, 'source': 'IBKR'},
                    started_at=TS, decision='ACHETER', score=82)
    assert t['tracking_id'] == 't1'
    assert t['started_at'] == TS
    assert t['status'] == models.ST_ACTIVE


def test_follow_stores_reference_price_and_source(_isolated_store):
    t = repo.create(tracking_id='t1', entity_type='STOCK', symbol='NVDA',
                    quote={'bid': 100, 'ask': 100.4, 'source': 'IBKR'}, started_at=TS)
    assert t['reference_price'] == 100.2      # mid
    assert t['reference_price_type'] == 'MID'
    assert t['reference_price_source'] == 'IBKR'
    assert t['reference_price_timestamp'] == TS


def test_follow_does_not_create_real_position(_isolated_store):
    t = repo.create(tracking_id='t1', entity_type='STOCK', symbol='NVDA',
                    quote={'bid': 100, 'ask': 101}, started_at=TS)
    assert t['is_hypothetical'] is True


def test_hypothetical_label_is_visible():
    assert 'hypothétique' in perf.HYPOTHETICAL_LABEL.lower()


# ─────────────────────────────────────────── prix de référence honnête (§14)
def test_reference_prefers_mid_then_last_then_close():
    p, ty, _, st, _ = refp.pick_stock_reference({'bid': 10, 'ask': 10.2})
    assert (p, ty) == (10.1, 'MID')
    p, ty, _, _, _ = refp.pick_stock_reference({'last': 10.5}, market_open=True)
    assert (p, ty) == (10.5, 'LAST')
    p, ty, _, _, _ = refp.pick_stock_reference({'close': 9.9}, market_open=False)
    assert (p, ty) == (9.9, 'CLOSE')


def test_reference_missing_yields_data_required():
    p, ty, _, st, warns = refp.pick_stock_reference({})
    assert p is None and st == models.ST_DATA_REQUIRED and warns


def test_option_reference_uses_mid_or_mark():
    p, ty, _, _, _ = refp.pick_option_reference({'bid': 4.8, 'ask': 5.2})
    assert (p, ty) == (5.0, 'MID')
    p, ty, _, _, _ = refp.pick_option_reference({'mark': 4.7})
    assert (p, ty) == (4.7, 'MARK')


def test_option_reference_rejects_missing(_isolated_store):
    t = repo.create(tracking_id='o1', entity_type='OPTION', symbol='AAPL',
                    quote={}, started_at=TS, contract_id='AAPL 260918C200')
    assert t['status'] == models.ST_DATA_REQUIRED
    assert t['reference_price'] is None


def test_reference_never_uses_ask_silently():
    # ask seul (pas de bid) → pas de mid ; pour une option → DATA via last absent
    p, ty, _, st, _ = refp.pick_option_reference({'ask': 5.5})
    assert st == models.ST_DATA_REQUIRED       # jamais l'ask comme prix simulé


# ─────────────────────────────────────────── rendement / benchmark (§15)
def test_stock_return_since_follow():
    assert R.simple_return(100, 110) == 10.0
    assert R.simple_return(100, 90) == -10.0
    assert R.simple_return(None, 90) is None


def test_benchmark_and_alpha_since_follow():
    entity = R.simple_return(100, 112)     # +12 %
    bench = B.benchmark_return(400, 420)   # +5 %
    assert B.alpha_since(entity, bench) == 7.0


def test_mae_mfe_since_follow():
    mm = R.mae_mfe(100, [100, 108, 96, 104])
    assert mm['mfe_pct'] == 8.0 and mm['mae_pct'] == -4.0


def test_drawdown_since_follow():
    assert R.drawdown_from_high([100, 120, 108]) == -10.0


def test_split_adjustment():
    assert R.split_adjust(200, 2) == 100.0   # 2-for-1


def test_dividend_return_is_separate():
    # le module ne mélange pas : price return only ; le total return est explicite ailleurs.
    p = perf.compute({'reference_price': 100, 'benchmark': 'SPY',
                      'benchmark_reference_price': 400, 'snapshots': []}, 110,
                     bench_current=408)
    assert p['return_pct'] == 10.0
    assert any('dividendes' in l.lower() for l in p['limitations'])


# ─────────────────────────────────────────── options : suivi de la prime (§15)
def test_option_tracking_uses_mid_and_computes_premium_return(_isolated_store):
    t = repo.create(tracking_id='o2', entity_type='OPTION', symbol='AAPL',
                    quote={'bid': 4.8, 'ask': 5.2, 'source': 'IBKR'}, started_at=TS,
                    contract_id='AAPL 260918C200')
    assert t['reference_price'] == 5.0
    p = perf.compute(t, 6.5)
    assert p['return_pct'] == 30.0        # +30 % de prime (hypothétique)
    assert p['is_hypothetical'] is True


# ─────────────────────────────────────────── arrêt / réactivation (§16)
def test_stop_tracking_freezes_final_result_and_keeps_history(_isolated_store):
    repo.create(tracking_id='t1', entity_type='STOCK', symbol='NVDA',
                quote={'bid': 100, 'ask': 100}, started_at=TS)
    repo.add_snapshot('t1', price=120, at='2026-07-13T20:00:00Z')
    t = repo.stop('t1', at='2026-07-20T20:00:00Z', final_price=115,
                  final_decision='RÉDUIRE', reason='objectif atteint')
    assert t['status'] == models.ST_STOPPED
    assert t['final']['return_pct'] == 15.0
    assert t['final']['mfe_pct'] == 20.0      # plus haut 120 conservé
    assert t['snapshots']                      # historique conservé
    assert t['final']['is_hypothetical'] is True


def test_stopped_tracking_is_immutable_to_snapshots(_isolated_store):
    repo.create(tracking_id='t1', entity_type='STOCK', symbol='NVDA',
                quote={'bid': 100, 'ask': 100}, started_at=TS)
    repo.stop('t1', at='2026-07-20T20:00:00Z', final_price=110)
    repo.add_snapshot('t1', price=200, at='2026-07-21T20:00:00Z')  # no-op
    assert not repo.get('t1')['snapshots']


def test_restart_creates_new_tracking_id(_isolated_store):
    repo.create(tracking_id='t1', entity_type='STOCK', symbol='NVDA',
                quote={'bid': 100, 'ask': 100}, started_at=TS)
    repo.stop('t1', at='2026-07-20T20:00:00Z', final_price=110)
    t2 = repo.restart('t1', new_tracking_id='t2',
                      quote={'bid': 111, 'ask': 111}, started_at='2026-07-21T14:00:00Z')
    assert t2['tracking_id'] == 't2'
    assert t2['reference_price'] == 111
    assert repo.get('t1')['status'] == models.ST_STOPPED   # ancien intact


# ─────────────────────────────────────────── invariants
def test_tracking_never_places_order():
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    import glob
    banned = re.compile(r'(?:\.|\bdef\s+)(place_order|placeOrder|submit_order|'
                        r'close_position|closePosition|execute_trade|send_order)\s*\(')
    for path in glob.glob(os.path.join(root, 'vertex/tracking/*.py')):
        assert not banned.search(open(path, encoding='utf-8').read()), path


def test_summary_counts(_isolated_store):
    repo.create(tracking_id='t1', entity_type='STOCK', symbol='NVDA',
                quote={'bid': 100, 'ask': 100}, started_at=TS)
    repo.create(tracking_id='o1', entity_type='OPTION', symbol='AAPL',
                quote={'bid': 4, 'ask': 5}, started_at=TS, contract_id='x')
    s = repo.summary()
    assert s['active'] == 2 and s['stocks'] == 1 and s['options'] == 1
