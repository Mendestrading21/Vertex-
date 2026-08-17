from vertex.options import legacy_engine as engine
import pandas as pd


def test_call_and_put_non_arbitrage_bounds_are_exposed_read_only():
    call = engine.option_price_integrity(100.0, 95.0, 0.5, 8.0, True)
    put = engine.option_price_integrity(100.0, 105.0, 0.5, 8.0, False)
    assert call['available'] is True and call['status'] == 'OPTION_PRICE_COHERENT'
    assert put['available'] is True and put['read_only'] is True
    assert call['lower_bound'] > 0 and put['upper_bound'] < 105.0


def test_impossible_option_prices_are_rejected_before_iv_solving():
    call = engine.option_price_integrity(100.0, 100.0, 1.0, 101.0, True)
    put = engine.option_price_integrity(100.0, 120.0, 1.0, 1.0, False)
    assert call['status'] == 'PRICE_OUTSIDE_NO_ARBITRAGE'
    assert put['status'] == 'PRICE_OUTSIDE_NO_ARBITRAGE'
    assert engine._iv_from_price(100.0, 100.0, 1.0, 101.0, True) is None
    assert engine._iv_from_price(100.0, 120.0, 1.0, 1.0, False) is None


def test_invalid_inputs_do_not_become_implied_volatility():
    out = engine.option_price_integrity(0.0, 100.0, 1.0, 5.0, True)
    assert out['available'] is False and out['status'] == 'OPTION_INPUT_INSUFFICIENT'


def test_contract_liquidity_coverage_distinguishes_zero_from_missing(monkeypatch):
    class _Ticker:
        options = ['2027-02-20']
        def option_chain(self, _expiry):
            return type('Chain', (), {'calls': pd.DataFrame([{
                'strike': 100.0, 'impliedVolatility': 0.2, 'openInterest': None,
                'volume': 0, 'bid': None, 'ask': None, 'lastPrice': 5.0,
            }])})()
    monkeypatch.setattr(engine.yf, 'Ticker', lambda _symbol: _Ticker())
    monkeypatch.setattr(engine, '_pick_expiries', lambda *_args, **_kwargs: [('2027-02-20', 180, 'long')])
    contracts = engine.best_for_symbol('TEST', 100.0, 112.0, 'call', buckets=('long',))
    coverage = contracts[0]['liquidity_coverage']
    assert coverage['bid_present'] is False and coverage['ask_present'] is False
    assert coverage['volume_present'] is True and coverage['open_interest_present'] is False
    assert coverage['reported_fields'] == 1 and coverage['quoted_bid_ask'] is False


def test_board_screen_exposes_rejected_quote_without_derived_metrics(monkeypatch):
    class _Ticker:
        options = ['2027-02-20']
        def option_chain(self, _expiry):
            return type('Chain', (), {'calls': pd.DataFrame([{
                'strike': 100.0, 'impliedVolatility': 0.2, 'openInterest': 1000,
                'volume': 10, 'bid': 150.0, 'ask': 152.0, 'lastPrice': 151.0,
            }])})()
    monkeypatch.setattr(engine.yf, 'Ticker', lambda _symbol: _Ticker())
    monkeypatch.setattr(engine, '_pick_expiries', lambda *_args, **_kwargs: [('2027-02-20', 180, 'long')])
    screened = engine.best_for_symbol('TEST', 100.0, 112.0, 'call', buckets=('long',),
                                      include_diagnostics=True)
    assert screened['contracts'] == [] and screened['price_rejection_count'] == 1
    rejection = screened['price_rejections'][0]
    assert rejection['price_integrity']['status'] == 'PRICE_OUTSIDE_NO_ARBITRAGE'
    assert rejection['derived_metrics_withheld'] is True
    assert 'iv' not in rejection and 'delta' not in rejection and 'gamma' not in rejection


def test_options_endpoint_serves_structured_price_rejections(monkeypatch):
    import terminal
    rejection = {'price_integrity': {'status': 'PRICE_OUTSIDE_NO_ARBITRAGE'},
                 'derived_metrics_withheld': True}
    monkeypatch.setattr(terminal, 'options_pack', lambda _sym: {
        'sym': _sym, 'contracts': [], 'option_price_rejection_count': 1,
        'option_price_rejections': [rejection], 'error': None})
    payload = terminal.app.test_client().get('/options/TEST').get_json()
    assert payload['option_price_rejection_count'] == 1
    served = payload['option_price_rejections'][0]
    assert served['price_integrity']['status'] == 'PRICE_OUTSIDE_NO_ARBITRAGE'
    assert served['derived_metrics_withheld'] is True
    assert not any(key in served for key in ('iv', 'delta', 'gamma', 'theta', 'probability'))


def test_options_endpoint_builds_and_serves_real_rejection(monkeypatch):
    import terminal
    index = pd.date_range('2025-01-01', periods=252, freq='B')
    history = pd.DataFrame({'Close': [100.0 + i * 0.1 for i in range(252)]}, index=index)
    class _Ticker:
        fast_info = {'lastPrice': 100.0}
        info, calendar, news = {}, {}, []
        options = ['2027-02-20']
        def history(self, **_kwargs): return history
        def option_chain(self, _expiry):
            calls = pd.DataFrame([{'strike': 100.0, 'impliedVolatility': 0.2,
                                  'openInterest': 1000, 'volume': 10,
                                  'bid': 150.0, 'ask': 152.0, 'lastPrice': 151.0}])
            return type('Chain', (), {'calls': calls, 'puts': pd.DataFrame(columns=calls.columns)})()
    monkeypatch.setattr(terminal.yf, 'Ticker', lambda _symbol: _Ticker())
    monkeypatch.setattr(terminal.ai, 'fr_news', lambda _sym, news: (news, None))
    monkeypatch.setattr(terminal.research, 'chart_read', lambda _detail: '')
    monkeypatch.setattr(terminal.research, 'chart_verdict', lambda _detail: '')
    monkeypatch.setattr(terminal.engine, 'decide', lambda *_args: {})
    monkeypatch.setattr(terminal.ibkr, 'verdict', lambda *_args: {})
    terminal.scan_state.setdefault('detail', {})['TEST'] = {'price': 100.0, 'plan': {'tp2': 112.0, 'atr': 2.0}}
    try:
        payload = terminal.app.test_client().get('/options/TEST').get_json()
        assert payload['option_price_rejection_count'] == 1
        rejected = payload['option_price_rejections'][0]
        assert rejected['price_integrity']['status'] == 'PRICE_OUTSIDE_NO_ARBITRAGE'
        assert rejected['derived_metrics_withheld'] is True
        assert not any(k in rejected for k in ('iv', 'delta', 'gamma', 'theta', 'pop'))
    finally:
        terminal.scan_state['detail'].pop('TEST', None)
