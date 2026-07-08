"""
tests/test_demo.py — Données de vitrine (mode démo).

Déterminisme par graine (mêmes prix pour un symbole donné), structure OHLCV
valide, board d'options crédible mais fictif. Aucune donnée réelle, aucun ordre.
"""

from vertex.data import demo


def test_demo_one_is_seed_deterministic():
    a = demo.demo_one('NVDA')
    b = demo.demo_one('NVDA')
    assert list(a['Close'].values) == list(b['Close'].values)      # même graine → mêmes prix
    assert demo.demo_one('NVDA')['Close'].iloc[-1] != demo.demo_one('AAPL')['Close'].iloc[-1]


def test_demo_one_ohlcv_shape():
    df = demo.demo_one('MSFT', n=200)
    assert len(df) == 200
    assert set(df.columns) == {'Open', 'High', 'Low', 'Close', 'Volume'}
    assert (df['High'] >= df['Close']).all() and (df['Low'] <= df['Close']).all()
    assert df['Close'].notna().all()


def test_demo_universe_covers_all_tickers():
    uni = demo.demo_universe(['AAPL', 'MSFT', 'NVDA'])
    assert set(uni.keys()) == {'AAPL', 'MSFT', 'NVDA'}
    assert all(len(v) > 0 for v in uni.values())


def test_demo_options_board_is_synthetic_but_structured():
    rows = [{'symbol': 'AAPL', 'score': 85, 'price': 230}, {'symbol': 'MSFT', 'score': 70, 'price': 420}]
    board = demo.demo_options_board(rows, {'AAPL': {'rs': 75}, 'MSFT': {'rs': 55}})
    types = {c['type'] for c in board}
    assert board and types <= {'CALL', 'PUT'} and 'CALL' in types    # CALL + PUT (couverture)
    assert {c['bucket'] for c in board} == {'court', 'moyen', 'long'}
    for c in board:
        assert 20 <= c['quality'] <= 94 and c['cost'] > 0 and c['strike'] > 0
        # liquidité synthétique présente — nourrit le cockpit Options Lab
        assert c['oi'] > 0 and c['vol'] >= 0 and c['spread_pct'] > 0


def test_demo_puts_target_weak_names_and_hedge_leaders():
    rows = [{'symbol': 'AAA', 'score': 90, 'price': 100}, {'symbol': 'ZZZ', 'score': 25, 'price': 50}]
    board = demo.demo_options_board(rows, {})
    put_syms = {c['sym'] for c in board if c['type'] == 'PUT'}
    assert 'ZZZ' in put_syms                     # pari baissier sur le titre faible
    assert 'AAA' in put_syms                     # couverture sur le leader


def test_terminal_bindings_are_the_module():
    import terminal
    assert terminal._demo_one is demo.demo_one
    assert terminal._demo_options_board is demo.demo_options_board
