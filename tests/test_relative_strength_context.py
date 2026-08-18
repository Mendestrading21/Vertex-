from vertex.engines import relative_strength_context
from vertex.engines import skyler_core


def _series(base, step, count=70):
    return {'dates': [f'2026-01-{index:03d}' for index in range(count)],
            'close': [base + step * index for index in range(count)]}


def test_relative_strength_uses_aligned_observed_returns():
    ctx = relative_strength_context.build(_series(100, 1.0), _series(100, 0.5))
    assert ctx['available'] is True
    assert ctx['status'] == 'OBSERVED_RELATIVE_PERFORMANCE'
    assert {item['window_sessions'] for item in ctx['windows']} == {20, 63}
    assert all(item['excess_return_pct'] > 0 for item in ctx['windows'])
    assert ctx['read_only'] is True


def test_relative_strength_refuses_unaligned_or_short_series():
    ctx = relative_strength_context.build({'dates': ['a'], 'close': [100]}, {'dates': ['b'], 'close': [100]})
    assert ctx['available'] is False
    assert ctx['status'] == 'INSUFFICIENT_ALIGNED_SERIES'


def test_relative_strength_is_carried_without_scoring_effect():
    ctx = relative_strength_context.build(_series(100, 1.0), _series(100, 0.5))
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, relative_strength_ctx=ctx)
    assert packet['contexts']['relative_strength'] == ctx
    assert 'relative_strength' not in skyler_core.score40(packet)['blocks']
