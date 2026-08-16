from flask import Flask

import terminal
from vertex.app.routes import options_intel_api


def test_options_overview_does_not_expose_exception_text(monkeypatch):
    app = Flask(__name__)
    app.register_blueprint(options_intel_api.bp)
    monkeypatch.setattr(options_intel_api._ov, 'summarize',
                        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError('secret-board-path')))
    response = app.test_client().get('/api/options/overview')
    assert response.status_code == 500
    assert response.get_json()['error'] == 'options_overview_unavailable'
    assert 'secret-board-path' not in response.get_data(as_text=True)


def test_global_api_error_does_not_expose_exception_text():
    with terminal.app.test_request_context('/api/test'):
        response, status = terminal._err_500(RuntimeError('secret-local-path'))
    assert status == 500
    assert response.get_json() == {'error': 'internal'}
