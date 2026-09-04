from flask import Flask

from vertex.app import input_validation
from vertex.app.routes import analysis_api


def test_symbol_validation_is_strict_and_never_truncates():
    assert input_validation.symbol('aapl') == 'AAPL'
    assert input_validation.symbol('BRK.B') == 'BRK.B'
    assert input_validation.symbol('AAPL!') is None
    assert input_validation.symbol('A' * 13) is None
    assert input_validation.symbol('../AAPL') is None


def test_priority_analytics_routes_reject_invalid_symbol_before_compute():
    app = Flask(__name__)
    app.register_blueprint(analysis_api.bp)
    client = app.test_client()
    for path in ('/api/vertex/AAPL!', '/api/anomalies/AAPL!',
                 '/api/evidence/AAPL!', '/api/skyler/AAPL!'):
        response = client.get(path)
        assert response.status_code == 400
        assert response.get_json()['error'] == 'symbole_invalide'
