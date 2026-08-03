"""tests/test_gamma_surveillance.py — surveillance gamma des positions (descriptive)."""
import json

import pytest

import terminal
from vertex.app.state import scan_state
from vertex.services import persist


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _seed(client, spot):
    """Position déclarée MSFT + board dont le mur put est à 430 et la bascule calculable."""
    persist.save_json('desk_data.json', {'ts': 1, 'data': {'myTrades': json.dumps([
        {'id': 1, 'type': 'STK', 'sym': 'MSFT', 'qty': 10, 'cost': 4000,
         'added': '2026-07-01', 'entrySnap': {}}])}})
    scan_state['options_board'] = [
        {'sym': 'MSFT', 'type': 'PUT', 'strike': 430, 'gamma': 0.05, 'oi': 4000, 'spot': spot},
        {'sym': 'MSFT', 'type': 'CALL', 'strike': 470, 'gamma': 0.02, 'oi': 1000, 'spot': spot},
    ]
    scan_state.setdefault('detail', {})['MSFT'] = {'price': spot}


def test_support_break_detected(client):
    _seed(client, spot=425)                      # spot SOUS le mur put (430)
    try:
        d = client.get('/api/positions/alerts').get_json()
        types = [g['type'] for g in d.get('gamma') or []]
        assert 'GAMMA_SUPPORT_BREAK' in types
        ev = next(g for g in d['gamma'] if g['type'] == 'GAMMA_SUPPORT_BREAK')
        assert ev['symbol'] == 'MSFT' and ev['put_wall'] == 430
        assert 'aucun ordre' not in ev['detail']  # le détail décrit, la bannière porte l'avertissement
    finally:
        scan_state['options_board'] = []


def test_no_event_when_above_walls(client):
    _seed(client, spot=460)                      # au-dessus du mur put ET de la bascule
    try:
        d = client.get('/api/positions/alerts').get_json()
        types = [g['type'] for g in d.get('gamma') or []]
        assert 'GAMMA_SUPPORT_BREAK' not in types
    finally:
        scan_state['options_board'] = []


def test_empty_board_is_honest(client):
    persist.save_json('desk_data.json', {'ts': 1, 'data': {'myTrades': json.dumps([
        {'id': 1, 'type': 'STK', 'sym': 'MSFT', 'qty': 10, 'cost': 4000,
         'added': '2026-07-01', 'entrySnap': {}}])}})
    scan_state['options_board'] = []
    d = client.get('/api/positions/alerts').get_json()
    assert d.get('gamma') == []


def test_pin_risk_detected_near_max_pain_short_dte(client):
    """Spot collé au max pain (≤1,5 %) et échéance ≤7 j → GAMMA_PIN_RISK."""
    persist.save_json('desk_data.json', {'ts': 1, 'data': {'myTrades': json.dumps([
        {'id': 1, 'type': 'STK', 'sym': 'MSFT', 'qty': 10, 'cost': 4000,
         'added': '2026-07-01', 'entrySnap': {}}])}})
    scan_state['options_board'] = [
        # max pain sera 450 (grille), spot 451 → 0,22 % ; dte 3 → pin risk
        {'sym': 'MSFT', 'type': 'CALL', 'strike': 450, 'gamma': 0.05, 'oi': 3000,
         'spot': 451, 'dte': 3},
        {'sym': 'MSFT', 'type': 'PUT', 'strike': 450, 'gamma': 0.05, 'oi': 3000,
         'spot': 451, 'dte': 3},
    ]
    scan_state.setdefault('detail', {})['MSFT'] = {'price': 451}
    try:
        d = client.get('/api/positions/alerts').get_json()
        types = [g['type'] for g in d.get('gamma') or []]
        assert 'GAMMA_PIN_RISK' in types
        ev = next(g for g in d['gamma'] if g['type'] == 'GAMMA_PIN_RISK')
        assert ev['max_pain'] == 450 and ev['min_dte'] == 3
    finally:
        scan_state['options_board'] = []


def test_no_pin_risk_when_dte_far(client):
    persist.save_json('desk_data.json', {'ts': 1, 'data': {'myTrades': json.dumps([
        {'id': 1, 'type': 'STK', 'sym': 'MSFT', 'qty': 10, 'cost': 4000,
         'added': '2026-07-01', 'entrySnap': {}}])}})
    scan_state['options_board'] = [
        {'sym': 'MSFT', 'type': 'CALL', 'strike': 450, 'gamma': 0.05, 'oi': 3000,
         'spot': 451, 'dte': 60},          # échéance lointaine → pas d'épinglage
    ]
    scan_state.setdefault('detail', {})['MSFT'] = {'price': 451}
    try:
        d = client.get('/api/positions/alerts').get_json()
        types = [g['type'] for g in d.get('gamma') or []]
        assert 'GAMMA_PIN_RISK' not in types
    finally:
        scan_state['options_board'] = []
