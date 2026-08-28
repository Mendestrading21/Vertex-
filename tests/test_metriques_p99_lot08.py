"""Lot 8 — la latence p99 rejoint p50/p95 dans la télémétrie locale.

Le contrat du skill demande p50/p95/p99. p99 est celle qui voit les pannes :
p95 lisse encore un appel sur vingt, et c'est précisément le vingtième — la
chaîne à 75 s derrière la file unique — qui fait l'expérience réelle.
"""
from __future__ import annotations

from vertex.services import request_metrics as M


def test_p99_est_calculee_et_bornee_par_max():
    M.reset_for_test()
    for i in range(100):
        M.record('ep', 200, float(i + 1))     # 1..100 ms
    e = M.summary()['endpoints']['ep']
    assert 'p99_ms' in e, 'le contrat exige p50/p95/p99 — p99 manque.'
    assert e['p95_ms'] <= e['p99_ms'] <= e['max_ms']
    assert e['p99_ms'] >= 99.0
    M.reset_for_test()


def test_p99_sur_un_echantillon_minuscule_reste_le_max():
    M.reset_for_test()
    M.record('ep2', 200, 5.0)
    e = M.summary()['endpoints']['ep2']
    assert e['p99_ms'] == e['max_ms'] == 5.0
    M.reset_for_test()
