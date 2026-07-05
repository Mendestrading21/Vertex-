"""
tests/test_decision_api_routes.py — API décision en Blueprint (Ch. II).

Le premier groupe de routes sorti du monolithe : état injecté, mêmes réponses.
"""

from flask import Flask
from vertex.app.routes import decision_api


def _app_with_state(scan_state):
    app = Flask(__name__)
    app.register_blueprint(decision_api.make_blueprint(scan_state=scan_state, demo_mode=True))
    return app


def test_blueprint_registers_the_three_routes():
    app = _app_with_state({})
    rules = {r.rule for r in app.url_map.iter_rules()}
    assert '/api/decision/<sym>' in rules
    assert '/api/brief' in rules
    assert '/api/committee-review' in rules


def test_empty_state_is_honest_not_crashing():
    # Sans scan (état vide) : la décision est DATA_INSUFFICIENT, jamais une erreur 500.
    c = _app_with_state({}).test_client()
    r = c.get('/api/decision/AAPL')
    assert r.status_code == 200
    assert r.get_json()['final_decision'] == 'DATA_INSUFFICIENT'
    b = c.get('/api/brief')
    assert b.status_code == 200 and b.get_json()['counts']['buy'] == 0
    rv = c.get('/api/committee-review')
    assert rv.status_code == 200 and rv.get_json()['count'] == 0


def test_injected_state_is_live():
    # scan_state est injecté par référence : muter le dict après l'enregistrement se voit.
    state = {}
    app = _app_with_state(state)
    state['rows'] = [{'symbol': 'AAPL', 'score': 80}]
    state['detail'] = {'AAPL': {'symbol': 'AAPL'}}
    j = app.test_client().get('/api/brief').get_json()
    assert any(s['symbol'] == 'AAPL' for s in j['setups'])   # la route voit l'état frais


def test_terminal_registered_the_blueprint():
    import terminal
    rules = {r.rule for r in terminal.app.url_map.iter_rules()}
    assert '/api/brief' in rules and '/api/committee-review' in rules
