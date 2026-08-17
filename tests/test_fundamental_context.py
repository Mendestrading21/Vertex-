from vertex.engines.fundamental_context import build


def test_fundamental_context_exposes_available_values_and_missing_fields():
    out = build('TST', {'by_sym': {'TST': {'sector': 'Tech', 'pe': 20.0, 'margin': 0.2}},
                        'by_sector': {'Tech': {'median_pe': 25.0, 'n': 10}}})
    assert out['available'] is True and out['read_only'] is True
    assert out['values']['pe'] == 20.0
    assert out['sector_medians']['median_pe'] == 25.0
    assert 'growth' in out['missing_fields']


def test_fundamental_context_is_honest_when_symbol_is_missing():
    out = build('TST', {'by_sym': {}})
    assert out == {'available': False, 'reason': 'fondamentaux par titre indisponibles', 'read_only': True}
