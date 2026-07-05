"""
tests/test_system_routes.py — Santé système & PWA en Blueprint (Ch. II).

Health-check public, enveloppe PWA correcte, invariant lecture-seule dans
l'état système.
"""

from flask import Flask
from vertex.app.routes import system


def _client():
    app = Flask(__name__)
    app.register_blueprint(system.bp)
    return app.test_client()


def test_healthz_is_public_and_ok():
    r = _client().get('/healthz')
    assert r.status_code == 200
    j = r.get_json()
    assert j['status'] == 'ok' and 'build' in j and 'engines' in j


def test_system_status_asserts_readonly_invariant():
    j = _client().get('/api/system-status').get_json()
    assert j['readonly'] is True and j['analysis_only'] is True


def test_favicon_is_inline_svg():
    r = _client().get('/favicon.svg')
    assert r.status_code == 200
    assert 'image/svg+xml' in r.headers['Content-Type']
    assert b'<svg' in r.data


def test_manifest_is_standalone_pwa():
    j = _client().get('/manifest.webmanifest').get_json()
    assert j['display'] == 'standalone' and j['short_name'] == 'Vertex'


def test_service_worker_served_as_js():
    r = _client().get('/sw.js')
    assert r.status_code == 200
    assert 'javascript' in r.headers['Content-Type']
    assert r.headers.get('Service-Worker-Allowed') == '/'


def test_terminal_registered_system():
    import terminal
    rules = {r.rule for r in terminal.app.url_map.iter_rules()}
    assert '/healthz' in rules and '/sw.js' in rules and '/manifest.webmanifest' in rules
