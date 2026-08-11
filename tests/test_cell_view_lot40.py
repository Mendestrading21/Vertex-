"""tests/test_cell_view_lot40.py — SKYLER LOT 40 : vue HTML lisible de cellule.

`/memory/cell/<group>/<key>` : rendu HTML serveur d'une cellule de
calibration — résumé (statut, hit rate, n, basis) + table des décisions
MESURÉES (titre, séance, décision, niveau, régime, catalyseur/type,
hit/miss) avec lien post-mortem par record (/memory/<id>). MÊME mécanique
markupsafe que la vue post-mortem du lot 23 : TOUT contenu mémoire échappé.
404 LISIBLES (groupe/cellule inconnus). Les badges de la carte Mémoire
pointent désormais vers la vue lisible (le JSON /api/... reste pour
l'audit). Shell visible → SW v105 → v106.
"""
import json
import re

import pytest

from vertex.engines import decision_memory as DM


def _mk(i, symbol=None, level='A', ret=5.0, version=None):
    from vertex.engines import skyler_core as SK
    version = version or SK.ENGINE_VERSION
    d = {'symbol': symbol or ('V%03d' % i), 'as_of': str(i), 'decision': 'ACHETER',
         'score': {'total': 30, 'level': level, 'insufficient_blocks': []},
         'level': level, 'contradictions': [], 'unknowns': [],
         'catalyst': 'Résultats (J-9)', 'catalyst_kind': 'earnings',
         'scenarios': {'available': True, 'bear': {'return_pct': -6.0},
                       'base': {'return_pct': 12.0}, 'bull': {'return_pct': 18.0}}}
    r = DM.freeze(decision=d, packet={'schema_version': 1, 'engine_version': version},
                  price=100.0, closes=None, portfolio_ctx=None, now=i,
                  session_date='2026-08-0%d' % (1 + i % 5))
    o = {'decision_id': r['decision_id'], 'engine_version': version,
         'symbol': r['symbol'], 'sessions_observed': 20,
         'horizons': {'H20': {'status': 'MESURE', 'sessions': 20,
                              'return_pct': ret, 'basis': 't'}},
         'mfe_pct': None, 'mae_pct': None}
    return r, o


def _store(tmp_path, rows):
    mem = DM.empty_memory()
    for r, o in rows:
        mem = DM.append_outcome(DM.append_decision(mem, r), o)
    (tmp_path / 'skyler_memory.json').write_text(json.dumps(mem),
                                                 encoding='utf-8')
    return mem


@pytest.fixture()
def client(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    return terminal.app.test_client(), tmp_path


def test_cell_view_renders_summary_and_measured_table(client):
    c, tmp = client
    rows = [_mk(i, ret=(5.0 if i < 20 else -15.0)) for i in range(25)]
    _store(tmp, rows)
    r = c.get('/memory/cell/by_level/A')
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert 'niveau=A' in body                     # basis du résumé de cellule
    assert 'V000' in body and 'V024' in body      # décisions listées
    assert '/memory/' in body                     # lien post-mortem par record
    assert body.count('vx-table') >= 1


def test_cell_view_says_hit_and_miss_honestly(client):
    c, tmp = client
    _store(tmp, [_mk(i, ret=(5.0 if i < 20 else -15.0)) for i in range(25)])
    body = c.get('/memory/cell/by_level/A').get_data(as_text=True)
    assert 'contenu' in body.lower() or 'hit' in body.lower()
    assert 'hors' in body.lower() or 'miss' in body.lower()


def test_cell_view_escapes_hostile_memory_content(client):
    """Un symbole hostile figé dans le magasin ne s'exécute JAMAIS dans la
    vue — markupsafe partout (même exigence que la vue post-mortem lot 23)."""
    c, tmp = client
    _store(tmp, [_mk(i) for i in range(20)]
           + [_mk(100, symbol='<script>alert(1)</script>')])
    body = c.get('/memory/cell/by_level/A').get_data(as_text=True)
    assert '<script>alert(1)</script>' not in body
    assert '&lt;script&gt;' in body               # affiché échappé, pas caché


def test_cell_view_readable_404s(client):
    c, _ = client
    r = c.get('/memory/cell/by_magie/A')
    assert r.status_code == 404 and 'inconnu' in r.get_data(as_text=True).lower()
    r2 = c.get('/memory/cell/by_level/INEXISTANT')
    assert r2.status_code == 404
    assert 'cellule' in r2.get_data(as_text=True).lower()


def test_cell_view_corrupted_store_never_500(client):
    c, tmp = client
    (tmp / 'skyler_memory.json').write_text(
        '{"decisions": [7, "x", null], "outcomes": "y"}', encoding='utf-8')
    r = c.get('/memory/cell/by_level/A')
    assert r.status_code in (200, 404) and r.status_code != 500


def test_badges_now_link_to_readable_view():
    import terminal
    body = terminal.app.test_client().get(
        '/journal', follow_redirects=True).get_data(as_text=True)
    assert 'href="/memory/cell/' in body             # les badges visent la vue
    assert 'href="/api/skyler/memory/cell/' not in body


def test_service_worker_bumped_to_at_least_v106():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 106
    assert 'td-shell-v105' not in body
