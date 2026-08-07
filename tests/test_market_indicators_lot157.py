"""
LOT 157 — Caractérisation étendue des indicateurs techniques purs
(`vertex/market/indicators.py`, §12 — sans pandas, utilisés par
l'analyse, le portefeuille et les marchés).

Les 11 tests existants (`tests/test_market_indicators.py`) couvrent
les bases ; ceux-ci figent les LACUNES réelles : robustesse aux
entrées illisibles, fenêtres nulles, valeur golden du RSI de Wilder,
et surtout les ASYMÉTRIES de trous de données (sma se réinitialise,
ema traverse, atr recopie, vwap recopie) — les changer devient une
décision explicite.
"""

from vertex.market import indicators as ind


# ── Robustesse d'entrée ──────────────────────────────────────────────────────

def test_valeur_non_numerique_none_traversant_jamais_d_exception():
    # 'a' → None dans la série ; la fenêtre SMA se réinitialise dessus.
    assert ind.sma(['a', 1, 2, 3], 2) == [None, None, 1.5, 2.5]


def test_fenetre_nulle_ou_negative_tout_none():
    assert ind.sma([1, 2, 3], 0) == [None, None, None]
    assert ind.ema([1, 2, 3], 0) == [None, None, None]
    assert ind.sma([1, 2, 3], -1) == [None, None, None]


# ── ASYMÉTRIES de trous de données (comportements limites DOCUMENTÉS) ────────

def test_trou_de_donnees_sma_se_reinitialise_ema_traverse():
    # DOCUMENTÉ : sur un trou, la SMA repart de zéro (honnêteté de
    # fenêtre) mais l'EMA CONTINUE depuis sa valeur précédente (le
    # lissage exponentiel n'a pas de fenêtre à invalider). Deux
    # philosophies assumées — les unifier = décision explicite.
    assert ind.sma([1, 2, None, 4, 5, 6], 3)[3] is None      # réinitialisée
    e = ind.ema([10, None, 20], 2)
    assert e == [10.0, None, 16.6667]                        # traverse


def test_trou_de_donnees_atr_recopie_la_derniere_valeur():
    # DOCUMENTÉ : un true-range incalculable (High manquant) ne casse
    # pas la série — l'ATR précédent est RECOPIÉ tel quel (pas de None
    # au milieu, pas d'invention non plus : c'est la dernière mesure).
    h = [101 + i for i in range(20)]
    l = [99 + i for i in range(20)]
    c = [100 + i for i in range(20)]
    h[16] = None
    a = ind.atr(h, l, c, 14)
    assert a[15] == a[16] == a[17] == 2.0


def test_trou_de_volume_vwap_recopie_le_dernier_vwap():
    # DOCUMENTÉ : volume nul/illisible → le VWAP courant est resservi
    # (le cumul n'avance pas), puis reprend quand le volume revient.
    v = ind.vwap([10, 11, 12], [8, 9, 10], [9, 10, 11], [100, 0, 100])
    assert v == [9.0, 9.0, 10.0]


def test_longueurs_differentes_tronquees_au_minimum():
    # H/L/C de longueurs différentes → alignement sur la plus courte,
    # jamais d'IndexError.
    assert len(ind.atr([1] * 20, [0] * 20, [0.5] * 10, 5)) == 10


# ── RSI de Wilder : valeur golden et bornes ──────────────────────────────────

def test_rsi_golden_serie_classique_de_wilder():
    # La série d'exemple classique du RSI : premier point 70.5 —
    # l'implémentation suit bien le lissage de Wilder (pas une SMA).
    vals = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
            46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46.00, 46.03, 46.41,
            46.22, 45.64]
    r = ind.rsi(vals, 14)
    assert r[14] == 70.5
    assert r[-1] == 57.9


def test_rsi_toutes_pertes_zero():
    assert ind.rsi(list(range(40, 1, -1)), 14)[-1] == 0.0


# ── Bollinger : le multiplicateur agit, la médiane n'en dépend pas ───────────

def test_bollinger_multiplicateur_ecarte_les_bandes():
    v = [1, 2, 3, 4, 5, 6]
    b1 = ind.bollinger(v, window=3, mult=1.0)
    b2 = ind.bollinger(v, window=3, mult=2.0)
    assert b1['mid'][5] == b2['mid'][5] == 5.0
    assert b2['upper'][5] > b1['upper'][5] > b1['mid'][5]
    # écart symétrique : upper - mid == mid - lower
    assert round(b2['upper'][5] - b2['mid'][5], 4) == \
        round(b2['mid'][5] - b2['lower'][5], 4)
