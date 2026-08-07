"""
LOT 164 — Caractérisation du risque de panier
(`vertex/portfolio/legacy_basket_risk.py` — VIVANT : servi par
analysis_api, command et risk_engine ; 0 test direct). Le « no-trade
de concentration » : corrélations, HHI, exposition sectorielle,
sizing inverse-vol capé.

Ces tests figent les gardes, les drapeaux et TROIS limites
documentées (cap infaisable, concentration non détectée sur petit
panier, fail-open sur erreur) — les changer devient une décision
explicite. Séries déterministes (graines fixes).
"""

import numpy as np

from vertex.portfolio import legacy_basket_risk as lbr


def _detail(series_map):
    return {s: {'series': {'close': list(v)}} for s, v in series_map.items()}


def _walk(seed, n=120):
    return np.cumsum(np.random.default_rng(seed).normal(0, 1, n)) + 200


# ── Gardes : panier trop petit, séries courtes exclues ───────────────────────

def test_panier_trop_petit_honnete_sans_blocage():
    r = lbr.build([], {})
    assert r == {'n': 0, 'symbols': [], 'flags': [], 'no_new_risk': False,
                 'note': 'panier trop petit pour une analyse de corrélation'}


def test_serie_trop_courte_exclue_moins_de_40_points():
    base = _walk(9)
    r = lbr.build(['NVDA', 'AMD'], _detail({'NVDA': base, 'AMD': base[:30]}))
    assert 'panier trop petit' in r['note']    # AMD exclu → 1 seul titre


# ── Drapeau de corrélation : le no-trade du panier cloné ─────────────────────

def test_paire_quasi_identique_correlation_elevee_bloque():
    rng = np.random.default_rng(9)
    base = _walk(9)
    d = _detail({'NVDA': base, 'AMD': base + rng.normal(0, 0.3, 120)})
    r = lbr.build(['NVDA', 'AMD'], d)
    assert r['avg_corr'] > 0.65
    assert r['flags'] == ['correlation_panier_elevee']
    assert r['no_new_risk'] is True
    assert r['top_pair'][:2] == ['NVDA', 'AMD']   # la paire coupable expliquée


def test_panier_diversifie_decorrele_aucun_drapeau():
    d = _detail({'NVDA': _walk(1), 'MSFT': _walk(2), 'JPM': _walk(3),
                 'XOM': _walk(4), 'LLY': _walk(5)})
    r = lbr.build(['NVDA', 'MSFT', 'JPM', 'XOM', 'LLY'], d)
    assert abs(r['avg_corr']) < 0.3
    assert r['flags'] == [] and r['no_new_risk'] is False
    assert r['diversification'] >= 80             # 1 - HHI élevé


# ── LIMITES DOCUMENTÉES ──────────────────────────────────────────────────────

def test_cap_infaisable_somme_des_poids_inferieure_a_100():
    # LIMITE DOCUMENTÉE : avec n titres et cap 15 %, si n × 15 % < 100 %
    # les poids restent au cap et la somme vaut n × cap (75 % pour 5
    # titres) — le sizing n'est PAS renormalisé au-delà du cap.
    d = _detail({'NVDA': _walk(1), 'MSFT': _walk(2), 'JPM': _walk(3),
                 'XOM': _walk(4), 'LLY': _walk(5)})
    r = lbr.build(['NVDA', 'MSFT', 'JPM', 'XOM', 'LLY'], d)
    assert r['max_weight'] == 15.0
    assert round(sum(r['weights'].values()), 1) == 75.0


def test_concentration_sectorielle_non_detectee_sur_petit_panier():
    # LIMITE DOCUMENTÉE : 2 titres 100 % Semiconducteurs, mais les poids
    # capés somment à 30 % → l'exposition secteur (30 %) reste SOUS le
    # seuil 40 % : le drapeau de concentration ne se déclenche PAS sur
    # un petit panier mono-secteur. Renormaliser = décision explicite.
    rng = np.random.default_rng(9)
    base = _walk(9)
    r = lbr.build(['NVDA', 'AMD'],
                  _detail({'NVDA': base, 'AMD': base + rng.normal(0, 0.3, 120)}))
    assert r['sectors'] == {'Semiconducteurs': 30.0}
    assert 'concentration_sectorielle' not in r['flags']


def test_erreur_fail_open_documente():
    # LIMITE DOCUMENTÉE : une entrée illisible → dict d'erreur avec
    # no_new_risk False (FAIL-OPEN : l'analyse de panier ne bloque pas
    # le risque quand elle ne peut pas conclure — l'erreur est exposée).
    bad = {'NVDA': {'series': {'close': ['x'] * 50}},
           'AMD': {'series': {'close': list(_walk(9))}}}
    r = lbr.build(['NVDA', 'AMD'], bad)
    assert 'error' in r and r['error'].startswith('ValueError')
    assert r['no_new_risk'] is False


# ── _cap_weights : redistribution ────────────────────────────────────────────

def test_cap_weights_redistribue_et_somme_1_quand_faisable():
    w = lbr._cap_weights([0.5, 0.3, 0.1, 0.1], 0.3)
    assert round(float(w.sum()), 3) == 1.0
    # tolérance d'itération : léger dépassement possible (≤ 1 %)
    assert float(w.max()) <= 0.31
    assert list(lbr._cap_weights([0, 0], 0.15)) == [0.0, 0.0]  # tout nul → nul
