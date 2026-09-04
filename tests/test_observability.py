"""
LOT 179 — Caractérisation de l'OBSERVABILITÉ du Strategy OS (§37)
(`vertex/observability/metrics.py` — ZÉRO test direct — et les
sections de `diagnostics.py` ; servis par /api/diagnostics et
/api/data-quality via strategy_os_api). Le webhook TradingView
(candidat prévu) s'est révélé complet (12 tests) — constat honnête,
repli sur la vraie lacune. Tests sur une instance FRAÎCHE de Metrics
(jamais le singleton METRICS — pas de pollution de suite).
"""
import pytest

from vertex.observability.diagnostics import data_quality_report, system_diagnostics
from vertex.observability.metrics import Metrics


# ── Metrics : compteurs, jauges, percentiles ─────────────────────────────────

def test_compteurs_cumulent_et_jauges_ecrasent():
    m = Metrics()
    m.inc('scans')                                  # défaut +1
    m.inc('scans')
    m.inc('scans', 2.5)
    m.gauge('rows', 100)
    m.gauge('rows', 42)                             # la jauge ÉCRASE
    s = m.snapshot()
    assert s['counters'] == {'scans': 4.5}
    assert s['gauges'] == {'rows': 42}


def test_percentiles_exacts_sur_100_echantillons():
    m = Metrics()
    for ms in range(1, 101):
        m.timing('ibkr', float(ms))
    t = m.snapshot()['timings']['ibkr']
    assert t == {'n': 100, 'p50_ms': 51.0, 'p95_ms': 95.0, 'max_ms': 100.0}


def test_echantillon_unique_p50_p95_max_confondus():
    m = Metrics()
    m.timing('x', 7.0)
    assert m.snapshot()['timings']['x'] == {'n': 1, 'p50_ms': 7.0,
                                            'p95_ms': 7.0, 'max_ms': 7.0}


def test_anneau_de_200_echantillons_oublie_les_plus_vieux():
    m = Metrics()
    for ms in range(1, 251):                        # 250 mesures
        m.timing('x', float(ms))
    t = m.snapshot()['timings']['x']
    assert t['n'] == 200                            # bornage mémoire
    assert t['max_ms'] == 250.0
    assert t['p50_ms'] == 151.0                     # fenêtre = 51..250


def test_timer_contextuel_mesure_et_propage_l_exception():
    m = Metrics()
    with m.timer('op'):
        pass
    assert m.snapshot()['timings']['op']['n'] == 1
    with pytest.raises(ValueError):                 # __exit__ False → jamais avalée
        with m.timer('op'):
            raise ValueError('boom')
    assert m.snapshot()['timings']['op']['n'] == 2  # la durée est mesurée quand même


def test_snapshot_est_une_copie_isolee():
    m = Metrics()
    m.inc('a')
    s = m.snapshot()
    s['counters']['a'] = 999                        # muter le snapshot…
    assert m.snapshot()['counters']['a'] == 1       # …ne touche pas le registre


# ── system_diagnostics : sections strictement optionnelles ───────────────────

def test_sections_optionnelles_absentes_sans_dependance():
    d = system_diagnostics()
    assert set(d.keys()) == {'metrics'}             # rien d'inventé sans source


def test_sections_presentes_selon_le_contrat_des_dependances():
    class _S:                                        # contrats minimaux
        def status(self):
            return {'ok': True}

    class _A:
        def stats(self):
            return {'calls': 3}

    d = system_diagnostics(scan_state={'rows': [1, 2], 'source': 'demo'},
                           scheduler=_S(), alert_engine=_S(),
                           ai_audit=_A(), signal_store=_S())
    assert d['scan']['rows'] == 2 and d['scan']['source'] == 'demo'
    assert d['ibkr_scheduler'] == {'ok': True}
    assert d['alerts'] == {'ok': True}
    assert d['ai'] == {'calls': 3}
    assert d['tradingview'] == {'ok': True}


# ── data_quality_report : bornes des dégradés ────────────────────────────────

def test_degrades_bornes_20_et_warnings_bornes_3():
    packets = [{'symbol': 'S%d' % i,
                'quality': {'overall': 'STALE',
                            'warnings': ['w1', 'w2', 'w3', 'w4', 'w5']}}
               for i in range(30)]
    rep = data_quality_report(packets)
    assert rep['total'] == 30
    assert rep['by_quality'] == {'STALE': 30}       # tous comptés…
    assert len(rep['degraded']) == 20               # …mais la liste bornée à 20
    assert rep['degraded'][0]['warnings'] == ['w1', 'w2', 'w3']   # cap 3
