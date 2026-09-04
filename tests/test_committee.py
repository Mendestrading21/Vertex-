"""tests/test_committee.py — SKYLER LOT 92 : committee.py figé.

`vertex/engines/committee.py` (le comité d'investissement : 4 portes,
verdicts ACHETER/RENFORCER/ATTENDRE/ÉVITER, anti-impatience) n'avait
AUCUN test dédié. Caractérisations nées vertes (dites) — moteur INTACT.
"""
from vertex.engines import committee as cm

GOOD = {'score': 80, 'grade': 'A', 'price': 100, 'rsi': 55, 'ext_atr': 1,
        'pos52': 70, 'mom': 72, 'regime': 'TREND',
        'signals': {'above50': True, 'goldenNow': True},
        'plan': {'entry': 100, 'stop': 92, 'resistance': 120, 'rr_res': 2.5,
                 'tp2': 115, 'tp3': 124},
        'structure': {'trend': 'UP', 'confirmed': True, 'logic': 'Cassure reprise.',
                      'last_high': 118, 'last_low': 94}}


def _d(**kw):
    d = {k: (dict(v) if isinstance(v, dict) else v) for k, v in GOOD.items()}
    d.update(kw)
    return d


def test_empty_universe_says_no_buy_honestly():
    out = cm.evaluate([], {})
    assert out['decisions'] == []
    assert out['counts'] == {'ACHETER': 0, 'RENFORCER': 0, 'ATTENDRE': 0, 'ÉVITER': 0}
    assert 'AUCUN ACHAT' in out['verdict_global']
    assert out['rr_min'] == 2.0


def test_symbol_without_detail_is_skipped():
    out = cm.evaluate([{'symbol': 'GHOST'}], {})
    assert out['decisions'] == []


def test_low_quality_is_avoided():
    r = cm._evaluate_one('XX', _d(score=50, grade='C'))
    assert r['verdict'] == 'ÉVITER' and 'Qualité insuffisante' in r['note']


def test_downtrend_rebound_is_a_trap_never_bought():
    r = cm._evaluate_one('XX', _d(structure={'trend': 'DOWN', 'confirmed': False,
                                             'last_high': 110, 'last_low': 90}))
    assert r['verdict'] == 'ÉVITER'
    assert 'PIÈGE' in r['note'], 'un rebond en tendance baissière est refusé explicitement'


def test_overextended_waits_for_pullback():
    r = cm._evaluate_one('XX', _d(ext_atr=3.5))
    assert r['verdict'] == 'ATTENDRE' and 'étendu' in r['note']


def test_chop_timing_waits():
    r = cm._evaluate_one('XX', _d(regime='CHOP'))
    assert r['verdict'] == 'ATTENDRE' and 'range (chop)' in r['note']


def test_entry_zone_formula_and_in_zone_buy():
    # R:R < 2 sans structure confirmée ni cassure → la zone d'achat est calculée :
    # entrée ≤ (résistance + 2·stop)/3 = (120 + 184)/3 ≈ 101,33 — mais elle doit
    # être SOUS le cours pour être un repli réaliste.
    base = _d(plan={'entry': 100, 'stop': 92, 'resistance': 120, 'rr_res': 1.5},
              structure={'trend': 'UP', 'confirmed': False}, pos52=50, mom=50)
    waiting = cm._evaluate_one('XX', dict(base, price=110))
    assert waiting['verdict'] == 'ATTENDRE'
    assert waiting['entry_zone'] == round((120 + 2 * 92) / 3, 2)
    assert 'Zone d\'achat' in waiting['note']
    buying = cm._evaluate_one('XX', dict(base, price=100))
    assert buying['verdict'] == 'ACHETER' and buying['in_zone'] is True
    assert 'DANS LA ZONE' in buying['note'], 'le repli atteint → fenêtre ouverte, dit'


def test_confirmed_structure_elite_vs_build():
    elite = cm._evaluate_one('XX', _d(score=80))
    build = cm._evaluate_one('XX', _d(score=68))
    assert elite['verdict'] == 'ACHETER' and 'élite' in elite['note']
    assert build['verdict'] == 'RENFORCER'


def test_global_verdict_thresholds_and_sorting():
    detail = {'A1': _d(score=80), 'A2': _d(score=80), 'A3': _d(score=80),
              'W1': _d(regime='CHOP'), 'E1': _d(score=40, grade='C')}
    rows = [{'symbol': s} for s in detail]
    out = cm.evaluate(rows, detail)
    assert out['counts']['ACHETER'] == 3
    assert 'déployer avec discipline' in out['verdict_global']
    verdicts = [x['verdict'] for x in out['decisions']]
    assert verdicts == sorted(verdicts, key=lambda v: cm._ORDER[v]), (
        'ACHETER toujours listé avant ATTENDRE avant ÉVITER')
