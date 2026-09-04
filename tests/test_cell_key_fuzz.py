"""tests/test_cell_key_fuzz.py — SKYLER LOT 43 : fuzz clés des routes cellule.

Les routes cellule (lots 39/40) sont POSTÉRIEURES à la batterie HTTP du
lot 34 — la couverture adversariale « complète » avait donc un trou. Batterie
à LISTE FIXE (zéro aléatoire) sur les DEUX routes :
`/api/skyler/memory/cell/<group>/<key>` (JSON) et `/memory/cell/<group>/<key>`
(HTML). Contrat : JAMAIS de 500 ; 404 structuré (JSON) / lisible (HTML) ;
clé hostile JAMAIS réfléchie brute ; une cellule valide reste servie au
milieu des clés hostiles ; unicode NFD/percent-encodé/500 chars tolérés.
"""
import json
import unicodedata

import pytest

from vertex.engines import decision_memory as DM


DEGENERATE_KEYS = ('%2e%2e', '%2e%2e%2f%2e%2e', 'K' * 500,
                   '<script>alert(1)</script>', "l'clé",
                   unicodedata.normalize('NFD', 'décomposé'),   # é en NFD
                   '漢字', ' ', '%20', 'null', 'undefined', '-')

DEGENERATE_GROUPS = ('by_magie', '%2e%2e', 'G' * 500, '<script>')


@pytest.fixture()
def client(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    return terminal.app.test_client(), tmp_path


def _seed_measured(tmp_path):
    """25 records mesurés niveau A sous le moteur courant → cellule réelle."""
    from vertex.engines import skyler_core as SK
    mem = DM.empty_memory()
    for i in range(25):
        d = {'symbol': 'F%03d' % i, 'as_of': str(i), 'decision': 'ACHETER',
             'score': {'total': 30, 'level': 'A', 'insufficient_blocks': []},
             'level': 'A', 'contradictions': [], 'unknowns': []}
        r = DM.freeze(decision=d, packet={'schema_version': 1,
                                          'engine_version': SK.ENGINE_VERSION},
                      price=100.0, closes=None, portfolio_ctx=None, now=i)
        r_scen = dict(r)
        mem = DM.append_decision(mem, r_scen)
        mem = DM.append_outcome(mem, {
            'decision_id': r['decision_id'], 'engine_version': SK.ENGINE_VERSION,
            'symbol': r['symbol'], 'sessions_observed': 20,
            'horizons': {'H20': {'status': 'MESURE', 'sessions': 20,
                                 'return_pct': 5.0, 'basis': 't'}},
            'mfe_pct': None, 'mae_pct': None})
    (tmp_path / 'skyler_memory.json').write_text(json.dumps(mem),
                                                 encoding='utf-8')


def test_api_cell_degenerate_keys_never_500(client):
    c, _ = client
    for k in DEGENERATE_KEYS:
        r = c.get('/api/skyler/memory/cell/by_level/' + k)
        assert r.status_code in (200, 404), 'key=%r → HTTP %d' % (k, r.status_code)
        if r.status_code == 404:
            d = r.get_json()
            assert d and (d.get('ok') is False or d.get('error'))


def test_api_cell_degenerate_groups_never_500(client):
    c, _ = client
    for g in DEGENERATE_GROUPS:
        r = c.get('/api/skyler/memory/cell/%s/A' % g)
        assert r.status_code in (200, 404), 'group=%r → HTTP %d' % (g, r.status_code)
        if r.status_code == 404:
            d = r.get_json()
            assert d and (d.get('ok') is False or d.get('error'))


def test_view_cell_degenerate_keys_never_500_never_reflected(client):
    c, _ = client
    for k in DEGENERATE_KEYS:
        r = c.get('/memory/cell/by_level/' + k)
        assert r.status_code in (200, 404), 'key=%r → HTTP %d' % (k, r.status_code)
        assert '<script>alert(1)</script>' not in r.get_data(as_text=True)


def test_view_cell_degenerate_groups_never_500_never_reflected(client):
    c, _ = client
    for g in DEGENERATE_GROUPS:
        r = c.get('/memory/cell/%s/A' % g)
        assert r.status_code in (200, 404), 'group=%r → HTTP %d' % (g, r.status_code)
        assert '<script>' not in r.get_data(as_text=True)


def test_valid_cell_served_amid_hostile_keys(client):
    """Les clés hostiles n'empoisonnent rien : la cellule réelle reste servie
    exactement entre deux salves de fuzz."""
    c, tmp = client
    _seed_measured(tmp)
    for k in DEGENERATE_KEYS[:4]:
        c.get('/api/skyler/memory/cell/by_level/' + k)
    r = c.get('/api/skyler/memory/cell/by_level/A')
    assert r.status_code == 200 and r.get_json()['n_measured'] == 25
    for k in DEGENERATE_KEYS[4:]:
        c.get('/memory/cell/by_level/' + k)
    r2 = c.get('/memory/cell/by_level/A')
    assert r2.status_code == 200 and 'F000' in r2.get_data(as_text=True)


def test_traversal_paths_never_serve_files(client):
    c, _ = client
    for path in ('/memory/cell/by_level/../../etc/passwd',
                 '/api/skyler/memory/cell/../../../etc/passwd'):
        r = c.get(path)
        assert r.status_code != 500
        assert b'root:' not in r.get_data()


def test_nfd_key_matches_only_itself(client):
    """Une clé NFD ne matche pas silencieusement une cellule NFC — pas de
    normalisation cachée : la donnée figée est la seule vérité."""
    c, tmp = client
    _seed_measured(tmp)
    nfd_a = unicodedata.normalize('NFD', 'Á')      # ≠ 'A'
    r = c.get('/api/skyler/memory/cell/by_level/' + nfd_a)
    assert r.status_code == 404
