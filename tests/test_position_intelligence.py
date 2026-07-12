"""Tests Position Intelligence OS (§42-43) — golden numériques documentés.

Chaque calcul est vérifié à la main. Invariants : donnée absente = None
(jamais 0), multiplicateur appliqué une fois, Greeks positionnels signés,
aucun chemin d'ordre, aucune clôture automatique.
"""
import os
import re

import pytest

from vertex.positions import models, calculator, lifecycle, thesis_health, audit
from vertex.positions.repository import load_positions
from vertex.positions.reconciler import reconcile
from vertex.positions.recalculator import recalculate_all, aggregate
from vertex.positions.change_detector import diff
from vertex.positions.alerts import PositionAlerts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _stk(**kw):
    base = {'id': 't', 'type': 'STK', 'sym': 'NVDA', 'qty': 10, 'cost': 1000.0,
            'added': '2026-01-01', 'entrySnap': {'stop': 90, 'tgt': 130, 'thesis': 'x'}}
    base.update(kw)
    return models.stock_position(base, 'MANUAL')


def _opt(**kw):
    base = {'id': 'o', 'type': 'CALL', 'sym': 'MSFT', 'qty': 2, 'cost': 3680.0,
            'exp': '2099-12-18', 'strike': 520, 'right': 'C',
            'entrySnap': {'spot': 498, 'stop': 470, 'tgt': 560, 'thesis': 'x'}}
    base.update(kw)
    return models.option_position(base, 'MANUAL')


# ── Modèles & sources ────────────────────────────────────────────────────

def test_position_models_have_source_and_readonly():
    p = _stk()
    assert p['source'] == 'MANUAL' and p['is_readonly'] is True
    assert p['average_cost'] == 100.0  # 1000 / 10


def test_simulated_is_not_real():
    blob = {'data': {'simTrades': [{'id': 's', 'type': 'STK', 'sym': 'AAPL',
                                    'qty': 5, 'cost': 500}]}}
    pos = load_positions(blob)
    assert pos and pos[0]['source'] == 'SIMULATED' and pos[0]['is_real'] is False


def test_startup_detects_positions():
    blob = {'data': {'myTrades': '[{"id":"1","type":"STK","sym":"NVDA","qty":10,"cost":1000}]'}}
    assert len(load_positions(blob)) == 1


def test_ibkr_offline_does_not_close_positions():
    local = [_stk()]
    r = reconcile(local, [], ibkr_online=False)
    assert r['issues'] == [] and local[0]['status'] != 'CLOSED'


def test_duplicate_positions_are_detected():
    local = [_stk(id='a'), _stk(id='b')]  # même identité (NVDA/USD/STK)
    r = reconcile(local, [], ibkr_online=True)
    assert any(i['code'] == 'POSITION_DUPLICATE' for i in r['issues'])


def test_quantity_conflict_requires_repair():
    loc, brk = _stk(qty=10), _stk(qty=12)
    brk['source'] = 'IBKR'
    r = reconcile([loc], [brk], ibkr_online=True)
    assert any(i['code'] == 'QUANTITY_MISMATCH' and i['action'] == 'DATA_REPAIR_REQUIRED'
               for i in r['issues'])


def test_cost_basis_conflict_requires_repair():
    loc = _stk(qty=10, cost=1000)   # avg 100
    brk = _stk(qty=10, cost=1200)   # avg 120
    brk['source'] = 'IBKR'
    r = reconcile([loc], [brk], ibkr_online=True)
    assert any(i['code'] == 'COST_BASIS_MISMATCH' for i in r['issues'])


def test_option_contract_uses_conid_identity():
    p = _opt()
    assert p['contract_id'] == 'MSFT|2099-12-18|520|C'


def test_multiplier_is_applied_once():
    p = _opt(qty=2, cost=3680)   # prime/action = 3680/(2*100) = 18.40
    assert p['average_cost'] == 18.40
    calculator.enrich_option(p, {'mark': 20.0, 'source': 'IBKR'}, None,
                             {'source': 'BROKER_GREEKS', 'delta': 0.5}, None)
    # valeur = 20 * 100 * 2 = 4000 (×100 UNE fois)
    assert p['market_value'] == 4000.0


# ── Calculs actions (golden) ─────────────────────────────────────────────

def test_missing_price_does_not_become_zero():
    p = _stk()
    calculator.enrich_stock(p, None)
    assert p['current_price'] is None and p['market_value'] is None
    assert p['unrealized_pnl'] is None


def test_stale_price_is_visible():
    p = _stk()
    calculator.enrich_stock(p, {'price': 110, 'source': 'scan', 'stale': True})
    assert p['price_stale'] is True and p['data_quality']['overall'] == 'STALE'


def test_stock_pnl_is_correct():
    p = _stk(qty=10, cost=1000)   # avg 100
    calculator.enrich_stock(p, {'price': 115, 'source': 'IBKR', 'stale': False})
    assert p['market_value'] == 1150.0
    assert p['unrealized_pnl'] == 150.0
    assert p['unrealized_pnl_pct'] == 15.0


