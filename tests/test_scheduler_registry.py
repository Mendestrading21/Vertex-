"""tests/test_scheduler_registry.py — SKYLER LOT 109 : registre des jobs figé.

Trou réel de couverture : vertex/scheduler/registry.py (§24 — le registre
des boucles de fond que la vue Système/Automatisations affiche) n'avait
AUCUN test direct : son seul usage en test est un len() dans startup.
Caractérisations nées vertes (dites) — moteur INTACT ; l'état module
_JOBS est sauvegardé/restauré autour de chaque test (jamais pollué).
"""
import copy
import time

import pytest

# Le package rebinde le nom « registry » vers l'OBJET façade, donc même
# « import … as » (qui passe par getattr) rendrait l'objet — on attrape le
# MODULE réel (état _JOBS + fonctions) via sys.modules.
import sys
import vertex.scheduler.registry  # noqa: F401 — force le chargement du sous-module

reg = sys.modules['vertex.scheduler.registry']


@pytest.fixture(autouse=True)
def _restore_jobs():
    saved = copy.deepcopy(reg._JOBS)
    yield
    reg._JOBS.clear()
    reg._JOBS.update(saved)


def test_snapshot_order_is_the_product_priority_and_honest_when_never_run():
    snap = reg.jobs()
    assert [j['name'] for j in snap] == [n for n, _, _ in reg._CANONICAL]
    assert snap[0]['name'] == 'STARTUP_HEALTH_CHECK'
    assert [j['name'] for j in snap].index('POSITION_REFRESH') < \
           [j['name'] for j in snap].index('MARKET_DATA_REFRESH'), (
        'priorité produit : positions ouvertes avant univers')
    never = next(j for j in snap if j['runs'] == 0)
    assert never['last_run'] is None and never['age_s'] is None
    assert never['next_run_eta_s'] is None, 'jamais exécuté → aucune ETA inventée'


def test_adhoc_beat_is_recorded_but_not_exposed_in_snapshot():
    reg.beat('JOB_INVENTE_LOT109')
    assert 'JOB_INVENTE_LOT109' in reg._JOBS
    assert all(j['name'] != 'JOB_INVENTE_LOT109' for j in reg.jobs()), (
        'le snapshot n\'expose QUE les jobs canoniques — pas de surprise en UI')


def test_beat_ok_increments_and_rounds_duration():
    reg.beat('ALERTS_EVALUATION', ok=True, duration_ms=12.7)
    j = reg._JOBS['ALERTS_EVALUATION']
    assert j['runs'] == 1 and j['last_ok'] is True and j['last_error'] is None
    assert j['last_duration_ms'] == 13


def test_beat_error_truncates_to_200_chars():
    reg.beat('SYSTEM_AUDIT', ok=False, error='x' * 500)
    j = reg._JOBS['SYSTEM_AUDIT']
    assert j['last_ok'] is False and len(j['last_error']) == 200


def test_eta_only_for_interval_jobs_and_bounded():
    reg.beat('ALERTS_EVALUATION')            # interval 60 s
    reg.beat('SYSTEM_AUDIT')                 # job événement, interval None
    snap = {j['name']: j for j in reg.jobs()}
    assert 0 <= snap['ALERTS_EVALUATION']['next_run_eta_s'] <= 60
    assert snap['SYSTEM_AUDIT']['next_run_eta_s'] is None, (
        'un job à la demande n\'a jamais de prochaine échéance estimée')


def test_eta_never_negative_when_overdue():
    reg.beat('ALERTS_EVALUATION')
    reg._JOBS['ALERTS_EVALUATION']['last_run'] = time.time() - 1000
    snap = {j['name']: j for j in reg.jobs()}
    assert snap['ALERTS_EVALUATION']['next_run_eta_s'] == 0, (
        'boucle en retard → ETA 0, jamais un délai négatif')
    assert snap['ALERTS_EVALUATION']['age_s'] >= 999


def test_registry_facade_delegates_to_module_functions():
    assert reg.registry.beat is reg.beat
    assert reg.registry.jobs is reg.jobs


def test_snapshot_is_a_copy_not_the_live_state():
    snap = reg.jobs()
    snap[0]['runs'] = 999
    assert reg._JOBS[snap[0]['name']]['runs'] != 999, (
        'muter le snapshot ne falsifie jamais le registre')
