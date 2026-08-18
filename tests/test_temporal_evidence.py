from vertex.data.temporal_evidence import assess


def test_temporal_evidence_accepts_strict_canonical_series():
    out = assess({'dates': ['2026-01-02', '2026-01-05', '2026-01-06'], 'close': [100, 101, 99]})
    assert out['available'] is True and out['status'] == 'TEMPORAL_EVIDENCE_AVAILABLE'
    assert out['no_interpolation'] is True


def test_temporal_evidence_rejects_unsorted_dates_and_invalid_prices():
    out = assess({'dates': ['2026-01-05', '2026-01-02'], 'close': [100, 101]})
    assert out['available'] is False and out['status'] == 'TEMPORAL_EVIDENCE_REQUIRED'
    out = assess({'dates': ['2026-01-02', '2026-01-05'], 'close': [100, None]})
    assert out['available'] is False and out['read_only'] is True
