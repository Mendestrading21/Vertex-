"""Lot 46 — la fraîcheur affichée vient du SERVEUR, jamais de l'horloge du
navigateur.

Besoin consigné depuis la campagne visuelle (RECAPITULATIF, « Besoin hors
périmètre ») : `/cal-feed` ne portait aucun champ `ts` — les pages ne
pouvaient afficher qu'une heure de navigateur ou un libellé figé. Et
`options-symbol.js` passait `timestamp: Date.now()` sur 7 cartes (« source :
scan » avec l'heure du CLIC) — une fraîcheur toujours verte, donc fausse.

Contrat : chaque flux porte son époque serveur (`ts`), et les cartes le
transmettent tel quel — absent → « Âge inconnu » (honnête), jamais maintenant.
"""
import time

import terminal
from vertex.app.state import cal_state, scan_state


def test_cal_feed_porte_une_epoque_serveur():
    sauv = dict(cal_state)
    try:
        cal_state['items'] = [{'sym': 'NVDA', 'date': '2026-09-04', 'dte': 7}]
        cal_state['updated'] = '15:00 28/08'
        cal_state['ts'] = time.time()
        d = terminal.app.test_client().get('/cal-feed').get_json()
        assert isinstance(d.get('ts'), (int, float)) and d['ts'] > 1.7e9, (
            '/cal-feed doit porter une époque serveur `ts` — sans elle, la '
            'page ne peut afficher que l\'heure du navigateur')
    finally:
        cal_state.clear(); cal_state.update(sauv)


def test_les_deux_ecrivains_du_calendrier_posent_ts():
    src = open('terminal.py', encoding='utf-8').read()
    n_updated = src.count("cal_state['updated'] =")
    n_ts = src.count("cal_state['ts'] =")
    assert n_updated >= 2 and n_ts >= n_updated, (
        "chaque écrivain de cal_state['updated'] doit poser aussi "
        "cal_state['ts'] (époque) — %d updated pour %d ts" % (n_updated, n_ts))


def test_vol_charts_et_scenarios_portent_ts():
    sauv = {k: scan_state.get(k) for k in ('options_as_of', 'scan_ts')}
    try:
        scan_state['options_as_of'] = 1787000000.0
        c = terminal.app.test_client()
        d = c.get('/api/options/vol-charts/NVDA').get_json() or {}
        assert isinstance(d.get('ts'), (int, float)), (
            'vol-charts doit porter l\'époque de SES données (options_as_of '
            'ou scan_ts) — les 4 cartes de volatilité l\'affichent')
        #  scenarios : le chemin succès exige un contrat simulable complet —
        #  trop lourd à semer ici ; on épingle la SOURCE (le payload succès
        #  porte ts, à côté du as_of humain).
        src = open('vertex/app/routes/options_intel_api.py', encoding='utf-8').read()
        assert "'as_of': _as_of(), 'ts': _ts_epoch()" in src, (
            'le payload succès de /api/options/scenarios doit porter ts')
    finally:
        for k, v in sauv.items():
            if v is None: scan_state.pop(k, None)
            else: scan_state[k] = v


def test_aucune_carte_ne_ment_avec_l_horloge_du_navigateur():
    js = open('vertex/static/vertex/js/pages/options-symbol.js', encoding='utf-8').read()
    assert 'timestamp: Date.now()' not in js, (
        'une carte affiche l\'heure du CLIC comme âge de la donnée — '
        'transmettre le ts du flux (absent → « Âge inconnu », honnête)')
