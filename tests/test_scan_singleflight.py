import copy

import terminal


def test_scan_skips_concurrent_download_and_preserves_last_state(monkeypatch):
    saved = copy.deepcopy(terminal.scan_state)
    called = {'download': 0}
    try:
        terminal.scan_state.update({'rows': [{'sym': 'NVDA'}], 'error': None, 'scan_skip_count': 0})

        def forbidden_download(_tickers):
            called['download'] += 1
            raise AssertionError('un second scan ne doit pas télécharger')

        monkeypatch.setattr(terminal, '_download_universe', forbidden_download)
        assert terminal._SCAN_LOCK.acquire(blocking=False)
        try:
            assert terminal.scan() is False
        finally:
            terminal._SCAN_LOCK.release()
        assert called['download'] == 0
        assert terminal.scan_state['rows'] == [{'sym': 'NVDA'}]
        assert terminal.scan_state['scan_status'] == 'RUNNING'
        assert terminal.scan_state['scan_skip_count'] == 1
    finally:
        terminal.scan_state.clear()
        terminal.scan_state.update(saved)
