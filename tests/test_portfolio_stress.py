"""tests/test_portfolio_stress.py — stress-scénarios du book : maths exactes + honnêteté."""
from vertex.engines import portfolio_stress as ps


def _pos():
    return [
        {'sym': 'AAPL', 'type': 'STK', 'qty': 10, 'cost': 1500},
        {'sym': 'MSFT', 'type': 'STK', 'qty': 5, 'cost': 2000},
        {'sym': 'NVDA', 'type': 'CALL', 'qty': 2, 'cost': 800, 'strike': 120},   # option → exclue
        {'sym': 'ZZZZ', 'type': 'STK', 'qty': 3, 'cost': 300},                    # sans prix → exclue
    ]


def _prices():
    return {'AAPL': 200.0, 'MSFT': 400.0}


def test_stress_math_exact():
    d = ps.build(_pos(), _prices())
    assert d['empty'] is False
    # valeur stressée = 10*200 + 5*400 = 4000
    assert d['stressed_value'] == 4000.0
    sc5 = next(s for s in d['scenarios'] if s['shock_pct'] == -5.0)
    assert sc5['impact'] == -200.0                       # 4000 × −5 %
    assert sc5['value_after'] == 3800.0
    # pire contributeur du choc −5 % : MSFT (2000×−5% = −100 > AAPL −100 ? égal…)
    imps = {r['sym']: r['impact'] for r in sc5['by_position']}
    assert imps == {'AAPL': -100.0, 'MSFT': -100.0}


def test_options_and_unpriced_excluded_honestly():
    d = ps.build(_pos(), _prices())
    reasons = {e['sym']: e['reason'] for e in d['excluded']}
    assert 'NVDA' in reasons and 'IBKR' in reasons['NVDA']       # option jamais estimée
    assert 'ZZZZ' in reasons and 'prix réel' in reasons['ZZZZ']
    # couverture = 4000 / (4000 + 800 + 300)
    assert d['coverage_pct'] == round(100 * 4000 / 5100)


def test_narrative_states_assumption_not_advice():
    d = ps.build(_pos(), _prices())
    assert 'beta 1' in d['narrative']
    assert 'pas une prévision' in d['narrative']


def test_beta_assumptions_expose_declared_and_defaulted_coverage():
    from vertex.portfolio.models import Position, PortfolioSnapshot
    snapshot = PortfolioSnapshot(positions=[Position('AAA', 1, last_price=100, beta=1.2),
                                            Position('BBB', 1, last_price=100)])
    from vertex.portfolio.stress_tests import run_stress_tests
    out = run_stress_tests(snapshot, type('Profile', (), {'portfolio_max_drawdown_pct': -25})())
    assert out['beta_assumptions']['declared_symbols'] == ['AAA']
    assert out['beta_assumptions']['defaulted_symbols'] == ['BBB']
    assert out['beta_assumptions']['declared_weight_pct'] == 50.0
    assert out['beta_assumptions']['read_only'] is True


def test_no_stock_positions_is_honest():
    d = ps.build([{'sym': 'NVDA', 'type': 'CALL', 'qty': 2, 'cost': 800}], {})
    assert d['empty'] is True
    assert d['reason'] and 'IBKR' in d['reason']


def test_empty_book():
    d = ps.build([], {})
    assert d['empty'] is True and d['excluded'] == []


def test_stress_route_reads_desk_and_scan(tmp_path, monkeypatch):
    import json
    import terminal
    from vertex.services import persist
    from vertex.app.state import scan_state
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    persist.save_json('desk_data.json', {'ts': 1, 'data': {'myTrades': json.dumps([
        {'id': 1, 'sym': 'AAPL', 'type': 'STK', 'qty': 10, 'cost': 1500}])}})
    scan_state.setdefault('detail', {})['AAPL'] = {'price': 200.0}
    client = terminal.app.test_client()
    d = client.get('/api/portfolio/stress').get_json()
    assert d['empty'] is False
    assert d['stressed_value'] == 2000.0
    sc = next(s for s in d['scenarios'] if s['shock_pct'] == -5.0)
    assert sc['impact'] == -100.0


def test_risk_view_mentions_stress():
    import terminal
    body = terminal.app.test_client().get('/portfolio?view=risk').get_data(as_text=True)
    assert 'renderStress' in body                     # loader câblé dans la vue Risque
