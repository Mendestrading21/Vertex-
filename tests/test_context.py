"""
tests/test_context.py — Contexte relatif (analyse transversale).

Un titre situé parmi l'univers scanné : percentiles corrects, rang sectoriel,
langage clair, cas dégénérés sûrs.
"""

from vertex.engines import context


def _universe():
    # 5 titres, 2 secteurs
    return {
        'AAA': {'score': 95, 'rs': 90, 'mom': 80, 'setup_quality': 70, 'pos52': 88, 'sector': 'Tech'},
        'BBB': {'score': 70, 'rs': 60, 'mom': 55, 'setup_quality': 50, 'pos52': 60, 'sector': 'Tech'},
        'CCC': {'score': 50, 'rs': 45, 'mom': 40, 'setup_quality': 40, 'pos52': 40, 'sector': 'Tech'},
        'DDD': {'score': 30, 'rs': 30, 'mom': 25, 'setup_quality': 30, 'pos52': 20, 'sector': 'Energy'},
        'EEE': {'score': 60, 'rs': 55, 'mom': 50, 'setup_quality': 45, 'pos52': 50, 'sector': 'Energy'},
    }


def test_best_stock_is_leader_top_of_universe():
    c = context.context_for('AAA', _universe())
    sc = next(d for d in c['dimensions'] if d['key'] == 'score')
    assert sc['pct_universe'] == 90          # meilleur des 5 → mid-rank 90
    assert sc['standing'] == 'leader'
    assert c['universe_n'] == 5


def test_worst_stock_is_laggard():
    c = context.context_for('DDD', _universe())
    sc = next(d for d in c['dimensions'] if d['key'] == 'score')
    assert sc['pct_universe'] == 10          # pire des 5
    assert sc['standing'] == 'retardataire'


def test_sector_rank_and_headline():
    c = context.context_for('AAA', _universe())
    assert c['sector'] == 'Tech'
    assert c['sector_rank'] == 1 and c['sector_n'] == 3     # meilleur des 3 Tech
    assert 'Tech' in c['headline'] and '#1/3' in c['headline']


def test_sector_percentile_needs_enough_peers():
    # Energy n'a que 2 titres (< 3) → pct_sector reste None
    c = context.context_for('EEE', _universe())
    sc = next(d for d in c['dimensions'] if d['key'] == 'score')
    assert sc['pct_sector'] is None
    assert sc['pct_universe'] is not None


def test_unknown_symbol_is_none():
    assert context.context_for('ZZZ', _universe()) is None


def test_missing_fields_are_skipped_not_crashing():
    uni = {'X': {'score': 50, 'sector': 'Tech'}, 'Y': {'score': 60, 'sector': 'Tech'},
           'Z': {'score': 70, 'sector': 'Tech'}}
    c = context.context_for('Y', uni)
    keys = {d['key'] for d in c['dimensions']}
    assert keys == {'score'}                 # seul score présent → seule dimension notée
