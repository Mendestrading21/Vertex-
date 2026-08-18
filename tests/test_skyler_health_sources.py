from vertex.app.routes import analysis_api
from vertex.app.state import scan_state


def test_source_health_summary_bounds_states_and_hides_unknown_details():
    summary = analysis_api._source_health_summary({
        'scan': 'degraded', 'market': 'unavailable', 'options': 'NOT_COLLECTED',
        'fundamentals': 'provider-token: secret-value', 'client_ip': '198.51.100.3',
    })
    assert summary['available'] is True
    assert summary['sources'] == {
        'scan': 'DEGRADED', 'market': 'UNAVAILABLE', 'options': 'NOT_COLLECTED',
        'fundamentals': 'UNKNOWN',
    }
    assert 'client_ip' not in summary['sources']
    assert 'secret' not in str(summary).lower()


def test_skyler_health_serves_non_sensitive_source_summary(monkeypatch):
    import terminal
    monkeypatch.setitem(scan_state, 'source_health', {
        'scan': 'DEGRADED', 'market': 'AVAILABLE', 'options': 'NOT_COLLECTED',
        'fundamentals': 'UNAVAILABLE',
    })
    response = terminal.app.test_client().get('/api/skyler/health')
    assert response.status_code == 200
    payload = response.get_json()['source_health']
    assert payload['sources']['market'] == 'AVAILABLE'
    assert payload['counts']['DEGRADED'] == 1
    assert payload['read_only'] is True
