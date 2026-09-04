from vertex.data_sources.models import (
    MODE_EOD, MODE_LIVE, SOURCE_FALLBACK_EOD, SOURCE_IBKR, ProvenancedValue,
)
from vertex.data_sources.source_router import SourceRouter


def test_router_opens_circuit_then_recovers_without_exception_detail():
    now = [0.0]
    primary_calls = [0]
    primary_ok = [False]

    def clock():
        return now[0]

    def primary():
        primary_calls[0] += 1
        if not primary_ok[0]:
            raise RuntimeError('private-provider-token')
        return ProvenancedValue(value=101)

    router = SourceRouter(failure_threshold=2, cooldown_seconds=10, clock=clock)
    router.register(SOURCE_IBKR, MODE_LIVE, primary)
    router.register(SOURCE_FALLBACK_EOD, MODE_EOD, lambda: ProvenancedValue(value=99))
    assert router.fetch().value == 99
    assert router.fetch().value == 99
    assert primary_calls[0] == 2
    assert router.fetch().value == 99
    assert primary_calls[0] == 2
    state = router.health()['providers'][0]
    assert state['status'] == 'OPEN' and state['failures'] == 2
    assert 'private-provider-token' not in str(router.fetch().warnings)
    now[0] = 11.0
    primary_ok[0] = True
    assert router.fetch().value == 101
    assert router.health()['providers'][0]['status'] == 'CLOSED'


def test_router_marks_slow_success_without_changing_provenance():
    now = [0.0]

    def clock():
        return now[0]

    def slow_provider():
        now[0] += 3.0
        return ProvenancedValue(value=12)

    router = SourceRouter(slow_provider_ms=100, clock=clock)
    router.register(SOURCE_IBKR, MODE_LIVE, slow_provider)
    out = router.fetch()
    assert out.source == SOURCE_IBKR and out.source_mode == MODE_LIVE
    assert any('latence_source_elevee' in warning for warning in out.warnings)
    assert router.health()['providers'][0]['slow_calls'] == 1
