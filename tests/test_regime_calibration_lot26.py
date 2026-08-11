"""tests/test_regime_calibration_lot26.py — SKYLER LOT 26 : calibration par régime.

Le record mémoire fige le RÉGIME de marché au moment de la décision (label du
packet — None honnête si absent, anciens records compatibles). La calibration
par contexte gagne la découpe `by_regime` (mêmes règles d'échantillon par
cellule) et la sélection du facteur suit une priorité DOCUMENTÉE :
cellule niveau → cellule régime → global — portée (`scope`) explicite.
ENGINE_VERSION 0.7.0 → 0.8.0 (règle de consommation étendue). La carte Mémoire
affiche la calibration par contexte (SW v99 → v100).
"""
import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import skyler_core as SK


def _mk(i, level='A', regime='TREND_UP', ret=5.0, version='vR'):
    d = {'symbol': 'R%03d' % i, 'as_of': str(i), 'decision': 'ACHETER',
         'score': {'total': 30, 'level': level, 'insufficient_blocks': []},
         'level': level, 'contradictions': [], 'unknowns': [],
         'scenarios': {'available': True, 'bear': {'return_pct': -6.0},
                       'base': {'return_pct': 12.0}, 'bull': {'return_pct': 18.0}}}
    packet = {'schema_version': 1, 'engine_version': version,
              'contexts': {'market': {'regime': {'label': regime}}} if regime else {}}
    r = DM.freeze(decision=d, packet=packet, price=100.0, closes=None,
                  portfolio_ctx=None, now=i)
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


# ─── Le régime est figé dans le record ──────────────────────────────────────────

def test_freeze_stores_regime_label():
    r, _ = _mk(0, regime='RISK_OFF')
    assert r['regime'] == 'RISK_OFF'


def test_freeze_regime_none_honest_when_absent():
    r, _ = _mk(0, regime=None)
    assert r['regime'] is None                        # absent ≠ inventé
    # ancien record sans champ : compatible (dict.get)
    old = {k: v for k, v in r.items() if k != 'regime'}
    assert old.get('regime') is None


# ─── Découpe by_regime ──────────────────────────────────────────────────────────

def test_context_calibration_has_regime_cells():
    rows = [_mk(i, regime='TREND_UP', ret=(5.0 if i < 20 else -15.0))
            for i in range(25)]
    rows += [_mk(100 + i, regime='RISK_OFF', ret=3.0) for i in range(3)]
    ctx = DM.calibration_by_context(_mem(rows), 'vR')
    up = ctx['by_regime']['TREND_UP']
    assert up['status'] == 'MESURE' and up['n_measured'] == 25
    assert up['hit_rate'] == pytest.approx(0.8)
    off = ctx['by_regime']['RISK_OFF']
    assert off['status'] == 'INSUFFISANT' and off['value'] is None


def test_regime_none_not_a_cell():
    rows = [_mk(i, regime=None) for i in range(25)]
    ctx = DM.calibration_by_context(_mem(rows), 'vR')
    assert ctx['by_regime'] == {}                     # régime inconnu ≠ cellule


# ─── Priorité de sélection : niveau → régime → global ───────────────────────────

def test_factor_for_priority_level_then_regime_then_global():
    # 25 mesures : niveau A + régime TREND_UP → les deux cellules mesurées
    rows = [_mk(i, level='A', regime='TREND_UP', ret=5.0) for i in range(25)]
    mem = _mem(rows)
    f = DM.calibration_factor_for(mem, 'vR', level='A', regime='TREND_UP')
    assert f['scope'] == 'context:level=A'            # le niveau prime
    f2 = DM.calibration_factor_for(mem, 'vR', level='B', regime='TREND_UP')
    assert f2['scope'] == 'context:regime=TREND_UP'   # niveau insuffisant → régime
    assert f2['value'] == pytest.approx(0.9)
    f3 = DM.calibration_factor_for(mem, 'vR', level='B', regime='CHOP')
    assert f3['scope'] == 'global'                    # ni niveau ni régime → global
    f4 = DM.calibration_factor_for(DM.empty_memory(), 'vR', level='B', regime='CHOP')
    assert f4['scope'] == 'global' and f4['value'] == 0.5


def test_factor_for_versions_never_mixed():
    rows = [_mk(i, version='old', regime='TREND_UP') for i in range(25)]
    f = DM.calibration_factor_for(_mem(rows), 'vR', regime='TREND_UP')
    assert f['scope'] == 'global' and f['value'] == 0.5


# ─── Moteur 0.8.0 + route ───────────────────────────────────────────────────────

def test_engine_version_bumped_for_regime_consumption():
    parts = tuple(int(x) for x in SK.ENGINE_VERSION.split('.'))
    assert parts >= (0, 8, 0)


def test_memory_endpoint_serves_by_regime(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    rows = [_mk(i, version=SK.ENGINE_VERSION, regime='TREND_UP') for i in range(25)]
    persist.save_json(DM.MEMORY_FILE, _mem(rows))
    d = terminal.app.test_client().get('/api/skyler/memory').get_json()
    assert d['calibration_by_context']['by_regime']['TREND_UP']['status'] == 'MESURE'


# ─── Surfaçage : calibration par contexte dans la carte Mémoire, SW v100 ────────

def test_memory_card_shows_context_calibration():
    import terminal
    body = terminal.app.test_client().get('/journal', follow_redirects=True).get_data(as_text=True)
    assert 'calibration_by_context' in body
    assert 'Calibration par contexte' in body


def test_service_worker_bumped_to_at_least_v100():
    import re
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 100
    assert 'td-shell-v99' not in body
