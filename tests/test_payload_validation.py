from vertex.app import payload_validation as payload


def test_payload_requires_bounded_object_and_strict_symbol():
    assert payload.required_symbol({'symbol': 'brk.b'}) == 'BRK.B'
    try:
        payload.required_symbol({'symbol': 'AAPL!'})
        assert False, 'invalid symbol must be rejected'
    except payload.PayloadError as exc:
        assert str(exc) == 'symbole_invalide'
    try:
        payload.object_body([], max_keys=4)
        assert False, 'array payload must be rejected'
    except payload.PayloadError as exc:
        assert str(exc) == 'payload_json_objet_requis'


def test_payload_bounded_lists_and_numbers_reject_unsafe_shapes():
    assert payload.object_list({'legs': [{'type': 'CALL'}]}, 'legs', 2, 1) == [{'type': 'CALL'}]
    assert payload.optional_number({'amount': '12.5'}, 'amount') == 12.5
    for body in ({'amount': 'nan'}, {'amount': float('inf')}, {'amount': 1_000_000_001}):
        try:
            payload.optional_number(body, 'amount')
            assert False, 'non finite or oversized numeric value must be rejected'
        except payload.PayloadError:
            pass
