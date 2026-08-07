"""
LOT 145 — Caractérisation du moteur scorecard
(`vertex/engines/scorecard.py`).

Ce moteur est VIVANT : `terminal.py` l'importe (alias `ibkr`) et appelle
`verdict()` pendant le scan — il produit le SCORE /40, les niveaux
S+/S/A/B/rejeté avec allocations, l'entry timing (BUY NOW / PULLBACK /
WATCH / TOO LATE), le filtre no-chase et le verdict final affichés dans
Opportunités. Il n'avait AUCUN test direct. Ces tests figent le
comportement observé : tout changement futur doit faire échouer cette
suite et être assumé explicitement.

Dictionnaires synthétiques déterministes — on caractérise des formes de
signaux, pas des titres réels.
"""

import pytest

from vertex.engines import scorecard as sc

# Idée « propre » : score fort, rien en surchauffe, plan complet.
CLEAN = {'score': 75, 'rsi': 55, 'ext_atr': 1.0, 'change': 0.5, 'atr_pct': 2.0,
         'pos52': 80, 'volx': 1.2, 'rs': 70, 'regime': 'TREND',
         'plan': {'entry': 100.0, 'stop': 95.0, 'resistance': 108.0, 'tp1': 110.0}}


# ── level : la grille S+/S/A/B/rejeté et ses bornes EXACTES ──────────────────

@pytest.mark.parametrize('total,niveau,alloc', [
    (40, 'S+', '10-15 %'), (36, 'S+', '10-15 %'),
    (35, 'S', '7-10 %'), (32, 'S', '7-10 %'),
    (31, 'A', '3-5 %'), (28, 'A', '3-5 %'),
    (27, 'B', '1-2 %'), (22, 'B', '1-2 %'),
    (21, 'rejeté', '0 %'), (0, 'rejeté', '0 %'),
])
def test_grille_des_niveaux_bornes_exactes(total, niveau, alloc):
    n, a, col = sc.level(total)
    assert n == niveau and a == alloc
    assert col.startswith('#') and len(col) == 7


# ── no_chase : les 4 raisons de surchauffe, chacune isolée ───────────────────

def test_no_chase_rsi_en_surchauffe():
    assert any('RSI' in r for r in sc.no_chase({'rsi': 72}))


def test_no_chase_extension_au_dessus_mm20():
    assert any('Extension' in r for r in sc.no_chase({'ext_atr': 2.5}))


def test_no_chase_bougie_violente():
    # +4 % avec un ATR de 2 % = mouvement à 2x l'ATR → violent.
    assert any('violent' in r for r in sc.no_chase({'change': 4.0, 'atr_pct': 2.0}))


def test_no_chase_colle_au_sommet_sans_volume():
    assert any('sommet' in r for r in sc.no_chase({'pos52': 99, 'volx': 0.8}))


def test_no_chase_titre_propre_liste_vide():
    assert sc.no_chase({'rsi': 55, 'ext_atr': 1.0, 'change': 0.5,
                        'atr_pct': 2.0, 'pos52': 80, 'volx': 1.2}) == []


# ── entry_timing : les 6 chemins d'état ──────────────────────────────────────

@pytest.mark.parametrize('patch,state', [
    ({}, 'BUY_NOW'),                    # propre, score 75, rien à redire
    ({'score': 49}, 'AVOID'),           # sous 50 : pas de setup
    ({'rsi': 76}, 'TOO_LATE'),          # surchauffe extrême : ne pas poursuivre
    ({'rsi': 73}, 'BUY_PULLBACK'),      # no-chase déclenché : attendre un repli
    ({'score': 65}, 'WATCH_BREAKOUT'),  # bon mais pas excellent : cassure exigée
    ({'score': 55}, 'BUY_PULLBACK'),    # 50-59 : repli par défaut
])
def test_entry_timing_etats(patch, state):
    r = sc.entry_timing({**CLEAN, **patch})
    assert r['state'] == state
    assert r['label'].strip()


