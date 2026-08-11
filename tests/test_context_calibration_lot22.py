"""tests/test_context_calibration_lot22.py — SKYLER LOT 22 : calibration par contexte.

SCENARIO_CALIBRATION §13 : découper les résultats par contexte. La calibration
se découpe par NIVEAU (S_PLUS/S/A/B/REFUS_WATCH) et par DÉCISION
(ACHETER/ATTENDRE/REFUSER) — chaque cellule reçoit son propre hit rate
SEULEMENT si son échantillon atteint MIN_CALIBRATION_SAMPLE ; sinon la cellule
est honnêtement INSUFFISANTE et l'agrégat global reste le secours. Jamais de
mélange de versions. `decide()` consomme le facteur CONTEXTUEL du niveau
courant quand il existe (0.6.0 → 0.7.0 : règle de consommation changée).
"""
import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import skyler_core as SK


def _mk(i, decision='ACHETER', level='A', ret=5.0, version='vC'):
    d = {'symbol': 'X%03d' % i, 'as_of': str(i), 'decision': decision,
         'score': {'total': 30, 'level': level, 'insufficient_blocks': []},
         'level': level, 'contradictions': [], 'unknowns': [],
         'scenarios': {'available': True, 'bear': {'return_pct': -6.0},
                       'base': {'return_pct': 12.0}, 'bull': {'return_pct': 18.0}}}
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


# ─── Découpe par contexte, honnête sous échantillon ─────────────────────────────

def test_context_cells_need_their_own_sample():
    """25 mesures A/ACHETER (80 % hits) mais 3 mesures B/ATTENDRE : la cellule
    A obtient SON hit rate, la cellule B reste INSUFFISANTE."""
    rows = [_mk(i, level='A', decision='ACHETER', ret=(5.0 if i < 20 else -15.0))
            for i in range(25)]
    rows += [_mk(100 + i, level='B', decision='ATTENDRE', ret=3.0) for i in range(3)]
    ctx = DM.calibration_by_context(_mem(rows), 'vC')
    a = ctx['by_level']['A']
    assert a['status'] == 'MESURE'
    assert a['n_measured'] == 25
    assert a['hit_rate'] == pytest.approx(0.8)
    assert a['value'] == pytest.approx(0.5 + 0.4 * 0.8)
    b = ctx['by_level']['B']
    assert b['status'] == 'INSUFFISANT'
    assert b['n_measured'] == 3 and b['value'] is None      # jamais inventé
    bd = ctx['by_decision']['ACHETER']
    assert bd['status'] == 'MESURE' and bd['n_measured'] == 25


def test_context_never_mixes_versions():
    rows = [_mk(i, version='old') for i in range(30)]
    ctx = DM.calibration_by_context(_mem(rows), 'vC')
    assert all(c['status'] == 'INSUFFISANT'
               for c in list(ctx['by_level'].values()) + list(ctx['by_decision'].values())
               if c['n_measured'] == 0) or ctx['by_level'] == {}
    assert ctx['n_measured_total'] == 0


def test_context_empty_memory_honest():
    ctx = DM.calibration_by_context(DM.empty_memory(), 'vC')
    assert ctx['n_measured_total'] == 0
    assert ctx['by_level'] == {} and ctx['by_decision'] == {}
    assert ctx['note']


def test_context_deterministic():
    rows = [_mk(i) for i in range(25)]
    m = _mem(rows)
    assert DM.calibration_by_context(m, 'vC') == DM.calibration_by_context(m, 'vC')


# ─── Sélection du facteur : contextuel → global → 0,50 ──────────────────────────

def test_factor_for_prefers_context_cell():
    """La cellule du niveau courant prime quand elle est mesurée ; sinon le
    global ; sinon 0,50."""
    rows = [_mk(i, level='A', ret=(5.0 if i < 15 else -15.0)) for i in range(25)]
    mem = _mem(rows)
    f = DM.calibration_factor_for(mem, 'vC', level='A')
    assert f['scope'] == 'context:level=A'
    assert f['hit_rate'] == pytest.approx(15 / 25)
    f2 = DM.calibration_factor_for(mem, 'vC', level='B')   # cellule B insuffisante
    assert f2['scope'] == 'global'                          # secours global (25 mesures)
    assert f2['n_measured'] == 25
    f3 = DM.calibration_factor_for(DM.empty_memory(), 'vC', level='A')
    assert f3['scope'] == 'global' and f3['value'] == 0.5
    assert 'insuffisant' in f3['basis']


# ─── decide() consomme le contextuel (0.7.0) ────────────────────────────────────

def test_engine_version_bumped_for_context_consumption():
    parts = tuple(int(x) for x in SK.ENGINE_VERSION.split('.'))
    assert parts >= (0, 7, 0)


def test_decide_carries_scoped_calibration():
    d = SK.decide('CTX', {'score': 70, 'verdict': 'ATTENDRE',
                          'plan': {'entry': 100, 'stop': 94, 'tp2': 112, 'rr_res': 3.0}},
                  as_of='t',
                  calibration={'value': 0.82, 'scope': 'context:level=A',
                               'basis': 'hit rate 20/25 = 80 % (cellule A)'})
    cal = d['confidence']['factors']['calibration']
    assert cal['value'] == 0.82
    assert 'cellule A' in cal['basis']


# ─── API : la découpe est servie, la route passe le facteur du niveau ───────────

def test_memory_endpoint_serves_context_calibration(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    rows = [_mk(i, version=SK.ENGINE_VERSION) for i in range(25)]
    persist.save_json(DM.MEMORY_FILE, _mem(rows))
    d = terminal.app.test_client().get('/api/skyler/memory').get_json()
    ctx = d['calibration_by_context']
    assert ctx['engine_version'] == SK.ENGINE_VERSION
    assert ctx['by_level']['A']['status'] == 'MESURE'
    assert ctx['by_decision']['ACHETER']['n_measured'] == 25


def test_skyler_route_uses_scoped_factor(tmp_path, monkeypatch):
    """La route passe le facteur du NIVEAU de la décision courante quand la
    cellule est mesurée — visible dans la base du facteur servi."""
    import terminal
    from vertex.services import persist
    from vertex.app.state import scan_state
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    # 25 mesures REFUS_WATCH parfaites sous la version courante : la décision
    # démo (dossier faible → REFUS_WATCH) doit recevoir la cellule contextuelle.
    rows = [_mk(i, level='REFUS_WATCH', decision='REFUSER', ret=5.0,
                version=SK.ENGINE_VERSION) for i in range(25)]
    persist.save_json(DM.MEMORY_FILE, _mem(rows))
    scan_state.setdefault('detail', {})['CTXR'] = {
        'price': 100.0, 'score': 10, 'verdict': 'ATTENDRE'}
    try:
        d = terminal.app.test_client().get('/api/skyler/CTXR').get_json()
        cal = d['decision']['confidence']['factors']['calibration']
        assert 'REFUS_WATCH' in cal['basis']                # cellule contextuelle servie
        assert cal['value'] == pytest.approx(0.9)           # 100 % de hits, borné 0,90
    finally:
        scan_state['detail'].pop('CTXR', None)
