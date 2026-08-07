"""
LOT 161 — Caractérisation des constituants d'indices
(`vertex/data/constituents.py`, 0 test direct — nourrit
`data/universe.py` : l'univers des titres au démarrage ; Wikipedia +
cache disque + snapshot statique embarqué → le démarrage n'est
JAMAIS bloqué).

Ces tests figent la normalisation, le filtrage, l'ORDRE DE
RÉSOLUTION cache → live → cache-périmé → statique, le garde-fou de
parsing et l'intégrité du snapshot statique — sans AUCUN accès
réseau (fetch monkeypatché).
"""

import json
import time

import pytest

from vertex.data import constituents as cn
from vertex.data._constituents_static import SP_SP500, SP_NDX100, SP_DOW30


# ── Normalisation et filtrage ────────────────────────────────────────────────

def test_norm_yfinance_maj_trim_points_en_tirets():
    assert cn._norm(' brk.b ') == 'BRK-B'
    assert cn._norm('AAPL') == 'AAPL'


def test_clean_filtre_les_tickers_implausibles_et_deduplique():
    # minuscules normalisées, doublon AAPL éliminé (ordre conservé),
    # nombres/trop longs/vides rejetés, tiret autorisé.
    assert cn._clean(['aapl', 'BRK.B', 'AAPL', '123', 'TOOLONGG', '', 'C', 'x-y']) \
        == ['AAPL', 'BRK-B', 'C', 'X-Y']


# ── Snapshot statique : intégrité du filet de sécurité ───────────────────────

def test_snapshot_statique_complet_et_deja_normalise():
    assert len(SP_SP500) >= 400 and len(SP_NDX100) >= 80 and len(SP_DOW30) >= 25
    # Chaque liste embarquée est DÉJÀ propre : _clean est idempotent dessus.
    assert cn._clean(SP_SP500) == SP_SP500
    assert cn._clean(SP_NDX100) == SP_NDX100
    assert cn._clean(SP_DOW30) == SP_DOW30


# ── Ordre de résolution (sans réseau — fetch monkeypatché) ───────────────────

@pytest.fixture()
def _iso(tmp_path, monkeypatch):
    """Cache isolé + réseau coupé par défaut."""
    cache = tmp_path / 'constituents_cache.json'
    monkeypatch.setattr(cn, '_CACHE_FILE', str(cache))

    def _boom():
        raise RuntimeError('réseau coupé (test)')
    monkeypatch.setattr(cn, '_fetch_all', _boom)
    return cache


def test_sans_cache_reseau_mort_snapshot_statique_jamais_bloque(_iso):
    r = cn.get_index_members()
    assert r['source'] == 'static'
    assert len(r['sp500']) >= 400
    assert len(r['union']) == len(dict.fromkeys(r['sp500'] + r['ndx100'] + r['dow30']))


def test_cache_frais_prioritaire_sur_le_reseau(_iso):
    json.dump({'sp500': ['AAA'], 'ndx100': ['BBB'], 'dow30': ['CCC'],
               '_ts': time.time()}, open(_iso, 'w'))
    r = cn.get_index_members()
    assert r['source'] == 'cache'
    assert r['union'] == ['AAA', 'BBB', 'CCC']


def test_force_ignore_le_cache_frais_et_retombe_cache_stale(_iso):
    json.dump({'sp500': ['AAA'], 'ndx100': ['BBB'], 'dow30': ['CCC'],
               '_ts': time.time()}, open(_iso, 'w'))
    r = cn.get_index_members(force=True)      # fetch tenté (mort) → cache périmé
    assert r['source'] == 'cache-stale'
    assert r['sp500'] == ['AAA']


def test_liste_vide_dans_le_cache_repli_statique_par_indice(_iso):
    # ndx100 vide dans le cache : repli STATIQUE pour CE SEUL indice —
    # les autres listes du cache restent servies.
    json.dump({'sp500': ['AAA'], 'ndx100': [], 'dow30': ['CCC'], '_ts': 0},
              open(_iso, 'w'))
    r = cn.get_index_members()
    assert r['source'] == 'cache-stale'
    assert r['sp500'] == ['AAA']
    assert len(r['ndx100']) >= 80             # statique injecté


def test_fetch_reussi_source_live_et_cache_sauvegarde(_iso, monkeypatch):
    monkeypatch.setattr(cn, '_fetch_all', lambda: {
        'sp500': ['S%d' % i for i in range(401)],
        'ndx100': ['N%d' % i for i in range(81)],
        'dow30': ['D%d' % i for i in range(26)]})
    r = cn.get_index_members(force=True)
    assert r['source'] == 'live' and len(r['sp500']) == 401
    assert json.load(open(_iso))['sp500'][:2] == ['S0', 'S1']   # persisté


def test_garde_fou_parsing_listes_trop_courtes_refusees(monkeypatch):
    # Des listes anormalement courtes = parsing Wikipedia cassé → refus
    # explicite (le fallback prend le relais en amont).
    monkeypatch.setattr(cn, '_fetch_one', lambda *a: ['X'])
    with pytest.raises(ValueError):
        cn._fetch_all()
