"""tests/test_no_store_personnel.py — contrôle 025 de l'audit-150.

Mesuré : seules les routes /api/desk portaient `Cache-Control: no-store`.
Les autres surfaces PERSONNELLES (positions déclarées, portefeuille,
suivi, journal, track-record) partaient sans directive — un cache
intermédiaire partagé pouvait retenir des données de patrimoine. Né ROUGE.
"""
import pytest


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


@pytest.mark.parametrize('chemin', [
    '/api/desk/load', '/api/positions/state', '/api/positions/report',
    '/api/portfolio/stress', '/api/portfolio/team', '/api/tracking',
    '/api/journal/postmortem', '/api/track-record',
])
def test_les_routes_personnelles_sont_no_store(client, chemin):
    r = client.get(chemin)
    #  le statut importe peu (404/405 compris) : l'en-tête doit couvrir
    #  TOUTE réponse de ces préfixes, une erreur aussi.
    assert r.headers.get('Cache-Control') == 'no-store', (
        '%s → %r' % (chemin, r.headers.get('Cache-Control')))


def test_une_route_publique_reste_cacheable(client):
    r = client.get('/healthz')
    assert r.headers.get('Cache-Control') != 'no-store'
