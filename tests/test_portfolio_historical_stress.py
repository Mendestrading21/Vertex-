"""Stress test historique du portefeuille : données datées ou indisponibilité honnête."""

from datetime import date, timedelta

from vertex.engines import portfolio_context as context
from vertex.portfolio import historical_stress as stress


def _series(returns):
    price, closes, dates = 100.0, [100.0], [date(2025, 1, 1).isoformat()]
    for index, value in enumerate(returns, 1):
        price *= 1.0 + value
        closes.append(round(price, 6))
        dates.append((date(2025, 1, 1) + timedelta(days=index)).isoformat())
    return {'dates': dates, 'close': closes}


def _positions():
    return [
        {'symbol': 'AAA', 'asset_type': 'STOCK', 'quantity': 1, 'cost_basis': 100,
         'source': 'MANUAL', 'is_real': True, 'status': 'OPEN'},
        {'symbol': 'BBB', 'asset_type': 'ETF', 'quantity': 1, 'cost_basis': 100,
         'source': 'MANUAL', 'is_real': True, 'status': 'OPEN'},
    ]


def test_historical_stress_uses_only_common_dated_observations():
    returns_aaa = [0.01] * 40
    returns_bbb = [0.0] * 40
    returns_aaa[12] = -0.10
    out = stress.assess({'AAA': 50.0, 'BBB': 50.0},
                        {'AAA': _series(returns_aaa), 'BBB': _series(returns_bbb)})
    assert out['available'] is True
    assert out['status'] == 'HISTORICAL_STRESS_AVAILABLE'
    assert out['n_common_sessions'] == 41
    assert out['worst_1d']['portfolio_return_pct'] == -5.0
    assert out['largest_worst_day_contributor'] == 'AAA'
    assert out['flags'] == ['HISTORICAL_TAIL_CONCENTRATION']
    assert out['never_triggers_orders'] is True


def test_historical_stress_refuses_partial_or_undated_portfolio():
    out = stress.assess({'AAA': 50.0, 'BBB': 50.0}, {'AAA': _series([0.01] * 40)})
    assert out['available'] is False
    assert out['status'] == 'TEMPORAL_EVIDENCE_REQUIRED'
    assert out['missing_symbols'] == ['BBB']

    undated = {'AAA': {'close': [100.0] * 40}, 'BBB': {'close': [100.0] * 40}}
    out = stress.assess({'AAA': 50.0, 'BBB': 50.0}, undated)
    assert out['available'] is False
    assert out['status'] == 'TEMPORAL_EVIDENCE_REQUIRED'


def test_historical_stress_consumer_refuses_unsorted_canonical_dates():
    aaa = _series([0.01] * 40)
    aaa['dates'][10], aaa['dates'][11] = aaa['dates'][11], aaa['dates'][10]
    out = stress.assess({'AAA': 50.0, 'BBB': 50.0},
                        {'AAA': aaa, 'BBB': _series([0.0] * 40)})
    assert out['available'] is False
    assert out['status'] == 'TEMPORAL_EVIDENCE_REQUIRED'
    assert out['read_only'] is True


def test_portfolio_context_exposes_read_only_historical_stress():
    series = {'AAA': _series([0.01] * 40), 'BBB': _series([0.0] * 40)}
    out = context.build(_positions(), quotes={'AAA': 100.0, 'BBB': 100.0}, series_by_symbol=series)
    stress_test = out['stress_test']
    assert stress_test['available'] is True
    assert stress_test['read_only'] is True
    assert stress_test['symbols'] == ['AAA', 'BBB']
    assert 'order' not in str(stress_test).lower().replace('never_triggers_orders', '')
    factors = out['factor_exposure']
    assert factors['available'] is True
    assert factors['read_only'] is True
    assert factors['factors']['MARKET']['coverage_pct'] == 100.0
    assert factors['availability']['BETA']['available'] is False
    assert factors['availability']['BETA']['reason']
