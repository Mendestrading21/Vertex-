"""
tests/test_stats.py — Statistiques d'agrégation (Spearman + médianes secteur).

Helpers purs extraits du monolithe. Bornes, cas dégénérés, valeurs golden.
"""

from vertex.engines import stats


def test_spearman_golden_and_bounds():
    assert stats.spearman([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]) == 0.939
    assert stats.spearman(list(range(12)), list(range(12))) == 1.0            # monotone parfait
    assert stats.spearman(list(range(12)), list(range(11, -1, -1))) == -1.0   # anti-monotone


def test_spearman_too_few_points_is_none():
    assert stats.spearman([1, 2, 3], [3, 2, 1]) is None                       # < 8 points → None


def test_sector_medians_golden():
    by_sym = {
        'A': {'sector': 'Tech', 'pe': 30, 'fwd_pe': 25, 'margin': 0.2, 'growth': 0.15},
        'B': {'sector': 'Tech', 'pe': 40, 'fwd_pe': 35, 'margin': 0.3, 'growth': 0.25},
        'C': {'sector': 'Energy', 'pe': 12, 'margin': 0.1, 'growth': 0.05},
        'D': {'sector': 'Tech', 'pe': 500, 'margin': None, 'growth': None},   # PE aberrant filtré
    }
    sec = stats.sector_medians(by_sym)
    assert sec['Tech']['median_pe'] == 35.0        # 500 exclu (>250), médiane de {30,40}
    assert sec['Tech']['median_margin'] == 25.0    # en %
    assert sec['Tech']['n'] == 3
    assert sec['Energy']['median_fwd_pe'] is None   # pas de fwd_pe → None, pas de crash


def test_terminal_bindings_are_the_module():
    import terminal
    assert terminal._spearman is stats.spearman
    assert terminal._recompute_sectors is stats.sector_medians
