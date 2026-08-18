import terminal


def test_terminal_enforces_request_body_limit_before_route_processing():
    limit = terminal.app.config['MAX_CONTENT_LENGTH']
    response = terminal.app.test_client().post(
        '/api/client-log',
        data=b'x' * (limit + 1),
        content_type='application/json',
    )
    assert limit == 2 * 1024 * 1024
    assert response.status_code == 413
