from flask import Flask

from vertex.app.routes import system
from vertex.app.state import scan_state


def test_healthz_exposes_only_safe_scan_code_and_source_status(monkeypatch):
    app = Flask(__name__)
    app.register_blueprint(system.bp)
    monkeypatch.setitem(scan_state, 'error', 'scan_failed')
    monkeypatch.setitem(scan_state, 'source_health', {
        'scan': 'DEGRADED', 'market': 'UNKNOWN', 'options': 'UNKNOWN',
        'fundamentals': 'UNKNOWN',
    })
    out = app.test_client().get('/healthz').get_json()
    assert out['scan_error'] == 'scan_failed'
    assert out['source_health']['scan'] == 'DEGRADED'
    assert 'Exception' not in str(out) and 'Traceback' not in str(out)
