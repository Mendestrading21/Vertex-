from vertex.portfolio.correlation import correlation_matrix


def test_correlation_reports_measured_and_unmeasured_pair_coverage():
    matrix = correlation_matrix({
        'AAA': [0.01 if i % 2 else -0.01 for i in range(31)],
        'BBB': [0.02 if i % 2 else -0.02 for i in range(31)],
        'CCC': [0.03] * 10,
    })
    coverage = matrix['coverage']
    assert coverage['total_pairs'] == 3
    assert coverage['measured_pairs'] == 1
    assert coverage['unmeasured_pairs'] == ['AAA/CCC', 'BBB/CCC']
    assert coverage['coverage_pct'] == 33.3
