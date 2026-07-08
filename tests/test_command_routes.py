"""
tests/test_command_routes.py — Command Center en Blueprint (Ch. II).

Le régime final, la décision du jour, les alertes et le portefeuille sur
capital, testés sur un état de scan contrôlé. Lecture seule — la réponse ne
contient jamais d'ordre, seulement une analyse.
"""

import copy

import pytest
from flask import Flask

from vertex.app.routes import command
from vertex.app.state import scan_state


@pytest.fixture()
def client():
    app = Flask(__name__)
    app.register_blueprint(command.bp)
    saved = copy.deepcopy(scan_state)
    yield app.test_client()
    scan_state.clear()
    scan_state.update(saved)


def _set_market(roro='RISK-ON', regime='UP', vix=15):
    scan_state['market_ctx'] = {'roro': roro, 'spy_regime': regime, 'vix': vix,
                                'vix_band': 'calme', 'breadth': {'above50': 60}}


# ─── /api/command ───

def test_command_risk_off_goes_defensive(client):
    _set_market(roro='RISK-OFF')
    j = client.get('/api/command').get_json()
    assert 'RISK-OFF' in j['regime']['label']
    assert j['decision']['action'] == 'RÉDUIRE / DÉFENSIF'
    assert any(a[1] == 'RISK-OFF' for a in j['alerts'])


def test_command_chop_means_patience(client):
    _set_market(roro='RISK-ON', regime='CHOP')
    j = client.get('/api/command').get_json()
    assert j['regime']['label'].endswith('NEUTRE')
    assert j['decision']['action'] == 'RÉDUIRE / DÉFENSIF'
    assert any(a[1] == 'RANGE' for a in j['alerts'])


def test_command_high_vix_raises_alert(client):
    _set_market(vix=28)
    j = client.get('/api/command').get_json()
    assert any(a[1] == 'VOLATILITÉ' for a in j['alerts'])


def test_command_top_stocks_only_actionable(client):
    _set_market()
    scan_state['committee'] = {'decisions': [
        {'symbol': 'AAA', 'verdict': 'ACHETER', 'color': '#0f0', 'conviction': 80,
         'price': 10, 'note': 'ok', 'plan': {'rr': 2.5}},
        {'symbol': 'BBB', 'verdict': 'ÉVITER', 'color': '#f00', 'conviction': 20,
         'price': 5, 'note': 'non'},
    ], 'counts': {'ACHETER': 1}}
    j = client.get('/api/command').get_json()
    syms = [s['symbol'] for s in j['top_stocks']]
    assert syms == ['AAA']
    assert j['counts'] == {'ACHETER': 1}


def test_command_never_contains_orders(client):
    _set_market()
    j = client.get('/api/command').get_json()
    flat = str(j).lower()
    for forbidden in ('placeorder', 'order_id', 'submit_order'):
        assert forbidden not in flat


# ─── /api/portefeuille ───

def test_portefeuille_empty_without_rows(client):
    scan_state['rows'] = []
    assert client.get('/api/portefeuille').get_json() == {}


def test_portefeuille_capital_is_clamped(client, monkeypatch):
    scan_state['rows'] = [{'symbol': 'AAA'}]
    seen = {}

    def fake_build(rows, detail, market=None, capital=None):
        seen['capital'] = capital
        return {'capital': capital}
    monkeypatch.setattr(command.strategy, 'build_portfolio', fake_build)
    client.get('/api/portefeuille?capital=999999999')
    assert seen['capital'] == command.CAPITAL_MAX
    client.get('/api/portefeuille?capital=12')
    assert seen['capital'] == command.CAPITAL_MIN
    client.get('/api/portefeuille?capital=pas-un-nombre')
    assert seen['capital'] == command.CAPITAL_DEFAULT


def test_portefeuille_engine_error_is_reported(client, monkeypatch):
    scan_state['rows'] = [{'symbol': 'AAA'}]

    def boom(*a, **k):
        raise ValueError('cassé')
    monkeypatch.setattr(command.strategy, 'build_portfolio', boom)
    j = client.get('/api/portefeuille').get_json()
    assert j['error'] == 'ValueError: cassé'


# ─── Intégration monolithe ───

def test_terminal_registers_command_blueprint():
    import terminal
    rules = {r.rule for r in terminal.app.url_map.iter_rules()}
    assert '/api/command' in rules and '/api/portefeuille' in rules
