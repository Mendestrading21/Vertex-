"""tests/test_decide_edges.py — SKYLER LOT 91 : decide.py figé.

`vertex/engines/decide.py` (le verdict de scan ACHETER FORT→ÉVITER) n'avait
qu'UN test dédié (le hard gate R:R, test_strategy_consistency). Tests de
CARACTÉRISATION nés verts (dits) — moteur INTACT.
"""
from vertex.engines import decide as dz

GOOD = {'score': 82, 'trend': 70, 'regime': 'TREND', 'setup_quality': 70,
        'confidence': 72, 'rsi': 55, 'ext_atr': 1, 'pos52': 70, 'rs': 70,
        'volx': 1.5, 'signals': {'stacked': True, 'above200': True, 'above50': True},
        'plan': {'entry': 100, 'stop': 95, 'tp1': 108, 'tp2': 115, 'tp3': 124,
                 'rr_res': 2.6}}


def _d(**kw):
    d = {k: (dict(v) if isinstance(v, dict) else v) for k, v in GOOD.items()}
    d.update(kw)
    return d


def test_none_or_empty_detail_returns_none():
    # dict vide = falsy → refus honnête None (jamais un verdict sans données)
    assert dz.decide(None) is None
    assert dz.decide({}) is None


def test_weak_detail_is_avoid_with_honest_action():
    r = dz.decide({'score': 10, 'trend': 10})
    assert r['decision'] == 'ÉVITER'
    assert 0 <= r['conviction'] <= 100
    assert 'Structure faible' in r['action']


def test_strong_setup_is_strong_buy_with_full_plan():
    r = dz.decide(_d())
    assert r['decision'] == 'ACHETER FORT'
    assert 'Entrée vers $100' in r['action']


def test_hard_gate_stop_missing_downgrades():
    r = dz.decide(_d(plan={'entry': 100, 'rr_res': 2.6}))
    assert r['decision'] == 'SURVEILLER'
    assert any('invalidation (stop) absente' in c for c in r['cons'])


def test_hard_gate_unknown_regime_downgrades():
    r = dz.decide(_d(regime='UNKNOWN'))
    assert r['decision'] == 'SURVEILLER'
    assert any('régime de marché inconnu' in c for c in r['cons'])


def test_hard_gate_rr_boundary_2_0():
    ok = dz.decide(_d(plan=dict(GOOD['plan'], rr_res=2.0)))
    bad = dz.decide(_d(plan=dict(GOOD['plan'], rr_res=1.9)))
    assert ok['decision'] == 'ACHETER FORT', 'R:R 2.0 exact passe le gate'
    assert bad['decision'] == 'SURVEILLER'
    assert any('1.9 < 2:1' in c for c in bad['cons'])


def test_chop_blocks_any_buy():
    r = dz.decide(_d(regime='CHOP'))
    assert r['decision'] == 'SURVEILLER', 'jamais un achat en marché de range'


def test_extended_buy_says_wait_for_pullback():
    r = dz.decide(_d(ext_atr=5, score=88, setup_quality=80, confidence=80))
    if r['decision'] in ('ACHETER FORT', 'ACHETER'):
        assert 'attendre un repli' in r['action'].lower()


def test_earnings_within_14_days_is_a_risk():
    r = dz.decide(_d(), opt={'earnings_dte': 7})
    assert any('Résultats dans 7 jours' in c for c in r['cons'])
    r2 = dz.decide(_d(), opt={'earnings_dte': 60})
    assert not any('Résultats dans' in c for c in r2['cons'])
