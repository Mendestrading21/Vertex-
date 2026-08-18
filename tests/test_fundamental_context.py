from vertex.engines.fundamental_context import build


def test_fundamental_context_exposes_available_values_and_missing_fields():
    out = build('TST', {'by_sym': {'TST': {'sector': 'Tech', 'pe': 20.0, 'margin': 0.2}},
                        'by_sector': {'Tech': {'median_pe': 25.0, 'n': 10}},
                        'provenance': {'source': 'yfinance.info', 'as_of': '2026-08-17T10:00:00Z',
                                       'refresh_policy_hours': 6}})
    assert out['available'] is True and out['read_only'] is True
    assert out['values']['pe'] == 20.0
    assert out['sector_medians']['median_pe'] == 25.0
    assert 'growth' in out['missing_fields']
    freshness = out['freshness_coverage']
    assert freshness['timestamp_available'] is True
    assert freshness['field_coverage_pct'] < 100.0


def test_fundamental_context_keeps_missing_provenance_explicit():
    out = build('TST', {'by_sym': {'TST': {'sector': 'Tech', 'pe': 20.0}}})
    assert out['freshness_coverage']['timestamp_available'] is False
    assert out['freshness_coverage']['as_of'] is None


def test_fundamental_context_is_honest_when_symbol_is_missing():
    out = build('TST', {'by_sym': {}})
    assert out == {'available': False, 'reason': 'fondamentaux par titre indisponibles', 'read_only': True}
