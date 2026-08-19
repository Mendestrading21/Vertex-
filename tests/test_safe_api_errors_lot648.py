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
    """Le gestionnaire 500 a déménagé dans `vertex/app/factory.py` (#779/G1).

    Il est désormais éprouvé **de bout en bout** plutôt qu'appelé à la main :
    une route qui lève, une requête réelle, la réponse servie. C'est plus fort
    que l'ancienne forme — elle vérifiait la fonction, celle-ci vérifie en plus
    qu'elle est bien **enregistrée** sur l'application."""
    from vertex.app import factory

    app = factory.create_app()
    app.config['PROPAGATE_EXCEPTIONS'] = False

    @app.route('/api/leve-une-erreur')
    def _leve():
        raise RuntimeError('secret-local-path')

    response = app.test_client().get('/api/leve-une-erreur')
    assert response.status_code == 500
    assert response.get_json() == {'error': 'internal'}
    assert 'secret-local-path' not in response.get_data(as_text=True)


def test_l_application_servie_passe_bien_par_la_fabrique():
    """Le test ci-dessus n'aurait aucune valeur si `terminal.app` était
    construite autrement : il éprouverait une application que personne ne sert."""
    assert 500 in terminal.app.error_handler_spec[None], (
        'l\'application servie n\'a plus de gestionnaire 500 : une exception '
        'd\'API renverrait la page de trace de Flask'
    )
    from werkzeug.exceptions import InternalServerError

    with terminal.app.test_request_context('/api/test'):
        gestionnaire = terminal.app.error_handler_spec[None][500][InternalServerError]
        response, status = gestionnaire(RuntimeError('secret-local-path'))
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
