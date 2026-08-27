"""tests/test_robust_lot74.py — SKYLER LOT 74 : robustesse données limites.

Sondes réelles (serveur démo) : symboles invalides/injection/longs/unicode
sur /analysis/<SYM> et /api/skyler/<SYM>, ?view=inexistant sur les 8
pages, POST malformés sur /api/pos-quotes — résultat : PARTOUT 200 avec
état honnête ou 4xx structuré, 0×5xx, aucun écho XSS (le 404 API est
application/json + X-Content-Type-Options: nosniff — jamais interprété
HTML ; la page 404 HTML n'échoit pas le chemin). SAIN — lot documentaire.

Gardiens PROSPECTIFS (nés verts, dits) : ils fixent ce contrat de
robustesse pour toujours.
"""
import json

import pytest

import terminal


@pytest.fixture()
def client():
    return terminal.app.test_client()


BAD_SYMS = ['INEXISTANT', 'aaa', 'AAPL;DROP TABLE', 'A' * 120, 'été',
            '<script>alert(1)</script>', '-1', 'NULL']
#  `/markets` retire : Marches est fusionne dans le Dashboard et la route
#  redirige (302). Une redirection n'est pas un 5xx — ce banc verifie
#  qu'une vue inconnue ne casse rien, pas qu'une page existe.
PAGES = ['/', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system']


def test_bad_symbols_never_5xx(client):
    for s in BAD_SYMS:
        for tpl in ('/analysis/{}', '/api/skyler/{}'):
            r = client.get(tpl.format(s))
            assert r.status_code < 500, f'{tpl.format(s)!r} → {r.status_code}'


def test_api_404_is_json_nosniff_not_html(client):
    r = client.get('/api/skyler/<script>alert(1)</script>')
    assert r.status_code == 404
    assert r.content_type.startswith('application/json')
    assert r.headers.get('X-Content-Type-Options') == 'nosniff'
    json.loads(r.get_data(as_text=True))  # corps strictement JSON


def test_unknown_view_param_never_5xx(client):
    for p in PAGES:
        r = client.get(p + '?view=inexistant__')
        assert r.status_code == 200, f'{p} → {r.status_code}'


def test_malformed_pos_quotes_payloads_honest(client):
    for payload in ('not json at all', '{"positions":"pas une liste"}',
                    '{"positions":[{"symbol":1e308}]}', '[]', 'null'):
        r = client.post('/api/pos-quotes', data=payload,
                        content_type='application/json')
        assert r.status_code < 500, f'{payload!r} → {r.status_code}'
        if r.status_code == 200:
            d = json.loads(r.get_data(as_text=True))
            assert d.get('live') is False and 'ts' in d, (
                'refus honnête attendu : live:false + ts, jamais un chiffre inventé')
