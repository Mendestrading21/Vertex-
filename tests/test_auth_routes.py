"""
tests/test_auth_routes.py — Verrou d'accès en Blueprint (Ch. II · Ch. XV).

Le verrou est testé en ISOLATION (app Flask minimale + code injecté) : garde
globale, login/logout, anti-force-brute, et refus des redirections ouvertes.
Le conftest désactive le verrou pour le reste de la suite — ici on l'active
explicitement via make_blueprint(code=...).
"""

from flask import Flask

from vertex.app.routes import auth


CODE = '4321'


def _app(code=CODE):
    app = Flask(__name__)
    app.secret_key = 'test-secret'
    app.register_blueprint(auth.make_blueprint(code=code))

    @app.route('/')
    def home():
        return 'HOME'

    @app.route('/api/watchlist')
    def api_watchlist():
        return 'DATA'

    @app.route('/healthz')
    def healthz():
        return 'OK'

    return app


def _login(client, code=CODE, next_='/'):
    return client.post('/login?next=' + next_, data={'code': code})


# ─── Garde globale (before_app_request) ───

def test_pages_redirect_to_login_when_locked():
    r = _app().test_client().get('/')
    assert r.status_code == 302
    assert r.headers['Location'].startswith('/login?next=/')


def test_api_returns_401_json_when_locked():
    r = _app().test_client().get('/api/watchlist')
    assert r.status_code == 401
    assert r.get_json() == {'error': 'auth', 'login': '/login'}


def test_health_stays_public_when_locked():
    r = _app().test_client().get('/healthz')
    assert r.status_code == 200 and r.data == b'OK'


def test_gate_inactive_without_code():
    c = _app(code='').test_client()
    assert c.get('/').status_code == 200
    assert c.get('/api/watchlist').status_code == 200
    # /login sans verrou renvoie vers l'accueil
    r = c.get('/login')
    assert r.status_code == 302 and r.headers['Location'] == '/'


# ─── Login / logout ───

def test_login_page_renders_form():
    r = _app().test_client().get('/login')
    assert r.status_code == 200
    assert b'VERTEX' in r.data and b'name="code"' in r.data


def test_good_code_opens_session():
    c = _app().test_client()
    r = _login(c)
    assert r.status_code == 302 and r.headers['Location'] == '/'
    assert c.get('/').status_code == 200
    assert c.get('/api/watchlist').status_code == 200


def test_bad_code_stays_locked():
    c = _app().test_client()
    r = _login(c, code='0000')
    assert r.status_code == 200 and 'Code incorrect'.encode() in r.data
    assert c.get('/api/watchlist').status_code == 401


def test_logout_clears_session():
    c = _app().test_client()
    _login(c)
    r = c.get('/logout')
    assert r.status_code == 302 and r.headers['Location'] == '/login'
    assert c.get('/api/watchlist').status_code == 401


def test_next_param_is_honoured():
    c = _app().test_client()
    r = _login(c, next_='/journal')
    assert r.headers['Location'] == '/journal'


# ─── Anti-force-brute ───

def test_lockout_after_five_failures():
    c = _app().test_client()
    for _ in range(5):
        r = _login(c, code='0000')
    assert 'Bloqué'.encode() in r.data
    # même le bon code est refusé pendant le verrou
    r = _login(c)
    assert "Trop d'essais".encode() in r.data
    assert c.get('/api/watchlist').status_code == 401


def test_fail_counters_are_per_instance():
    a = _app().test_client()
    for _ in range(6):
        _login(a, code='0000')
    b = _app().test_client()          # nouveau blueprint → compteur neuf
    assert _login(b).status_code == 302


# ─── Redirections sûres ───

def test_next_rejects_absolute_urls():
    c = _app().test_client()
    assert _login(c, next_='https://evil.com').headers['Location'] == '/'


def test_next_rejects_protocol_relative_urls():
    c = _app().test_client()
    assert _login(c, next_='//evil.com').headers['Location'] == '/'


def test_login_form_escapes_next():
    r = _app().test_client().get('/login?next=/"><script>alert(1)</script>')
    assert b'<script>alert(1)' not in r.data


# ─── Intégration monolithe ───

def test_terminal_registers_auth_blueprint():
    import terminal
    rules = {r.rule for r in terminal.app.url_map.iter_rules()}
    assert '/login' in rules and '/logout' in rules
