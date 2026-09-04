"""Scanner institutionnel multi-étages, régimes de marché, couche institutionnelle."""
from vertex.market.regime_engine import classify_regime, REGIMES
from vertex.scanner.stages import STAGE_ORDER
from vertex.research.institutional import factor_model


def strong_candidate(**kw):
    c = {'symbol': 'NVDA',
         'fundamentals': {'revenue_growth': 0.35, 'margin': 0.30, 'pe': 45,
                          'sector_median_pe': 30},
         'catalysts': {'has_catalyst': True, 'next_events': [{'type': 'EARNINGS'}]},
         'technical': {'trend': 'UP', 'relative_strength': 82, 'reward_risk': 2.4,
                       'overextended': False},
         'sentiment': {'news_tone': 'POSITIVE'},
         'anomalies': [],
         'portfolio_fit': {'improves_quality': True},
         'option_selection': {'primary': {'category': 'DYNAMIC', 'score': 72}},
         'risk': {},
         'data_quality': {'actionable_allowed': True},
         'reconciliation_ok': True}
    c.update(kw)
    return c


# ── Ordre et sorties du pipeline ──────────────────────────────────────


















# ── Régimes de marché ─────────────────────────────────────────────────
def test_regime_unknown_with_too_few_dimensions():
    r = classify_regime({'vix': 18})
    assert r['regime'] == 'UNKNOWN'
    assert r['adjustments']['size_factor_if_capital'] < 1


def test_regime_panic_blocks_new_risk_but_never_trades():
    r = classify_regime({'index_trend': 'DOWN', 'breadth_pct': 15, 'vix': 42,
                         'credit_spread_trend': 'WIDENING'})
    assert r['regime'] == 'PANIC'
    adj = r['adjustments']
    assert adj['new_risk_allowed'] is False
    assert 'trade' not in str(adj).lower() and 'order' not in str(adj).lower()


def test_regime_trend_up_and_risk_on():
    r = classify_regime({'index_trend': 'UP', 'breadth_pct': 72, 'vix': 13,
                         'leadership': 'CYCLICAL'})
    assert r['regime'] in ('TREND_UP', 'RISK_ON')
    assert r['regime'] in REGIMES
    assert r['adjustments']['new_risk_allowed'] is True


def test_regime_only_modulates():
    """Un régime ne produit que des modulations (seuils, taille, confirmations)."""
    for inputs in ({'index_trend': 'UP', 'breadth_pct': 70, 'vix': 13},
                   {'index_trend': 'DOWN', 'breadth_pct': 20, 'vix': 30}):
        adj = classify_regime(inputs)['adjustments']
        assert set(adj) == {'setup_priority', 'score_threshold_shift',
                            'size_factor_if_capital', 'confidence_factor',
                            'confirmation_required', 'new_risk_allowed'}


# ── Couche institutionnelle ───────────────────────────────────────────
def test_factor_exposures_honest_when_data_missing():
    f = factor_model.factor_exposures({'returns': []})
    assert f['BETA']['value'] is None
    assert f['MOMENTUM']['value'] is None
    assert set(f) == set(factor_model.FACTORS)








