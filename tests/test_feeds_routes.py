"""
tests/test_feeds_routes.py — Flux de données en Blueprint (Ch. II).

Import direct de l'état partagé, réponses lecture seule, jamais d'erreur 500
sur état vide.
"""

from flask import Flask
from vertex.app.routes import feeds


def _app():
    app = Flask(__name__)
    app.register_blueprint(feeds.bp)
    return app


def test_all_feed_routes_registered():
    rules = {r.rule for r in _app().url_map.iter_rules()}
    for path in ('/api/market/summary', '/api/cockpit', '/api/watchlist', '/api/options',
                 '/api/search', '/api/weekly', '/api/strategie', '/api/comite'):
        assert path in rules


def test_feeds_are_read_only_and_safe_on_empty_state():
    c = _app().test_client()
    for path in ('/api/market/summary', '/api/cockpit', '/api/watchlist', '/api/options',
                 '/api/weekly', '/api/strategie', '/api/comite'):
        r = c.get(path)
        assert r.status_code == 200, path


def test_market_summary_verdict_tracks_score():
    from vertex.app import state
    state.scan_state['market_ctx'] = {'spy_regime': 'TREND', 'roro': 'RISK-ON',
                                      'vix_band': 'calme', 'breadth': {'above50': 75}}
    try:
        j = _app().test_client().get('/api/market/summary').get_json()
        assert j['verdict'] == 'FAVORABLE' and j['score'] >= 65
    finally:
        state.scan_state['market_ctx'] = None


def test_search_filters_universe():
    j = _app().test_client().get('/api/search?q=AAP').get_json()
    assert isinstance(j, list) and all('AAP' in x['ticker'] for x in j)


def test_terminal_registered_feeds():
    import terminal
    rules = {r.rule for r in terminal.app.url_map.iter_rules()}
    assert '/api/cockpit' in rules and '/api/watchlist' in rules
