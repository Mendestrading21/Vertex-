"""tests/test_post_routes.py — SKYLER LOT 94 : contrat des routes POST.

Sondes réelles sur les 12 routes POST non couvertes par une suite dédiée
(tradingview en a déjà 12 ; desk/pos-quotes/memory-import figées aux lots
74/84) : TOUTES répondent sans 5xx avec des refus STRUCTURÉS honnêtes
(« symbol requis », « question vide », « jambes manquantes », « scan pas
encore prêt »). Caractérisations nées vertes (dites) + bornes de la
télémétrie client (troncatures 120/300/160, maxlen 100).
"""
import json

import pytest

import terminal


@pytest.fixture()
def client():
    return terminal.app.test_client()


def test_post_routes_never_5xx_with_edge_payloads(client):
    probes = [
        ('/api/ai/refresh', '{}'), ('/api/copilot/ask', 'pas du json'),
        ('/api/options/analyze', '{}'), ('/api/planning/ticket', '{"x": 1e308}'),
        ('/api/portfolio/team', 'null'), ('/api/pretrade/check', '{}'),
        ('/api/tracking', '{}'), ('/api/live/refresh', '{}'),
        ('/weekly-regen', '{}'), ('/login', '{}'),
    ]
    for path, payload in probes:
        r = client.post(path, data=payload, content_type='application/json')
        assert r.status_code < 500, f'{path} → {r.status_code}'


def test_structured_refusals_are_honest(client):
    r = client.post('/api/copilot/ask', data='{"q": ""}',
                    content_type='application/json')
    d = r.get_json()
    assert d['ok'] is False and d['answer'] is None and 'vide' in d['error']

    r = client.post('/api/tracking', json={})
    assert r.status_code == 400 and 'symbol requis' in r.get_data(as_text=True)

    r = client.post('/api/options/analyze', json={})
    d = r.get_json()
    assert d['available'] is False and 'manquant' in d['reason']


def test_client_log_truncates_and_bounds(client):
    huge = {'page': 'P' * 500, 'msg': 'M' * 1000, 'src': 'S' * 500,
            'line': 'pas un entier'}
    r = client.post('/api/client-log', json=huge)
    assert r.status_code == 200
    log = client.get('/api/client-log').get_json()
    last = log['errors'][-1]
    assert len(last['page']) == 120 and len(last['msg']) == 300
    assert len(last['src']) == 160
    assert last['line'] is None, 'line non entier → None, jamais une valeur inventée'


def test_client_log_ring_buffer_capped_at_100(client):
    for i in range(105):
        client.post('/api/client-log', json={'msg': f'borne-{i}'})
    log = client.get('/api/client-log').get_json()
    assert log['count'] <= 100, 'deque maxlen=100 — jamais de croissance infinie'
    msgs = [e['msg'] for e in log['errors']]
    assert 'borne-104' in msgs and 'borne-0' not in msgs, (
        'les plus anciens sont évincés, les récents conservés')
