from vertex.options import quote_resolver as qr


def _contract(**overrides):
    base = {
        'sym': 'ABC', 'type': 'CALL', 'exp': '2026-12-18', 'strike': 125,
        'bid': 3.0, 'ask': 3.4, 'mid': 3.2, 'oi': 900, 'cost': 320,
    }
    base.update(overrides)
    return base


def test_contract_identity_is_exact_and_shared_shape():
    assert qr.contract_id(_contract()) == 'ABC|2026-12-18|125|C'
    assert qr.contract_id(_contract(type='PUT')) == 'ABC|2026-12-18|125|P'
    assert qr.contract_id({'sym': 'ABC'}) is None


def test_resolve_uses_exact_contract_and_preserves_bid_ask_evidence():
    cid = qr.contract_id(_contract())
    out = qr.resolve([_contract(), _contract(strike=130)], contract_id_value=cid,
                     symbol='ABC', as_of=123, source='ibkr')
    assert out['available'] is True
    assert out['quote']['bid'] == 3.0
    assert out['quote']['ask'] == 3.4
    assert out['evidence']['price_kind'] == 'BID_ASK_MID'
    assert out['evidence']['cost_used_as_quote'] is False


def test_resolve_refuses_symbol_only_and_does_not_promote_cost_to_quote():
    assert qr.resolve([_contract()], symbol='ABC')['available'] is False
    c = _contract(bid=None, ask=None, mid=None)
    out = qr.resolve([c], contract_id_value=qr.contract_id(c), symbol='ABC')
    assert out['available'] is False
    assert out['quote'].get('mark') is None
    assert 'cost' not in out['evidence']['board_fields']
