from vertex.engines import portfolio_context


class _Profile:
    portfolio_min_positions = 1
    portfolio_max_positions = 10
    max_stock_weight_pct = 30
    raw = {'position_rules': {}, 'conviction_levels': {}}


def test_portfolio_context_reports_declared_multi_asset_mix():
    positions = [
        {'symbol': 'SPY', 'asset_type': 'ETF', 'quantity': 2, 'cost_basis': 900, 'status': 'OPEN'},
        {'symbol': 'NVDA', 'asset_type': 'STOCK', 'quantity': 1, 'cost_basis': 100, 'status': 'OPEN'},
        {'symbol': 'NVDA', 'asset_type': 'OPTION', 'quantity': 1, 'cost_basis': 50, 'status': 'OPEN'},
    ]
    out = portfolio_context.build(positions, quotes={'SPY': 500, 'NVDA': 110}, profile=_Profile())
    assert out['asset_mix']['ETF']['positions'] == 1
    assert out['asset_mix']['STOCK']['positions'] == 1
    assert out['asset_mix']['OPTION']['positions'] == 1
    assert out['asset_mix']['ETF']['weight_pct'] > out['asset_mix']['OPTION']['weight_pct']


def test_portfolio_context_keeps_undeclared_asset_type_explicit():
    positions = [{'symbol': 'XYZ', 'quantity': 1, 'cost_basis': 100, 'status': 'OPEN'}]
    out = portfolio_context.build(positions, profile=_Profile())
    assert out['asset_mix']['UNCLASSIFIED']['positions'] == 1
    assert 'sans type' in out['asset_mix_note']
