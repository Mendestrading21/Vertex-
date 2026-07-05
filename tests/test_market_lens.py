"""
tests/test_market_lens.py — Prisme marché & secteur (alignement titre × secteur × marché).
"""

from vertex.engines import market_lens as ml


_SECTORS = [
    {'sector': 'Energy', 'avg_score': 78, 'avg_change': 1.2},
    {'sector': 'Tech', 'avg_score': 60, 'avg_change': 0.3},
    {'sector': 'Utilities', 'avg_score': 40, 'avg_change': -0.5},
]
_BULL = {'spy_regime': 'TREND', 'roro': 'RISK-ON', 'vix_band': 'calme', 'breadth': {'above50': 70}}
_BEAR = {'spy_regime': 'CHOP', 'roro': 'RISK-OFF', 'vix_band': 'stress', 'breadth': {'above50': 25}}


def test_climate_favorable_vs_dangerous():
    assert ml.climate(_BULL)['label'] == 'FAVORABLE'
    assert ml.climate(_BEAR)['label'] == 'DANGEREUX'
    assert ml.climate(None) is None


def test_sector_standing_rank_and_favor():
    s = ml.sector_standing(_SECTORS, 'Energy')
    assert s['rank'] == 1 and s['n'] == 3 and s['in_favor'] is True
    u = ml.sector_standing(_SECTORS, 'Utilities')
    assert u['rank'] == 3 and u['in_favor'] is False


def test_full_alignment_is_tailwind():
    r = ml.build(market=_BULL, sectors=_SECTORS, sector_name='Energy', stock_pct=90)
    assert r['alignment'] == 'aligné'
    assert r['lights'] == {'market': True, 'sector': True, 'stock': True}
    assert 'dos' in r['headline'].lower()


def test_strong_stock_against_the_tape_is_flagged():
    r = ml.build(market=_BEAR, sectors=_SECTORS, sector_name='Utilities', stock_pct=85)
    assert r['alignment'] == 'à contre-courant'
    assert r['lights']['stock'] is True and r['lights']['market'] is False


def test_all_red_is_unfavourable():
    r = ml.build(market=_BEAR, sectors=_SECTORS, sector_name='Utilities', stock_pct=20)
    assert r['alignment'] == 'défavorable'


def test_degenerate_inputs_are_safe():
    r = ml.build(market=None, sectors=None, sector_name=None, stock_pct=None)
    assert r['climate'] is None and r['sector'] is None
    assert r['alignment'] in ('défavorable', 'partiellement aligné', 'à contre-courant', 'aligné')
