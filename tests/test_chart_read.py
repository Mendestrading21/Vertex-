"""tests/test_chart_read.py — SKYLER LOT 118 : lecture graphique figée.

Trou réel de couverture : vertex/research/chart_read.py (169 lignes —
la lecture technique FR dérivée UNIQUEMENT des indicateurs calculés,
zéro donnée inventée) n'avait AUCUN test direct.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
from vertex.research.chart_read import chart_read, chart_verdict, thesis


def test_none_and_empty_are_none_minimal_reads_fragile_defaults():
    assert chart_read(None) is None
    assert chart_read({}) is None, 'dict vide = pas de données → None (falsy)'
    assert chart_read({'rsi': 50}) == ('sous la MM200 (structure fragile) · '
                                       'RSI 50 (momentum sain)'), (
        'défauts honnêtes : sans signaux = fragile, RSI 50 neutre, rien d\'autre')


def test_trend_structure_hierarchy():
    stacked = chart_read({'signals': {'stacked': True}})
    assert 'MM20 > MM50 > MM200 empilées' in stacked
    fond = chart_read({'signals': {'above200': True, 'above50': True}})
    assert 'fond haussier' in fond
    conso = chart_read({'signals': {'above200': True}})
    assert 'consolidation' in conso


def test_rsi_thresholds_78_60_48():
    assert 'surchauffe' in chart_read({'rsi': 78})
    assert 'momentum fort' in chart_read({'rsi': 60})
    assert 'momentum sain' in chart_read({'rsi': 48})
    assert 'momentum faible' in chart_read({'rsi': 47.9})


def test_range_extension_volume_and_relative_strength_cues():
    r = chart_read({'pos52': 92, 'ext_atr': 4.2, 'volx': 1.5, 'rs': 70})
    assert 'collé aux plus-hauts 52s (92%)' in r
    assert 'sur-étendu (4.2 ATR' in r
    assert 'volume soutenu (1.5×' in r
    assert 'surperforme le marché (force relative 70)' in r
    low = chart_read({'pos52': 25, 'volx': 0.6, 'rs': 35})
    assert 'bas de range' in low and 'volume sec' in low and 'sous-performe' in low


def test_accumulation_wins_over_distribution_when_both():
    both = chart_read({'accumulation': True, 'distribution': True})
    assert 'accumulation détectée' in both and 'distribution cachée' not in both, (
        'réalité figée : le elif donne la priorité à l\'accumulation')
    assert 'divergence baissière' in chart_read({'rsi_div': 'bear'})
    assert 'divergence haussière' in chart_read({'rsi_div': 'bull'})


def test_chart_verdict_four_outcomes():
    assert chart_verdict(None) is None
    ok = chart_verdict({'signals': {'stacked': True}, 'score': 72, 'ext_atr': 1})
    assert ok.startswith('✓') and 'CALL' in ok
    wait = chart_verdict({'signals': {'stacked': True}, 'ext_atr': 4})
    assert wait.startswith('⚠') and 'attendre un repli' in wait
    no = chart_verdict({'signals': {}})
    assert no.startswith('⛔') and 'sous la MM200' in no
    mixed = chart_verdict({'signals': {'above200': True}, 'score': 50})
    assert mixed.startswith('≈')


def test_thesis_driver_priority_distribution_first():
    d = {'verdict': 'BUY', 'score': 80, 'grade': 'S',
         'distribution': True, 'breakout': True}
    t = thesis(d)
    assert t.startswith("signal d'ACHAT · score 80/100 (S)")
    assert 'Distribution cachée' in t and 'cassure confirmée' not in t, (
        'la méfiance PRIME toujours sur l\'enthousiasme (driver capitalisé en tête)')


def test_thesis_play_by_profile_and_mtf_wind():
    off = thesis({'verdict': 'WATCH', 'score': 70, 'grade': 'A',
                  'profile': 'OFFENSIF', 'regime': 'TREND',
                  'plan': {'rr_res': 2.5},
                  'mtf': {'state': 'ALIGNÉ HAUSSIER'}})
    assert 'CALL court/moyen (1-8 sem)' in off
    assert 'R:R ~2.5:1 vers la résistance' in off
    assert 'vent porteur, pleine conviction' in off
    defensive = thesis({'verdict': 'WAIT', 'score': 50, 'grade': 'C',
                        'profile': 'DÉFENSIF'})
    assert 'action ou LEAPS long' in defensive
