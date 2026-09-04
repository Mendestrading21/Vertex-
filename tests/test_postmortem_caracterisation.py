"""
LOT 148 — Caractérisation étendue du post-mortem du Journal
(`vertex/engines/postmortem.py`, servi par /api/journal/postmortem,
affiché dans Journal/Discipline).

Le fichier existant (`tests/test_postmortem.py`) fige le scénario
principal ; il ne couvrait ni la robustesse de la coercition numérique
(booléens, chaînes, infinis), ni le break-even, ni le profit factor
sans perte, ni le drapeau « win rate élevé mais P&L négatif », ni le
tri des récidives, ni les troncatures. Ces tests figent le comportement
observé — le changer devient une décision explicite.

Données synthétiques déterministes — des formes de trades, pas des
trades réels.
"""

from vertex.engines import postmortem as pm


# ── Coercition numérique : ce qui entre et ce qui est rejeté ─────────────────

def test_cout_booleen_rejete_bool_nest_pas_un_nombre():
    # True est une instance d'int en Python : la garde _num le rejette
    # explicitement — un flag ne devient jamais un coût.
    assert pm.build([{'sym': 'A', 'cost': True, 'exit': 100}])['trades_n'] == 0


def test_chaines_numeriques_acceptees_infinis_et_zero_rejetes():
    d = pm.build([
        'pas-un-dict',                                    # entrée non-dict → sautée
        {'sym': 'A', 'cost': '1000', 'exit': '1300'},     # chaînes numériques OK
        {'sym': 'B', 'cost': 'inf', 'exit': 100},         # infini → rejeté
        {'sym': 'C', 'cost': 0, 'exit': 50},              # coût nul → inexploitable
        {'sym': 'D', 'cost': -100, 'exit': 50},           # coût négatif → inexploitable
    ])
    assert d['trades_n'] == 1
    assert d['total_pnl'] == 300.0


# ── Comportements limites DOCUMENTÉS (pas des souhaits — l'existant) ─────────

def test_break_even_classe_comme_perte():
    # pnl == 0 tombe dans les pertes (pnl <= 0) : un trade qui ne gagne
    # rien n'est pas un gagnant. gl = 0 → profit factor None (pas ÷0).
    d = pm.build([{'sym': 'A', 'cost': 100, 'exit': 100}])
    assert d['wins'] == 0 and d['losses'] == 1
    assert d['win_rate'] == 0
    assert d['profit_factor'] is None


def test_echantillon_sans_perte_profit_factor_none_pas_infini():
    # 100 % gagnant : PF est None (honnête — indéfini, pas ∞) et la
    # narrative saute la phrase PF ; aucun drapeau sur un échantillon sain.
    d = pm.build([{'sym': 'A', 'cost': 100, 'exit': 150},
                  {'sym': 'B', 'cost': 100, 'exit': 120}])
    assert d['profit_factor'] is None
    assert 'Profit factor' not in d['narrative']
    assert d['flags'] == []
    assert 'Aucun drapeau' in d['narrative']


# ── Drapeaux : chaque dérivation chiffrée ────────────────────────────────────

def test_drapeau_win_rate_eleve_mais_pnl_negatif():
    # 2 petits gains + 1 grosse perte : wr 67 % mais total -480 → le
    # drapeau « pertes trop grosses » se déclenche.
    d = pm.build([{'sym': 'A', 'cost': 100, 'exit': 110},
                  {'sym': 'B', 'cost': 100, 'exit': 110},
                  {'sym': 'C', 'cost': 1000, 'exit': 500}])
    assert d['win_rate'] == 67 and d['total_pnl'] == -480.0
    assert any('élevé' in f and 'négatif' in f for f in d['flags'])


def test_recidives_triees_par_nombre_de_pertes_decroissant():
    mk = lambda s: {'sym': s, 'cost': 100, 'exit': 50}
    d = pm.build([mk('X'), mk('X'), mk('Y'), mk('Y'), mk('Y'), mk('Z')])
    # Y (3 pertes) avant X (2) ; Z (1 seule) n'est pas une récidive.
    assert d['repeat_losers'] == ['Y', 'X']


# ── Dates de détention : robustesse et honnêteté ─────────────────────────────

def test_dates_inversees_valeur_absolue_et_non_parsables_exclues():
    d = pm.build([
        {'sym': 'A', 'cost': 100, 'exit': 150,
         'added': '2026-07-10', 'closed': '2026-07-01'},   # inversées → abs = 9 j
        {'sym': 'B', 'cost': 100, 'exit': 150,
         'added': 'n/a', 'closed': '???'},                  # non parsables → None
    ])
    # La moyenne ne compte QUE les durées connues : 9.0 (pas de 0 inventé).
    assert d['hold_days_avg'] == 9.0


# ── Journal : troncatures des erreurs notées ─────────────────────────────────

def test_mistakes_les_8_dernieres_texte_tronque_140():
    j = [{'ticker': 'T%d' % i, 'mistake': 'x' * 200, 'date': '2026-01-01'}
         for i in range(10)]
    d = pm.build([{'sym': 'A', 'cost': 100, 'exit': 150}], journal=j)
    assert len(d['mistakes']) == 8
    assert d['mistakes'][0]['ticker'] == 'T2'       # les 8 DERNIÈRES (T2..T9)
    assert d['mistakes'][-1]['ticker'] == 'T9'
    assert len(d['mistakes'][0]['mistake']) == 140  # texte borné


# ── Contrat de sortie : mêmes clés plein/vide, générateur déterministe ───────

def test_contrat_de_sortie_cles_identiques_plein_et_vide():
    plein = pm.build([{'sym': 'A', 'cost': 100, 'exit': 150}])
    vide = pm.build([])
    communes = {'empty', 'trades_n', 'wins', 'losses', 'win_rate', 'total_pnl',
                'avg_win', 'avg_loss', 'profit_factor', 'expectancy', 'best',
                'worst', 'by_type', 'repeat_losers', 'hold_days_avg', 'flags',
                'mistakes', 'narrative', 'generator'}
    assert communes <= set(plein)
    assert communes <= set(vide)          # + 'reason' côté vide
    assert vide['reason']
    assert plein['generator'] == vide['generator'] == 'deterministic'


def test_by_type_agregation_par_instrument():
    d = pm.build([
        {'sym': 'A', 'type': 'STK', 'cost': 100, 'exit': 200},
        {'sym': 'B', 'type': 'STK', 'cost': 100, 'exit': 150},
        {'sym': 'C', 'type': 'CALL', 'cost': 100, 'exit': 40},
    ])
    assert d['by_type'] == {'STK': {'n': 2, 'pnl': 150.0},
                            'CALL': {'n': 1, 'pnl': -60.0}}
