"""
LOT 151 — Caractérisation du « cerveau physique »
(`vertex/market/regime_features.py` — AUCUN test direct avant ce lot).

Ce module modifie le SCORE VERTEX : analysis.py l'importe (`physics`)
et applique `score_adjust` (composante du struct_adj borné [-12, +10]
figé au lot 146). Ces tests figent les mesures (Hurst, entropie,
efficience, demi-vie), la synthèse d'état et la rétroaction exacte —
les changer devient une décision explicite.

Séries déterministes : graines fixes `np.random.default_rng(n)`
(générateur PCG64 au flux garanti stable par numpy) — mêmes séries à
chaque exécution.
"""

import numpy as np

from vertex.market import regime_features as rf


def _mean_reverting():
    # Ornstein-Uhlenbeck discret : rappel fort vers 100 (graine fixe).
    rng = np.random.default_rng(42)
    p = [100.0]
    for _ in range(399):
        p.append(p[-1] + 0.6 * (100 - p[-1]) + rng.normal(0, 1))
    return np.array(p)


def _persistent():
    # Incréments AUTOCORRÉLÉS (bruit lissé sur 12) → mémoire longue.
    rng = np.random.default_rng(7)
    inc = np.convolve(rng.normal(0, 1, 460), np.ones(12) / 12, mode='valid')
    return 100 + np.cumsum(inc)


# ── hurst : persistance, anti-persistance, gardes ────────────────────────────

def test_hurst_incrementss_persistants_superieur_a_0_5():
    assert rf.hurst(_persistent()) > 0.56


def test_hurst_retour_moyenne_tres_inferieur_a_0_5():
    assert rf.hurst(_mean_reverting()) < 0.2


def test_hurst_droite_pure_none_limite_documentee():
    # Comportement limite DOCUMENTÉ : sur une droite PURE, les
    # différences décalées sont constantes → écart-type nul → tous les
    # lags filtrés → None. Le Hurst exige de la variation autour de la
    # tendance ; une rampe parfaite n'a pas d'exposant mesurable.
    assert rf.hurst(np.linspace(100, 200, 400)) is None


def test_hurst_gardes_serie_courte_et_constante():
    assert rf.hurst(np.linspace(100, 200, 90)) is None   # < 2×max_lag
    assert rf.hurst(np.full(400, 100.0)) is None         # aucune variance


# ── entropy : désordre borné [0,1], gardes ───────────────────────────────────

def test_entropy_rendements_constants_zero_et_garde_30():
    assert rf.entropy(np.full(100, 0.01)) == 0.0     # aucun étalement
    assert rf.entropy(np.full(20, 0.01)) is None     # < 30 points


def test_entropy_concentre_bas_disperse_haut():
    conc = np.concatenate([np.zeros(90), [0.1] * 5, [-0.1] * 5])
    rng = np.random.default_rng(42)
    walk = 100 + np.cumsum(rng.normal(0, 1, 400))
    disp = np.diff(walk) / walk[:-1]
    e_conc, e_disp = rf.entropy(conc), rf.entropy(disp)
    assert e_conc < 0.3 < e_disp <= 1.0


# ── efficiency : signal/bruit de Kaufman ─────────────────────────────────────

def test_efficiency_monotone_1_oscillant_0_plat_none():
    assert rf.efficiency(np.linspace(100, 200, 400)) == 1.0
    osc = 100 + np.tile([0.0, 1.0], 200)     # aller-retour pur : net nul
    assert rf.efficiency(osc) == 0.0
    assert rf.efficiency(np.full(100, 5.0)) is None    # chemin nul
    assert rf.efficiency(np.linspace(0, 1, 15)) is None  # < n+1 barres


# ── half_life : demi-vie OU, None sans rappel ────────────────────────────────

def test_half_life_retour_moyenne_courte_et_tendance_none():
    hl = rf.half_life(_mean_reverting())
    assert hl is not None and 0 < hl < 10     # rappel fort → demi-vie courte
    # Série tendancielle : beta ≥ 0 → PAS de demi-vie (None honnête).
    assert rf.half_life(np.linspace(100, 200, 400)) is None
    assert rf.half_life(_mean_reverting()[:30]) is None  # < 40 points


# ── analyze : synthèse d'état et contrat ─────────────────────────────────────

def test_analyze_persistant_tendance_fractale():
    a = rf.analyze(_persistent())
    assert a['state'] == 'TENDANCE FRACTALE'
    assert a['hurst'] > 0.56 and a['efficiency'] >= 0.38
    assert 'Hurst' in a['note']


def test_analyze_retour_moyenne_avec_demi_vie():
    a = rf.analyze(_mean_reverting())
    assert a['state'] == 'RETOUR MOYENNE'
    assert a['half_life'] is not None
    assert 'demi-vie' in a['note']


def test_analyze_droite_pure_neutre_limite_documentee():
    # Conséquence de hurst=None sur une rampe parfaite : l'état reste
    # NEUTRE malgré une efficience de 1.0 (la synthèse exige H ET E).
    a = rf.analyze(np.linspace(100, 200, 400))
    assert a['state'] == 'NEUTRE'
    assert a['hurst'] is None and a['efficiency'] == 1.0


def test_analyze_gardes_et_contrat():
    assert rf.analyze(np.linspace(100, 200, 70)) is None   # < 80 points
    a = rf.analyze(_persistent())
    assert set(a) == {'hurst', 'entropy', 'efficiency', 'half_life',
                      'state', 'state_col', 'note'}


# ── score_adjust : la rétroaction EXACTE sur le score Vertex ─────────────────

def test_score_adjust_valeurs_exactes_par_etat():
    assert rf.score_adjust({'state': 'TENDANCE FRACTALE', 'efficiency': 0.3})[0] == 4
    assert rf.score_adjust({'state': 'TENDANCE FRACTALE', 'efficiency': 0.5})[0] == 7
    assert rf.score_adjust({'state': 'CHAOS'})[0] == -7
    assert rf.score_adjust({'state': 'RETOUR MOYENNE'})[0] == -3
    assert rf.score_adjust({'state': 'RETOUR MOYENNE'}, ext_atr=3)[0] == -6


def test_score_adjust_entropie_extreme_et_extremes_atteignables():
    # Entropie ≥ 0.92 retire 2 de plus. Extrêmes RÉELS : +7 (TF propre)
    # et -9 (CHAOS + entropie) — les bornes [-10, +8] gardent une marge.
    adj, why = rf.score_adjust({'state': 'CHAOS', 'entropy': 0.95})
    assert adj == -9 and 'entropie' in why
    assert rf.score_adjust({'state': 'RETOUR MOYENNE', 'entropy': 0.93},
                           ext_atr=4)[0] == -8


def test_score_adjust_sans_physique_zero():
    assert rf.score_adjust(None) == (0, '')
    assert rf.score_adjust({}) == (0, '')
