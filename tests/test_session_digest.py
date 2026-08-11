"""Session d'analyse — gardiens du digest de commandement (P12).

Le digest est un AGRÉGAT en lecture seule de l'état déjà calculé : il ne doit
inventer aucune donnée (absent → None), rester honnête sur son état, et ne jamais
contenir de chemin d'ordre. L'endpoint doit répondre 200 et servir un instantané
peuplé même à froid.
"""
import os

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('DEMO', '1')

import pytest

import terminal
from vertex.engines import session_digest


@pytest.fixture(scope='module')
def client():
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


# ── Builder pur ───────────────────────────────────────────────────────────
def test_empty_state_is_honest_analyzing():
    """Aucune donnée → état 'analyzing', régime/opportunités honnêtement vides."""
    d = session_digest.build({}, {}, demo=True)
    assert d['state'] == 'analyzing'
    assert d['regime']['label'] is None
    assert d['opportunities']['actionable'] == 0
    assert d['catalysts']['next'] is None
    assert d['confidence'] is None
    assert d['generator'] == 'deterministic'
    assert d['demo'] is True


def test_populated_state_reads_engine_output_only():
    """État peuplé : lit régime + verdicts comité + catalyseurs SANS recalcul."""
    import time
    ss = {
        'rows': [{'symbol': 'ACN'}, {'symbol': 'AFL'}],
        'detail': {'ACN': {'x': 1}, 'AFL': {'x': 1}},
        'market_ctx': {'roro': 'RISK-ON', 'spy_regime': 'UP', 'vix': 13.2},
        'committee': {'decisions': [
            {'symbol': 'ACN', 'verdict': 'ACHETER'},
            {'symbol': 'AFL', 'verdict': 'RENFORCER'},
            {'symbol': 'XYZ', 'verdict': 'REFUSER'}]},
        'scan_ts': time.time(),
    }
    d = session_digest.build(ss, {'items': [{'label': 'CPI', 'dte': 3}]}, demo=False)
    assert d['state'] == 'ready'
    assert d['regime']['label'] == 'RISK-ON' and d['regime']['tone'] == 'go'
    assert d['opportunities']['actionable'] == 2          # ACN + AFL (REFUSER exclu)
    assert d['opportunities']['top'] == ['ACN', 'AFL']
    assert d['catalysts']['next'] == {'label': 'CPI', 'dte': 3}
    assert d['confidence'] == 100                          # 2/2 couverts
    assert d['market']['vix'] == 13.2


def test_confidence_is_real_coverage_not_invented():
    """La confiance = couverture RÉELLE (titres avec détail), jamais un chiffre inventé."""
    ss = {'rows': [{'symbol': 'A'}, {'symbol': 'B'}, {'symbol': 'C'}, {'symbol': 'D'}],
          'detail': {'A': {'x': 1}}, 'market_ctx': {'roro': 'RISK-ON'}}
    d = session_digest.build(ss, {}, demo=False)
    assert d['confidence'] == 25                           # 1/4


def test_no_order_path_in_digest():
    """Le digest ne contient aucun verbe d'ordre (invariant READONLY)."""
    import json
    blob = json.dumps(session_digest.build(
        {'rows': [{'symbol': 'A'}], 'detail': {}, 'market_ctx': {'roro': 'RISK-OFF'},
         'committee': {'decisions': []}}, {})).lower()
    for w in ('place_order', 'submit_order', 'transmit', 'placeorder'):
        assert w not in blob


# ── Endpoint ──────────────────────────────────────────────────────────────
def test_endpoint_200_and_shape(client):
    r = client.get('/api/session/digest')
    assert r.status_code == 200
    j = r.get_json()
    assert j['state'] in ('ready', 'restored', 'analyzing')
    for k in ('regime', 'opportunities', 'catalysts', 'market', 'confidence', 'generator'):
        assert k in j


def test_briefing_page_carries_session_section(client):
    """La page Aujourd'hui expose la section Session d'analyse + son loader."""
    html = client.get('/').get_data(as_text=True)
    assert 'vx-session' in html
    assert '/api/session/digest' in html
