"""tests/test_headers_lot77.py — SKYLER LOT 77 : sécurité en-têtes/contenu servi.

Mesures : les 4 en-têtes de sécurité (nosniff, SAMEORIGIN, Referrer-Policy,
Permissions-Policy) sont présents sur pages HTML ET API ; Content-Type
corrects partout ; sw.js en no-cache ; contenu servi (8 pages + JS
statiques) : 0 email, 0 secret, 0 chemin absolu — SAINS.

UN défaut réel : `/api/desk` sert le blob de données PERSONNELLES
(trades, positions, journal) SANS Cache-Control — un cache intermédiaire
(proxy, navigateur partagé) pouvait le stocker. Corrigé PAR la source
(middleware `_security_headers`) : `Cache-Control: no-store` sur toutes
les routes /api/desk*.
"""
import pytest

import terminal


@pytest.fixture()
def client():
    return terminal.app.test_client()


def test_desk_personal_data_is_no_store(client):
    for path in ('/api/desk', '/api/desk/backups'):
        r = client.get(path)
        assert r.status_code == 200
        assert r.headers.get('Cache-Control') == 'no-store', (
            f'{path} : données personnelles — no-store obligatoire, '
            f'reçu {r.headers.get("Cache-Control")!r}')


def test_security_headers_on_pages_and_api(client):
    for path in ('/', '/markets', '/api/command', '/api/market/summary'):
        h = client.get(path).headers
        assert h.get('X-Content-Type-Options') == 'nosniff', path
        assert h.get('X-Frame-Options') == 'SAMEORIGIN', path
        assert h.get('Referrer-Policy'), path
        assert h.get('Permissions-Policy'), path
