"""tests/test_pretrade.py — ticket pré-trade : contrôles réels + verdict honnête."""
from vertex.engines import pretrade


def test_favorable_when_all_green():
    d = pretrade.build('AAPL', 1000, verdict='ACHETER', roro='RISK-ON',
                       gex_bias='haussier', gex_regime='stabilisant',
                       earnings_in_days=30,
                       positions=[{'sym': 'MSFT', 'type': 'STK', 'qty': 10, 'cost': 3000}],
                       prices_by_sym={'MSFT': 400.0, 'AAPL': 200.0},
                       plan={'stop': 180.0, 'tp1': 250.0})
    by = {c['key']: c for c in d['checks']}
    assert by['verdict']['status'] == 'ok'
    assert by['regime']['status'] == 'ok'
    # concentration : (0 + 1000) / (4000 + 1000) = 20 % → attention ? non : 20 > 15 → warn
    # → recalibrons : book MSFT = 10×400 = 4000 ; poids AAPL = 1000/5000 = 20 % → WARN
    assert by['concentration']['status'] == 'attention'
    assert d['overall'] in ('FAVORABLE', 'MITIGÉ')      # le warn concentration → MITIGÉ
    assert d['overall'] == 'MITIGÉ'


def test_risk_off_and_committee_against_is_defavorable():
    d = pretrade.build('XYZ', 500, verdict='EVITER', roro='RISK-OFF')
    assert d['overall'] == 'DÉFAVORABLE'
    by = {c['key']: c for c in d['checks']}
    assert by['verdict']['status'] == 'defavorable'
    assert by['regime']['status'] == 'defavorable'


def test_concentration_math_exact():
    """Book 4000 (MSFT réel) + 2000 envisagés sur AAPL → 2000/6000 = 33 % → défavorable."""
    d = pretrade.build('AAPL', 2000, verdict='ACHETER', roro='RISK-ON',
                       positions=[{'sym': 'MSFT', 'type': 'STK', 'qty': 10, 'cost': 3000}],
                       prices_by_sym={'MSFT': 400.0})
    by = {c['key']: c for c in d['checks']}
    assert by['concentration']['status'] == 'defavorable'
    assert '33 %' in by['concentration']['detail']


def test_loser_guard_blocks_adding_to_losing_position():
    """Position AAPL en perte (prix réel 150 < revient 200) → §18 défavorable."""
    d = pretrade.build('AAPL', 500, verdict='ACHETER', roro='RISK-ON',
                       positions=[{'sym': 'AAPL', 'type': 'STK', 'qty': 10, 'cost': 2000}],
                       prices_by_sym={'AAPL': 150.0})
    by = {c['key']: c for c in d['checks']}
    assert by['losers']['status'] == 'defavorable'
    assert '§18' in by['losers']['label'] or 'perdant' in by['losers']['label'].lower()
    assert d['overall'] == 'DÉFAVORABLE'


def test_rr_computed_from_real_plan():
    """R:R = (250−200)/(200−180) = 2,5:1 → ok."""
    d = pretrade.build('AAPL', 100, verdict='ACHETER', roro='RISK-ON',
                       prices_by_sym={'AAPL': 200.0}, plan={'stop': 180.0, 'tp1': 250.0})
    by = {c['key']: c for c in d['checks']}
    assert by['plan']['status'] == 'ok'
    assert 'R:R 2.5' in by['plan']['detail'].replace(',', '.')


def test_earnings_imminent_flags():
    d = pretrade.build('AAPL', 100, verdict='ACHETER', roro='RISK-ON', earnings_in_days=1)
    by = {c['key']: c for c in d['checks']}
    assert by['earnings']['status'] == 'defavorable'    # J-1 → gap possible


def test_unknowns_are_honest_not_invented():
    d = pretrade.build('ZZZZ', None)
    by = {c['key']: c for c in d['checks']}
    assert by['verdict']['status'] == 'inconnu'
    assert by['concentration']['status'] == 'inconnu'
    assert 'jamais d\'ordre' in d['narrative'] or 'ne passe jamais d\'ordre' in d['narrative']


def test_pretrade_route_end_to_end(tmp_path, monkeypatch):
    """La route assemble comité + régime + prix + desk réels et rend le ticket."""
    import json
    import terminal
    from vertex.services import persist
    from vertex.app.state import scan_state
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    persist.save_json('desk_data.json', {'ts': 1, 'data': {'myTrades': json.dumps([
        {'id': 1, 'sym': 'MSFT', 'type': 'STK', 'qty': 10, 'cost': 3000}])}})
    scan_state['committee'] = {'decisions': [{'symbol': 'AAPL', 'verdict': 'ACHETER'}]}
    scan_state['market_ctx'] = {'roro': 'RISK-ON'}
    scan_state.setdefault('detail', {}).update({
        'AAPL': {'price': 200.0, 'earnings_in_days': 30, 'plan': {'stop': 180.0, 'tp1': 250.0}},
        'MSFT': {'price': 400.0}})
    try:
        client = terminal.app.test_client()
        d = client.post('/api/pretrade/check',
                        json={'symbol': 'AAPL', 'amount': 1000}).get_json()
        assert d['symbol'] == 'AAPL'
        by = {c['key']: c for c in d['checks']}
        assert by['verdict']['status'] == 'ok'          # ACHETER
        assert by['regime']['status'] == 'ok'           # RISK-ON
        assert by['plan']['status'] == 'ok'             # R:R 2,5:1
        assert by['concentration']['status'] == 'attention'   # 1000/5000 = 20 %
        assert d['overall'] in ('MITIGÉ', 'FAVORABLE')
    finally:
        scan_state['committee'] = {}
        scan_state['market_ctx'] = {}


def test_analysis_page_has_pretrade_card():
    import terminal
    body = terminal.app.test_client().get('/analysis/AAPL').get_data(as_text=True)
    assert 'an-pretrade' in body and 'an-pt-go' in body
    assert 'Ticket pré-trade' in body
    for verb in ('place_order', 'placeOrder', 'submit_order', 'transmit'):
        assert verb not in body
