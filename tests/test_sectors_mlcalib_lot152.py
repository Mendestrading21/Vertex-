"""
LOT 152 — Caractérisation de la rotation sectorielle
(`vertex/market/sectors.py` — servie par le comité et la fiche
Analyse) et de la calibration ML (`vertex/quant/ml_calibration.py` —
probabilité de gain consommée par quant_engine). Deux modules à ZÉRO
test direct, combinés (minces).

Ces tests figent agrégats, bornes, défauts et comportements limites
observés — les changer devient une décision explicite. Données
synthétiques déterministes.
"""

from vertex.market import sectors as sc
from vertex.quant import ml_calibration as mlc


ROWS = [{'symbol': 'NVDA'}, {'symbol': 'AMD'}, {'symbol': 'XOM'}, {'symbol': 'ZZZZ'}]
DETAIL = {
    'NVDA': {'score': 80, 'verdict': 'BUY', 'change': 2.0, 'rs': 70, 'volx': 1.5,
             'atr_pct': 4.0, 'sigcount': 6, 'grade': 'S',
             'signals': {'above50': True, 'above200': True}},
    'AMD': {'score': 60, 'verdict': 'WATCH', 'change': -1.0, 'rs': 55, 'volx': 1.0,
            'atr_pct': 6.0, 'sigcount': 3, 'grade': 'B', 'signals': {'above50': True}},
    'XOM': {'score': 40, 'verdict': 'AVOID', 'change': 0.5, 'atr_pct': 1.5, 'signals': {}},
}


# ═══ sectors.build_sectors ═══

def test_agregation_et_classement_par_score_moyen():
    out = sc.build_sectors(ROWS, DETAIL)
    assert [s['sector'] for s in out] == ['Semiconducteurs', 'Energie']  # tri desc
    semis = out[0]
    assert semis['n'] == 2 and semis['avg_score'] == 70
    assert semis['pct_buy'] == 50 and semis['n_buy'] == 1 and semis['n_watch'] == 1
    assert semis['b50'] == 100 and semis['b200'] == 50   # breadth des signaux


def test_symbole_hors_mapping_exclu_silencieusement():
    # ZZZZ n'est dans aucun secteur → exclu ; les membres sont classés
    # par (score, sigcount) décroissant.
    out = sc.build_sectors(ROWS, DETAIL)
    assert [m['symbol'] for m in out[0]['members']] == ['NVDA', 'AMD']
    assert out[0]['leader']['symbol'] == 'NVDA'
    assert out[0]['laggard']['symbol'] == 'AMD'


def test_bornes_risk_band_exactes():
    for atr, want in ((2.9, 'Low'), (3.0, 'Med'), (5.0, 'Med'), (5.1, 'High')):
        o = sc.build_sectors([{'symbol': 'XOM'}], {'XOM': {'atr_pct': atr}})
        assert o[0]['risk_band'] == want, (atr, o[0]['risk_band'])


def test_delta_vs_veille_ignore_les_scores_none():
    # prev : NVDA 70, AMD None (ignoré) → moyenne veille 70 ; moyenne du
    # jour (80+60)/2 = 70 → delta 0. Sans baseline → None honnête.
    prev = {'NVDA': {'score': 70}, 'AMD': {'score': None}}
    o = sc.build_sectors(ROWS[:2], {k: DETAIL[k] for k in ('NVDA', 'AMD')}, prev=prev)
    assert o[0]['delta'] == 0
    assert sc.build_sectors(ROWS[:2], DETAIL)[0]['delta'] is None


def test_detail_absent_defauts_neutres_et_rows_vides():
    assert sc.build_sectors([], {}) == []
    o = sc.build_sectors([{'symbol': 'COIN'}], {})
    # Sans détail moteur : score 0, atr par défaut 2 → Low, rs 50, rvol 1.
    assert o[0]['avg_score'] == 0 and o[0]['risk_band'] == 'Low'
    assert o[0]['avg_rs'] == 50 and o[0]['avg_rvol'] == 1.0


def test_contrat_carte_secteur():
    s = sc.build_sectors(ROWS, DETAIL)[0]
    assert {'sector', 'icon', 'n', 'avg_score', 'pct_buy', 'n_buy', 'n_watch',
            'n_avoid', 'avg_change', 'avg_rs', 'avg_rvol', 'b50', 'b200',
            'risk_band', 'delta', 'leader', 'laggard', 'members'} <= set(s)
    for m in s['members']:
        assert {'symbol', 'score', 'grade', 'verdict', 'change', 'rvol'} == set(m)


# ═══ ml_calibration.predict ═══

def test_point_neutre_edge_54_probabilite_0_5():
    r = mlc.predict({'edge': 54})
    assert r == {'p_win': 0.5, 'meta_score': 50, 'model': 'logistic'}


def test_calibration_annoncee_edge_86_et_30():
    # Le module annonce : edge 86 → ~0.74, edge 30 → ~0.32 — figé.
    assert mlc.predict({'edge': 86})['p_win'] == 0.736
    assert mlc.predict({'edge': 30})['p_win'] == 0.317


def test_bornes_humbles_jamais_sous_5_ni_sur_85_pct():
    assert mlc.predict({'edge': 10000})['p_win'] == 0.85   # jamais une promesse
    assert mlc.predict({'edge': -10000})['p_win'] == 0.05  # jamais un zéro absolu


def test_monte_carlo_first_touch_ajuste_la_proba():
    # first-touch favorable (+0.4 net) : logit +0.1 → p > 0.5.
    r = mlc.predict({'edge': 54, 'mc': {'p_tp1_first': 0.6, 'p_stop_before_tp1': 0.2}})
    assert r['p_win'] == 0.525


def test_nuance_structure_trend_quality():
    r = mlc.predict({'edge': 54, 'trend_quality': 100, 'extension_penalty': 0})
    assert r['p_win'] == 0.574


def test_bloc_absent_proba_neutre_mais_edge_illisible_none():
    # Comportements limites DOCUMENTÉS : bloc None → repli edge 50 →
    # proba quasi neutre (0.468) ; mais un edge NON NUMÉRIQUE lève dans
    # float() → toute la prédiction répond None (pas de repli partiel).
    assert mlc.predict(None) == {'p_win': 0.468, 'meta_score': 47, 'model': 'logistic'}
    assert mlc.predict({'edge': 'abc'}) is None


def test_meta_score_coherent_avec_p_win():
    for blk in ({'edge': 54}, {'edge': 86}, {'edge': 30}, None):
        r = mlc.predict(blk)
        assert r['meta_score'] == round(r['p_win'] * 100)
        assert 0.05 <= r['p_win'] <= 0.85
