from datetime import datetime, timezone

from vertex.data_sources import scan_evidence as SE


class _Frame:
    def __init__(self, stamp):
        self.index = [stamp]


def _detail():
    return {'price': 100.0, 'series': {'close': list(range(1, 80))}}


def test_scan_evidence_requires_an_explicit_options_timestamp():
    packet, report = SE.build_symbol(
        'TST', _detail(), _Frame(datetime.now(timezone.utc)), 'yfinance',
        options_board=[{'sym': 'TST', 'underlying': 'TST'}], options_as_of=None,
    )
    assert packet['quality']['overall'] == 'MISSING'
    assert report['actionable_allowed'] is True


def test_scan_evidence_marks_fresh_spot_and_delayed_options_when_timestamped():
    now = datetime.now(timezone.utc)
    packet, report = SE.build_symbol(
        'TST', _detail(), _Frame(now), 'yfinance',
        options_board=[{'sym': 'TST', 'underlying': 'TST', 'underlying_price': 100.0,
                        'bid': 2.0, 'ask': 2.2}], options_as_of=now,
    )
    assert packet['quality']['actionable_allowed'] is True
    assert packet['sources']['spot']['quality'] == 'FRESH'
    assert packet['sources']['options']['quality'] == 'FRESH'
    assert report['blocking'] is False
    assert report['coverage']['price_comparison_available'] is True
    assert report['coverage']['price_comparisons_attempted'] == 1
    assert report['coverage']['status'] == 'COMPARABLE'


def test_scan_evidence_marks_non_comparable_prices_without_synthesis():
    packet, report = SE.build_symbol(
        'TST', _detail(), _Frame(datetime.now(timezone.utc)), 'yfinance',
        options_board=[{'sym': 'TST', 'underlying': 'TST'}], options_as_of=None,
    )
    coverage = report['coverage']
    assert packet['sources']['spot']['value'] == 100.0
    assert coverage['price_comparison_available'] is False
    assert coverage['price_comparisons_attempted'] == 0
    assert coverage['status'] == 'INSUFFICIENT_COMPARABLE_SOURCES'
    assert 'synthèse' in coverage['note']
