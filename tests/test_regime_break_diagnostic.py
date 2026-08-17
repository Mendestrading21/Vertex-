"""Rupture de régime descriptive : aucune prévision ni modification de décision."""

from datetime import date, timedelta

from vertex.market import regime_break as regime


def _series(returns):
    close, dates, closes = 100.0, [date(2025, 1, 1).isoformat()], [100.0]
    for index, value in enumerate(returns, 1):
        close *= 1.0 + value
        dates.append((date(2025, 1, 1) + timedelta(days=index)).isoformat())
        closes.append(round(close, 8))
    return {'dates': dates, 'close': closes}


def _baseline():
    return [0.003 if index % 2 else -0.001 for index in range(60)]


def test_regime_break_requires_full_dated_evidence():
    out = regime.assess({'close': [100.0] * 81})
    assert out['available'] is False
    assert out['status'] == 'TEMPORAL_EVIDENCE_REQUIRED'

    out = regime.assess(_series(_baseline() + [0.01] * 19))
    assert out['available'] is False
    assert out['status'] == 'INSUFFICIENT_SAMPLE'


def test_regime_break_flags_realized_volatility_expansion_without_prediction():
    recent = [0.04 if index % 2 else -0.035 for index in range(20)]
    out = regime.assess(_series(_baseline() + recent))
    assert out['available'] is True
    assert out['status'] == 'REGIME_BREAK_WATCH'
    assert 'VOLATILITY_REGIME_BREAK' in out['flags']
    assert out['volatility_ratio'] >= 1.80
    assert out['read_only'] is True and out['does_not_change_decision'] is True
    assert 'ne prédit pas' in out['note']


def test_regime_break_flags_directional_reversal_with_separate_windows():
    recent = [-0.020 if index % 2 else -0.016 for index in range(20)]
    out = regime.assess(_series(_baseline() + recent))
    assert out['available'] is True
    assert 'MEAN_RETURN_REGIME_BREAK' in out['flags']
    assert 'DIRECTIONAL_REGIME_REVERSAL' in out['flags']
    assert out['baseline_end'] == out['recent_start']
    assert out['baseline_return_pct'] > 0 > out['recent_return_pct']
