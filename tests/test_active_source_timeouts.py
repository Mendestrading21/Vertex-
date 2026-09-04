import terminal


def test_yfinance_download_uses_explicit_timeout(monkeypatch):
    seen = {}
    monkeypatch.setitem(terminal.scan_state, 'source', terminal.scan_state.get('source'))

    class Empty:
        def __len__(self):
            return 0

    def fake_download(*args, **kwargs):
        seen.update(kwargs)
        return Empty()

    monkeypatch.setattr(terminal.yf, 'download', fake_download)
    monkeypatch.setattr(terminal, '_stooq_download', lambda tickers: {})
    terminal._download_universe(['AAA'], chunk=1)
    assert seen['timeout'] == terminal.YFINANCE_BATCH_TIMEOUT_SECONDS
    assert terminal._SOURCE_BUDGET_STATE['yfinance'] == 'UNAVAILABLE'


def test_stooq_request_uses_explicit_timeout(monkeypatch):
    seen = {}

    class Response:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self):
            return b'No data'

    def fake_open(request, timeout):
        seen['timeout'] = timeout
        return Response()

    import urllib.request
    monkeypatch.setattr(urllib.request, 'urlopen', fake_open)
    _, frame = terminal._stooq_one('AAA')
    assert frame is None
    assert seen['timeout'] == terminal.STOOQ_REQUEST_TIMEOUT_SECONDS
