"""Routes Strategy OS (§36-37) : hub, décision unique, diagnostics, mode dégradé."""
import pytest
from flask import Flask

from vertex.app.routes import strategy_os_api


@pytest.fixture()
def client():
    app = Flask(__name__)
    scan_state = {
        'source': 'stooq',
        'detail': {
            'NVDA': {'score': 78, 'rr': 2.3, 'rs': 70, 'st_fund': 72,
                     'st_timing': 65, 'ext_atr': 1.0, 'earnings_dte': 20,
                     'plan': {'entry': 490, 'stop': 465, 'tp1': 540},
                     'series': {'close': [400 + i for i in range(60)]}},
        },
        'market': {'regime': 'TREND', 'vix': 15.0, 'breadth': 68, 'risk': 'Risk-On'},
        'rows': [{'symbol': 'NVDA'}],
    }
    app.register_blueprint(strategy_os_api.make_blueprint(scan_state=scan_state))
    # `/strategy-os` etait monte ICI sur le module mort `vertex/ui/strategy_os.py`
    # (supprime au lot 17). En PRODUCTION cette URL est une REDIRECTION vers
    # /intelligence?view=strategy, mesuree au lot 17 : ce montage n'a jamais
    # decrit le produit, il fabriquait une route pour se la tester a soi-meme.
    return app.test_client()


def test_profile_route(client):
    r = client.get('/api/strategy/profile')
    assert r.status_code == 200
    data = r.get_json()
    assert data['display_name'] == 'Stratégie Vertex'
    assert data['strategy_id'].startswith('vertex_strategy_v')


def test_decision_route_uses_executive_engine(client):
    r = client.get('/api/strategy/decision/NVDA')
    data = r.get_json()
    assert data['final_decision'] in ('ACHETER', 'RENFORCER', 'ATTENDRE',
                                      'REDUIRE', 'REFUSER')
    assert data['audit_trail']
    assert set(data['scores']) == {'conviction', 'risk', 'timing', 'asymmetry',
                                   'data_quality'}


def test_decision_route_honest_when_symbol_unknown(client):
    r = client.get('/api/strategy/decision/ZZZZ')
    assert r.status_code == 200
    j = r.get_json()
    assert j['available'] is False
    assert j['final_decision'] == 'ATTENDRE'


def test_regime_route(client):
    data = client.get('/api/market/regime').get_json()
    assert data['regime'] in ('TREND_UP', 'RISK_ON', 'TRANSITION', 'UNKNOWN',
                              'VOLATILITY_COMPRESSION', 'CHOP')
    assert 'adjustments' in data


def test_anomalies_route(client):
    data = client.get('/api/anomalies/NVDA').get_json()
    assert data['symbol'] == 'NVDA'
    assert isinstance(data['anomalies'], list)


def test_team_route_requires_explicit_positions(client):
    usage = client.get('/api/portfolio/team').get_json()
    assert 'positions réelles' in usage['usage'] or 'simulées explicites' in usage['usage']
    r = client.post('/api/portfolio/team', json={
        'positions': [{'symbol': 'NVDA', 'quantity': 10, 'avg_cost': 400,
                       'last_price': 500, 'sector': 'Technologie', 'beta': 1.6}],
        'cash': 5000, 'simulated': True})
    data = r.get_json()
    assert data['risk']['provenance'] == 'SIMULATED'
    assert 'stress' in data and 'guard' in data


def test_diagnostics_and_data_quality(client):
    d = client.get('/api/system/diagnostics').get_json()
    assert 'scan' in d and 'alerts' in d and 'tradingview' in d
    blob = str(d).lower()
    for secret_like in ('anthropic_api_key', 'vertex_secret', 'password'):
        assert secret_like not in blob
    dq = client.get('/api/data-quality').get_json()
    assert dq['total'] == 1 and 'by_quality' in dq


def test_degraded_mode_empty_scan():
    """Sans scan, sans IBKR, sans IA : les routes répondent proprement."""
    app = Flask(__name__)
    app.register_blueprint(strategy_os_api.make_blueprint(scan_state={}))
    c = app.test_client()
    assert c.get('/api/strategy/profile').status_code == 200
    dec = c.get('/api/strategy/decision/NVDA')
    assert dec.status_code == 200 and dec.get_json()['available'] is False
    regime = c.get('/api/market/regime').get_json()
    assert regime['regime'] == 'UNKNOWN'
    assert c.get('/api/system/diagnostics').status_code == 200
    assert c.get('/api/data-quality').get_json()['total'] == 0
