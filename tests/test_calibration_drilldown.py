"""tests/test_calibration_drilldown.py — SKYLER LOT 39 : drill-down cellule.

Un badge de calibration par contexte dit « niveau=A : 0,82 (25 mesures) » —
mais QUELLES 25 décisions ? `decision_memory.cell_decisions` répond :
les décisions MESURÉES d'une cellule, avec hit/miss par record, via la MÊME
règle d'appartenance que `calibration_by_context` (source unique,
anti-divergence). Route `GET /api/skyler/memory/cell/<group>/<key>` —
404 structuré si groupe ou cellule inconnus, jamais 500, magasin corrompu
toléré. Badges de la carte Mémoire cliquables → SW v104 → v105.
"""
import re

import pytest

from vertex.engines import decision_memory as DM


def _mk(i, catalyst='Résultats (J-21)', kind='earnings', level='A',
        ret=5.0, version='vD'):
    d = {'symbol': 'D%03d' % i, 'as_of': str(i), 'decision': 'ACHETER',
         'score': {'total': 30, 'level': level, 'insufficient_blocks': []},
         'level': level, 'contradictions': [], 'unknowns': [],
         'catalyst': catalyst,
         'scenarios': {'available': True, 'bear': {'return_pct': -6.0},
                       'base': {'return_pct': 12.0}, 'bull': {'return_pct': 18.0}}}
    if kind is not None:
        d['catalyst_kind'] = kind
    r = DM.freeze(decision=d, packet={'schema_version': 1, 'engine_version': version},
                  price=100.0, closes=None, portfolio_ctx=None, now=i)
    o = {'decision_id': r['decision_id'], 'engine_version': version,
         'symbol': r['symbol'], 'sessions_observed': 20,
         'horizons': {'H20': {'status': 'MESURE', 'sessions': 20,
                              'return_pct': ret, 'basis': 't'}},
         'mfe_pct': None, 'mae_pct': None}
    return r, o


def _mem(rows):
    mem = DM.empty_memory()
    for r, o in rows:
        mem = DM.append_outcome(DM.append_decision(mem, r), o)
    return mem


def _built():
    rows = [_mk(i, kind='earnings', ret=(5.0 if i < 20 else -15.0))
            for i in range(25)]
    rows += [_mk(100 + i, kind='macro', ret=3.0) for i in range(3)]
    rows += [_mk(200 + i, catalyst=None, kind=None, ret=3.0) for i in range(3)]
    return _mem(rows)


# ─── Moteur : mêmes règles d'appartenance que calibration_by_context ────────────

def test_cell_decisions_matches_cell_counts():
    mem = _built()
    out = DM.cell_decisions(mem, 'vD', 'by_catalyst_type', 'earnings')
    assert out['n_measured'] == 25
    assert out['hits'] == 20                       # hit rate 0,8 du lot 30
    assert len(out['decisions']) == 25
    first = out['decisions'][0]
    assert first['decision_id'] and first['symbol'] and 'hit' in first


def test_cell_decisions_anti_divergence_all_groups():
    """Pour CHAQUE cellule publiée par calibration_by_context, le drill-down
    retrouve EXACTEMENT le même n_measured — source unique prouvée."""
    mem = _built()
    ctx = DM.calibration_by_context(mem, 'vD')
    checked = 0
    for group in DM.CONTEXT_GROUPS:
        for key, cell in (ctx.get(group) or {}).items():
            out = DM.cell_decisions(mem, 'vD', group, key)
            assert out['n_measured'] == cell['n_measured'], (group, key)
            checked += 1
    assert checked >= 5                            # plusieurs cellules réelles


def test_cell_decisions_unknown_group_or_degenerate_refused():
    mem = _built()
    for group, key in (('by_magie', 'A'), ('', 'A'), (None, 'A'),
                       ({'g': 1}, 'A'), ('by_level', ''), ('by_level', None),
                       ('by_level', {'k': 1})):
        assert DM.cell_decisions(mem, 'vD', group, key) is None


def test_cell_decisions_version_separation():
    """Les décisions d'une AUTRE version ne fuient jamais dans la cellule."""
    mem = _built()
    out = DM.cell_decisions(mem, 'vAUTRE', 'by_catalyst', 'avec_catalyseur')
    assert out['n_measured'] == 0 and out['decisions'] == []


# ─── Route : 404 structurés, jamais 500 ─────────────────────────────────────────

@pytest.fixture()
def client(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    return terminal.app.test_client(), tmp_path


def test_route_serves_cell_with_summary(client, monkeypatch):
    import json as _json
    from vertex.engines import skyler_core as SK
    c, tmp = client
    rows = [_mk(i, version=SK.ENGINE_VERSION) for i in range(25)]
    (tmp / 'skyler_memory.json').write_text(_json.dumps(_mem(rows)),
                                            encoding='utf-8')
    r = c.get('/api/skyler/memory/cell/by_level/A')
    assert r.status_code == 200
    d = r.get_json()
    assert d['n_measured'] == 25 and len(d['decisions']) == 25
    assert d['cell']['status'] == 'MESURE'         # résumé de cellule joint


def test_route_unknown_group_structured_404(client):
    c, _ = client
    r = c.get('/api/skyler/memory/cell/by_magie/A')
    assert r.status_code == 404
    d = r.get_json()
    assert d['ok'] is False and d['error'] == 'groupe_inconnu'
    assert 'by_level' in d['groups']


def test_route_unknown_cell_structured_404(client):
    c, _ = client
    r = c.get('/api/skyler/memory/cell/by_level/INEXISTANT')
    assert r.status_code == 404
    assert r.get_json()['error'] == 'cellule_inconnue'


def test_route_corrupted_store_never_500(client):
    c, tmp = client
    (tmp / 'skyler_memory.json').write_text(
        '{"decisions": [7, "x", null], "outcomes": "y"}', encoding='utf-8')
    r = c.get('/api/skyler/memory/cell/by_level/A')
    assert r.status_code in (200, 404) and r.status_code != 500


# ─── UI : badges cliquables + SW v105 ───────────────────────────────────────────

def test_memory_card_badges_link_to_cells():
    # depuis le lot 40, les badges visent la VUE LISIBLE /memory/cell/… ;
    # l'API JSON /api/skyler/memory/cell reste servie (tests de route ci-dessus)
    import terminal
    body = terminal.app.test_client().get(
        '/journal', follow_redirects=True).get_data(as_text=True)
    assert '/memory/cell/' in body


def test_service_worker_bumped_to_at_least_v105():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 105
    assert 'td-shell-v104' not in body
