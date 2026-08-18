from vertex.options.iv_hv import describe


def test_iv_hv_context_is_unavailable_without_both_observed_measures():
    out = describe(35.0, None)
    assert out['available'] is False
    assert out['status'] == 'INSUFFICIENT_IV_HV'
    assert out['gap_pct_points'] is None


def test_iv_hv_context_reports_gap_without_predictive_claim():
    out = describe(35.0, 20.0)
    assert out['available'] is True
    assert out['status'] == 'IV_ABOVE_HV'
    assert out['gap_pct_points'] == 15.0
    assert out['ratio'] == 1.75
    assert out['read_only'] is True


def test_iv_hv_context_treats_nearby_measurements_as_near():
    out = describe(22.0, 20.0)
    assert out['status'] == 'IV_NEAR_HV'


def test_realized_volatility_requires_twenty_observed_returns():
    from vertex.options.iv_hv import realized_volatility_20d
    assert realized_volatility_20d([100.0] * 20) is None
    assert realized_volatility_20d([100.0 + idx * 0.5 for idx in range(21)]) is not None
