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


def test_command_exposes_unavailable_portfolio_controls_without_changing_decision(client, monkeypatch):
    _set_market()
    baseline = client.get('/api/command').get_json()['decision']

    def _unavailable(*args, **kwargs):
        raise RuntimeError('interne')

    monkeypatch.setattr(command.portfolio_risk, 'build', _unavailable)
    monkeypatch.setattr(command.validator, 'build', _unavailable)
    j = client.get('/api/command').get_json()
    assert j['decision'] == baseline
    assert j['risk'] is None and j['validation'] is None
    assert j['controls_availability'] == {
        'risk': {'available': False, 'status': 'PORTFOLIO_RISK_UNAVAILABLE',
                 'read_only': True, 'reason': 'contrôle de risque portefeuille indisponible'},
        'validation': {'available': False, 'status': 'PORTFOLIO_VALIDATION_UNAVAILABLE',
                       'read_only': True, 'reason': 'validation portefeuille indisponible'},
        'does_not_change_decision': True,
        'read_only': True,
    }


# ─── /api/portefeuille ───

def test_portefeuille_empty_without_rows(client):
    scan_state['rows'] = []
    assert client.get('/api/portefeuille').get_json() == {}


def test_le_double_de_build_portfolio_SUIT_la_vraie_signature():
    """Un double qui ne suit plus la signature reelle transforme un changement
    d'API en reponse vide : la route attrape `Exception` et rend `{}`. Le banc
    d'a cote echouait alors sur un `KeyError`, sans dire pourquoi.

    Ce temoin fait echouer le double AVANT, et avec le bon message.
    """
    import inspect
    from vertex.strategy import legacy_adapter
    attendus = set(inspect.signature(legacy_adapter.build_portfolio).parameters)
    assert 'board' in attendus


def test_portefeuille_capital_is_clamped(client, monkeypatch):
    scan_state['rows'] = [{'symbol': 'AAA'}]
    seen = {}

    #  `**extra` : la route passe desormais `board=` (D-107). Sans lui, l'appel
    #  levait, et le `except Exception` de la route rendait `{}` — le banc
    #  echouait sur un KeyError au lieu de dire ce qui s'etait passe. Le double
    #  doit suivre la signature reelle, et le banc suivant l'y oblige.
    def fake_build(rows, detail, market=None, capital=None, **extra):
        seen['capital'] = capital
        seen['extra'] = extra
        return {'capital': capital}
    monkeypatch.setattr(command.strategy, 'build_portfolio', fake_build)
    client.get('/api/portefeuille?capital=999999999')
    assert seen['capital'] == command.CAPITAL_MAX
    assert 'board' in seen['extra'], 'la route doit passer le board (D-107)'
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
    assert j['error'] == 'portfolio_analysis_unavailable'


# ─── Intégration monolithe ───

def test_terminal_registers_command_blueprint():
    import terminal
    rules = {r.rule for r in terminal.app.url_map.iter_rules()}
    assert '/api/command' in rules and '/api/portefeuille' in rules
