"""tests/test_track_record_lot89.py — SKYLER LOT 89 : track_record figé.

`vertex/engines/track_record.py` (181 lignes — le moteur qui NOTE Vertex
lui-même sur ses verdicts passés) n'avait AUCUN test dédié. Tests de
CARACTÉRISATION nés verts (dits), sans jamais toucher aux fichiers
runtime (ledger simulé par monkeypatch, mémo réinitialisé).
"""
import time
from datetime import datetime

import pytest

from vertex.engines import track_record as tr


@pytest.fixture(autouse=True)
def _reset_memo():
    tr._MEMO['ts'] = 0.0
    tr._MEMO['data'] = None
    yield
    tr._MEMO['ts'] = 0.0
    tr._MEMO['data'] = None


def test_record_without_rows_returns_zero_touches_nothing():
    assert tr.record({}) == 0
    assert tr.record({'rows': []}) == 0


def test_fwd_edge_cases_never_invent():
    closes, dates = [100, 102, 104], ['08-01', '08-02', '08-03']
    assert tr._fwd(closes, dates, '07-15', 1) == (None, None)   # date inconnue
    r, i = tr._fwd(closes, dates, '08-03', 1)                   # bord de série
    assert r is None and i == 2
    r, _ = tr._fwd([0, 102, 104], dates, '08-01', 1)            # clôture 0 (falsy)
    assert r is None
    r, _ = tr._fwd(closes, dates, '08-01', 2)
    assert round(r, 1) == 4.0                                    # nominal exact


def test_hit_tp1_branches():
    closes = [100, 101, 106, 90]
    assert tr._hit_tp1(closes, 0, 100, 105, 95) is True          # TP1 d'abord
    assert tr._hit_tp1([100, 94, 106], 0, 100, 105, 95) is False # stop d'abord
    assert tr._hit_tp1([100, 101, 102], 0, 100, 105, 95) is None # non résolu (honnête)
    assert tr._hit_tp1(closes, 0, None, 105, 95) is None         # plan incomplet
    assert tr._hit_tp1(closes, None, 100, 105, 95) is None       # index absent


def test_evaluate_empty_ledger_is_honest(monkeypatch):
    monkeypatch.setattr(tr, '_load_ledger', lambda: [])
    out = tr.evaluate({'detail': {}})
    assert out['entries'] == 0 and out['resolved'] == 0
    assert out['by_verdict'] == {} and out['by_grade'] == {} and out['by_regime'] == {}
    assert 'CLÔTURES' in out['note'], 'la méthode approximative reste toujours dite'


def test_evaluate_min_sample_and_no_division_by_zero(monkeypatch):
    # 6 entrées BUY résolubles (≥ 5 → publié) ; 1 entrée WATCH (< 5 → tue).
    dates = ['08-01', '08-02', '08-03', '08-04', '08-05', '08-06', '08-07']
    closes = [100, 101, 102, 103, 104, 105, 106]
    day_ts = time.mktime(datetime.strptime(
        f'{datetime.now().year}-08-01', '%Y-%m-%d').timetuple())
    mk = lambda sym, dec: {'ts': day_ts, 'ticker': sym, 'decision': dec,
                           'entry': None, 'stop': None, 'targets': {},
                           'features': {'grade': 'A'}, 'market_regime': 'TREND'}
    entries = [mk(f'S{i}', 'BUY') for i in range(6)] + [mk('W1', 'WATCH')]
    detail = {e['ticker']: {'series': {'close': closes, 'dates': dates}}
              for e in entries}
    monkeypatch.setattr(tr, '_load_ledger', lambda: entries)
    out = tr.evaluate({'detail': detail})
    assert out['resolved'] == 7
    assert 'BUY' in out['by_verdict'] and 'WATCH' not in out['by_verdict'], (
        'jamais de statistique publiée sur un échantillon < 5')
    buy = out['by_verdict']['BUY']
    assert buy['n'] == 6 and buy['win_1j'] == 100
    assert buy['tp1_rate'] is None and buy['tp1_resolved'] == 0, (
        'plan absent → TP1 jamais inventé, dénominateur 0 → None honnête')


def test_evaluate_is_memoized(monkeypatch):
    calls = {'n': 0}

    def fake():
        calls['n'] += 1
        return []
    monkeypatch.setattr(tr, '_load_ledger', fake)
    tr.evaluate({'detail': {}})
    tr.evaluate({'detail': {}})
    assert calls['n'] == 1, 'mémoïsé 30 min — le ledger n\'est pas relu à chaque appel'
