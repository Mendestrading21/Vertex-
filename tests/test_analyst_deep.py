"""
LOT 180 — Caractérisation des données analystes PROFONDES
(`vertex/data_sources/analyst_deep.py`, 226 lignes, ZÉRO test — servi
par la fiche titre de terminal.py). Testé HORS LIGNE : faux ticker
pandas, faux module yfinance injecté, cache isolé. Figé : la lecture
robuste des DataFrames yfinance, les agrégats (révisions, surprises,
initiés), et la politique de cache « périmé plutôt que rien /
jamais cacher un échec total ».
"""
import json
import math
import sys
import time
import types

import pandas as pd
import pytest

from vertex.data_sources import analyst_deep as ad


@pytest.fixture()
def _cache(tmp_path, monkeypatch):
    path = tmp_path / 'analyst_cache.json'
    monkeypatch.setattr(ad, 'CACHE_PATH', str(path))
    return path


# ── Lecture robuste des blocs (faux ticker) ──────────────────────────────────

def test_nan_ecarte_jamais_un_chiffre_fantome():
    assert ad._num(float('nan')) is None
    assert ad._num('12.5') == 12.5
    assert ad._num('abc') is None


def test_revisions_bpa_net_et_tendance():
    t = types.SimpleNamespace(eps_revisions=pd.DataFrame(
        {'upLast30days': [5.0], 'downLast30days': [2.0],
         'upLast7days': [1.0], 'downLast7Days': [0.0]}, index=['0y']))
    r = ad._eps_revisions(t)
    assert r == {'up30': 5, 'down30': 2, 'up7': 1, 'down7': 0,
                 'net30': 3, 'trend': 'up'}


def test_revisions_repli_trimestre_si_annee_absente():
    t = types.SimpleNamespace(eps_revisions=pd.DataFrame(
        {'upLast30days': [0.0], 'downLast30days': [4.0]}, index=['0q']))
    r = ad._eps_revisions(t)
    assert r['net30'] == -4 and r['trend'] == 'down'


def test_surprises_separe_le_trimestre_a_venir_et_compte_les_beats():
    df = pd.DataFrame(
        {'EPS Estimate': [2.0, 1.9, 1.8, 1.7],
         'Reported EPS': [math.nan, 2.1, 1.7, 1.9],
         'Surprise(%)': [math.nan, 10.5, -5.6, 11.8]},
        index=['2026-09-01', '2026-06-01', '2026-03-01', '2025-12-01'])
    t = types.SimpleNamespace(get_earnings_dates=lambda limit: df)
    s = ad._surprises(t, n=8)
    assert s['next'] == '2026-09-01'                # publié None → à venir
    assert [h['date'] for h in s['history']] == ['2026-06-01', '2026-03-01',
                                                 '2025-12-01']
    assert s['summary'] == {'beats': 2, 'total': 3, 'avg': 5.6}   # (10.5-5.6+11.8)/3


def test_notes_triees_recentes_d_abord_cap_et_bornes():
    df = pd.DataFrame(
        {'Firm': ['F%d' % i if i else 'X' * 60 for i in range(8)],
         'ToGrade': ['Buy'] * 8, 'FromGrade': ['Hold'] * 8,
         'Action': ['up'] * 8},
        index=['2026-01-0%d' % (i + 1) for i in range(8)])
    t = types.SimpleNamespace(upgrades_downgrades=df)
    r = ad._ratings_actions(t, n=6)
    assert len(r) == 6                              # cap dur
    assert r[0]['date'] == '2026-01-08'             # les plus récentes d'abord
    assert len(ad._ratings_actions(
        types.SimpleNamespace(upgrades_downgrades=df.head(1)))[0]['firm']) <= 40


def test_initiés_solde_et_biais_ou_none_sans_mouvement():
    df = pd.DataFrame({'Transaction': ['Buy', 'Sale', 'Buy'],
                       'Text': ['', '', ''],
                       'Shares': [1000.0, 300.0, 500.0]})
    r = ad._insider(types.SimpleNamespace(insider_transactions=df))
    assert r == {'buys': 2, 'sells': 1, 'net_shares': 1200, 'bias': 'buy'}
    vide = pd.DataFrame({'Transaction': ['Gift'], 'Text': [''], 'Shares': [10.0]})
    assert ad._insider(types.SimpleNamespace(insider_transactions=vide)) is None


# ── get() : politique de cache ───────────────────────────────────────────────

def test_symbole_vide_none(_cache):
    assert ad.get('') is None and ad.get(None) is None


def test_cache_frais_servi_sans_aucun_appel_reseau(_cache, monkeypatch):
    _cache.write_text(json.dumps({'TSTQ': {'_ts': time.time(), 'insider': {'buys': 1}}}))
    boom = types.ModuleType('yfinance')
    boom.Ticker = lambda sym: (_ for _ in ()).throw(AssertionError('appel réseau interdit'))
    monkeypatch.setitem(sys.modules, 'yfinance', boom)
    p = ad.get('tstq')                              # symbole normalisé + cache frais
    assert p['insider'] == {'buys': 1}


def test_yfinance_mort_cache_perime_servi_plutot_que_rien(_cache, monkeypatch):
    _cache.write_text(json.dumps({'TSTQ': {'_ts': 1.0, 'insider': {'buys': 1}}}))
    monkeypatch.setitem(sys.modules, 'yfinance', None)   # import impossible
    p = ad.get('TSTQ')                              # TTL 12 h largement dépassé
    assert p['insider'] == {'buys': 1}              # périmé > rien


def test_echec_total_jamais_cache(_cache, monkeypatch):
    # Tous les blocs à None (ticker sans données) → le paquet n'est PAS
    # persisté (on ne cache jamais un échec total) et get renvoie None.
    fake = types.ModuleType('yfinance')
    fake.Ticker = lambda sym: types.SimpleNamespace()    # aucun attribut → blocs None
    monkeypatch.setitem(sys.modules, 'yfinance', fake)
    assert ad.get('TSTQ') is None
    assert not _cache.exists()                       # rien écrit sur disque
