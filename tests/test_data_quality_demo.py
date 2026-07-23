"""tests/test_data_quality_demo.py — /api/data-quality honnête en mode démo (C-07).

La démo produit des données synthétiques PRÉSENTES : elles doivent être
étiquetées `DEMO`, jamais `MISSING` (qui signifie « absente ») ni comptées comme
« dégradées ». Règle d'intégrité : la démo est étiquetée, pas masquée.
"""
from flask import Flask

from vertex.app.routes import strategy_os_api
from vertex.observability.diagnostics import data_quality_report


def _client(scan_state):
    app = Flask(__name__)
    app.register_blueprint(strategy_os_api.make_blueprint(scan_state))
    return app.test_client()


def test_demo_data_quality_is_labelled_demo_not_missing():
    state = {'source': 'demo', 'detail': {'AAPL': {'price': 1}, 'MSFT': {'price': 2}}}
    r = _client(state).get('/api/data-quality')
    assert r.status_code == 200
    body = r.get_json()
    by_q = body['by_quality']
    assert by_q.get('DEMO') == 2, 'les titres démo doivent être étiquetés DEMO'
    assert 'MISSING' not in by_q, 'la démo ne doit jamais être comptée MISSING'
    # DEMO n'est PAS une dégradation (≠ STALE/EXPIRED/MISSING)
    assert body['degraded'] == []


def test_real_source_stays_recent():
    state = {'source': 'ibkr', 'detail': {'AAPL': {'price': 1}}}
    body = _client(state).get('/api/data-quality').get_json()
    assert body['by_quality'].get('RECENT') == 1
    assert 'DEMO' not in body['by_quality']


def test_no_source_is_missing():
    body = _client({'source': '', 'detail': {'AAPL': {}}}).get('/api/data-quality').get_json()
    assert body['by_quality'].get('MISSING') == 1


def test_report_does_not_degrade_demo_packets():
    rep = data_quality_report([{'symbol': 'X', 'quality': {'overall': 'DEMO', 'warnings': []}}])
    assert rep['by_quality'] == {'DEMO': 1}
    assert rep['degraded'] == []
