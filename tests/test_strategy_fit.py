"""
tests/test_strategy_fit.py — Couche stratégie (véhicule / score / playbook / tilt).

Non-régression golden : re-pondération offensive de champs déjà calculés, sans
jamais toucher elio, sans passer d'ordre.
"""

from vertex.engines import strategy_fit as sf


def test_vehicle_selection_golden():
    assert sf.vehicle_of({'verdict': 'AVOID', 'score': 30}, None)['reco'] == '—'
    assert sf.vehicle_of({'verdict': 'BUY', 'score': 80}, None)['reco'] == 'ACTION'      # pas d'option
    assert sf.vehicle_of({'verdict': 'BUY', 'score': 80}, {'quality': 30, 'pop': 20})['reco'] == 'ACTION'
    opt = sf.vehicle_of({'verdict': 'BUY', 'score': 80},
                        {'quality': 75, 'pop': 55, 'iv': 40, 'pot': 120, 'strike': 110, 'exp': '2025'})
    assert opt['reco'] == 'OPTION' and opt['opt']['strike'] == 110
    # IV chère → action (évite de surpayer la prime)
    assert sf.vehicle_of({'verdict': 'BUY', 'score': 60}, {'quality': 50, 'pop': 40, 'iv': 70, 'pot': 50})['reco'] == 'ACTION'


def test_strat_score_golden():
    assert sf.strat_score({'score': 80, 'st_mom': 85, 'rs': 75, 'regime': 'TREND', 'pos52': 82}) == 82
    assert sf.strat_score({'score': 40, 'regime': 'CHOP', 'rsi': 80, 'ext_atr': 4, 'vx_notrade': True}) == 6
    assert 0 <= sf.strat_score({'score': 60, 'regime': 'NEUTRAL'}) <= 100


def test_playbook_matching():
    assert sf.playbook_of({'regime': 'TREND', 'rs': 75, 'pos52': 85})['name'] == 'Momentum Breakout'
    assert sf.playbook_of({'score': 75, 'verdict': 'BUY'})['name'] == 'Qualité forte'
    assert sf.playbook_of({'regime': 'CHOP', 'score': 30}) is None


def test_strat_tilt_climate():
    fav = sf.strat_tilt({'spy_regime': 'TREND', 'roro': 'RISK-ON', 'vix_band': 'calme', 'breadth': {'above50': 70}})
    dang = sf.strat_tilt({'spy_regime': 'CHOP', 'roro': 'RISK-OFF', 'vix_band': 'stress', 'breadth': {'above50': 30}})
    assert fav['regime'] == 'FAVORABLE' and dang['regime'] == 'DANGEREUX'
    assert sf.strat_tilt(None) is None


def test_attach_mutates_rows():
    rows = [{'symbol': 'X', 'verdict': 'BUY', 'score': 80, 'st_mom': 85, 'rs': 75, 'regime': 'TREND'}]
    sf.attach_vehicle(rows, [{'sym': 'X', 'type': 'CALL', 'quality': 75, 'pop': 55, 'iv': 40, 'pot': 120,
                              'strike': 110, 'exp': '2025'}])
    sf.attach_strategy(rows, {'X': {'plan': {'rr_res': 2.5}}})
    r = rows[0]
    assert r['vehicle']['reco'] == 'OPTION'
    assert r['rr'] == 2.5 and r['rr_ok'] is True
    # pos52 absent → Momentum Breakout ne matche pas ; score 80 + BUY → « Qualité forte »
    assert r['playbook']['name'] == 'Qualité forte'


def test_terminal_bindings_are_the_module():
    import terminal
    assert terminal._vehicle_of is sf.vehicle_of
    assert terminal._strat_tilt is sf.strat_tilt
