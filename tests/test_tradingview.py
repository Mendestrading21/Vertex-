"""Webhook TradingView : secret, anti-replay, dédup, jamais un achat direct."""
import time

from flask import Flask

from vertex.data_sources.tradingview_signal_store import (
    TradingViewSignalStore, ALLOWED_SIGNALS, REPLAY_WINDOW_S)
from vertex.data_sources.tradingview_webhooks import make_blueprint

SECRET = 'test-secret-webhook'


def make_app(store=None, on_signal=None, secret=SECRET):
    app = Flask(__name__)
    app.register_blueprint(make_blueprint(store=store or TradingViewSignalStore(),
                                          secret=secret, on_signal=on_signal))
    return app


def _post(client, **body):
    return client.post('/api/tradingview/webhook', json=body)


def test_webhook_requires_secret():
    app = make_app()
    c = app.test_client()
    r = _post(c, symbol='NVDA', signal='BREAKOUT_CONFIRMED', timestamp=time.time())
    assert r.status_code == 403
    r = _post(c, secret='wrong', symbol='NVDA', signal='BREAKOUT_CONFIRMED',
              timestamp=time.time())
    assert r.status_code == 403


def test_webhook_disabled_without_configured_secret():
    app = make_app(secret='')
    r = app.test_client().post('/api/tradingview/webhook', json={'secret': ''})
    assert r.status_code == 503


def test_webhook_accepts_valid_signal_and_reevaluates_only():
    seen = []
    store = TradingViewSignalStore()
    app = make_app(store=store, on_signal=seen.append)
    r = _post(app.test_client(), secret=SECRET, symbol='NVDA',
              signal='BREAKOUT_CONFIRMED', timestamp=time.time(), price=495.2)
    assert r.status_code == 200
    assert r.get_json()['action'] == 'REEVALUATE'
    assert seen and seen[0]['action'] == 'REEVALUATE'


def test_tradingview_never_directly_buys():
    """Aucune entrée stockée ne peut porter une action d'achat/ordre."""
    store = TradingViewSignalStore()
    app = make_app(store=store)
    _post(app.test_client(), secret=SECRET, symbol='NVDA',
          signal='MOMENTUM_ACCELERATION', timestamp=time.time())
    for entry in store.recent():
        assert entry['action'] == 'REEVALUATE'
    import inspect
    from vertex.data_sources import tradingview_webhooks, tradingview_signal_store
    src = inspect.getsource(tradingview_webhooks) + inspect.getsource(tradingview_signal_store)
    for forbidden in ('place_order', 'placeOrder', 'submit_order', 'BUY_NOW',
                      'auto_execute', 'transmit'):
        assert forbidden not in src


def test_webhook_replay_and_dedup():
    store = TradingViewSignalStore()
    app = make_app(store=store)
    c = app.test_client()
    old_ts = time.time() - REPLAY_WINDOW_S - 10
    r = _post(c, secret=SECRET, symbol='NVDA', signal='SUPPORT_RECLAIM', timestamp=old_ts)
    assert r.status_code == 400 and 'replay' in r.get_json()['error']
    now = time.time()
    assert _post(c, secret=SECRET, symbol='NVDA', signal='SUPPORT_RECLAIM',
                 timestamp=now).status_code == 200
    r = _post(c, secret=SECRET, symbol='NVDA', signal='SUPPORT_RECLAIM', timestamp=now)
    assert r.status_code == 400 and 'doublon' in r.get_json()['error']


def test_webhook_validates_symbol_and_signal():
    app = make_app()
    c = app.test_client()
    assert _post(c, secret=SECRET, symbol='../etc', signal='BREAKOUT_CONFIRMED',
                 timestamp=time.time()).status_code == 400
    assert _post(c, secret=SECRET, symbol='NVDA', signal='HACK',
                 timestamp=time.time()).status_code == 400
    assert 'THESIS_INVALIDATION' in ALLOWED_SIGNALS


# ─────────────────────────────────────── honnêteté du secret (nom documenté)
def test_webhook_secret_resolves_documented_name(monkeypatch):
    """Un utilisateur qui suit la doc (TRADINGVIEW_WEBHOOK_SECRET) doit être actif —
    pas un webhook qui répond 503 en prétendant être configuré."""
    import os
    from vertex.data_sources import tradingview_webhooks as tw
    from vertex.data_sources.tradingview_signal_store import TradingViewSignalStore
    monkeypatch.delenv('TRADINGVIEW_SECRET', raising=False)
    monkeypatch.setenv('TRADINGVIEW_WEBHOOK_SECRET', 'doc-secret')
    assert tw._resolve_secret() == 'doc-secret'
    app = Flask(__name__)
    app.register_blueprint(tw.make_blueprint(store=TradingViewSignalStore(), secret=None))
    r = app.test_client().post('/api/tradingview/webhook',
                               json={'secret': 'doc-secret', 'symbol': 'NVDA',
                                     'signal': 'BREAKOUT_CONFIRMED', 'timestamp': time.time()})
    assert r.status_code == 200          # actif, pas 503


def test_webhook_secret_legacy_name_still_works(monkeypatch):
    from vertex.data_sources import tradingview_webhooks as tw
    monkeypatch.delenv('TRADINGVIEW_WEBHOOK_SECRET', raising=False)
    monkeypatch.setenv('TRADINGVIEW_SECRET', 'legacy')
    assert tw._resolve_secret() == 'legacy'


# ─────────────────────────────────────── statut honnête : off / attente / actif
def test_status_distinguishes_disabled_waiting_active():
    store = TradingViewSignalStore()
    assert store.status()['state'] == 'DISABLED'      # secret jamais déclaré
    store.set_configured(True)
    st = store.status()
    assert st['state'] == 'WAITING' and st['configured'] is True and st['stored'] == 0
    store.add(symbol='NVDA', signal='BREAKOUT_CONFIRMED', event_ts=time.time())
    st = store.status()
    assert st['state'] == 'ACTIVE' and st['fresh'] == 1


def test_recent_entries_carry_server_freshness():
    store = TradingViewSignalStore()
    store.add(symbol='NVDA', signal='TREND_ALIGNMENT', event_ts=time.time())
    e = store.recent()[0]
    assert 'age_s' in e and e['fresh'] is True and e['age_s'] >= 0


def test_stale_signal_marked_not_fresh():
    clock = {'t': 1_000_000.0}
    store = TradingViewSignalStore(clock=lambda: clock['t'])
    store.set_configured(True)
    store.add(symbol='NVDA', signal='VOLUME_EXPANSION', event_ts=clock['t'])
    clock['t'] += 7 * 3600            # +7 h > seuil de fraîcheur (6 h)
    assert store.recent()[0]['fresh'] is False
    assert store.status()['state'] == 'WAITING'   # configuré mais plus de signal frais


def test_seen_keys_pruned_under_load():
    clock = {'t': 1_000.0}
    store = TradingViewSignalStore(clock=lambda: clock['t'])
    from vertex.data_sources.tradingview_signal_store import MAX_SIGNALS, DEDUP_WINDOW_S
    for i in range(MAX_SIGNALS + 50):
        clock['t'] += DEDUP_WINDOW_S + 1        # chaque clé expire avant la suivante
        store.add(symbol='SYM%d' % (i % 90 or 1), signal='TREND_ALIGNMENT', event_ts=clock['t'])
    assert len(store._seen_keys) <= MAX_SIGNALS + 1
