"""tests/test_operational_confidence_lot13.py — SKYLER LOT 13 : moteur 0.3.0.

Deux champs du ledger institutionnel encore honnêtement vides prennent vie :

  1. ÉTAT OPÉRATIONNEL (DECISION_ENGINE §2.2) : dérivé DÉTERMINISTIQUEMENT de la
     décision, des gates et du plan — jamais une décision finale de plus, avec
     base explicite.
  2. CONFIANCE FACTORISÉE (DECISION_ENGINE §7) :
     confidence = data_quality × agreement × robustness × calibration,
     chaque facteur borné [0,1] avec base, plafonds obligatoires appliqués
     (régime UNKNOWN ≤ 0,55 ; conflit de sources ≤ 0,50 ; contradiction ≤ 0,60),
     calibration plafonnée à 0,50 tant qu'aucun historique n'existe — étiquetée
     ESTIMÉE avec méthode, jamais 100 %.

Changement de règle = changement de version : ENGINE_VERSION 0.2.0 → 0.3.0.
La mémoire (lot 10) fige désormais ces champs quand le moteur les produit.
"""
import pytest

from vertex.engines import skyler_core as SK


def _detail(verdict='ATTENDRE', score=70, plan=True):
    d = {'score': score, 'verdict': verdict}
    if plan:
        d['plan'] = {'entry': 100, 'stop': 94, 'tp1': 106, 'tp2': 112,
                     'tp3': 118, 'rr_res': 3.0}
    return d


# ─── Version et énumération ─────────────────────────────────────────────────────

def test_engine_version_bumped():
    """États opérationnels + confiance sont entrés en 0.3.0 — jamais moins."""
    parts = tuple(int(x) for x in SK.ENGINE_VERSION.split('.'))
    assert parts >= (0, 3, 0)


def test_operational_states_enum_canonical():
    assert set(SK.OPERATIONAL_STATES) == {
        'SURVEILLER', 'PREPARER', 'DECLENCHEMENT_CONDITIONNEL',
        'CONFIRMATION_REQUISE', 'SECURISATION_PARTIELLE', 'RUNNER',
        'THESE_A_REEVALUER', 'DONNEES_INSUFFISANTES'}


# ─── État opérationnel : dérivation déterministe avec base ──────────────────────

def _gates(**trig):
    ids = ['RR_BELOW_2', 'NO_INVALIDATION', 'DATA_QUALITY_CRITICAL',
           'SOURCES_CONFLICT', 'THESIS_BROKEN']
    return [{'id': g, 'triggered': trig.get(g, False), 'reason': 'x'} for g in ids]


def test_state_data_insufficient_dominates():
    st, basis = SK.operational_state('ATTENDRE', _gates(DATA_QUALITY_CRITICAL=True),
                                     {'entry': 100})
    assert st == 'DONNEES_INSUFFISANTES' and basis


def test_state_thesis_broken():
    st, _ = SK.operational_state('ATTENDRE', _gates(THESIS_BROKEN=True), {})
    assert st == 'THESE_A_REEVALUER'


def test_state_conditional_trigger_when_waiting_with_plan():
    st, basis = SK.operational_state('ATTENDRE', _gates(), {'entry': 100, 'tp2': 112})
    assert st == 'DECLENCHEMENT_CONDITIONNEL'
    assert basis


def test_state_confirmation_required_when_gated():
    st, _ = SK.operational_state('ATTENDRE', _gates(RR_BELOW_2=True),
                                 {'entry': 100, 'tp2': 112})
    assert st == 'CONFIRMATION_REQUISE'


def test_state_surveiller_on_refusal_or_planless_wait():
    assert SK.operational_state('REFUSER', _gates(), {})[0] == 'SURVEILLER'
    assert SK.operational_state('ATTENDRE', _gates(), None)[0] == 'SURVEILLER'


def test_state_preparer_on_buy():
    assert SK.operational_state('ACHETER', _gates(), {'entry': 100})[0] == 'PREPARER'


