"""
tests/test_live_engine.py — Vertex Live Engine (moteur + API).

Le moteur central : statuts par domaine (source/ts/fraîcheur/état), mode
global honnête (live/delayed/demo/offline), refresh global et partiel qui
réveille la chaîne de recalcul, rapport de synchronisation, et l'injection
du Sync Center sur toutes les pages.
"""

import threading
import time

from vertex.services import live_engine
from vertex.ui import sync_center


def _wire(scan=None, demo=True, ibkr=False, ev=None):
    live_engine.configure(scan_state=scan or {}, news_state={'items': []},
                          cal_state={'items': []}, weekly_state={'data': None},
                          rescan_event=ev, ibkr_enabled=ibkr, demo=demo)


def test_freshness_rule_single_source():
    assert live_engine.calculate_freshness(None)[0] == 'offline'
    assert live_engine.calculate_freshness(30, 'prices') == ('ok', 'il y a 30s')
    assert live_engine.calculate_freshness(900, 'prices')[0] == 'stale'
    assert live_engine.calculate_freshness(7200, 'prices')[0] == 'offline'
    assert live_engine.calculate_freshness(1800, 'options')[0] == 'ok'   # seuil par domaine


def test_mode_reflects_reality():
    _wire(scan={}, demo=True)
    assert live_engine.mode() == 'offline'                    # jamais scanné
    _wire(scan={'scan_ts': time.time()}, demo=True)
    assert live_engine.mode() == 'demo'
    _wire(scan={'scan_ts': time.time()}, demo=False, ibkr=False)
    assert live_engine.mode() == 'delayed'
    _wire(scan={'scan_ts': time.time()}, demo=False, ibkr=True)
    assert live_engine.mode() == 'live'


def test_status_has_all_domains_with_freshness():
    _wire(scan={'scan_ts': time.time(), 'rows': [{}] * 5,
                'options_board': [{}] * 3, 'committee': {'decisions': [{}] * 2}}, demo=True)
    st = live_engine.status()
    assert set(st['domains']) == {'prices', 'options', 'companies', 'news',
                                  'calendar', 'weekly', 'ai'}
    for d in st['domains'].values():
        assert d['state'] in ('ok', 'stale', 'offline')
        assert d['source'] and d['freshness'] and d['label']
    assert st['domains']['prices']['count'] == 5
    assert st['mode'] == 'demo'


def test_offline_prices_reported_as_error():
    _wire(scan={}, demo=True)
    st = live_engine.status()
    assert any(e['domain'] == 'prices' for e in st['errors'])


def test_refresh_kicks_rescan_and_builds_report():
    ev = threading.Event()
    _wire(scan={'scan_ts': time.time(), 'rows': [{}]}, demo=True, ev=ev)
    out = live_engine.refresh()
    assert out['ok'] and out['kicked'] and ev.is_set()
    labels = {l['domain'] for l in out['report']['lines']}
    assert 'prices' in labels and 'ai' in labels and 'options' in labels
    assert all(l['action'] for l in out['report']['lines'])
    assert live_engine.report()['ts'] is not None


def test_partial_refresh_only_touches_asked_domains():
    ev = threading.Event()
    _wire(scan={'scan_ts': time.time()}, demo=True, ev=ev)
    out = live_engine.refresh(['news'])
    assert {l['domain'] for l in out['report']['lines']} == {'news'}
    assert not ev.is_set()                                     # news ne réveille pas le scan
    assert 'démo' in out['report']['lines'][0]['action']       # honnête : pas de réseau en démo


def test_api_routes_and_global_injection():
    import terminal
    from vertex.app.state import cal_state, news_state, scan_state, weekly_state
    # re-câble l'état RÉEL de l'app (les tests précédents ont posé des états factices)
    live_engine.configure(scan_state=scan_state, news_state=news_state,
                          cal_state=cal_state, weekly_state=weekly_state,
                          rescan_event=terminal._rescan_evt, ibkr_enabled=False, demo=True)
    c = terminal.app.test_client()
    st = c.get('/api/live/status').get_json()
    assert st['mode'] in ('live', 'delayed', 'demo', 'offline') and 'domains' in st
    r = c.post('/api/live/refresh?domains=prices').get_json()
    assert r['ok'] and r['report']['requested'] == ['prices']
    rp = c.get('/api/live/report').get_json()
    assert rp['lines']
    # Sync Center présent sur les pages _vpage ET sur la home standalone
    assert 'vxSyncOpen' in terminal._NAVJS_BLOCK
    assert 'vxSyncOpen' in terminal.PAGE_DAILY
    assert 'Mettre à jour' in terminal.PAGE_DAILY


def test_sync_center_features():
    for marker in ('vxRefresh', 'vxReport', 'vxLiveToggle', 'vxLiveMode',
                   'Sync Center', 'Live Mode', 'Rapport de synchronisation',
                   'LIVE', 'DELAYED', 'DÉMO', 'OFFLINE'):
        assert marker in sync_center.JS, marker
