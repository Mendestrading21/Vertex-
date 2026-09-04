"""
LOT 150 — Caractérisation étendue du digest de session
(`vertex/engines/session_digest.py`, servi par /api/session/digest,
affiché en tête d'Aujourd'hui).

Les tests existants figent les scénarios vide/peuplé ; ces tests
figent les gardes du régime, le filtrage des catalyseurs, la
robustesse d'âge et les bornes — les changer devient une décision
explicite. Données synthétiques déterministes.
"""

import time

from vertex.engines import session_digest as sd


# ── Régime : les gardes non couvertes ────────────────────────────────────────

def test_risk_on_mais_spy_chop_retombe_neutre():
    # RISK-ON n'est affiché GO que si le S&P n'est pas en CHOP — un
    # risk-on dans un marché haché n'est pas un feu vert.
    d = sd.build({'market_ctx': {'roro': 'RISK-ON', 'spy_regime': 'CHOP'}}, {})
    assert d['regime']['label'] == 'NEUTRE' and d['regime']['tone'] == 'wait'


def test_risk_off_prioritaire_sur_tout():
    # RISK-OFF gagne même quand il est la seule donnée connue.
    d = sd.build({'market_ctx': {'roro': 'RISK-OFF'}}, {})
    assert d['regime']['label'] == 'RISK-OFF' and d['regime']['tone'] == 'risk'
    assert d['state'] == 'ready'          # un market_ctx suffit à has_data


def test_score_regime_branche_sur_market_lens_climate():
    # Le score /100 vient de l'UNIQUE source market_lens.climate (93 sur
    # le contexte porteur caractérisé au lot 149) — jamais réinventé.
    bull = {'roro': 'RISK-ON', 'spy_regime': 'TREND', 'vix_band': 'calme',
            'breadth': {'above50': 70}}
    assert sd.build({'market_ctx': bull}, {})['regime']['score'] == 93


# ── Catalyseurs : filtrage honnête des dte ───────────────────────────────────

def test_catalyseurs_dte_booleen_texte_et_brut_ignores_tri_croissant():
    # dte True (bool), 'demain' (texte) et une entrée brute sont ignorés
    # SANS masquer les catalyseurs valides ; le plus proche gagne.
    cal = {'items': [{'label': 'A', 'dte': True}, {'label': 'B', 'dte': 'demain'},
                     {'label': 'C', 'dte': 9}, {'label': 'D', 'dte': 2}, 'brut']}
    d = sd.build({'rows': [{'symbol': 'X'}], 'detail': {}}, cal)
    assert d['catalysts'] == {'count': 2, 'next': {'label': 'D', 'dte': 2}}


# ── Âge du scan : jamais un âge inventé ──────────────────────────────────────

def test_age_s_ts_booleen_none_ts_numerique_entier():
    # scan_ts True (bool ~ int) → None (pas d'âge fantôme) ; ts réel →
    # entier en secondes.
    assert sd.build({'scan_ts': True}, {})['age_s'] is None
    age = sd.build({'scan_ts': time.time() - 10}, {})['age_s']
    assert isinstance(age, int) and 9 <= age <= 12


# ── Entrées dégradées et bornes ──────────────────────────────────────────────

def test_build_none_none_honnete_analyzing():
    d = sd.build(None, None)
    assert d['state'] == 'analyzing'
    assert d['confidence'] is None
    assert d['regime']['label'] is None and d['regime']['tone'] == 'idle'


def test_top_borne_a_3_et_entrees_invalides_exclues():
    # 4 actionnables → top n'affiche que 3 (le compte reste 4) ; une
    # décision sans symbol et une entrée brute sont exclues.
    cm = {'decisions': [
        {'symbol': 'A', 'verdict': 'ACHETER'}, {'symbol': 'B', 'verdict': 'ACHETER'},
        {'symbol': 'C', 'verdict': 'RENFORCER'}, {'symbol': 'D', 'verdict': 'ACHETER'},
        {'verdict': 'ACHETER'}, 'brut']}
    d = sd.build({'rows': [{'symbol': 'A'}], 'detail': {}, 'committee': cm}, {})
    assert d['opportunities']['actionable'] == 4
    assert d['opportunities']['top'] == ['A', 'B', 'C']


def test_contrat_de_sortie_stable():
    d = sd.build({}, {}, demo=True)
    assert set(d) == {'state', 'as_of', 'age_s', 'demo', 'generator', 'regime',
                      'opportunities', 'catalysts', 'market', 'confidence'}
    assert set(d['regime']) == {'label', 'tone', 'roro', 'spy_regime', 'score'}
    assert set(d['opportunities']) == {'actionable', 'universe', 'top'}
    assert set(d['catalysts']) == {'count', 'next'}
    assert set(d['market']) == {'vix', 'vix_band', 'breadth'}
    assert d['generator'] == 'deterministic'
