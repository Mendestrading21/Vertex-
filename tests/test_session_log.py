"""tests/test_session_log.py — SKYLER LOT 15 : série datée par séance.

Le log de séances (`skyler_sessions.json`, runtime, gitignoré) accumule UNE
clôture par symbole et par jour de scan RÉEL (date d'observation, jamais
inventée). Les horizons de la mémoire décisionnelle (lot 10) comptent alors de
VRAIES séances : les clôtures aux dates strictement postérieures à la date de
la décision — le log est autoritaire quand il couvre le titre, l'empreinte de
fin de série reste le secours pour les anciens records.
"""
import pytest

from vertex.engines import session_log as SL
from vertex.engines import decision_memory as DM


# ─── Log : append par date réelle, dédupliqué, borné, refus des invalides ───────

def test_record_close_appends_and_dedupes_by_date():
    log = SL.empty_log()
    log = SL.record_close(log, 'NVDA', '2026-08-03', 100.0)
    log = SL.record_close(log, 'NVDA', '2026-08-04', 101.0)
    assert [e['date'] for e in log['symbols']['NVDA']] == ['2026-08-03', '2026-08-04']
    # même date = même séance : la dernière observation raffine la clôture
    log = SL.record_close(log, 'NVDA', '2026-08-04', 101.5)
    assert len(log['symbols']['NVDA']) == 2
    assert log['symbols']['NVDA'][-1]['close'] == 101.5


def test_record_close_sorted_even_out_of_order():
    log = SL.record_close(SL.empty_log(), 'AAA', '2026-08-04', 2.0)
    log = SL.record_close(log, 'AAA', '2026-08-03', 1.0)
    assert [e['date'] for e in log['symbols']['AAA']] == ['2026-08-03', '2026-08-04']


def test_record_close_refuses_invalid_inputs():
    log = SL.empty_log()
    assert SL.record_close(log, 'AAA', '2026-08-03', float('nan')) == log
    assert SL.record_close(log, 'AAA', 'pas-une-date', 1.0) == log
    assert SL.record_close(log, 'AAA', None, 1.0) == log
    assert SL.record_close(log, '', '2026-08-03', 1.0) == log


