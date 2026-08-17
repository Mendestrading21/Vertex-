from vertex.engines import skyler_journal as journal


def test_calibration_reports_measured_outcome_coverage_without_brier():
    entries = [
        {'symbol': 'AAA', 'decision': 'ATTENDRE', 'as_of': 't1', 'price': 100.0},
        {'symbol': 'BBB', 'decision': 'ATTENDRE', 'as_of': 't2', 'price': None},
    ]
    report = journal.calibration(entries, quotes={'AAA': 110.0})
    assert report['outcomes']['available'] is True
    assert report['outcomes']['measured'] == 1
    assert report['outcomes']['unmeasured'] == 1
    assert report['outcomes']['coverage_pct'] == 50.0
    assert report['brier']['available'] is False
