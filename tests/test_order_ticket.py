"""Tests — dimensionnement & ticket d'ordre READONLY (§4/§11/§32).

Garde-fous stratégie (poids 15 %, R:R 2:1), honnêteté (donnée absente → None),
et invariant absolu : jamais de transmission d'ordre.
"""
import os
import re

from vertex.planning import order_ticket as OT


# ─────────────────────────────────────────── dimensionnement action
def test_stock_sizing_from_risk_budget():
    # compte 100k, risque 1 % = 1000 ; risque/action = 100-95 = 5 → 200 actions
    s = OT.size_position(100000, 1.0, entry=100, stop=95)
    assert s['qty'] == 200
    assert s['capital_at_risk'] == 1000.0
    assert s['capital_deployed'] == 20000.0
    assert s['weight_pct'] == 20.0


def test_stock_weight_over_15pct_warns():
    s = OT.size_position(100000, 1.0, entry=100, stop=95)  # poids 20 %
    assert any('poids' in w.lower() for w in s['warnings'])


def test_stock_stop_above_entry_is_rejected():
    s = OT.size_position(100000, 1.0, entry=100, stop=105)
    assert s['qty'] is None and s['warnings']


def test_missing_account_is_none_not_zero():
    s = OT.size_position(None, 1.0, entry=100, stop=95)
    assert s['qty'] is None


# ─────────────────────────────────────────── dimensionnement option
def test_option_sizing_uses_premium_as_max_loss():
    # budget risque 2000 ; prime 5 × 100 = 500 par contrat → 4 contrats
    s = OT.size_position(100000, 2.0, entry=None, stop=None,
                         is_option=True, premium=5.0)
    assert s['qty'] == 4
    assert s['capital_at_risk'] == 2000.0


def test_option_without_premium_is_none():
    s = OT.size_position(100000, 2.0, entry=None, stop=None, is_option=True)
    assert s['qty'] is None


# ─────────────────────────────────────────── ticket
def test_ticket_is_never_transmitted_and_readonly():
    t = OT.build_ticket('NVDA', qty=100, entry=100, stop=95, tp1=115)
    assert t['transmitted'] is False and t['readonly'] is True
    assert 'lecture seule' in t['disclaimer'].lower()
    assert 'PRÉPARATION' in t['copy_text']


def test_ticket_blocks_when_rr_below_2():
    # entry 100, stop 95, tp1 108 → R:R = 8/5 = 1.6 < 2
    t = OT.build_ticket('NVDA', qty=100, entry=100, stop=95, tp1=108)
    assert t['blocked'] is True
    assert any('R:R' in b for b in t['blockers'])


def test_ticket_ok_when_rr_ge_2():
    t = OT.build_ticket('NVDA', qty=100, entry=100, stop=95, tp1=112)  # 12/5=2.4
    assert not any('R:R' in b for b in t['blockers'])


def test_ticket_blocks_when_stop_missing():
    t = OT.build_ticket('NVDA', qty=100, entry=100, tp1=120)
    assert t['blocked'] is True
    assert any('stop' in b.lower() for b in t['blockers'])


def test_ticket_computes_qty_from_account_and_risk():
    t = OT.build_ticket('NVDA', entry=100, stop=95, tp1=115,
                        account_value=100000, risk_pct=1.0)
    assert t['qty'] == 200
    assert t['sizing'] is not None


def test_ticket_copy_text_contains_contract_for_option():
    t = OT.build_ticket('AAPL', is_option=True, right='C', strike=200,
                        expiry='2026-09-18', contract_id='AAPL260918C200',
                        qty=2, limit_price=5.0, premium=5.0, rr_res=2.5)
    assert 'OPTION C' in t['copy_text']
    assert 'AAPL260918C200' in t['copy_text']


# ─────────────────────────────────────────── invariant lecture seule
def test_no_order_execution_path_in_planning():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    banned = re.compile(r'(?:\.|\bdef\s+)(place_order|placeOrder|submit_order|'
                        r'transmit_order|send_order|execute_trade|cancel_order|'
                        r'modify_order)\s*\(')
    import glob
    for p in glob.glob(os.path.join(root, 'vertex/planning/*.py')):
        assert not banned.search(open(p, encoding='utf-8').read()), p
