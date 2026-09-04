"""
LOT 168 — Caractérisation de la stratégie options personnalisée
(`vertex/strategy/legacy_adapter.py` — VIVANT : servi par command et
terminal ; échelle 1/2/3/6/9/12 mois, mark-to-market Black-Scholes,
constructeur de portefeuille). Pur (BS interne), aucun réseau.

Ces tests figent le régime, les échelles, les règles de sortie et le
constructeur — les changer devient une décision explicite.
"""

import pytest

from vertex.strategy import legacy_adapter as la

PLAN = {'tp2': 120.0, 'stop': 90.0}


# ── _bias : le régime pondère la direction ───────────────────────────────────

@pytest.mark.parametrize('market,bias', [
    ({'regime': 'RISK-ON'}, 'favorable'),
    ({'label': 'stress volatil'}, 'dangerous'),
    ({'score': 60}, 'favorable'), ({'score': 59}, 'neutral'),
    ({'score': 39}, 'dangerous'),
    ({}, 'neutral'), (None, 'neutral'),
])
def test_bias_mots_cles_et_seuils_60_40(market, bias):
    assert la._bias(market) == bias


# ── Briques : proxy IV, pas de strike, durée de détention ────────────────────

def test_iv_proxy_bornes_022_110():
    assert round(la._iv_proxy(None), 3) == 0.317       # défaut ATR 2 %
    assert la._iv_proxy(0.1) == 0.22                   # plancher
    assert la._iv_proxy(50) == 1.10                    # plafond


@pytest.mark.parametrize('S,k,attendu', [
    (40, 41.3, 41), (80, 81.3, 82.5), (200, 203.4, 205), (400, 407.0, 410),
])
def test_round_strike_pas_1_25_5_10(S, k, attendu):
    assert la._round_strike(S, k) == attendu


@pytest.mark.parametrize('dte,jours', [(10, 5), (30, 10), (90, 31), (365, 45)])
def test_hold_days_un_tiers_borne_5_45(dte, jours):
    assert la._hold_days(dte) == jours


# ── _leg : la jambe d'option complète ────────────────────────────────────────

def test_leg_call_breakeven_sorties_et_scenarios_ordonnes():
    leg = la._leg(100.0, 0.35, PLAN, True, la.HORIZONS[2])   # 3 mois
    assert leg['breakeven'] == round(leg['strike'] + leg['premium'], 2)
    assert leg['exit']['tp50'] == round(leg['premium'] * 1.5, 2)
    assert leg['exit']['stop50'] == round(leg['premium'] * 0.5, 2)
    assert leg['exit']['theta_alert_dte'] == 45                # 90 - 45
    sc = leg['scenarios']
    assert sc['pess']['pct'] < sc['prob']['pct'] < sc['except']['pct']
    assert leg['tp_tech']['px'] == 120.0                        # cible du plan


def test_leg_put_breakeven_sous_le_strike_et_theta_court_zero():
    put = la._leg(100.0, 0.35, PLAN, False, la.HORIZONS[2])
    assert put['breakeven'] == round(put['strike'] - put['premium'], 2)
    m1 = la._leg(100.0, 0.35, PLAN, True, la.HORIZONS[0])      # 1 mois
    assert m1['exit']['theta_alert_dte'] == 0                  # 30-45 clampé à 0


# ── build : direction croisée conviction × régime ────────────────────────────

def test_regime_dangereux_impose_le_put_meme_haussier():
    rows = [{'symbol': 'AAA'}]
    detail = {'AAA': {'price': 100.0, 'atr_pct': 2.5, 'verdict': 'BUY',
                      'grade': 'S', 'score': 80, 'plan': PLAN}}
    b = la.build(rows, detail, market={'regime': 'RISK-OFF'})
    assert b['regime'] == 'dangerous'
    assert b['picks'][0]['primary'] == 'PUT'                   # défense d'abord
    fav = la.build(rows, detail, market={'regime': 'RISK-ON'})
    assert fav['picks'][0]['primary'] == 'CALL'
    assert len(fav['picks'][0]['call']) == 6                   # les 6 horizons


# ── build_portfolio : allocation cœur/satellites bornée ──────────────────────

def test_portefeuille_roles_cash_et_risque_par_position():
    rows = [{'symbol': s} for s in ('AAA', 'BBB', 'CCC', 'DDD', 'EEE')]
    detail = {s: {'price': 100.0 + i * 10, 'atr_pct': 2.5, 'verdict': 'BUY',
                  'grade': 'A', 'score': 70, 'plan': PLAN}
              for i, s in enumerate(('AAA', 'BBB', 'CCC', 'DDD', 'EEE'))}
    pf = la.build_portfolio(rows, detail, market={'regime': 'RISK-ON'},
                            capital=100000, n_core=3, n_sat=2)
    assert pf['n'] == 5
    assert [p['role'] for p in pf['positions']] == \
        ['CŒUR', 'CŒUR', 'CŒUR', 'SATELLITE', 'SATELLITE']
    assert pf['cash'] == round(100000 - pf['deployed'])        # arithmétique fermée
    assert pf['maxloss'] == pf['deployed']    # achat sec : perte max = coût déployé
    # Risque par position borné ~10 % du capital (tolérance : 1 contrat).
    assert all(p['cost'] <= 100000 * la._MAX_POS_RISK + p['premium'] * 100
               for p in pf['positions'])


def test_portefeuille_vide_honnete_sans_candidats():
    pf = la.build_portfolio([], {}, capital=50000)
    assert pf['n'] == 0 and pf['deployed'] == 0 and pf['cash'] == 50000
    assert pf['positions'] == []
