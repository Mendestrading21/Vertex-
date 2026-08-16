from flask import Flask

import terminal
from vertex.app.routes import command, opportunities_api
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


def test_command_and_opportunities_do_not_expose_exception_text(monkeypatch):
    app = Flask(__name__)
    app.register_blueprint(command.bp)
    app.register_blueprint(opportunities_api.bp)
    monkeypatch.setitem(command.scan_state, 'rows', [{'symbol': 'SAFE'}])
    monkeypatch.setattr(command.strategy, 'build_portfolio',
                        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError('secret-capital-path')))
    monkeypatch.setattr(opportunities_api._funnel, 'build_funnel',
                        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError('secret-funnel-path')))
    client = app.test_client()
    command_response = client.get('/api/portefeuille')
    funnel_response = client.get('/api/opportunities/funnel')
    assert command_response.get_json()['error'] == 'portfolio_analysis_unavailable'
    assert funnel_response.get_json()['error'] == 'opportunities_funnel_unavailable'
    assert 'secret-' not in command_response.get_data(as_text=True)
    assert 'secret-' not in funnel_response.get_data(as_text=True)
