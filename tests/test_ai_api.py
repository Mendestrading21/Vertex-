"""Tests — API du cerveau Claude+web & invariant lecture seule (§28)."""
import glob
import os
import re


def test_enrich_symbols_dedup_and_cap(monkeypatch):
    from vertex.app.routes import ai_api
    from vertex.app import state
    monkeypatch.setitem(state.scan_state, 'rows',
                        [{'symbol': 'ACN'}, {'symbol': 'ABT'}, {'symbol': 'ACN'},
                         {'symbol': 'SPY.X'}])
    syms = ai_api.enrich_symbols()
    assert syms.count('ACN') == 1          # dédupliqué
    assert 'SPY.X' not in syms             # les symboles à point exclus
    assert 'ABT' in syms


def test_ai_status_endpoint_is_honest_without_key():
    import terminal
    client = terminal.app.test_client()
    r = client.get('/api/ai/status')
    assert r.status_code == 200
    data = r.get_json()
    assert 'status' in data and 'health' in data
    # Sans clé configurée dans l'environnement de test : jamais « CONNECTED ».
    if not os.environ.get('ANTHROPIC_API_KEY'):
        assert data['health']['status'] == 'MISSING'


def test_ai_enrichment_endpoint_never_fabricates_without_key():
    import terminal
    client = terminal.app.test_client()
    data = client.get('/api/ai/enrichment').get_json()
    if not os.environ.get('ANTHROPIC_API_KEY'):
        # Aucune cotation estimée ne doit exister sans clé.
        assert data.get('surfaces', {}).get('quotes', {}) in ({}, None)


def test_ai_refresh_endpoint_returns_202():
    import terminal
    client = terminal.app.test_client()
    r = client.post('/api/ai/refresh')
    assert r.status_code == 202
    assert 'accepted' in r.get_json()


def test_no_order_execution_verb_in_ai_package():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    banned = re.compile(r'(?:\.|\bdef\s+)(place_order|placeOrder|submit_order|'
                        r'transmit_order|send_order|execute_trade|cancel_order|'
                        r'modify_order|exercise_option)\s*\(')
    for p in glob.glob(os.path.join(root, 'vertex/ai/*.py')):
        assert not banned.search(open(p, encoding='utf-8').read()), p


def test_web_tool_is_read_only_search():
    """Le seul outil externe du cerveau est la recherche web (lecture)."""
    from vertex.ai import web_provider
    assert web_provider.WEB_TOOL_TYPE.startswith('web_search')
