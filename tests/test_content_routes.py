"""
tests/test_content_routes.py — Fils de contenu en Blueprint (Ch. II).

News / calendrier / hebdo lisent l'état partagé ; le flag ai_on est présent.
"""

from flask import Flask
from vertex.app.routes import content
from vertex.app import state


def _client():
    app = Flask(__name__)
    app.register_blueprint(content.bp)
    return app.test_client()


def test_content_routes_read_shared_state():
    c = _client()
    for path in ('/news-feed', '/cal-feed', '/weekly-feed'):
        assert c.get(path).status_code == 200


def test_news_and_weekly_expose_ai_flag():
    c = _client()
    assert 'ai_on' in c.get('/news-feed').get_json()
    assert 'ai_on' in c.get('/weekly-feed').get_json()


def test_cal_feed_reflects_shared_state():
    state.cal_state['items'] = [{'d': '2026-07-06', 'title': 'CPI'}]
    try:
        j = _client().get('/cal-feed').get_json()
        assert j['items'] and j['items'][0]['title'] == 'CPI'
    finally:
        state.cal_state['items'] = []


def test_terminal_registered_content_and_kept_regen():
    import terminal
    rules = {r.rule for r in terminal.app.url_map.iter_rules()}
    assert '/news-feed' in rules and '/cal-feed' in rules
    assert '/weekly-regen' in rules            # régen (couplé) reste dans terminal
