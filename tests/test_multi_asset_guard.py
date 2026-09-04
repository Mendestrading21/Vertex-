from flask import Flask

from vertex.app.routes import analysis_api
from vertex.engines import multi_asset_guard


def test_multi_asset_guard_requests_review_for_unknown_asset_and_partial_portfolio():
    out = multi_asset_guard.build(
        {'asset_class': 'UNKNOWN'}, {'available': False}, {},
        {'asset_mix': {'UNCLASSIFIED': {'positions': 2}}})
    assert out['status'] == 'REVIEW_REQUIRED'
    assert {issue['id'] for issue in out['issues']} == {
        'ASSET_TYPE_UNPROVEN', 'PORTFOLIO_ASSET_TYPES_PARTIAL'}
    assert out['does_not_change_verdict'] is True


def test_multi_asset_guard_identifies_partial_option_contract_evidence():
    out = multi_asset_guard.build(
        {'asset_class': 'ETF', 'sector_proxy': 'Semiconducteurs'}, {'available': True},
        {'available': True, 'best': {'mandate': {'oi_ok': True, 'spread_ok': None}}}, {})
    assert out['status'] == 'REVIEW_REQUIRED'
    assert out['issues'][0]['id'] == 'OPTION_CONTRACT_EVIDENCE_PARTIAL'


def test_multi_asset_guard_marks_truncated_option_board_for_review():
    out = multi_asset_guard.build(
        {'asset_class': 'EQUITY'}, {'available': True},
        {'available': True, 'input_truncated': True, 'input_limit': 5000, 'best': {}}, {})
    assert out['status'] == 'REVIEW_REQUIRED'
    assert out['issues'][0]['id'] == 'OPTION_BOARD_TRUNCATED'


def test_analysis_api_exposes_multi_asset_contract_without_changing_decision(monkeypatch):
    app = Flask(__name__)
    app.register_blueprint(analysis_api.bp)
    state = {
        'detail': {'NVDA': {'symbol': 'NVDA', 'price': 100, 'score': 72, 'verdict': 'ACHETER',
                            'trend': 80, 'rsi': 55, 'regime': 'TREND', 'setup_quality': 70,
                            'atr_pct': 2, 'confidence': 62,
                            'plan': {'entry': 100, 'stop': 94, 'tp1': 106, 'tp2': 112,
                                     'tp3': 118, 'rr': 3, 'rr_res': 3}}},
        'rows': [{'symbol': 'NVDA'}],
        'sectors': [{'sector': 'Semiconducteurs', 'avg_score': 68, 'pct_buy': 50,
                     'risk_band': 'High', 'n': 1, 'leader': {'symbol': 'NVDA'},
                     'members': [{'symbol': 'NVDA'}]}],
        'options_board': [], 'market_ctx': {},
    }
    monkeypatch.setattr(analysis_api, 'scan_state', state)
    response = app.test_client().get('/api/skyler/NVDA')
    assert response.status_code == 200
    out = response.get_json()['decision']
    assert out['instrument_profile']['asset_class'] == 'EQUITY'
    assert out['sector_coherence']['available'] is True
    assert out['multi_asset_guard']['does_not_change_verdict'] is True
