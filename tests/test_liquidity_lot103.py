"""tests/test_liquidity_lot103.py — SKYLER LOT 103 : barème de liquidité figé.

Trou réel de couverture : vertex/options/liquidity.py (assess — le juge
de traitabilité d'un contrat, consommé par le sélecteur et l'affichage)
n'avait qu'UN test superficiel (spread_pct >= 0 dans
test_calculations_golden). Le barème complet — refus bid/ask, pénalité
dégressive 4-10 %, OI inconnu ≠ OI faible, volume silencieux vs nommé,
seuil tradeable 40 — n'était figé nulle part.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
from vertex.options import liquidity as lq


def _c(**kw):
    base = {'bid': 10.0, 'ask': 10.2, 'mid': 10.1,
            'open_interest': 1000, 'volume': 100}
    base.update(kw)
    return base


def test_missing_or_zero_bid_ask_is_untradeable_score_zero():
    for bad in ({'bid': None}, {'ask': None}, {'bid': 0.0}, {'ask': -1.0}):
        r = lq.assess(_c(**bad))
        assert r == {'score': 0.0, 'tradeable': False,
                     'issues': ['bid/ask absent — contrat non traitable']}, bad


def test_perfect_contract_scores_100_no_issues():
    r = lq.assess(_c())        # spread 1.98 % ≤ 4 %
    assert r['score'] == 100.0 and r['tradeable'] is True
    assert r['issues'] == [] and r['spread_pct'] == 1.98


def test_degressive_penalty_between_4_and_10_pct_without_issue():
    # spread 7 % pile → 100 − (7−4)/(10−4)·25 = 87.5 ; zone grise SANS issue
    r = lq.assess(_c(bid=9.65, ask=10.35, mid=10.0))
    assert r['spread_pct'] == 7.0 and r['score'] == 87.5
    assert r['tradeable'] is True and r['issues'] == []


def test_wide_spread_is_named_and_blocks_tradeable_despite_score():
    r = lq.assess(_c(bid=9.0, ask=11.0, mid=10.0))   # 20 %
    assert r['score'] == 55.0                         # 100 − 45
    assert r['tradeable'] is False, (
        'spread > 10 % : jamais traitable, même avec un score ≥ 40')
    assert r['issues'] == ['spread 20.0% > 10.0%']


def test_missing_mid_means_spread_unknown_treated_as_100pct():
    r = lq.assess(_c(mid=None))
    assert r['spread_pct'] == 100.0 and r['tradeable'] is False


def test_unknown_oi_penalized_less_than_low_oi():
    unknown = lq.assess(_c(open_interest=None))
    low = lq.assess(_c(open_interest=100))
    assert unknown['score'] == 85.0                   # −15 « inconnu »
    assert unknown['issues'] == ['intérêt ouvert inconnu']
    assert low['score'] == 70.0                       # −30 « trop faible »
    assert low['issues'] == ['OI 100 < 200']
    assert unknown['score'] > low['score'], (
        'ne pas savoir coûte moins cher que savoir que c\'est illiquide')


def test_volume_none_is_silent_but_low_volume_is_named():
    silent = lq.assess(_c(volume=None))
    named = lq.assess(_c(volume=5))
    assert silent['score'] == 95.0 and silent['issues'] == []
    assert named['score'] == 90.0 and named['issues'] == ['volume 5 < 10']


def test_penalties_accumulate_exactly():
    r = lq.assess(_c(bid=9.0, ask=11.0, mid=10.0, open_interest=100, volume=5))
    assert r['score'] == 15.0                         # 100 − 45 − 30 − 10
    assert r['tradeable'] is False and len(r['issues']) == 3
