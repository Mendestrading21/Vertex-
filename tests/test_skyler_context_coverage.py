from vertex.engines import skyler_core as skyler


def test_packet_exposes_context_coverage_without_changing_contexts():
    packet = skyler.build_packet('TST', {'score': 70, 'verdict': 'ATTENDRE'}, as_of='2026-08-17')
    coverage = packet['context_coverage']
    assert coverage['total_contexts'] == len(packet['contexts'])
    assert coverage['coverage_pct'] < 100.0
    assert 'options' in coverage['unknown_contexts']
    assert coverage['read_only'] is True
