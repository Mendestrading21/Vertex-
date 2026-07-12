"""Tests — cohérence de la stratégie canonique (audit système).

Vérifie qu'aucun seuil concurrent ne subsiste : le minimum R:R est 2.0 PARTOUT
(DecisionStack, evidence, ExecutiveEngine), jamais 1,5. Une opportunité à
R:R 1,7 ne doit jamais ressortir « achat » dans un moteur et « bloquée » dans
un autre — source unique de vérité.
"""
import re
import os

from vertex.engines import decision_stack as ds
from vertex.engines import evidence as ev


def _detail(rr):
    return {'plan': {'entry': 100, 'stop': 95, 'tp1': 108, 'tp2': 116,
                     'tp3': 130, 'rr_res': rr}}


def test_rr_between_1p5_and_2_is_not_a_buy_in_decision_stack():
    """R:R 1,7 : sous le minimum 2,0 → la règle dégrade l'achat (plus de zone 1,5–2,0)."""
    audit = []
    out = ds._apply_rules('BUY', _detail(1.7), None, None, None, True, audit)
    assert out not in ('STRONG_BUY', 'BUY'), out
    assert any('2.0' in a for a in audit)


def test_rr_above_2_keeps_buy():
    audit = []
    out = ds._apply_rules('BUY', _detail(2.5), None, None, None, True, audit)
    assert out == 'BUY'
    assert not any('minimum stratégie' in a for a in audit)


def test_evidence_flags_rr_below_2_as_negative():
    out = ev.risk_analyst(_detail(1.7), None)
    neg = [e for e in out if e['kind'] == ev.NEGATIVE and 'récompense' in e['text'].lower()]
    assert neg, 'R:R 1,7 doit produire une preuve négative (sous le minimum 2:1)'


def test_evidence_rr_at_2_is_favorable():
    out = ev.risk_analyst(_detail(2.0), None)
    pos = [e for e in out if e['kind'] == ev.POSITIVE and 'récompense' in e['text'].lower()]
    assert pos


def test_no_stale_rr_1p5_threshold_in_engines():
    """Aucun seuil `rr < 1.5` / `rr >= 1.5` décisionnel ne subsiste dans les moteurs."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = ['vertex/engines/decision_stack.py', 'vertex/engines/evidence.py']
    pat = re.compile(r'rr\s*[<>]=?\s*1\.5')
    for rel in files:
        with open(os.path.join(root, rel), encoding='utf-8') as fh:
            src = fh.read()
        assert not pat.search(src), '%s : seuil R:R 1,5 concurrent encore présent' % rel