def test_record_close_bounded():
    log = SL.empty_log()
    for i in range(SL.MAX_SESSIONS + 10):
        log = SL.record_close(log, 'AAA', '2100-%02d-%02d' % (i // 28 + 1, i % 28 + 1), 1.0)
    assert len(log['symbols']['AAA']) == SL.MAX_SESSIONS


def test_record_close_pure():
    log = SL.empty_log()
    SL.record_close(log, 'AAA', '2026-08-03', 1.0)
    assert log['symbols'] == {}                     # l'entrée n'est pas mutée


# ─── Comptage de séances réelles ────────────────────────────────────────────────

def test_closes_after_date_strictly_after():
    log = SL.empty_log()
    for d, c in (('2026-08-01', 100.0), ('2026-08-02', 101.0),
                 ('2026-08-03', 102.0), ('2026-08-04', 103.0)):
        log = SL.record_close(log, 'NVDA', d, c)
    assert SL.closes_after_date(log, 'NVDA', '2026-08-02') == [102.0, 103.0]
    assert SL.closes_after_date(log, 'NVDA', '2026-08-04') == []


def test_closes_after_date_honest_none_when_unknown():
    log = SL.record_close(SL.empty_log(), 'NVDA', '2026-08-01', 100.0)
    assert SL.closes_after_date(log, 'ZZZ', '2026-08-01') is None    # titre non suivi
    assert SL.closes_after_date(log, 'NVDA', None) is None           # décision sans date
    assert SL.closes_after_date(None, 'NVDA', '2026-08-01') is None


# ─── La mémoire fige la date de séance et mesure en séances réelles ─────────────

def _decision(sym='SLX'):
    return {'symbol': sym, 'as_of': 't', 'decision': 'ATTENDRE',
            'score': {'total': 20, 'level': 'REFUS_WATCH', 'insufficient_blocks': []},
            'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': []}


def test_freeze_stores_real_session_date():
    r = DM.freeze(decision=_decision(), packet={'engine_version': 'x'}, price=100.0,
                  closes=None, portfolio_ctx=None, now=0, session_date='2026-08-05')
    assert r['session_date'] == '2026-08-05'
    r2 = DM.freeze(decision=_decision(), packet={'engine_version': 'x'}, price=100.0,
                   closes=None, portfolio_ctx=None, now=0)
    assert r2['session_date'] is None               # absent ≠ inventé


def test_measure_counts_real_sessions_from_log():
    r = DM.freeze(decision=_decision(), packet={'engine_version': 'x'}, price=100.0,
                  closes=None, portfolio_ctx=None, now=0, session_date='2026-08-01')
    log = SL.empty_log()
    for i, c in enumerate([101.0, 102.0, 103.0, 104.0, 105.0, 106.0]):
        log = SL.record_close(log, 'SLX', '2026-08-%02d' % (i + 2), c)
    after = SL.closes_after_date(log, 'SLX', r['session_date'])
    out = DM.measure(r, after)
    assert out['sessions_observed'] == 6
    assert out['horizons']['H5']['status'] == 'MESURE'
    assert out['horizons']['H5']['return_pct'] == pytest.approx(5.0)


# ─── Routes : alimentation fail-safe + priorité au log dans la mesure ───────────

def test_skyler_route_feeds_session_log(tmp_path, monkeypatch):
    import time
    import terminal
    from vertex.services import persist
    from vertex.app.state import scan_state
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    scan_state.setdefault('detail', {})['SLRX'] = {
        'price': 123.45, 'score': 70, 'verdict': 'ATTENDRE',
        'plan': {'entry': 100, 'stop': 94, 'tp2': 112, 'rr_res': 3.0}}
    try:
        assert terminal.app.test_client().get('/api/skyler/SLRX').status_code == 200
        log = persist.load_json(SL.SESSIONS_FILE, None)
        assert log and 'SLRX' in log['symbols']
        today = time.strftime('%Y-%m-%d', time.gmtime())
        assert log['symbols']['SLRX'][-1] == {'date': today, 'close': 123.45}
        # la décision figée porte la date de séance réelle
        mem = persist.load_json(DM.MEMORY_FILE, None)
        rec = [x for x in mem['decisions'] if x['symbol'] == 'SLRX'][0]
        assert rec['session_date'] == today
    finally:
        scan_state['detail'].pop('SLRX', None)


def test_memory_endpoint_prefers_session_log(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    # décision figée le 2026-08-01, log couvrant 3 séances postérieures
    r = DM.freeze(decision=_decision(sym='SLPX'), packet={'engine_version': 'x'},
                  price=100.0, closes=None, portfolio_ctx=None, now=0,
                  session_date='2026-08-01')
    persist.save_json(DM.MEMORY_FILE, DM.append_decision(DM.empty_memory(), r))
    log = SL.empty_log()
    for d, c in (('2026-08-02', 102.0), ('2026-08-03', 104.0), ('2026-08-04', 106.0)):
        log = SL.record_close(log, 'SLPX', d, c)
    persist.save_json(SL.SESSIONS_FILE, log)
    d = terminal.app.test_client().get('/api/skyler/memory').get_json()
    out = [o for o in d['outcomes'] if o['symbol'] == 'SLPX']
    assert out and out[0]['sessions_observed'] == 3
    assert out[0]['horizons']['H5']['status'] == 'EN_ATTENTE'   # 3/5 — jamais inventé
    assert out[0]['mfe_pct'] == pytest.approx(6.0)


def test_sessions_file_gitignored():
    import os
    gi = open(os.path.join(os.path.dirname(__file__), '..', '.gitignore'),
              encoding='utf-8').read()
    assert 'skyler_sessions.json' in gi
