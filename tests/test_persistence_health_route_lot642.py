from flask import Flask

from vertex.app.routes import analysis_api


def test_health_route_exposes_only_non_sensitive_persistence_counters():
    app = Flask(__name__)
    app.register_blueprint(analysis_api.bp)
    out = app.test_client().get('/api/skyler/health').get_json()
    assert out['read_only'] is True
    assert 'persistence' in out
    assert 'memory_entries' in out['persistence']
    assert '_BASE_DIR' not in out['persistence']
