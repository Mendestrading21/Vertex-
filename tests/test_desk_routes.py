"""
tests/test_desk_routes.py — Desk perso en Blueprint (Ch. II).

Sync du desk (validation + aller-retour), export TradingView, fiche express,
cotation des trades perso (cache TTL, borne dure, offline). Dépendances
réseau INJECTÉES en fakes — aucun accès réseau, aucun ordre possible.
"""

from flask import Flask

from vertex.app.routes import desk
from vertex.app.state import scan_state
from vertex.data.universe import UNIVERSE
from vertex.services import persist


def _client(*, ibkr=True, opt_job=None, pack=None, tmp_path=None, monkeypatch=None):
    if tmp_path is not None:
        monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    app = Flask(__name__)
    app.register_blueprint(desk.make_blueprint(
        options_pack=pack or (lambda s: {'sym': s, 'iv': 33.0}),
        opt_job=opt_job or (lambda kind, args, timeout: {}),
        ibkr_enabled=ibkr))
    return app.test_client()


# ─── /api/desk ───

def test_desk_round_trip(tmp_path, monkeypatch):
    c = _client(tmp_path=tmp_path, monkeypatch=monkeypatch)
    r = c.post('/api/desk', json={'ts': 1720000000, 'data': {'trades': [1, 2]}})
    assert r.status_code == 200 and r.get_json()['ok'] is True
    j = c.get('/api/desk').get_json()
    assert j == {'ts': 1720000000, 'data': {'trades': [1, 2]}}


def test_desk_rejects_invalid_payload(tmp_path, monkeypatch):
    c = _client(tmp_path=tmp_path, monkeypatch=monkeypatch)
    assert c.post('/api/desk', json={'ts': 1, 'data': 'pas un dict'}).status_code == 400
    assert c.post('/api/desk', json={'data': {}}).status_code == 400


def test_desk_empty_when_never_saved(tmp_path, monkeypatch):
    c = _client(tmp_path=tmp_path, monkeypatch=monkeypatch)
    assert c.get('/api/desk').get_json() == {}


# ─── /api/watchlist-tv ───

def test_watchlist_tv_exports_the_universe():
    j = _client().get('/api/watchlist-tv').get_json()
    assert j['count'] == len(UNIVERSE)
    assert j['tv'] == ','.join(j['symbols'])
    assert set(j['symbols']) == set(UNIVERSE)


# ─── /api/ticker/<sym> ───

def test_ticker_returns_detail_and_pack():
    scan_state.setdefault('detail', {})['AAPL'] = {'price': 190.0}
    try:
        j = _client().get('/api/ticker/aapl').get_json()
        assert j['symbol'] == 'AAPL' and j['in_universe'] is True
        assert j['detail'] == {'price': 190.0}
        assert j['pack'] == {'sym': 'AAPL', 'iv': 33.0}
    finally:
        scan_state['detail'].pop('AAPL', None)


# ─── /api/pos-quotes ───

def test_pos_quotes_offline_returns_cache_only():
    calls = []

    def job(kind, args, timeout):
        calls.append(kind)
        return {}
    j = _client(ibkr=False, opt_job=job).post(
        '/api/pos-quotes', json={'positions': [{'sym': 'AAPL'}]}).get_json()
    assert j['live'] is False and j['results'] == {} and calls == []


def test_pos_quotes_live_quotes_and_caches():
    calls = []

    def job(kind, args, timeout):
        calls.append((kind, [p['key'] for p in args[0]]))
        return {p['key']: {'px': 1.23} for p in args[0]}
    c = _client(ibkr=True, opt_job=job)
    body = {'positions': [{'sym': 'AAPL', 'exp': '2026-12', 'strike': 200, 'right': 'C'}]}
    j = c.post('/api/pos-quotes', json=body).get_json()
    key = 'AAPL|2026-12|200|C'
    assert j['live'] is True and j['results'][key] == {'px': 1.23}
    assert calls == [('posq', [key])]
    # 2e appel < TTL → servi du cache, aucun nouveau job IBKR
    j2 = c.post('/api/pos-quotes', json=body).get_json()
    assert j2['results'][key] == {'px': 1.23} and len(calls) == 1


def test_pos_quotes_hard_cap():
    seen = []

    def job(kind, args, timeout):
        seen.extend(args[0])
        return {}
    c = _client(ibkr=True, opt_job=job)
    c.post('/api/pos-quotes', json={'positions': [{'sym': f'S{i}'} for i in range(60)]})
    assert len(seen) == desk.POSQ_MAX_POSITIONS


def test_pos_quotes_ignores_garbage_entries():
    r = _client(ibkr=False).post('/api/pos-quotes', json={'positions': ['x', 42, None]})
    assert r.status_code == 200 and r.get_json()['results'] == {}


# ─── Intégration monolithe ───

def test_terminal_registers_desk_blueprint():
    import terminal
    rules = {r.rule for r in terminal.app.url_map.iter_rules()}
    assert {'/api/desk', '/api/watchlist-tv', '/api/ticker/<sym>', '/api/pos-quotes'} <= rules
