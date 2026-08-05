"""tests/test_http_fuzz_lot34.py — SKYLER LOT 34 : fuzz HTTP graphe/mémoire.

Batterie à LISTE FIXE (zéro aléatoire) sur les routes HTTP des lots 20/23/28 :
`/api/skyler/graph/<sym>` (?hops= dégénérés, symboles dégénérés),
`/api/skyler/memory/<decision_id>` et `/memory/<decision_id>` (ids dégénérés,
traversée, XSS, magasin corrompu). Contrat : JAMAIS de 500 — 200 avec clamp
dit, ou 404 structuré/lisible ; l'id hostile n'est JAMAAIS réfléchi sans
échappement dans le HTML.
"""
import json

import pytest


@pytest.fixture()
def client():
    import terminal
    return terminal.app.test_client()


# ─── /api/skyler/graph/<sym> — hops et symboles dégénérés ───────────────────────

DEGENERATE_HOPS = ('abc', '', '-1', '0', '99', '1e9', '3.5', 'None')


def test_graph_degenerate_hops_clamped_never_500(client):
    for h in DEGENERATE_HOPS:
        r = client.get('/api/skyler/graph/AAPL?hops=%s' % h)
        assert r.status_code == 200, 'hops=%r → HTTP %d' % (h, r.status_code)
        d = r.get_json()
        assert 1 <= d['hops'] <= 3                  # clamp TOUJOURS appliqué
        assert 'truncated' in d                     # troncature toujours dite


DEGENERATE_SYMS = ('A' * 500, 'AA PL', "l'sym", '<script>alert(1)</script>',
                   'sym%00', 'éàç漢字', '..', '...', 'CON', '-', '_')


def test_graph_degenerate_symbols_never_500(client):
    for s in DEGENERATE_SYMS:
        r = client.get('/api/skyler/graph/' + s)
        assert r.status_code != 500, 'sym=%r → HTTP 500' % s
        if r.status_code == 200:                    # réponse structurée honnête
            assert 'paths' in r.get_json()


# ─── /api/skyler/memory/<decision_id> — ids dégénérés → 404 structuré ───────────

DEGENERATE_IDS = ('x' * 500, "l'id", '<script>alert(1)</script>',
                  '%2e%2e%2f%2e%2e%2fetc%2fpasswd', 'décision-éàç',
                  '00000000deadbeef', ' ', '%20', 'null', 'undefined')


def test_memory_detail_degenerate_ids_structured_404(client):
    for i in DEGENERATE_IDS:
        r = client.get('/api/skyler/memory/' + i)
        assert r.status_code in (200, 404) and r.status_code != 500, \
            'id=%r → HTTP %d' % (i, r.status_code)
        if r.status_code == 404:
            d = r.get_json()
            # 404 STRUCTURÉ, jamais nu — forme route (ok:False) ou forme
            # applicative (error:not_found) selon que le chemin matche ou non
            assert d and (d.get('ok') is False or d.get('error'))


def test_memory_traversal_path_never_500(client):
    for path in ('/api/skyler/memory/../../etc/passwd',
                 '/memory/../../../etc/passwd'):
        r = client.get(path)
        assert r.status_code != 500
        assert b'root:' not in r.get_data()         # jamais un fichier système


# ─── /memory/<decision_id> — vue HTML : 404 lisible, jamais de reflet XSS ───────

def test_memory_view_degenerate_ids_readable_404_no_xss(client):
    for i in DEGENERATE_IDS:
        r = client.get('/memory/' + i)
        assert r.status_code in (200, 404) and r.status_code != 500, \
            'id=%r → HTTP %d' % (i, r.status_code)
        body = r.get_data(as_text=True)
        assert '<script>alert(1)</script>' not in body   # jamais réfléchi brut


# ─── Magasin corrompu : les routes détail ne tombent JAMAIS en 500 ──────────────

CORRUPTED_MEMORY = json.dumps({
    'schema': 1,
    'decisions': ['corrompu', 42, None, [], {'decision_id': 'ok1', 'symbol': 'OK',
                                             'decision': 'ATTENDRE'}],
    'outcomes': ['corrompu', 7, None, {}],
})


@pytest.fixture()
def corrupted_store(tmp_path, monkeypatch):
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    (tmp_path / 'skyler_memory.json').write_text(CORRUPTED_MEMORY,
                                                 encoding='utf-8')


def test_memory_detail_survives_corrupted_store(client, corrupted_store):
    r = client.get('/api/skyler/memory/inconnu123')
    assert r.status_code == 404 and r.get_json().get('ok') is False
    r2 = client.get('/api/skyler/memory/ok1')       # l'entrée valide reste servie
    assert r2.status_code == 200
    assert r2.get_json()['record']['symbol'] == 'OK'


def test_memory_view_survives_corrupted_store(client, corrupted_store):
    r = client.get('/memory/inconnu123')
    assert r.status_code == 404
    r2 = client.get('/memory/ok1')
    assert r2.status_code == 200 and 'OK' in r2.get_data(as_text=True)


def test_memory_list_survives_corrupted_store(client, corrupted_store):
    r = client.get('/api/skyler/memory')
    assert r.status_code == 200                     # la liste ne tombe jamais
