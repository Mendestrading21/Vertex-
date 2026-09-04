from vertex.services import request_metrics as metrics


def test_metrics_are_bounded_and_exclude_paths_and_payloads():
    metrics.reset_for_test()
    metrics.record('analysis_api.api_skyler', 200, 12.3)
    metrics.record('analysis_api.api_skyler', 503, 41.2)
    out = metrics.summary()
    row = out['endpoints']['analysis_api.api_skyler']
    assert out['read_only'] is True
    assert row['count'] == 2 and row['error_count'] == 1
    assert row['max_ms'] == 41.2
    assert 'path' not in row and 'payload' not in row


def test_metrics_keep_only_bounded_recent_samples():
    metrics.reset_for_test()
    for i in range(metrics.MAX_SAMPLES + 8):
        metrics.record('test.endpoint', 200, i)
    out = metrics.summary()
    assert out['sample_count'] == metrics.MAX_SAMPLES
    assert out['endpoints']['test.endpoint']['count'] == metrics.MAX_SAMPLES