def test_state_never_a_final_decision():
    for dec in ('ACHETER', 'ATTENDRE', 'REFUSER'):
        st, _ = SK.operational_state(dec, _gates(), {'entry': 100, 'tp2': 112})
        assert st in SK.OPERATIONAL_STATES
        assert st not in ('ACHETER', 'RENFORCER', 'ATTENDRE', 'REFUSER')


def test_decide_exposes_operational_state():
    d = SK.decide('OPX', _detail(), as_of='t')
    assert d['operational_state'] in SK.OPERATIONAL_STATES
    assert d['operational_state_basis']


# ─── Confiance factorisée avec plafonds ─────────────────────────────────────────

def test_confidence_factors_bounded_and_labelled():
    d = SK.decide('CFX', _detail(), as_of='t')
    c = d['confidence']
    assert c['estimated'] is True and c['method']
    f = c['factors']
    assert set(f) == {'data_quality', 'agreement', 'robustness', 'calibration'}
    for v in f.values():
        assert 0.0 <= v['value'] <= 1.0
        assert v['basis']
    assert 0.0 <= c['value'] <= 1.0


def test_confidence_never_full_without_calibration():
    d = SK.decide('CFX', _detail(), as_of='t')
    assert d['confidence']['factors']['calibration']['value'] <= 0.5
    assert d['confidence']['value'] < 1.0


def test_confidence_capped_on_unknown_regime():
    d = SK.decide('CFX', _detail(), market={'regime': {'label': 'UNKNOWN'}}, as_of='t')
    assert d['confidence']['value'] <= 0.55
    assert any('UNKNOWN' in cap for cap in d['confidence']['caps_applied'])


def test_confidence_capped_on_sources_conflict():
    m = {'regime': {'label': 'TREND_UP', 'confidence': 0.9},
         'conflicts': [{'dimension': 'vix'}]}
    d = SK.decide('CFX', _detail(), market=m, as_of='t')
    assert d['confidence']['value'] <= 0.50
    assert any('conflit' in cap or 'sources' in cap for cap in d['confidence']['caps_applied'])


def test_confidence_capped_on_contradiction():
    m = {'regime': {'label': 'RISK_OFF', 'confidence': 0.9,
                    'adjustments': {'new_risk_allowed': False}}}
    d = SK.decide('CFX', _detail(verdict='ACHETER'), market=m, as_of='t')
    assert d['contradictions']
    assert d['confidence']['value'] <= 0.60


def test_confidence_is_product_before_caps():
    d = SK.decide('CFX', _detail(), as_of='t')
    c = d['confidence']
    prod = 1.0
    for v in c['factors'].values():
        prod *= v['value']
    if not c['caps_applied']:
        assert c['value'] == pytest.approx(round(prod, 3))
    else:
        assert c['value'] <= round(prod, 3) + 1e-9


def test_confidence_deterministic():
    a = SK.decide('CFX', _detail(), as_of='t')
    b = SK.decide('CFX', _detail(), as_of='t')
    assert a['confidence'] == b['confidence'] and a['operational_state'] == b['operational_state']


# ─── La mémoire fige les nouveaux champs ────────────────────────────────────────

def test_memory_freezes_state_and_confidence_when_engine_provides():
    from vertex.engines import decision_memory as DM
    d = SK.decide('MFX', _detail(), as_of='t')
    packet = SK.build_packet('MFX', _detail(), as_of='t')
    r = DM.freeze(decision=d, packet=packet, price=100.0, closes=None,
                  portfolio_ctx=None, now=0)
    assert r['engine_version'] == SK.ENGINE_VERSION
    assert r['operational_state'] == d['operational_state']
    assert r['confidence'] == d['confidence']['value']
    assert r['confidence_factors'] is not None


def test_memory_stays_honest_for_old_records_without_fields():
    from vertex.engines import decision_memory as DM
    old = {'symbol': 'OLD', 'as_of': 't', 'decision': 'ATTENDRE',
           'score': {'total': 20, 'level': 'REFUS_WATCH', 'insufficient_blocks': []},
           'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': []}
    r = DM.freeze(decision=old, packet={'engine_version': '0.1.0'}, price=None,
                  closes=None, portfolio_ctx=None, now=0)
    assert r['operational_state'] is None            # absent ≠ inventé
    assert r['confidence'] is None
