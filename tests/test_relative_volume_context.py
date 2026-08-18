from vertex.engines import relative_volume_context
from vertex.engines import skyler_core


def _detail(current=300, prior=None):
    prior = prior if prior is not None else [100] * 20
    return {'series': {'volume': prior + [current]}}


def test_relative_volume_compares_current_to_complete_observed_window():
    ctx = relative_volume_context.build(_detail())
    assert ctx['available'] is True
    assert ctx['status'] == 'OBSERVED_RELATIVE_VOLUME'
    assert ctx['prior_median_volume'] == 100.0
    assert ctx['current_to_prior_median_ratio'] == 3.0


def test_relative_volume_refuses_incomplete_prior_window_without_imputation():
    ctx = relative_volume_context.build(_detail(prior=[100] * 19 + [None]))
    assert ctx['available'] is False
    assert ctx['status'] == 'INCOMPLETE_PRIOR_VOLUME_WINDOW'
    assert ctx['coverage']['prior_valid_count'] == 19


def test_relative_volume_refuses_absent_current_volume():
    ctx = relative_volume_context.build(_detail(current=None))
    assert ctx['available'] is False
    assert ctx['status'] == 'CURRENT_VOLUME_UNAVAILABLE'


def test_relative_volume_is_carried_without_scoring_effect():
    ctx = relative_volume_context.build(_detail())
    packet = skyler_core.build_packet('TST', {'score': 70, 'verdict': 'ACHETER'}, relative_volume_ctx=ctx)
    assert packet['contexts']['relative_volume'] == ctx
    assert 'relative_volume' not in skyler_core.score40(packet)['blocks']
