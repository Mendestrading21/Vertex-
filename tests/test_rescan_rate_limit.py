"""Tests d’intégration du déclencheur de rescan global, sans identité client."""

import terminal


def _reset_rescan(monkeypatch, now=1_000.0):
    monkeypatch.setattr(terminal, 'RESCAN_COOLDOWN_SEC', 30)
    monkeypatch.setattr(terminal, '_last_rescan_ts', 0.0)
    monkeypatch.setattr(terminal.time, 'monotonic', lambda: now)
    terminal._rescan_evt.clear()


def test_rescan_first_request_is_queued_and_preserves_market_state(monkeypatch):
    _reset_rescan(monkeypatch)
    sentinel = {'source': 'cached', 'rows': [{'symbol': 'AAA'}], 'scan_status': 'IDLE'}
    saved = dict(terminal.scan_state)
    terminal.scan_state.clear()
    terminal.scan_state.update(sentinel)
    try:
        response = terminal.app.test_client().post('/api/rescan')
        payload = response.get_json()
        assert response.status_code == 200
        assert payload['ok'] is True
        assert payload['status'] == 'rescan_queued'
        assert payload['universe'] == len(terminal.UNIVERSE)
        assert terminal._rescan_evt.is_set()
        assert terminal.scan_state == sentinel
    finally:
        terminal.scan_state.clear()
        terminal.scan_state.update(saved)


def test_rescan_rapid_second_request_is_rate_limited_without_identity(monkeypatch):
    _reset_rescan(monkeypatch)
    client = terminal.app.test_client()
    assert client.get('/api/rescan').status_code == 200

    response = client.post('/api/rescan')
    payload = response.get_json()

    assert response.status_code == 429
    assert payload == {'ok': False, 'error': 'rescan_rate_limited', 'retry_after': 30}
    assert response.headers['Retry-After'] == '30'
    flat_payload = str(payload).lower()
    for forbidden in ('ip', 'address', 'client', 'requester', 'identity', 'token'):
        assert forbidden not in flat_payload


def test_scan_endpoint_exposes_only_global_rescan_cooldown(monkeypatch):
    _reset_rescan(monkeypatch)
    client = terminal.app.test_client()
    assert client.post('/api/rescan').status_code == 200

    scan_payload = client.get('/scan').get_json()
    assert scan_payload['rescan_cooldown_remaining'] == 30
    assert 'ip' not in scan_payload
    assert 'requester' not in scan_payload

