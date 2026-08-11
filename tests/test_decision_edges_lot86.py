"""tests/test_decision_edges_lot86.py — SKYLER LOT 86 : cas limites du stack.

Tests de CARACTÉRISATION (moteur 0.9.0 INTACT — aucun calibrage modifié) :
ils FIGENT le comportement actuel des branches limites non couvertes par
tests/test_decision_stack.py. Nés verts (dits) — s'ils avaient trouvé un
résultat malhonnête, c'eût été un défaut réel à corriger.

Branches figées : detail=None honnête · score non numérique → 0 (jamais
un chiffre inventé) · bornes exactes 56/66/80 · verdict inconnu → WAIT ·
frontière « rassis » à 900 s · règle CHOP (cassure en range → surveiller)
· distribution cachée → surveiller · démo étiquetée · R:R absent ne
dégrade pas · véhicule ACTION hors décisions acheteuses.
"""
from vertex.engines import decision_stack as ds

BASE = {'price': 100, 'score': 70, 'verdict': 'BUY',
        'plan': {'entry': 100, 'stop': 95, 'rr_res': 2.5}}


def _d(**kw):
    d = dict(BASE)
    d.update(kw)
    return d


def test_none_detail_is_honestly_insufficient():
    r = ds.evaluate(None, symbol='XXX')
    assert r['final_decision'] == 'DATA_INSUFFICIENT'
    assert r['conviction'] == 0 and r['confidence'] == 0
    assert r['entry'] is None and r['stop'] is None


def test_garbage_score_never_invents_a_number():
    r = ds.evaluate(_d(score='n/a'))
    assert r['final_decision'] in ds.DECISIONS
    assert r['conviction'] == 0, 'score illisible → conviction 0, jamais inventée'


def test_exact_boundaries_56_66_80():
    assert ds._base_decision(_d(score=80)) == 'STRONG_BUY'
    assert ds._base_decision(_d(score=79.9)) == 'BUY'
    assert ds._base_decision(_d(score=66)) == 'BUY'
    assert ds._base_decision(_d(score=65.9)) == 'WATCH_BREAKOUT'
    assert ds._base_decision(_d(score=56, verdict='WATCH')) == 'WATCH_BREAKOUT'
    assert ds._base_decision(_d(score=55.9, verdict='WATCH')) == 'WAIT'


def test_unknown_verdict_falls_back_to_wait():
    r = ds.evaluate(_d(verdict='???'))
    assert r['final_decision'] == 'WAIT'


def test_stale_boundary_at_900_seconds():
    fresh = ds.assess_data_quality(BASE, scan_age_s=900)
    stale = ds.assess_data_quality(BASE, scan_age_s=901)
    assert fresh['stale'] is False and fresh['grade'] == 'A'
    assert stale['stale'] is True and stale['grade'] == 'B'
    assert stale['confidence_penalty'] == 15


def test_chop_breakout_is_watched_not_chased():
    r = ds.evaluate(_d(breakout=True), market={'spy_regime': 'CHOP'})
    assert r['final_decision'] == 'WATCH_BREAKOUT'
    assert any('range' in a for a in r['audit_trail'])


def test_hidden_distribution_downgrades_to_watch():
    r = ds.evaluate(_d(distribution=True))
    assert r['final_decision'] == 'WATCH_BREAKOUT'
    assert any('Distribution' in a for a in r['audit_trail'])


def test_demo_mode_is_always_labeled():
    r = ds.evaluate(_d(), demo=True)
    assert r['data_quality']['source'] == 'demo-synthetic'
    assert 'données synthétiques (démo)' in r['risk_flags']


def test_absent_rr_does_not_degrade():
    r = ds.evaluate(_d(plan={'entry': 100, 'stop': 95}))
    assert r['final_decision'] == 'BUY', 'R:R inconnu ≠ R:R mauvais'


def test_vehicle_is_action_outside_buyish_decisions():
    r = ds.evaluate(_d(verdict='WAIT'),
                    option={'spread': 1, 'oi': 5000, 'quality': 90})
    assert r['vehicle'] == 'ACTION'
