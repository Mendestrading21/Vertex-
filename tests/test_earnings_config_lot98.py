"""tests/test_earnings_config_lot98.py — SKYLER LOT 98 : earnings + barème figés.

Trous réels de couverture : les MODES post-earnings d'earnings_engine
(réaction ≤ 2 j vs drift), la date inconnue, le run-up > 10 j, la
désinfection multi-phrases ; et les BORNES EXACTES du barème
grade/verdict de vertex/strategy/config.py (source unique des seuils).
Caractérisations nées vertes (dites) — moteurs INTACTS.
"""
from vertex.catalysts import earnings_engine as ee
from vertex.strategy import config


def test_unknown_earnings_date_is_honest():
    plan = ee.evaluate_earnings_plan(None)
    assert plan['mode'] is None and plan['hold_through_allowed'] is False
    assert any('inconnue' in n for n in plan['notes'])


def test_post_earnings_reaction_vs_drift():
    assert ee.evaluate_earnings_plan(-1)['mode'] == 'POST_EARNINGS_REACTION'
    assert ee.evaluate_earnings_plan(-2)['mode'] == 'POST_EARNINGS_REACTION'
    assert ee.evaluate_earnings_plan(-5)['mode'] == 'POST_EARNINGS_DRIFT'


def test_far_earnings_runup_with_exit_flag():
    plan = ee.evaluate_earnings_plan(45)
    assert plan['mode'] == 'PRE_EARNINGS_RUNUP'
    assert plan['exit_before_announcement'] is True, (
        'défaut constitution : on sort AVANT l\'annonce')


def test_near_earnings_without_dossier_lists_every_missing_requirement():
    plan = ee.evaluate_earnings_plan(5, hold_through_dossier=None)
    assert plan['hold_through_allowed'] is False
    assert set(plan['missing_requirements']) == set(ee.HOLD_THROUGH_REQUIRED), (
        'chaque exigence manquante est NOMMÉE — jamais un refus muet')


def test_sanitize_language_is_case_insensitive_and_repeatable():
    txt = 'GARANTI, Sans Risque et 99% sûr — foncez !'
    out = ee.sanitize_language(txt)
    low = out.lower()
    for phrase in ('garanti', 'sans risque', '99% sûr'):
        assert phrase not in low, phrase
    assert 'probabilité estimée, aucune promesse' in out


def test_grade_boundaries_exact():
    for score, g in ((90, 'S+'), (89.9, 'S'), (80, 'S'), (79.9, 'A'),
                     (72, 'A'), (71.9, 'B'), (60, 'B'), (59.9, 'C'),
                     (45, 'C'), (44.9, 'D'), (0, 'D')):
        assert config.grade(score) == g, (score, g)


def test_verdict_thresholds_and_chop_downgrade():
    assert config.verdict(80, 70) == 'BUY'
    assert config.verdict(80, 70, regime='CHOP') == 'WATCH', (
        'en range agité, jamais un BUY — les cassures échouent dans le bruit')
    assert config.verdict(80, 60) == 'WATCH'      # trend < 66 → pas d'achat
    assert config.verdict(65, 40) == 'WATCH'
    assert config.verdict(50, 55) == 'WAIT'
    assert config.verdict(30, 30) == 'AVOID'


def test_weights_and_buckets_are_complete():
    assert set(config.WEIGHTS) == {'technical', 'momentum', 'fundamental',
                                   'options', 'risk'}
    assert sum(config.WEIGHTS.values()) == 100
    for b in config.OPTION_BUCKETS.values():
        assert b['min'] < b['target'] < b['max']
        assert 0 < b['delta_lo'] < b['delta_hi'] < 1
