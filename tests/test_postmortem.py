"""tests/test_postmortem.py — post-mortem du journal : stats réelles + drapeaux honnêtes."""
from vertex.engines import postmortem


def _closed():
    return [
        {'sym': 'AAPL', 'type': 'STK', 'cost': 1000, 'exit': 1300,
         'added': '2026-07-01', 'closed': '2026-07-10'},                   # +300
        {'sym': 'NVDA', 'type': 'CALL', 'cost': 800, 'exit': 200,
         'added': '2026-07-05', 'closed': '2026-07-20'},                   # −600
        {'sym': 'NVDA', 'type': 'CALL', 'cost': 500, 'exit': 100,
         'added': '2026-07-12', 'closed': '2026-07-22'},                   # −400
    ]


def test_stats_exact():
    d = postmortem.build(_closed())
    assert d['empty'] is False
    assert d['trades_n'] == 3 and d['wins'] == 1 and d['losses'] == 2
    assert d['win_rate'] == 33
    assert d['total_pnl'] == -700.0
    assert d['avg_win'] == 300.0
    assert d['avg_loss'] == -500.0
    assert d['profit_factor'] == 0.3            # 300 / 1000
    assert d['best']['sym'] == 'AAPL' and d['worst']['sym'] == 'NVDA'
    assert d['hold_days_avg'] is not None


def test_behavioral_flags_derived_from_numbers():
    d = postmortem.build(_closed())
    txt = ' '.join(d['flags'])
    assert 'NVDA' in txt                          # récidive de pertes détectée
    assert 'Profit factor' in txt                 # PF < 1 signalé
    assert 'options' in txt.lower()               # options détruisent vs actions


def test_empty_is_honest():
    d = postmortem.build([])
    assert d['empty'] is True
    assert d['win_rate'] is None
    assert d['narrative'] is None
    assert d['reason']


def test_unusable_rows_skipped_not_invented():
    d = postmortem.build([
        {'sym': 'X', 'type': 'STK', 'cost': None, 'exit': 100},     # coût absent
        {'sym': 'Y', 'type': 'STK', 'cost': 100, 'exit': 150},      # exploitable
    ])
    assert d['trades_n'] == 1


def test_mistakes_from_journal_text():
    d = postmortem.build(_closed(), journal=[
        {'ticker': 'NVDA', 'mistake': 'entré sans catalyseur', 'date': '2026-07-20'},
        {'ticker': 'AAPL', 'mistake': '', 'date': '2026-07-10'},          # vide → ignoré
    ])
    assert len(d['mistakes']) == 1
    assert d['mistakes'][0]['ticker'] == 'NVDA'


def test_narrative_is_descriptive_not_advice():
    d = postmortem.build(_closed())
    assert 'pas un conseil' in d['narrative']


def test_postmortem_route_reads_desk(tmp_path, monkeypatch):
    """La route lit le blob desk (myTradesClosed JSON-string) et rend les stats."""
    import json
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    persist.save_json('desk_data.json', {'ts': 1, 'data': {
        'myTradesClosed': json.dumps([
            {'sym': 'AAPL', 'type': 'STK', 'cost': 1000, 'exit': 1300,
             'added': '2026-07-01', 'closed': '2026-07-10'}]),
        'vxJournal': json.dumps([]),
    }})
    client = terminal.app.test_client()
    r = client.get('/api/journal/postmortem')
    assert r.status_code == 200
    d = r.get_json()
    assert d['trades_n'] == 1 and d['win_rate'] == 100


def test_journal_page_has_postmortem_card():
    import terminal
    client = terminal.app.test_client()
    body = client.get('/journal').get_data(as_text=True)
    assert 'vx-pf-postmortem' in body
    assert 'Post-mortem' in body
    assert 'pas un conseil' in body
