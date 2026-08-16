from vertex.market import regime_engine as RE


def test_macro_modulators_are_secondary_and_never_override_panic():
    out = RE.classify_regime({
        'index_trend': 'DOWN', 'breadth_pct': 20, 'vix': 38,
        'leadership': 'DEFENSIVE', 'yield_curve_bps': -25,
        'dollar_trend': 'STRENGTHENING',
    })
    assert out['regime'] == 'PANIC'
    assert 'YIELD_CURVE_INVERTED' in out['secondary']
    assert 'DOLLAR_STRENGTHENING' in out['secondary']
