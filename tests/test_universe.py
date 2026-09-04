"""
LOT 170 — Caractérisation de l'univers de Vertex
(`vertex/data/universe.py` — données pures : listes de tickers,
cartographies GICS/industrie, ensembles d'indices ; dernier module
de la file du périmètre). Les tests existants vérifient le câblage ;
ceux-ci figent les INVARIANTS DE COHÉRENCE des données — les changer
devient une décision explicite.
"""

from collections import Counter

from vertex.data import universe as un


# ── L'univers lui-même ───────────────────────────────────────────────────────

def test_univers_dedupliqueet_taille_plancher():
    assert len(un.UNIVERSE) == len(set(un.UNIVERSE))     # aucun doublon
    assert len(un.UNIVERSE) >= 400                        # les 3 indices US
    assert un.LIVE_SYMBOLS == un.UNIVERSE                 # même liste servie au live


def test_watchlist_57_sans_doublon():
    assert len(un.WATCHLIST) == 57
    assert len(set(un.WATCHLIST)) == 57


def test_source_des_constituants_est_un_etat_connu():
    assert un.INDEX_SOURCE in ('live', 'cache', 'cache-stale', 'static')
    assert un.INDEX_MEMBERS['union'] == un.UNIVERSE       # une seule vérité


def test_tickers_us_normalises_yfinance_sans_points():
    # L'univers US est normalisé (BRK.B → BRK-B) : aucun point — les
    # suffixes européens/asiatiques (.PA, .T…) vivent dans leurs listes.
    assert [s for s in un.UNIVERSE if '.' in s] == []
    assert [s for s in un.WATCHLIST if '.' in s] == []


# ── Cartographies : une seule vérité par ticker ──────────────────────────────

def test_gics_11_secteurs_comme_les_11_etf():
    assert len(un._GICS) == 11
    assert len(un._SECTOR_ETFS) == 11                     # XLK…XLC : miroir


def test_aucun_ticker_dans_deux_secteurs_gics():
    c = Counter(s for syms in un._GICS.values() for s in syms)
    assert [s for s, n in c.items() if n > 1] == []
    # L'aplati ticker→secteur couvre exactement les tickers déclarés.
    assert len(un._GICS_SECTOR) == sum(len(v) for v in un._GICS.values())
    assert set(un._GICS_SECTOR.values()) <= set(un._GICS.keys())


def test_aucun_ticker_dans_deux_industries():
    c = Counter(s for syms in un._INDUSTRY.values() for s in syms)
    assert [s for s, n in c.items() if n > 1] == []
    assert len(un._INDUSTRY_MAP) == sum(len(v) for v in un._INDUSTRY.values())


# ── Ensembles spéciaux ───────────────────────────────────────────────────────

def test_trend_set_derive_de_la_liste_buzz():
    assert un.TREND_SET == set(un._TREND_EXTRA)           # badge 🔥 de l'UI
    assert len(un.TREND_SET) >= 30


def test_europe_asie_suffixes_de_place_presents():
    # Les listes hors-US portent leurs suffixes de place (Euronext/Tokyo…)
    # — c'est le contrat yfinance pour ces marchés.
    assert all('.' in s for s in un._EUROPE)
    assert all('.' in s for s in un._ASIA)
