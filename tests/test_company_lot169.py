"""
LOT 169 — Caractérisation du profil d'entreprise
(`vertex/data/company.py` — le profil « lent » hebdomadaire : cache
disque + couche curée hors ligne + fetch yfinance sur la machine de
l'utilisateur). Testé HORS LIGNE : cache isolé, `_fetch_profile`
monkeypatché — aucun appel yfinance réel.

Ces tests figent la couche curée, l'ordre cache/fetch/curé, la
version de schéma et les médianes sectorielles — les changer devient
une décision explicite.
"""

import json
import time

import pytest

from vertex.data import company as co


@pytest.fixture()
def _iso(tmp_path, monkeypatch):
    cache = tmp_path / 'company_cache.json'
    monkeypatch.setattr(co, '_CACHE', str(cache))
    # réseau coupé par défaut
    monkeypatch.setattr(co, '_fetch_profile',
                        lambda sym: (_ for _ in ()).throw(RuntimeError('réseau coupé')))
    co._SECMED.update({'ts': 0.0, 'data': {}})     # memo des médianes réinitialisé
    yield cache
    co._SECMED.update({'ts': 0.0, 'data': {}})


# ── Données curées : intégrité du filet hors ligne ───────────────────────────

def test_segments_cures_somment_tous_a_100_pct():
    # INVARIANT : chaque répartition de CA curée somme exactement à 100 %.
    for sym, segs in co.REVENUE_SEGMENTS.items():
        assert sum(p for _, p in segs) == 100, sym


def test_demo_sert_la_couche_curee_et_signale_stale(_iso):
    p = co.get('nvda', demo=True)                  # jamais de réseau en démo
    assert p['symbol'] == 'NVDA'                   # symbole normalisé
    assert p['ceo'] == 'Jensen Huang'
    assert p['founded'] == 1993
    assert p['segments'][0] == ('Data Center', 78)
    assert p['country'] == '🇺🇸 États-Unis'         # libellé drapeau
    assert p['stale'] is True                      # curé = signalé rassis à l'UI


def test_symbole_inconnu_squelette_honnete_jamais_invente(_iso):
    u = co.get('ZZZQ', demo=True)
    assert u['name'] is None and u['ceo'] is None
    assert u['fundamentals']['pe'] is None         # l'UI affichera « — »
    assert u['stale'] is True


# ── Ordre cache / fetch / curé et version de schéma ──────────────────────────

def test_fetch_reussi_cache_ecrit_puis_servi_sans_reseau(_iso, monkeypatch):
    calls = []
    monkeypatch.setattr(co, '_fetch_profile', lambda sym: calls.append(sym) or
                        {'name': 'Test Corp', 'employees': 10, 'sector': 'Tech'})
    p1 = co.get('TSTX')
    assert p1['name'] == 'Test Corp' and p1['stale'] is False
    assert len(calls) == 1
    p2 = co.get('TSTX')                            # cache frais → AUCUN fetch
    assert p2['stale'] is False and len(calls) == 1


def test_schema_anterieur_force_le_refetch(_iso, monkeypatch):
    calls = []
    monkeypatch.setattr(co, '_fetch_profile', lambda sym: calls.append(sym) or
                        {'name': 'Test Corp', 'employees': 10})
    co.get('TSTX')
    cache = json.loads(open(_iso).read())
    cache['TSTX']['_v'] = co._SCHEMA_V - 1         # entrée d'un schéma antérieur
    json.dump(cache, open(_iso, 'w'))
    co.get('TSTX')
    assert len(calls) == 2                          # re-fetch automatique


def test_fetch_mort_secours_cure_jamais_de_page_vide(_iso):
    p = co.get('AAPL')                              # réseau coupé (fixture)
    assert p['ceo'] == 'Tim Cook'                   # couche curée
    assert p['stale'] is True


# ── peers : pairs de la même industrie ───────────────────────────────────────

def test_peers_meme_industrie_sans_soi_meme_cap_4():
    p = co.peers('NVDA')
    assert 'NVDA' not in p and len(p) <= 4
    assert 'AMD' in p                               # pair semi-conducteurs


# ── sector_medians : seuil 3, bornes PE, multiplicateurs ─────────────────────

def test_medianes_sectorielles_seuil_3_bornes_et_pourcentages(_iso):
    data = {f'S{i}': {'sector': 'Tech', 'pe': 20.0 + i, 'forward_pe': 18.0,
                      'margin': 0.2, 'rev_growth': 0.1, 'roe': 0.25}
            for i in range(3)}
    data['BAD'] = {'sector': 'Tech', 'pe': 500.0}   # > 250 → exclu des PE
    data['ONE'] = {'sector': 'Solo', 'pe': 10.0}    # < 3 membres → secteur absent
    json.dump(data, open(_iso, 'w'))
    sm = co.sector_medians()
    assert sm['Tech'] == {'median_pe': 21.0, 'median_fwd_pe': 18.0,
                          'median_margin': 20.0, 'median_growth': 10.0,
                          'median_roe': 25.0, 'n': 4}    # marge/roe en %
    assert 'Solo' not in sm


def test_medianes_memoisees_meme_vides(_iso):
    # Un résultat VIDE est aussi mémoïsé (memo sur le timestamp) — le
    # cache 1.4 Mo n'est pas reparsé à chaque appel.
    assert co.sector_medians() == {}
    json.dump({'X': {'sector': 'Tech', 'pe': 20.0}}, open(_iso, 'w'))
    assert co.sector_medians() == {}                # memo tient malgré le fichier