def test_distance_to_stop_is_correct():
    p = _stk(qty=10, cost=1000, entrySnap={'stop': 90, 'tgt': 130, 'thesis': 'x'})
    calculator.enrich_stock(p, {'price': 100, 'source': 'IBKR'})
    # (90/100 - 1)*100 = -10 %
    assert p['risk_to_stop_pct'] == -10.0
    assert p['risk_to_stop'] == 100.0  # (100-90)*10


def test_remaining_rr_is_correct():
    p = _stk(qty=10, cost=1000, entrySnap={'stop': 90, 'tgt': 130, 'thesis': 'x'})
    calculator.enrich_stock(p, {'price': 100, 'source': 'IBKR'})
    # (130-100)/(100-90) = 3.0
    assert p['remaining_rr'] == 3.0


def test_position_weight_is_correct():
    a = _stk(id='a', sym='NVDA', qty=10, cost=1000)
    b = _stk(id='b', sym='AAPL', qty=10, cost=3000)
    calculator.enrich_stock(a, {'price': 100})   # value 1000
    calculator.enrich_stock(b, {'price': 300})   # value 3000
    calculator.portfolio_weights([a, b])
    assert a['weight_pct'] == 25.0 and b['weight_pct'] == 75.0


def test_mae_mfe_is_correct():
    r = calculator.mae_mfe(1000.0, [1000, 1200, 900, 1100])
    assert r['mfe'] == 20.0 and r['mae'] == -10.0


# ── Calculs options (golden) ─────────────────────────────────────────────

def test_option_pnl_is_correct():
    p = _opt(qty=2, cost=3680)   # capital 3680
    calculator.enrich_option(p, {'mark': 22.0, 'source': 'IBKR'}, None, None, None)
    # value = 22*100*2 = 4400 ; pnl = 4400-3680 = 720 ; % = 720/3680
    assert p['market_value'] == 4400.0 and p['unrealized_pnl'] == 720.0
    assert p['unrealized_pnl_pct'] == pytest.approx(19.57, abs=0.02)


def test_option_dte_is_correct():
    from datetime import date, timedelta
    exp = (date.today() + timedelta(days=45)).isoformat()
    p = _opt(exp=exp)
    assert p['dte'] == 45


def test_option_breakeven_is_correct():
    p = _opt(strike=520, qty=2, cost=3680)  # prime/action 18.40
    calculator.enrich_option(p, {'mark': 18.40}, {'price': 500}, None, None)
    assert p['breakeven'] == 538.40   # CALL : 520 + 18.40


def test_option_intrinsic_value_is_correct():
    p = _opt(strike=520, right='C')
    calculator.enrich_option(p, {'mark': 30}, {'price': 540}, None, None)
    assert p['intrinsic_value'] == 20.0   # 540 - 520
    assert p['extrinsic_value'] == 10.0   # mark 30 - intrinsic 20


def test_option_delta_position_is_correct():
    p = _opt(qty=2)
    calculator.enrich_option(p, {'mark': 20}, {'price': 500},
                             {'source': 'BROKER_GREEKS', 'delta': 0.55}, None)
    # 0.55 * 100 * 2 = 110
    assert p['delta'] == 110.0


def test_option_theta_position_is_negative_for_long():
    p = _opt(qty=2)
    calculator.enrich_option(p, {'mark': 20}, {'price': 500},
                             {'source': 'BROKER_GREEKS', 'theta': -0.08}, None)
    assert p['theta'] == pytest.approx(-16.0)   # -0.08 * 100 * 2


def test_put_delta_sign_inconsistency_is_flagged():
    p = _opt(type='PUT', right='P', strike=88, sym='XLE')
    # PUT avec delta positif = incohérent
    calculator.enrich_option(p, {'mark': 4}, {'price': 90},
                             {'source': 'BROKER_GREEKS', 'delta': 0.4}, None)
    assert 'DELTA_SIGN_INCONSISTENT' in p['data_quality']['issues']


def test_greeks_divergence_is_flagged():
    p = _opt()
    calculator.enrich_option(p, {'mark': 20}, {'price': 500},
                             {'source': 'BROKER_GREEKS', 'delta': 0.5,
                              'broker_delta': 0.50, 'model_delta': 0.65}, None)
    assert 'BROKER_MODEL_GREEK_DIVERGENCE' in p['data_quality']['issues']


# ── Cycle de vie ─────────────────────────────────────────────────────────

def test_thesis_is_not_invalidated_by_small_move():
    p = _stk(qty=10, cost=1000, entrySnap={'stop': 90, 'tgt': 130, 'thesis': 'x'})
    calculator.enrich_stock(p, {'price': 99.5, 'source': 'IBKR'})  # -0.5 % intraday
    assert lifecycle.stock_status(p) != 'INVALIDATED'