def test_entry_timing_reprend_les_niveaux_du_plan():
    r = sc.entry_timing(CLEAN)
    assert r['optimal'] == 100.0
    assert r['invalidation'] == 95.0
    assert r['aggressive'] == 108.0  # resistance prioritaire sur tp1


# ── ibkr_score : plancher neutre et fenêtre catalyseur ───────────────────────

def test_donnees_inconnues_plancher_neutre_jamais_investissable():
    # Dict vide : chaque composante retombe sur sa valeur neutre — le total
    # (18/40) reste SOUS le seuil B (22). L'inconnu n'est jamais investissable.
    s = sc.ibkr_score({})
    assert s == {'total': 18, 'max': 40, 'fond': 5, 'tech': 1, 'cata': 3,
                 'inst': 2, 'optfit': 4, 'asym': 3, 'niveau': 'rejeté',
                 'alloc': '0 %', 'color': s['color']}


@pytest.mark.parametrize('ed,cata', [
    (None, 3),   # inconnu → neutre
    (3, 3),      # < 7 j : trop proche (risque IV / binaire)
    (7, 6),      # 7-45 j : fenêtre idéale
    (45, 6),
    (46, 4),     # 46-90 j : correct
    (90, 4),
    (91, 3),     # au-delà : trop loin
])
def test_fenetre_catalyseur_earnings(ed, cata):
    assert sc.ibkr_score({'score': 60}, opt={'earnings_dte': ed})['cata'] == cata


def test_bonus_regime_trend_plafonne_a_6():
    s = sc.ibkr_score({'score': 60, 'regime': 'TREND'}, opt={'earnings_dte': 30})
    assert s['cata'] == 6  # 6 (fenêtre idéale) + 1 (TREND) plafonné à 6


# ── verdict : contrat de sortie et honnêteté ─────────────────────────────────

def test_verdict_sans_donnees_renvoie_none():
    # None ET dict vide (falsy) : pas de données → pas de verdict, jamais
    # d'invention.
    assert sc.verdict(None) is None
    assert sc.verdict({}) is None


def test_verdict_accepte_sur_idee_propre():
    v = sc.verdict(CLEAN)
    assert v['decision'] == 'ACCEPTÉ' and v['tone'] == 'buy'
    assert v['timing']['state'] == 'BUY_NOW'
    assert 'stop' in v['action'] or '$' in v['action']


def test_verdict_refuse_score_insuffisant_taille_zero():
    v = sc.verdict({'score': 20})
    assert v['decision'] == 'REFUSÉ' and v['tone'] == 'avoid'
    assert v['taille'] == '0 %' and v['alloc'] == '0 %'
    assert 'Aucune position' in v['action']


def test_verdict_composantes_coherentes_somme_et_maxima():
    v = sc.verdict(CLEAN)
    comp = v['components']
    assert set(comp) == {'Fondamentaux', 'Technique', 'Catalyseur',
                         'Institutions', 'Option Fit', 'Asymétrie'}
    assert {k: c[1] for k, c in comp.items()} == {
        'Fondamentaux': 8, 'Technique': 8, 'Catalyseur': 6,
        'Institutions': 6, 'Option Fit': 6, 'Asymétrie': 6}
    # La somme des composantes EST le score affiché (pas deux vérités).
    assert sum(c[0] for c in comp.values()) == v['score40']
    for k, (val, mx) in comp.items():
        assert 0 <= val <= mx


def test_verdict_robuste_aux_valeurs_pourries():
    # Valeurs non numériques / None : _f retombe sur les défauts — jamais
    # d'exception, verdict honnêtement REFUSÉ (score inconnu = 0).
    v = sc.verdict({'score': 'abc', 'rsi': None, 'plan': {'entry': 'x'}})
    assert v['decision'] == 'REFUSÉ'
    assert v['score40'] == 18  # plancher neutre
