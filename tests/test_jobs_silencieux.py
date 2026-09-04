"""Lot 7 — un battement absent se voit ; un échec en série se compte.

Le registre des jobs a un battement (`beat`) mais ne détecte pas son
ABSENCE : une boucle qui a battu une fois puis est morte restait `ACTIF`
pour toujours. Un état affiché vert sur un job mort est le mensonge
d'automatisation le plus coûteux — l'utilisateur croit ses alertes évaluées.

Ce banc tient deux ajouts :

1. `SILENCIEUX` — implémenté, cadencé (`interval_s`), déjà battu, et plus
   aucun battement depuis > 2× sa cadence. Distinct d'ERREUR (le dernier
   passage a ÉCHOUÉ) et d'ACTIF (il bat).
2. `echecs_consecutifs` — compté par `beat(ok=False)`, remis à zéro par un
   succès : le signal de tempête de retries, sans toucher aux boucles.
"""
from __future__ import annotations

import time

import importlib

#  `vertex/scheduler/__init__.py` re-exporte l'OBJET `registry`, qui masque le
#  sous-module du même nom sur `import a.b as x`. On passe par importlib pour
#  atteindre le MODULE (et ses _JOBS internes que ce banc pilote).
R = importlib.import_module('vertex.scheduler.registry')


def _reset(name):
    j = R._JOBS[name]
    j.update(last_run=None, last_ok=None, last_error=None, runs=0,
             last_duration_ms=None, echecs_consecutifs=0)


def test_un_job_mort_devient_silencieux_pas_actif():
    nom = 'ALERTS_EVALUATION'          # cadence 60 s
    _reset(nom)
    R.beat(nom, ok=True)
    R._JOBS[nom]['last_run'] = time.time() - 500   # 8× la cadence sans battre
    j = next(x for x in R.jobs() if x['name'] == nom)
    assert j['etat'] == 'SILENCIEUX', (
        'un job cadencé à 60 s muet depuis 500 s se lit « %s » : une boucle '
        'morte passe pour vivante.' % j['etat'])
    _reset(nom)


def test_un_job_qui_bat_reste_actif():
    nom = 'ALERTS_EVALUATION'
    _reset(nom)
    R.beat(nom, ok=True)
    j = next(x for x in R.jobs() if x['name'] == nom)
    assert j['etat'] == 'ACTIF'
    _reset(nom)


def test_un_echec_recent_reste_erreur_meme_vieux():
    """ERREUR prime : le dernier passage a échoué — le silence qui suit ne
    transforme pas un échec en simple mutisme."""
    nom = 'ALERTS_EVALUATION'
    _reset(nom)
    R.beat(nom, ok=False, error='boom')
    R._JOBS[nom]['last_run'] = time.time() - 500
    j = next(x for x in R.jobs() if x['name'] == nom)
    assert j['etat'] == 'ERREUR'
    _reset(nom)


def test_un_job_sans_cadence_ne_devient_jamais_silencieux():
    nom = 'STARTUP_HEALTH_CHECK'       # évènement, interval_s None
    _reset(nom)
    R.beat(nom, ok=True)
    R._JOBS[nom]['last_run'] = time.time() - 10 ** 6
    j = next(x for x in R.jobs() if x['name'] == nom)
    assert j['etat'] == 'ACTIF', (
        'un job évènementiel n\'a pas de cadence : le silence n\'y est pas '
        'une panne.')
    _reset(nom)


def test_les_echecs_consecutifs_se_comptent_et_se_reinitialisent():
    nom = 'NEWS_REFRESH'
    _reset(nom)
    for _ in range(3):
        R.beat(nom, ok=False, error='timeout')
    j = next(x for x in R.jobs() if x['name'] == nom)
    assert j['echecs_consecutifs'] == 3, (
        'trois échecs de suite doivent se lire — c\'est le signal de tempête '
        'de retries.')
    R.beat(nom, ok=True)
    j = next(x for x in R.jobs() if x['name'] == nom)
    assert j['echecs_consecutifs'] == 0, 'un succès remet le compteur à zéro.'
    _reset(nom)
