"""
tests/test_decision_stack.py — La DecisionStack est la vérité : ses règles sont testées.

Chaque règle institutionnelle de dégradation a un test dédié. Toute sortie doit
appartenir à l'énumération autorisée et rester explicable.
"""

from vertex.engines import decision_stack as ds


def _stock(**over):
    base = {
        'symbol': 'TEST', 'price': 100, 'score': 82, 'grade': 'A', 'verdict': 'BUY',
        'rs': 75, 'rsi': 55, 'ext_atr': 1.0, 'pos52': 70, 'confidence': 70,
        'profile': 'OFFENSIF', 'signals': {'stacked': True},
        'plan': {'entry': 100, 'stop': 92, 'tp1': 108, 'tp2': 116, 'tp3': 130, 'rr_res': 2.5},
        'mtf': {'state': 'ALIGNÉ HAUSSIER'},
    }
    base.update(over)
    return base


def test_decision_in_allowed_set():
    r = ds.evaluate(_stock())
    assert r['final_decision'] in ds.DECISIONS
    assert r['decision_label'] and r['explanation']


def test_strong_setup_buys():
    r = ds.evaluate(_stock(), market={'roro': 'RISK-ON', 'spy_regime': 'TREND'})
    assert r['final_decision'] in {'STRONG_BUY', 'BUY'}
    assert r['market_permission'] is True


def test_missing_data_blocks():
    r = ds.evaluate({'symbol': 'X'})  # pas de price/score/plan
    assert r['final_decision'] == 'DATA_INSUFFICIENT'
    assert r['data_quality']['blocks_decision'] is True


def test_risk_off_no_strong_buy():
    r = ds.evaluate(_stock(score=90), market={'roro': 'RISK-OFF', 'spy_regime': 'TREND'})
    assert r['final_decision'] != 'STRONG_BUY'


def test_extension_downgrades():
    # sur-étendu + qualité forte → achat sur repli
    r = ds.evaluate(_stock(rsi=82, ext_atr=5, score=80))
    assert r['final_decision'] == 'BUY_PULLBACK'
    # sur-étendu + qualité moyenne → trop tard
    r2 = ds.evaluate(_stock(rsi=82, ext_atr=5, score=60, verdict='WATCH'))
    assert r2['final_decision'] in {'TOO_LATE', 'WATCH_BREAKOUT', 'WAIT'}


def test_low_rr_no_buy():
    r = ds.evaluate(_stock(plan={'entry': 100, 'stop': 96, 'tp1': 103, 'tp2': 105,
                                  'tp3': 108, 'rr_res': 1.0}))
    assert r['final_decision'] not in {'STRONG_BUY', 'BUY'}


def test_high_correlation_no_new_risk():
    r = ds.evaluate(_stock(), portfolio={'max_correlation': 0.9})
    assert r['final_decision'] == 'NO_NEW_RISK'


def test_illiquid_option_forces_action():
    r = ds.evaluate(_stock(), option={'quality': 80, 'spread': 20, 'oi': 50, 'iv': 40})
    assert r['vehicle'] == 'ACTION'


def test_liquid_option_offensive_allows_option():
    r = ds.evaluate(_stock(), option={'quality': 75, 'spread': 3, 'oi': 5000,
                                      'iv': 45, 'iv_rank': 40})
    assert r['vehicle'] == 'OPTION'


def test_expensive_iv_forces_action():
    r = ds.evaluate(_stock(), option={'quality': 75, 'spread': 3, 'oi': 5000,
                                      'iv': 95, 'iv_rank': 85})
    assert r['vehicle'] == 'ACTION'


def test_avoid_stays_avoid():
    r = ds.evaluate(_stock(verdict='AVOID', score=30))
    assert r['final_decision'] == 'AVOID'


def test_conviction_confidence_bounded():
    for over in [{}, {'score': 0}, {'score': 100}, {'confidence': 0}]:
        r = ds.evaluate(_stock(**over))
        assert 0 <= r['conviction'] <= 100
        assert 0 <= r['confidence'] <= 100
