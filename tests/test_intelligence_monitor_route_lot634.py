from flask import Flask

from vertex.app.routes import analysis_api
from vertex.engines import intelligence_monitor as monitor


def test_monitor_route_rejects_unknown_horizon():
    app = Flask(__name__)
    app.register_blueprint(analysis_api.bp)
    response = app.test_client().get('/api/skyler/monitor?horizon=H999')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'horizon_invalide'


def test_monitor_contract_marks_small_sample_as_unavailable():
    out = monitor.assess({'decisions': [], 'outcomes': []}, 'test-v1', horizon='H10')
    assert out['available'] is False
    assert out['status'] == 'INSUFFICIENT_SAMPLE'
    assert out['read_only'] is True
