"""
tests/test_reasoning.py — Le moteur de raisonnement (Ch. XVIII).

Trois scénarios conditionnels, invalidations explicites, conviction ≠ prédiction.
"""

from vertex.engines import reasoning


_D = {
    'symbol': 'TEST', 'price': 100,
    'plan': {'entry': 100, 'stop': 92, 'tp1': 108, 'tp2': 116, 'tp3': 130,
             'resistance': 104, 'rr_res': 2.5},
    'signals': {'above200': True},
}


def test_three_scenarios_present():
    sc = reasoning.scenarios(_D, {'lean': 60}, 'BUY')
    names = [s['name'] for s in sc]
    assert names == ['Haussier', 'Central', 'Baissier']
    for s in sc:
        assert s['trigger'] and s['invalidation']
        assert s['likelihood'] in {'plausible', 'possible', 'peu probable'}


def test_scenario_weights_sum_reasonably():
    sc = reasoning.scenarios(_D, {'lean': 50}, 'WAIT')
    total = sum(s['weight'] for s in sc)
    assert 95 <= total <= 105  # ~100%, arrondis


def test_bull_lean_raises_bull_weight():
    bull = reasoning.scenarios(_D, {'lean': 80}, 'BUY')[0]['weight']
    bear = reasoning.scenarios(_D, {'lean': 20}, 'AVOID')[0]['weight']
    assert bull > bear  # plus le comité penche haussier, plus le scénario haussier pèse


def test_invalidations_include_stop():
    inv = reasoning.invalidations(_D)
    assert any('92' in x for x in inv)
    assert 1 <= len(inv) <= 4


def test_below_ma200_adds_invalidation():
    inv = reasoning.invalidations({**_D, 'signals': {'above200': False}})
    assert any('MM200' in x for x in inv)


def test_build_carries_conviction_note():
    b = reasoning.build(_D, {'lean': 55}, 'BUY')
    assert 'scenarios' in b and 'invalidations' in b
    assert 'prédiction' in b['conviction_note'].lower()


def test_missing_plan_degrades_gracefully():
    # aucun plan → pas de crash, scénarios présents avec cibles None
    sc = reasoning.scenarios({'symbol': 'X'}, {'lean': 50}, 'WAIT')
    assert len(sc) == 3
