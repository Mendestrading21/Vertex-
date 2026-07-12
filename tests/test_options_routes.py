"""Tests §18 — routes Options Intelligence + garde-fous lecture seule.

Vérifie que les routes rendent le contrat canonique d'interprétation, que la
page /options existe et reste dans les huit espaces (nav actif = Opportunités),
et qu'aucun module ajouté n'expose de chemin d'ordre.
"""
import os
import re

import pytest

from vertex.visualization.schemas import is_valid_interpretation


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def test_options_overview_returns_canonical_interpretation(client):
    r = client.get('/api/options/overview')
    assert r.status_code == 200
    d = r.get_json()
    assert 'counters' in d and 'interpretation' in d
    assert is_valid_interpretation(d['interpretation'])


def test_options_volatility_route(client):
    r = client.get('/api/options/volatility/AAPL')
    assert r.status_code == 200
    d = r.get_json()
    assert d['symbol'] == 'AAPL'
    assert is_valid_interpretation(d['interpretation'])


def test_options_event_risk_route(client):
    r = client.get('/api/options/event-risk/AAPL')
    assert r.status_code == 200
    assert is_valid_interpretation(r.get_json()['interpretation'])


def test_options_environment_route(client):
    r = client.get('/api/options/environment')
    assert r.status_code == 200
    d = r.get_json()
    assert 'score' in d and 'dimensions' in d
    assert is_valid_interpretation(d['interpretation'])


def test_options_overview_includes_environment_and_pulses(client):
    d = client.get('/api/options/overview').get_json()
    assert 'environment' in d and 'option_pulse' in d and 'volatility_pulse' in d


def test_options_scenarios_route(client):
    r = client.get('/api/options/scenarios/AAPL')
    assert r.status_code == 200
    d = r.get_json()
    assert 'empty' in d
    # présent ou honnêtement vide (jamais une exception 500)
    if not d['empty']:
        assert 'sim' in d and 'contract' in d


def test_options_scenarios_subview_page(client):
    assert client.get('/options?view=scenarios').status_code == 200


def test_options_vol_charts_route(client):
    r = client.get('/api/options/vol-charts/AAPL')
    assert r.status_code == 200
    d = r.get_json()
    assert d['symbol'] == 'AAPL'
    for k in ('term_structure', 'expected_move_cone', 'oi_by_strike', 'iv_smile', 'interpretation'):
        assert k in d


def test_chart_interpretation_contract_route(client):
    r = client.get('/api/charts/options.overview_mix/interpretation')
    assert r.status_code == 200
    assert is_valid_interpretation(r.get_json())


def test_chart_interpretation_unknown_chart_is_honest(client):
    r = client.get('/api/charts/nope.unknown/interpretation')
    assert r.status_code == 200
    d = r.get_json()
    assert d['status'] == 'INCONNU'


def test_options_page_renders_and_stays_eight_spaces(client):
    r = client.get('/options')
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert 'Options Intelligence' in html
    # reste un approfondissement d'Opportunités : le nav marque Opportunités actif
    assert 'data-nav-id="opportunities"' in html
    # exactement huit espaces dans la nav principale
    assert len(re.findall(r'class="vx-nav-item"', html)) == 8


def test_options_page_subviews(client):
    for view in ('overview', 'volatility', 'radar', 'events'):
        r = client.get('/options?view=' + view)
        assert r.status_code == 200


# ─────────────────────────────────────────────── invariant lecture seule
_ORDER_WORDS = (
    'place_order', 'submit_order', 'transmit_order', 'modify_order',
    'cancel_order', 'exercise_option', 'close_position', 'auto_close',
    'auto_reduce', 'auto_rebalance', 'transfer_cash', 'withdraw_cash',
    'auto_execute', 'one_click_trade',
)

_NEW_FILES = (
    'vertex/visualization/schemas.py',
    'vertex/visualization/interpretation.py' if os.path.exists(
        'vertex/visualization/interpretation.py') else 'vertex/visualization/__init__.py',
    'vertex/options/volatility.py',
    'vertex/options/expected_move.py',
    'vertex/options/event_risk.py',
    'vertex/options/overview.py',
    'vertex/options/interpretation.py',
    'vertex/options/environment.py',
    'vertex/options/pulse.py',
    'vertex/options/vol_charts.py',
    'vertex/visualization/palette.py',
    'vertex/visualization/chart_spec.py',
    'vertex/app/routes/options_intel_api.py',
    'vertex/ui/pages/options_intel_page.py',
    'vertex/static/vertex/js/pages/options-intel.js',
)


def test_no_order_execution_path_in_new_modules():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    call_or_def = re.compile(
        r'(?:\.|\bdef\s+|\bfunction\s+)(' + '|'.join(_ORDER_WORDS) + r')\s*\(')
    for rel in _NEW_FILES:
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8') as fh:
            src = fh.read()
        m = call_or_def.search(src)
        assert not m, '%s : chemin d\'ordre interdit détecté (%s)' % (rel, m and m.group(1))
