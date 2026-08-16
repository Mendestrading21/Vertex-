import copy

import terminal


def test_yfinance_timeout_uses_stooq_fallback(monkeypatch):
    monkeypatch.setitem(terminal.scan_state, 'source', terminal.scan_state.get('source'))
    monkeypatch.setattr(terminal.yf, 'download',
                        lambda *args, **kwargs: (_ for _ in ()).throw(TimeoutError('private-yahoo-timeout')))
    monkeypatch.setattr(terminal, '_stooq_download', lambda tickers: {'SPY': object()})
    monkeypatch.setattr(terminal.time, 'sleep', lambda _seconds: None)
    out = terminal._download_universe(['SPY'], chunk=1)
    assert out == {'SPY': out['SPY']}
    assert terminal.scan_state['source'] == 'stooq'
    assert terminal._SOURCE_BUDGET_STATE['yfinance'] == 'UNAVAILABLE'
    assert 'private-yahoo-timeout' not in str(terminal.scan_state)


def test_scan_enters_safe_degraded_state_when_all_market_data_missing(monkeypatch):
    saved = copy.deepcopy(terminal.scan_state)
    try:
        monkeypatch.setattr(terminal, 'DEMO_MODE', False)
        monkeypatch.setattr(terminal, '_download_universe', lambda _tickers: {})
        terminal.scan()
        assert terminal.scan_state['error'] == 'market_data_unavailable'
        assert terminal.scan_state['source_health'] == {
            'scan': 'DEGRADED', 'market': 'UNAVAILABLE',
            'options': 'NOT_COLLECTED', 'fundamentals': 'NOT_COLLECTED',
        }
        assert 'Exception' not in str(terminal.scan_state['error'])
    finally:
        terminal.scan_state.clear()
        terminal.scan_state.update(saved)
