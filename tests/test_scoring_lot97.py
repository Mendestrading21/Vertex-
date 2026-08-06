"""tests/test_scoring_lot97.py — SKYLER LOT 97 : scoring pur figé.

`vertex/quant/scoring.py` (les fonctions PURES du score /100 — le cœur
chiffré que toute l'app affiche) n'avait que 5 tests indirects
(test_foundation). Caractérisations nées vertes (dites) — moteur INTACT.
"""
import numpy as np

from vertex.quant import scoring
from vertex.strategy import config


def test_all_subscores_clipped_0_100_on_extremes():
    maxed = {'above20': True, 'above50': True, 'above200': True, 'stacked': True,
             'golden': True, 'rsi': 60, 'roc': 100, 'rs': 100, 'volx': 5,
             'pos52': 50, 'atr_pct': 0, 'ext_atr': 0}
    floor = {'rsi': 100, 'roc': -100, 'rs': 0, 'volx': 0, 'atr_pct': 50,
             'pos52': 99, 'ext_atr': 9}
    for fn in (scoring.technical_score, scoring.momentum_score,
               scoring.fundamental_score, scoring.risk_score):
        assert 0 <= fn(maxed) <= 100
        assert 0 <= fn(floor) <= 100


def test_empty_indicators_exact_neutral_values():
    # Figé : dict vide → valeurs neutres EXACTES (défauts rsi 50, volx 1.0…)
    assert scoring.technical_score({}) == 18.0
    assert scoring.momentum_score({}) == 50.0
    assert scoring.fundamental_score({}) == 45.0     # proxy sans force relative
    assert scoring.risk_score({}) == 64.0            # 72 − 8 (atr_pct défaut 2.0)


def test_momentum_roc_is_clipped_at_25():
    a = scoring.momentum_score({'roc': 25})
    b = scoring.momentum_score({'roc': 250})
    assert a == b, 'un ROC extrême ne peut pas dominer le momentum (clip ±25)'


def test_fundamental_real_vs_proxy():
    real = scoring.fundamental_score({}, fund={'pe': 10, 'sector_median_pe': 20})
    assert real == 62.0                             # 50 + 12 (décote ≤ 0,75× pairs)
    proxy = scoring.fundamental_score({'rs': 70, 'stacked': True})
    assert proxy == 45 + 20 * 0.6 + 15              # formule proxy exacte


def test_options_score_none_and_earnings_crush_penalty():
    assert scoring.options_score(None) is None, 'pas d\'option → None, jamais 0 inventé'
    base = {'bucket': 'long', 'oi': 5000, 'spread_pct': 4, 'delta': 0.7,
            'dte': 150, 'iv_rank': 40, 'tech_ok': True, 'theta_burn': 0.2}
    clean = scoring.options_score(dict(base))
    crush = scoring.options_score(dict(base, earnings_dte=30))
    assert clean - crush == 10, 'échéance couvrant un earnings → −10 (IV-crush)'


def test_court_bucket_expensive_iv_double_penalty():
    base = {'bucket': 'court', 'oi': 5000, 'spread_pct': 4, 'delta': 0.55,
            'dte': 45, 'tech_ok': True, 'theta_burn': 0.2}
    cheap = scoring.options_score(dict(base, iv_rank=40))
    dear = scoring.options_score(dict(base, iv_rank=85))
    assert cheap - dear >= 10, 'court + IV chère = double peine au crush'


def test_compose_flags_proxy_and_confidence_is_selfconsistent():
    out = scoring.compose({})
    assert out['fundamental_is_proxy'] is True, 'proxy TOUJOURS signalé (honnêteté)'
    assert 'options' not in out, 'sans option, aucun sous-score options inventé'
    core = [out['technical'], out['momentum'], out['fundamental'], out['risk']]
    expected = round(max(0.0, min(100.0, 100 - min(float(np.std(core)) * 2.5, 60))))
    assert abs(out['confidence'] - expected) <= 1, (
        'confiance = alignement des sous-scores (écart-type), auto-cohérente')
    assert out['grade'] == config.grade(sum(config.WEIGHTS[k] * out[k]
                                            for k in ('technical', 'momentum',
                                                      'fundamental', 'risk'))
                                        / sum(config.WEIGHTS[k]
                                              for k in ('technical', 'momentum',
                                                        'fundamental', 'risk')))


def test_compose_with_real_fundamentals_clears_proxy_flag():
    out = scoring.compose({}, fund={'pe': 15, 'sector_median_pe': 20,
                                    'margin': 0.2, 'growth': 0.1})
    assert out['fundamental_is_proxy'] is False
