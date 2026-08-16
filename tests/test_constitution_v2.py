"""tests/test_constitution_v2.py — SKYLER LOT 2 : Constitution stratégique V2.

Exigences du skill (TRADING_CONSTITUTION_V2.md) : V2 créée PAR le mécanisme de
versioning (V1 jamais modifiée), niveaux S+/S/A/B, portefeuille 8–15 lignes,
mandat LEAPS 180–540 DTE / delta 0,70–0,90, règles gagnants/perdants,
versioning + diff + rollback prouvés.
"""
import json

from vertex.strategy import constitution as C


# ─── V2 existe par versioning, V1 intacte ───────────────────────────────────────

def test_v1_v2_v3_exist_and_v3_is_latest():
    versions = C.list_versions()
    assert {1, 2, 3}.issubset(set(versions))
    assert C.load_profile().version == 3          # dernière version par défaut


def test_v1_untouched_byte_identical_values():
    """La V1 reste chargeable et garde ses valeurs historiques exactes (rollback)."""
    p1 = C.load_profile(version=1)
    assert p1.portfolio_min_positions == 8 and p1.portfolio_max_positions == 10
    assert p1.dte.absolute_maximum == 270
    raw1 = json.loads((C.PROFILES_DIR / 'vertex_strategy_v1.json').read_text(encoding='utf-8'))
    assert raw1['version'] == 1
    assert 'conviction_levels' not in raw1        # la V1 n'a pas été enrichie en douce


def test_diff_v1_v2_is_explicit():
    old = C.load_profile(version=1).raw
    new = C.load_profile(version=2).raw
    diff = C.diff_profiles(old, new)
    assert any('conviction_levels' in d for d in diff)
    assert any('portfolio_target_positions' in d for d in diff)
    assert any('LEAPS' in d for d in diff)


# ─── Contenu V2 : niveaux S+/S/A/B ──────────────────────────────────────────────

def test_conviction_levels_s_plus_to_b():
    lv = C.load_profile().raw['conviction_levels']
    assert lv['S_PLUS']['score_min'] == 36 and lv['S_PLUS']['score_max'] == 40
    assert lv['S_PLUS']['allocation_pct'] == [10, 15]
    assert lv['S']['score_min'] == 32 and lv['S']['allocation_pct'] == [7, 10]
    assert lv['A']['score_min'] == 28 and lv['A']['allocation_pct'] == [3, 5]
    assert lv['B']['score_min'] == 24 and lv['B']['allocation_pct'] == [1, 2]
    assert lv['refusal_below_score'] == 24
    # plafonds ANALYTIQUES — jamais un ordre
    assert lv['allocations_are_analytical_caps'] is True
    assert lv['never_triggers_orders'] is True


def test_skyler_score_blocks_sum_to_40():
    sc = C.load_profile().raw['skyler_score']
    assert sc['total'] == 40
    assert sum(sc['blocks'].values()) == 40
    assert sc['blocks']['options_quality'] == 6
    assert sc['blocks']['asymmetry_scenarios'] == 6
    assert sc['blocks']['data_quality'] == 4


# ─── Portefeuille 8–15 ──────────────────────────────────────────────────────────

def test_portfolio_8_to_15_positions():
    p = C.load_profile()
    assert p.portfolio_min_positions == 8
    assert p.portfolio_max_positions == 15


# ─── Mandat LEAPS ───────────────────────────────────────────────────────────────

def test_leaps_category_delta_and_dte():
    p = C.load_profile()
    leaps = p.category('LEAPS')
    assert leaps['delta_min'] == 0.70 and leaps['delta_max'] == 0.90
    assert leaps['preferred_dte'] == [180, 540]
    assert leaps['requires_catalyst'] is True
    assert leaps['requires_invalidation'] is True
    assert leaps['iv_crush_check_required'] is True
    assert leaps['double_probability_labeled'] is True


def test_universes_include_swing_3_6m():
    u = C.load_profile().options_profile['universes']
    assert u['TACTICAL'] == [20, 60]
    assert u['SWING'] == [60, 180]
    assert u['SWING_3_6M'] == [75, 210]
    assert u['LEAPS'] == [180, 540]
    swing = C.load_profile().options_profile['swing_3_6m']
    assert swing['preferred_dte'] == [90, 180]
    assert swing['holding_plan_sessions'] == [5, 10, 15]


def test_dte_absolute_max_admits_leaps():
    dte = C.load_profile().dte
    assert dte.absolute_maximum == 540            # admission LEAPS
    assert dte.absolute_minimum == 60
    assert dte.preferred_minimum == 90 and dte.preferred_maximum == 210


def test_selling_still_forbidden_in_v2():
    opt = C.load_profile().options_profile
    for feature in C.FORBIDDEN_OPTION_FEATURES:
        assert not opt.get(feature), f'{feature} doit rester désactivé en V2'
    assert opt['primary_direction'] == 'LONG_CALL'


# ─── Règles gagnants / perdants ─────────────────────────────────────────────────

def test_position_rules_winners_losers():
    pr = C.load_profile().raw['position_rules']
    assert pr['never_add_to_losers'] is True
    assert 'BREAKOUT_CONFIRMED' in pr['add_only_after_confirmation']
    assert pr['winner_management']['auto_sell_at_100_pct'] is False
    assert pr['winner_management']['partial_secure_share_pct'] == [25, 50]
    assert pr['winner_management']['keep_runner_if_thesis_valid'] is True
    assert pr['reward_risk_min'] == 2.0


def test_hard_gates_listed():
    gates = C.load_profile().raw['hard_gates']
    for g in ('RR_BELOW_2', 'NO_INVALIDATION', 'DATA_QUALITY_CRITICAL',
              'UNBOUNDED_RISK_UNFLAGGED', 'LOSER_REINFORCEMENT',
              'CONCENTRATION_EXCESSIVE', 'DTE_OUT_OF_MANDATE'):
        assert g in gates, f'hard gate manquant : {g}'


# ─── Le moteur exécutif et les moteurs options fonctionnent sous V3 ─────────────

def test_executive_engine_runs_under_v3():
    from vertex.strategy import executive_engine as EE
    out = EE.decide({'symbol': 'X'}, C.load_profile())
    assert out['symbol'] == 'X'
    assert list(out['analysis_order']) == list(C.ANALYSIS_ORDER)  # scaffold canonique intact


def test_multileg_mandate_reads_v3():
    from vertex.engines import multileg_lab as ml
    ml._MANDATE_CACHE['loaded'] = False           # force le rechargement
    m = ml._options_mandate()
    assert m['profile_version'] == 3
    assert m['dte_max'] == 540
    assert m['short_options'] is False
    ml._MANDATE_CACHE['loaded'] = False           # ne pas polluer les autres tests
