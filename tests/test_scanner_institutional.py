"""Scanner institutionnel multi-étages, régimes de marché, couche institutionnelle."""
from vertex.market.regime_engine import classify_regime, REGIMES
from vertex.scanner.candidate_pipeline import evaluate_candidate, run_pipeline, OUTCOMES
from vertex.scanner.scan_budget import ScanBudget
from vertex.scanner.stages import STAGE_ORDER
from vertex.research.institutional import (crowding_proxies, factor_model,
                                           sector_rotation, signal_ensemble,
                                           cross_sectional_ranking as ranking)


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
def test_mandatory_stage_order():
    names = [n for n, _ in STAGE_ORDER]
    assert names == ['fundamental', 'catalysts', 'technical', 'sentiment',
                     'anomalies', 'portfolio', 'options', 'risk']
    r = evaluate_candidate(strong_candidate())
    assert r['analysis_order'][0] == 'fundamental'
    assert r['analysis_order'][-1] == 'decision'


def test_strong_candidate_is_actionable():
    r = evaluate_candidate(strong_candidate())
    assert r['outcome'] == 'ACTIONABLE'
    assert r['outcome'] in OUTCOMES


def test_stale_data_caps_below_actionable():
    r = evaluate_candidate(strong_candidate(
        data_quality={'actionable_allowed': False}))
    assert r['outcome'] != 'ACTIONABLE'


def test_source_disagreement_blocks_actionable():
    r = evaluate_candidate(strong_candidate(reconciliation_ok=False))
    assert r['outcome'] != 'ACTIONABLE'


def test_blocking_anomaly_rejects():
    r = evaluate_candidate(strong_candidate(
        anomalies=[{'code': 'SPLIT_MISMATCH', 'blocking': True}]))
    assert r['outcome'] == 'REJECTED'


def test_no_new_risk_rejects():
    r = evaluate_candidate(strong_candidate(
        risk={'no_new_risk': True, 'reason': 'drawdown portefeuille -25% atteint'}))
    assert r['outcome'] == 'REJECTED'


def test_missing_fundamentals_never_actionable():
    r = evaluate_candidate(strong_candidate(fundamentals={}))
    assert r['outcome'] != 'ACTIONABLE'
    assert 'fundamentals' in r['missing']


def test_thesis_invalidation():
    r = evaluate_candidate(strong_candidate(
        technical={'trend': 'UP', 'relative_strength': 82, 'reward_risk': 2.4,
                   'thesis_invalidated': True}))
    assert r['outcome'] == 'INVALIDATED'


def test_pipeline_budget_caps_work():
    candidates = [strong_candidate(symbol=f'S{i}') for i in range(30)]
    res = run_pipeline(candidates, budget=ScanBudget({'fundamental': 10}))
    assert len(res['results']) == 10
    assert res['budget']['used']['fundamental'] == 10


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


def test_cross_sectional_ranking():
    metrics = {f'S{i}': {'growth': i / 10} for i in range(20)}
    ranked = ranking.rank_universe(metrics, ['growth'])
    assert ranked['S19']['growth']['universe_pct'] == 100.0
    assert ranked['S0']['growth']['universe_pct'] == 5.0
    assert ranking.leaders(ranked, 3) == ['S19', 'S18', 'S17']


def test_sector_rotation_styles():
    res = sector_rotation.analyze_rotation(
        {'Technologie': {'r20': 0.05, 'r5': 0.03}, 'Santé': {'r20': -0.02, 'r5': -0.01},
         'Finance': {'r20': 0.03, 'r5': 0.005}}, benchmark_return_20d=0.01)
    assert res['rotation_style'] == 'CYCLICAL'
    assert res['leadership'] == 'Technologie'
    assert 'Technologie' in res['accelerating']


def test_crowding_is_always_a_proxy():
    res = crowding_proxies.crowding_score(
        {'correlation_to_leaders': 0.9, 'momentum_percentile': 95,
         'analyst_buy_ratio': 0.9, 'iv_percentile': 85})
    assert res['crowded'] is True
    assert 'INCONNUES' in res['disclaimer']
    for c in res['components']:
        assert 'proxy' in c['note']


def test_signal_ensemble_enriches_never_decides():
    ctx = signal_ensemble.institutional_context(
        {'returns': [0.001] * 300, 'revenue_growth': 0.3, 'margin': 0.25,
         'roe': 0.3, 'momentum_3m': 0.1}, market_regime='TREND_UP')
    assert 'summary' in ctx and 'factors' in ctx
    assert 'décision' in ctx['disclaimer'] or 'decision' in ctx['disclaimer']
    for forbidden in ('ACHETER', 'BUY_NOW', 'place_order'):
        assert forbidden not in str(ctx)