def test_stock_invalidated_when_stop_breached():
    p = _stk(qty=10, cost=1000, entrySnap={'stop': 90, 'tgt': 130, 'thesis': 'x'})
    calculator.enrich_stock(p, {'price': 88, 'source': 'IBKR'})
    assert lifecycle.stock_status(p) == 'INVALIDATED'


def test_stock_review_required_at_drawdown():
    p = _stk(qty=10, cost=1000, entrySnap={'stop': 70, 'tgt': 130, 'thesis': 'x'})
    calculator.enrich_stock(p, {'price': 79, 'source': 'IBKR'})  # -21 %
    assert lifecycle.stock_status(p) == 'REVIEW_REQUIRED'


def test_missing_thesis_requires_review():
    p = _stk(entrySnap={'stop': 90, 'tgt': 130})  # pas de thèse
    th = thesis_health.assess(p)
    assert th['overall_status'] == 'UNKNOWN' and 'THESIS_REQUIRED' in th['blocking_factors']


def test_option_dte_warning():
    from datetime import date, timedelta
    exp = (date.today() + timedelta(days=15)).isoformat()
    p = _opt(exp=exp)
    calculator.enrich_option(p, {'mark': 20}, {'price': 500}, None, None)
    assert lifecycle.option_status(p) == 'DTE_WARNING'


def test_option_review_before_total_loss():
    p = _opt(qty=2, cost=3680)
    calculator.enrich_option(p, {'mark': 8.0}, {'price': 500}, None, None)  # -56 %
    assert lifecycle.option_status(p) == 'REVIEW_REQUIRED'  # pas -100 %


def test_priority_p0_for_invalidated():
    p = _stk()
    p['lifecycle_status'] = 'INVALIDATED'
    assert lifecycle.priority(p) == 'P0_CRITICAL'


def test_materiality_ignores_micro_moves():
    assert lifecycle.materiality(0.3) == 'IMMATERIAL'
    assert lifecycle.materiality(3.0) == 'MEANINGFUL'
    assert lifecycle.materiality(6.0) == 'MAJOR'


# ── Portefeuille & agrégation ────────────────────────────────────────────

def test_portfolio_counts_calls_and_puts_separately():
    positions = [_stk(sym='NVDA'), _opt(sym='MSFT', right='C', type='CALL'),
                 _opt(sym='XLE', right='P', type='PUT', strike=88)]
    agg = aggregate(positions)
    assert agg['stocks_count'] == 1 and agg['calls_count'] == 1
    assert agg['puts_count'] == 1 and agg['options_count'] == 2


def test_positions_needing_action_lists_priority():
    p = _stk()
    p['lifecycle_status'] = 'STOP_APPROACHING'
    p['priority'] = 'P1_HIGH'
    agg = aggregate([p])
    assert len(agg['positions_needing_action']) == 1


def test_change_detector_has_reasons():
    before = {'position_id': 'x', 'unrealized_pnl_pct': 1.7, 'remaining_rr': 1.7}
    after = {'position_id': 'x', 'unrealized_pnl_pct': 8.0, 'remaining_rr': 2.3}
    d = diff(before, after)
    assert d['changed'] and any(c['label'] == 'R:R restant' for c in d['changes'])


def test_change_detector_ignores_none_none():
    d = diff({'iv': None}, {'position_id': 'x', 'iv': None})
    assert not d['changed']


def test_alerts_are_deduplicated():
    al = PositionAlerts()
    p = {'position_id': 'x', 'symbol': 'NVDA', 'lifecycle_status': 'STOP_APPROACHING',
         'data_quality': {}}
    first = al.evaluate([p], now=1000)
    second = al.evaluate([p], now=1100)   # même état, dans le cooldown
    assert len(first) == 1 and len(second) == 0


# ── Audit ────────────────────────────────────────────────────────────────

def test_audit_flags_expired_open_option():
    p = _opt(exp='2000-01-01')
    p['lifecycle_status'] = 'OPEN_HEALTHY'
    r = audit.audit_positions([p])
    assert r['status'] == 'CRITICAL'
    assert any('EXPIRED_STILL_OPEN' in f['errors'] for f in r['findings'])


def test_audit_healthy_for_complete_position():
    p = _stk()
    r = audit.audit_positions([p])
    assert r['status'] == 'HEALTHY'


# ── Sûreté : lecture seule ───────────────────────────────────────────────

def test_no_order_path_in_positions_package():
    forbidden = ('place_order', 'submit_order', 'transmit_order', 'modify_order',
                 'cancel_order', 'exercise_option', 'close_position', 'auto_close',
                 'auto_reduce', 'auto_rebalance')
    pat = re.compile(r'(?:\.|\bdef\s+)(?:' + '|'.join(forbidden) + r')\s*\(')
    pkg = os.path.join(ROOT, 'vertex', 'positions')
    for f in os.listdir(pkg):
        if f.endswith('.py'):
            src = open(os.path.join(pkg, f), encoding='utf-8').read()
            assert not pat.search(src), f'chemin d\'ordre dans {f}'


def test_all_positions_are_readonly():
    for p in [_stk(), _opt()]:
        assert p['is_readonly'] is True
