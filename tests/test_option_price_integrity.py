from vertex.options import legacy_engine as engine
import pandas as pd
from vertex.data_sources.rates import RateCurve


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


def test_option_rate_sensitivity_requires_non_fallback_curve():
    curve_quote = RateCurve({30: 0.04, 365: 0.045}, source='TEST_CURVE',
                            timestamp='2026-08-17T10:00:00Z').rate_for_tenor(180)
    measured = engine.option_rate_sensitivity(100.0, 100.0, 0.5, 0.2, True, curve_quote)
    assert measured['available'] is True
    assert measured['rate_provenance']['source'] == 'TEST_CURVE'
    assert measured['sensitivity']['sensitivity_per_bump'] is not None
    fallback = engine.option_rate_sensitivity(100.0, 100.0, 0.5, 0.2, True,
                                               RateCurve().rate_for_tenor(180))
    assert fallback['available'] is False
    assert 'repli' in fallback['reason']


def test_contract_liquidity_coverage_distinguishes_zero_from_missing(monkeypatch):
    class _Ticker:
        options = ['2027-02-20']
        def option_chain(self, _expiry):
            return type('Chain', (), {'calls': pd.DataFrame([{
                'strike': 100.0, 'impliedVolatility': 0.2, 'openInterest': None,
                'volume': 0, 'bid': None, 'ask': None, 'lastPrice': 5.0,
                'lastTradeDate': None,
            }])})()
    monkeypatch.setattr(engine.yf, 'Ticker', lambda _symbol: _Ticker())
    monkeypatch.setattr(engine, '_pick_expiries', lambda *_args, **_kwargs: [('2027-02-20', 180, 'long')])
    contracts = engine.best_for_symbol('TEST', 100.0, 112.0, 'call', buckets=('long',))
    coverage = contracts[0]['liquidity_coverage']
    assert coverage['bid_present'] is False and coverage['ask_present'] is False
    assert coverage['volume_present'] is True and coverage['open_interest_present'] is False
    assert coverage['reported_fields'] == 1 and coverage['quoted_bid_ask'] is False
    assert contracts[0]['quote_timestamp_coverage']['status'] == 'TIMESTAMP_UNAVAILABLE'


def test_contract_quote_timestamp_is_exposed_without_age_derivation(monkeypatch):
    class _Ticker:
        options = ['2027-02-20']
        def option_chain(self, _expiry):
            return type('Chain', (), {'calls': pd.DataFrame([{
                'strike': 100.0, 'impliedVolatility': 0.2, 'openInterest': 1000,
                'volume': 10, 'bid': 4.9, 'ask': 5.1, 'lastPrice': 5.0,
                'lastTradeDate': '2026-08-17T12:00:00Z',
            }])})()
    monkeypatch.setattr(engine.yf, 'Ticker', lambda _symbol: _Ticker())
    monkeypatch.setattr(engine, '_pick_expiries', lambda *_args, **_kwargs: [('2027-02-20', 180, 'long')])
    contract = engine.best_for_symbol('TEST', 100.0, 112.0, 'call', buckets=('long',))[0]
    timestamp = contract['quote_timestamp_coverage']
    assert timestamp['reported'] is True and timestamp['status'] == 'REPORTED_TIMESTAMP_ONLY'
    assert timestamp['timestamp'] == '2026-08-17T12:00:00Z'


def test_board_coverage_summarizes_contract_metadata_without_reordering():
    contracts = [
        {'liquidity_coverage': {'reported_fields': 4, 'quoted_bid_ask': True},
         'quote_timestamp_coverage': {'reported': True}},
        {'liquidity_coverage': {'reported_fields': 1, 'quoted_bid_ask': False},
         'quote_timestamp_coverage': {'reported': False}},
    ]
    coverage = engine.board_coverage(contracts)
    assert coverage['contract_count'] == 2
    assert coverage['liquidity_fields_complete'] == 1
    assert coverage['quoted_bid_ask'] == 1 and coverage['timestamps_reported'] == 1
    assert coverage['liquidity_fields_complete_pct'] == 50.0
    assert contracts[0]['liquidity_coverage']['reported_fields'] == 4


def test_options_pack_serves_board_coverage_without_mutating_contracts(monkeypatch):
    import terminal
    history = pd.DataFrame({'Close': [100.0 + i * 0.1 for i in range(252)]})
    class _Ticker:
        fast_info = {'lastPrice': 100.0}
        info, calendar, news, options = {}, {}, [], []
        def history(self, **_kwargs): return history
    contract = {'sym': 'TEST', 'suit': 60, 'bucket': 'long', 'pop': 55,
                'danger_n': 1, 'flags': [], 'theta_burn': 0.2, 'em_pct': 5.0}
    monkeypatch.setattr(terminal.yf, 'Ticker', lambda _symbol: _Ticker())
    monkeypatch.setattr(terminal.ai, 'fr_news', lambda _sym, news: (news, None))
    monkeypatch.setattr(terminal.options, 'best_for_symbol', lambda *_args, **_kwargs: {
        'contracts': [contract], 'price_rejections': [], 'price_rejection_count': 0})
    monkeypatch.setattr(terminal.options, 'board_coverage', lambda contracts: {
        'contract_count': len(contracts), 'read_only': True})
    monkeypatch.setattr(terminal.options, 'recommend', lambda contracts: None)
    monkeypatch.setattr(terminal.options, 'recommend_top', lambda contracts, _n: [])
    monkeypatch.setattr(terminal.research, 'chart_read', lambda _detail: '')
    monkeypatch.setattr(terminal.research, 'chart_verdict', lambda _detail: '')
    monkeypatch.setattr(terminal.engine, 'decide', lambda *_args: {})
    monkeypatch.setattr(terminal.ibkr, 'verdict', lambda *_args: {})
    terminal.scan_state.setdefault('detail', {})['TEST'] = {'price': 100.0, 'plan': {}}
    try:
        payload = terminal.options_pack('TEST')
        assert payload['option_board_coverage'] == {'contract_count': 1, 'read_only': True}
        assert payload['contracts'] == [contract]
    finally:
        terminal.scan_state['detail'].pop('TEST', None)
        terminal._OPTALL_CACHE.pop('TEST', None)


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
    #  #779/G1 — `/options/<sym>` est servi par `vertex/app/routes/ticker_api.py`,
    #  qui resout `options_pack` dans SON espace de noms. Patcher celui du
    #  monolithe ne l'atteint plus : la route aurait appele la vraie fonction, et
    #  le test aurait echoue sur une absence de reseau plutot que sur le contrat.
    from vertex.app.routes import ticker_api as _ticker
    rejection = {'price_integrity': {'status': 'PRICE_OUTSIDE_NO_ARBITRAGE'},
                 'derived_metrics_withheld': True}
    monkeypatch.setattr(_ticker, 'options_pack', lambda _sym: {
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
