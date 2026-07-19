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


# ─────────────────────────────── Analyste IA (§28) : dossier réel, jamais d'ordre
def test_ai_analyst_unknown_symbol_is_honest():
    import terminal
    client = terminal.app.test_client()
    d = client.get('/api/ai/analyst/ZZZZ').get_json()
    assert d['available'] is False           # 200 + état honnête, jamais un faux verdict
    assert 'content' not in d


def test_ai_analyst_fallback_is_deterministic_and_schema_valid(monkeypatch):
    from vertex.app import state
    from vertex.ai.response_validator import validate_analysis
    monkeypatch.setitem(state.scan_state, 'detail', {
        'ACN': {'score': 72, 'rr': 3.0, 'sector': 'Technology', 'price': 200.0,
                'vertex': {'rr': 3.0, 'mc': {}, 'bootstrap': {}, 'kelly': {'pct': 10},
                           'asymmetry': 60, 'ev': 1.2},
                'physics': {'hurst': 0.55}, 'mtf': {'state': 'ALIGNED'}, 'plan': {}}})
    import terminal
    d = terminal.app.test_client().get('/api/ai/analyst/ACN').get_json()
    assert d['available'] is True
    ok, errs = validate_analysis(d['content'])       # le fallback respecte le schéma strict
    assert ok, errs
    for k in ('order', 'orders', 'execute', 'trade_now', 'position_size_final'):
        assert k not in d['content']                 # aucune clé d'ordre, jamais
    if not os.environ.get('ANTHROPIC_API_KEY'):      # sans clé : honnêteté MISSING
        assert d['source'] == 'deterministic-fallback'
        assert d['health']['status'] == 'MISSING'
        assert d['model'] is None


def test_resolve_model_prefers_vertex_then_anthropic(monkeypatch):
    """Une seule source de vérité modèle : VERTEX_AI_MODEL > ANTHROPIC_MODEL > défaut."""
    from vertex.ai import health
    monkeypatch.setenv('VERTEX_AI_MODEL', 'claude-opus-4-8')
    monkeypatch.setenv('ANTHROPIC_MODEL', 'autre')
    assert health.resolve_model() == 'claude-opus-4-8'
    monkeypatch.delenv('VERTEX_AI_MODEL', raising=False)
    assert health.resolve_model() == 'autre'
    monkeypatch.delenv('ANTHROPIC_MODEL', raising=False)
    assert health.resolve_model() == health.DEFAULT_MODEL
