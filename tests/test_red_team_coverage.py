from vertex.engines import red_team


def test_red_team_reports_open_objection_coverage():
    review = red_team.review({'contexts': {}}, {'blocks': {}})
    coverage = review['coverage']
    assert coverage['total_questions'] == 10
    assert coverage['answered'] == review['answered']
    assert coverage['coverage_pct'] < 100.0
    assert coverage['unanswered_ids']
    assert review['complete'] is False
