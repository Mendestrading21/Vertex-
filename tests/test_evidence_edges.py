"""tests/test_evidence_edges.py — SKYLER LOT 88 : evidence + reasoning figés.

Tests de CARACTÉRISATION (moteurs INTACTS) : branches limites non
couvertes par tests/test_evidence.py (9), test_reasoning.py (7) et
test_evidence_lab_x2.py (8). Nés verts (dits) — le comportement actuel
des cas limites est figé.
"""
from vertex.engines import evidence as ev
from vertex.engines import reasoning as rs


def test_gather_with_nothing_is_honest_and_complete():
    b = ev.gather(None)
    for k in (ev.POSITIVE, ev.NEGATIVE, ev.NEUTRAL, ev.UNKNOWN, ev.CONTRADICTORY):
        assert b[k] == [], k
    assert b['balance'] == 0
    assert b['has_contradiction'] is False
    assert b['regime'] is None


def test_absent_analyst_inputs_produce_no_evidence():
    assert ev.market_analyst(None) == []
    assert ev.options_analyst(None) == []
    assert ev.relative_analyst(None) == []
    assert ev.data_quality_analyst(None) == []


def test_ev_strength_is_clamped_0_100():
    assert ev._ev('positive', 'x', -50, 'S')['strength'] == 0
    assert ev._ev('positive', 'x', 500, 'S')['strength'] == 100


def test_catalyst_exact_boundaries():
    assert ev.catalyst_analyst({'vol_z': 2.5}) != []      # 2.5 déclenche
    assert ev.catalyst_analyst({'vol_z': 2.49}) == []
    assert ev.catalyst_analyst({'gap_pct': -4}) != []     # |gap| = 4 déclenche
    assert ev.catalyst_analyst({'gap_pct': 3.9}) == []


def test_fundamental_zero_means_absent_not_negative():
    # note 0 = fondamentaux non branchés → AUCUNE preuve (jamais punir l'absent)
    assert ev.fundamental_analyst({'sub': {'fundamental': 0}}) == []
    assert ev.fundamental_analyst({'sub': {'fundamental': 35}})[0]['kind'] == ev.NEGATIVE


def test_missing_fields_wins_over_stale():
    out = ev.data_quality_analyst({'missing_fields': ['price'], 'stale': True})
    assert len(out) == 1 and out[0]['kind'] == ev.UNKNOWN


def test_chaos_with_stacked_trend_is_a_contradiction():
    b = ev.gather({'physics': {'state': 'CHAOS'},
                   'signals': {'stacked': True, 'above200': True}})
    texts = [c['text'] for c in b[ev.CONTRADICTORY]]
    assert any('chaotique' in t for t in texts)


def test_scenarios_with_empty_detail_never_crash_never_invent():
    scen = rs.scenarios(None, None, 'WAIT')
    assert len(scen) == 3
    for s in scen:
        assert s['move_pct'] is None, 'sans prix de base, jamais un % inventé'
        assert s['trigger'] and s['invalidation']
    weights = sum(s['weight'] for s in scen)
    assert 95 <= weights <= 105


def test_weights_with_no_committee_are_balanced():
    w = rs._weights(None, 'WAIT')
    assert w['bull'][0] == w['bear'][0], 'sans comité, aucun biais inventé'


def test_invalidations_always_actionable_and_capped():
    out = rs.invalidations({'plan': {'stop': 95}, 'signals': {'above200': False},
                            'distribution': True})
    assert len(out) == 4                       # plafonné à 4
    assert any('stop de la thèse' in x for x in out)
    empty = rs.invalidations(None)
    assert empty and 'RISK-OFF' in empty[-1], 'le régime de marché reste toujours cité'
