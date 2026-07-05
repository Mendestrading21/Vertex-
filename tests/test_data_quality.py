"""
tests/test_data_quality.py — La qualité de donnée est une métadonnée de première classe.

Chaque décision porte source / âge / fraîcheur / grade. Rien d'anonyme (Ch. IV).
Donnée manquante → on bloque honnêtement ; donnée rassie → confiance pénalisée.
"""

from vertex.engines import decision_stack as ds


_FULL = {'symbol': 'T', 'price': 100, 'score': 80,
         'plan': {'entry': 100, 'stop': 92, 'tp2': 116}}


def test_fresh_full_data_is_grade_a():
    dq = ds.assess_data_quality(_FULL, scan_age_s=30, demo=False)
    assert dq['grade'] == 'A'
    assert dq['blocks_decision'] is False
    assert dq['stale'] is False
    assert dq['confidence_penalty'] == 0
    assert dq['source'] == 'scan'


def test_missing_fields_block_and_downgrade():
    dq = ds.assess_data_quality({'symbol': 'T'}, scan_age_s=30)
    assert dq['blocks_decision'] is True
    assert dq['grade'] == 'C'
    assert 'price' in dq['missing_fields'] and 'plan' in dq['missing_fields']
    assert dq['confidence_penalty'] > 0


def test_stale_scan_penalises_without_blocking():
    dq = ds.assess_data_quality(_FULL, scan_age_s=5000)
    assert dq['stale'] is True
    assert dq['blocks_decision'] is False       # rassi ≠ absent : on décide, mais moins sûr
    assert dq['grade'] == 'B'
    assert dq['confidence_penalty'] >= 15
    assert dq['warning']


def test_demo_source_is_flagged():
    dq = ds.assess_data_quality(_FULL, scan_age_s=30, demo=True)
    assert dq['source'] == 'demo-synthetic'
    assert 'démo' in (dq['warning'] or '').lower()


def test_penalty_is_capped():
    dq = ds.assess_data_quality({'symbol': 'T'}, scan_age_s=99999, demo=False)
    assert dq['confidence_penalty'] <= 60          # jamais une pénalité absurde


def test_every_decision_carries_data_quality():
    r = ds.evaluate(_FULL, scan_age_s=30)
    assert 'data_quality' in r
    dq = r['data_quality']
    for key in ('source', 'grade', 'stale', 'age_seconds'):
        assert key in dq
