"""
LOT 155 — Caractérisation étendue du brief éditorial
(`vertex/market/editorial.py`, ratio 0.34 — le narratif de séance §10
affiché en tête d'Aujourd'hui ; chaque phrase n'est émise que si sa
donnée existe, jamais de récit inventé).

Les tests existants (`tests/test_editorial_brief.py`) couvrent les
grandes lignes ; ceux-ci figent les SEUILS exacts des phrases, la
priorité des risques et les troncatures — les changer devient une
décision explicite.
"""

#  VOCABULAIRE MIS A JOUR (fusion Black Glass). Les SEUILS — le vrai
#  contrat de ce fichier — n'ont pas bouge d'un centieme ; seule la
#  formulation a change, et dans le bon sens : « terminé en hausse »
#  affirmait une seance CLOSE a une heure ou elle peut etre ouverte.
#  « s'affichent en hausse » ne promet rien de tel. Les autres suivent
#  la meme logique : dire ce qui est observe, pas ce qu'on en conclut.
import pytest

from vertex.market import editorial as ed


def _idx(sp=None, ndx=None):
    out = []
    if sp is not None:
        out.append({'name': 'S&P 500', 'change': sp})
    if ndx is not None:
        out.append({'name': 'Nasdaq', 'change': ndx})
    return out


# ── Direction des indices : seuils EXACTS ±0.15 ──────────────────────────────

@pytest.mark.parametrize('chg,mot', [
    (0.15, 'en hausse'), (0.14, 'quasi inchangés'),
    (-0.15, 'en baisse'), (-0.14, 'quasi inchangés'),
])
def test_direction_indices_seuils_exacts(chg, mot):
    n = ed.build_narrative({'indices': _idx(sp=chg)})['narrative']
    #  « terminé » -> « s'affichent » : voir la note en tete de fichier.
    assert ("s'affichent %s" % mot) in n


# ── Leadership : écart STRICT > 0.2 entre Nasdaq et S&P ──────────────────────

def test_leadership_techno_exige_plus_de_0_2_strict():
    tech = ed.build_narrative({'indices': _idx(sp=1.0, ndx=1.3)})['narrative']
    pile = ed.build_narrative({'indices': _idx(sp=1.0, ndx=1.2)})['narrative']
    assert 'concentre le leadership' in tech
    assert 'concentre le leadership' not in pile     # +0.2 pile ne suffit pas


def test_rotation_cyclique_quand_sp_domine():
    n = ed.build_narrative({'indices': _idx(sp=1.3, ndx=1.0)})['narrative']
    assert 'profite aux valeurs cycliques' in n


# ── VIX : les trois phrases, bornes 18 / 25 ──────────────────────────────────

@pytest.mark.parametrize('vix,mot', [
    (17.9, 'convexité'), (18.0, 'médiane'), (25.0, 'médiane'), (25.1, 'renchérit'),
])
def test_phrases_vix_bornes_18_25(vix, mot):
    assert mot in ed.build_narrative({'market': {'vix': vix}})['narrative']


# ── Breadth : frontière 55 (saine / étroite) ─────────────────────────────────

def test_breadth_frontiere_55():
    saine = ed.build_narrative({'market': {'breadth': 55}})['narrative']
    etroite = ed.build_narrative({'market': {'breadth': 54.9}})['narrative']
    assert 'participation est large' in saine
    assert 'sélectivité' in etroite


# ── main_risk : priorité et frontière 45 ─────────────────────────────────────

def test_risque_risk_off_prioritaire_sur_breadth():
    r = ed.build_narrative({'market': {'roro': 'RISK-OFF', 'breadth': 30,
                                       'spy_regime': 'TREND'}})
    assert 'RISK-OFF' in r['main_risk']


def test_risque_breadth_sous_45_strict_sinon_aucun():
    faux = ed.build_narrative({'market': {'breadth': 44.9, 'spy_regime': 'TREND'}})
    ok = ed.build_narrative({'market': {'breadth': 45, 'spy_regime': 'TREND'}})
    assert 'faux départs' in faux['main_risk']
    assert ok['main_risk'] is None               # 45 pile : pas de risque déclaré


# ── calls_impact : la branche IV chère ───────────────────────────────────────

def test_calls_iv_chere_exige_rr_strict():
    r = ed.build_narrative({'market': {'vix': 30}})
    assert 'coûtent cher' in r['calls_impact']
    assert 'R:R strict' in r['calls_impact']


# ── Actualités : titre borné, sources tracées ────────────────────────────────

def test_titre_a_la_une_tronque_a_180():
    r = ed.build_narrative({}, news_state={'items': [{'title': 'X' * 300}]})
    une = next(s for s in r['narrative'].split('.') if 'la une' in s)
    assert une.count('X') == 180                  # borné, jamais le titre entier


def test_sources_triees_et_dedupliquees():
    r = ed.build_narrative(
        {'indices': _idx(sp=1.0), 'sectors': [{'sector': 'A', 'avg_score': 70}],
         'committee': {'counts': {'ACHETER': 2, 'ATTENDRE': 3}}},
        news_state={'items': [{'title': 'T'}]})
    assert r['sources'] == ['actualités (fil assaini)', 'indices (scan)',
                            'secteurs (scan)']
    assert '2 dossiers achetables' in r['narrative']
    assert '3 en surveillance' in r['narrative']


# ── Opportunité prioritaire : premier verdict ACHETER/RENFORCER ──────────────

def test_opportunite_prioritaire_saute_les_refus():
    r = ed.build_narrative({'committee': {'decisions': [
        {'symbol': 'Z', 'verdict': 'REFUSER'},
        {'symbol': 'ACN', 'verdict': 'ACHETER'}]}})
    assert r['main_opportunity'].startswith('ACN — ')
    assert 'dossier complet' in r['main_opportunity']
