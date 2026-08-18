from vertex.data_sources.models import (
    AnalyticsPacket, QUALITY_MISSING, SOURCE_SECONDARY, MODE_DELAYED,
)
from vertex.data_sources.provenance import stamp
from vertex.data_sources.quality import grade_packet


def test_quality_reports_available_missing_and_fallback_sources():
    packet = AnalyticsPacket(symbol='TST')
    packet.set_source('spot', stamp(100.0, SOURCE_SECONDARY, MODE_DELAYED,
                                    fallback_used=True))
    result = grade_packet(packet)
    coverage = result['coverage']
    assert result['overall'] == QUALITY_MISSING
    assert result['actionable_allowed'] is False
    assert coverage['available_sources'] == 1
    assert coverage['total_sources'] == 5
    assert coverage['missing_sources'] == ['history', 'fundamentals', 'catalysts', 'options']
    assert coverage['fallback_sources'] == ['spot']
    assert coverage['coverage_pct'] == 20.0
