"""
tests/test_evidence.py — Le comité d'analystes (couche de preuves).

Nouveaux analystes (fondamental, catalyseur) + pondération par régime de marché.
Chaque preuve reste atomique, signée, bornée 0-100.
"""

from vertex.engines import evidence as ev


def test_fundamental_analyst_reads_subscore():
    strong = ev.fundamental_analyst({'sub': {'fundamental': 82}})
    weak = ev.fundamental_analyst({'sub': {'fundamental': 25}})
    assert strong and strong[0]['kind'] == ev.POSITIVE and strong[0]['source'] == 'Fondamental'
    assert weak and weak[0]['kind'] == ev.NEGATIVE
    assert ev.fundamental_analyst({'sub': {'fundamental': 50}}) == []   # zone neutre → silence


def test_catalyst_analyst_flags_unusual_activity():
    vol = ev.catalyst_analyst({'vol_z': 3.1})
    gap = ev.catalyst_analyst({'gap_pct': -6})
    calm = ev.catalyst_analyst({'vol_z': 1.0, 'gap_pct': 0.5})
    assert vol and vol[0]['kind'] == ev.NEUTRAL and vol[0]['source'] == 'Catalyseur'
    assert gap and gap[0]['kind'] == ev.NEUTRAL
    assert calm == []


def test_regime_trend_amplifies_momentum():
    d = {'rs': 80, 'sub': {}}                      # momentum positif fort
    base = ev.gather(d, market={'spy_regime': 'NEUTRAL'})
    trend = ev.gather(d, market={'spy_regime': 'TREND'})
    def mom(buckets):
        return next((x['strength'] for x in buckets['positive'] if x['source'] == 'Momentum'), 0)
    assert mom(trend) > mom(base)                  # en tendance, le momentum pèse plus


def test_regime_chop_dampens_momentum():
    d = {'rs': 80, 'sub': {}}
    base = ev.gather(d, market={'spy_regime': 'NEUTRAL'})
    chop = ev.gather(d, market={'spy_regime': 'CHOP'})
    def mom(buckets):
        return next((x['strength'] for x in buckets['positive'] if x['source'] == 'Momentum'), 0)
    assert mom(chop) < mom(base)                    # en range, le momentum pèse moins


def test_risk_off_amplifies_negatives():
    d = {'plan': {'rr_res': 1.0}, 'sub': {}}        # R:R faible → preuve négative
    calm = ev.gather(d, market={'roro': 'RISK-ON'})
    off = ev.gather(d, market={'roro': 'RISK-OFF'})
    def neg(buckets):
        return sum(x['strength'] for x in buckets['negative'])
    assert neg(off) > neg(calm)                     # en RISK-OFF, les risques pèsent plus


def test_strength_stays_bounded_after_weighting():
    d = {'rs': 95, 'mtf': {'state': 'ALIGNÉ HAUSSIER'}, 'sub': {}}
    for regime in ('TREND', 'CHOP', 'NEUTRAL'):
        for it in ev.gather(d, market={'spy_regime': regime, 'roro': 'RISK-OFF'})['positive']:
            assert 0 <= it['strength'] <= 100


def test_relative_analyst_reads_cross_sectional_standing():
    leader = {'dimensions': [{'key': 'score', 'value': 90, 'pct_universe': 95, 'standing': 'leader'}],
              'sector_rank': 1, 'sector_n': 5, 'sector': 'Energy'}
    laggard = {'dimensions': [{'key': 'score', 'value': 20, 'pct_universe': 8, 'standing': 'retardataire'}],
               'sector_rank': 9, 'sector_n': 10, 'sector': 'Tech'}
    pos = ev.relative_analyst(leader)
    neg = ev.relative_analyst(laggard)
    assert any(e['kind'] == ev.POSITIVE and 'top' in e['text'].lower() for e in pos)
    assert any('Leader de son secteur' in e['text'] for e in pos)
    assert neg and neg[0]['kind'] == ev.NEGATIVE
    assert ev.relative_analyst(None) == []                     # pas de contexte → silence


def test_context_flows_into_committee_and_result():
    from vertex.engines import decision_stack as ds
    d = {'symbol': 'T', 'price': 100, 'score': 88,
         'plan': {'entry': 100, 'stop': 92, 'tp2': 116, 'rr_res': 2.0}}
    ctx = {'dimensions': [{'key': 'score', 'value': 88, 'pct_universe': 96, 'standing': 'leader'}],
           'sector_rank': 1, 'sector_n': 4, 'sector': 'Energy', 'headline': 'Top 4% de l\'univers'}
    r = ds.evaluate(d, context=ctx)
    assert r['context']['headline'] == 'Top 4% de l\'univers'
    assert 'Transversal' in [m['member'] for m in r['committee']['members']]


def test_new_members_reach_the_committee():
    from vertex.engines import decision_stack as ds
    d = {'symbol': 'T', 'price': 100, 'score': 80, 'sub': {'fundamental': 85},
         'vol_z': 3.0, 'plan': {'entry': 100, 'stop': 92, 'tp2': 116, 'rr_res': 2.0}}
    r = ds.evaluate(d, market={'spy_regime': 'TREND'})
    members = [m['member'] for m in r['committee']['members']]
    assert 'Fondamental' in members
    assert r['committee']['watch_signals']          # catalyseur remonté
