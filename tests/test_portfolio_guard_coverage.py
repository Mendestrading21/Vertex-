from vertex.portfolio.portfolio_guard import guard_rules


class _Profile:
    portfolio_max_drawdown_pct = -25.0
    stock_max_drawdown_pct = -20.0
    max_simultaneous_options = 3


def test_guard_exposes_partial_risk_coverage_without_new_blocking_rule():
    result = guard_rules({
        'beta_coverage': {'partial': True},
        'options_exposure': {'open_options': 0,
                             'coverage': {'delta_coverage_pct': 50.0}},
    }, _Profile())
    assert result['blocking_rules'] == []
    assert result['new_stock_allowed'] is True
    assert result['risk_coverage_warnings'] == [
        'BETA_COVERAGE_PARTIAL', 'GREEKS_COVERAGE_PARTIAL',
    ]
