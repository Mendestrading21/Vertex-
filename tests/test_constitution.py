"""Constitution Stratégie Vertex — versioning, validation, invariants produit."""
import json
from pathlib import Path

import pytest

from vertex.strategy import constitution as C


def test_profile_loads_and_validates():
    p = C.load_profile()
    assert p.strategy_id == f'vertex_strategy_v{p.version}'
    assert p.display_name == 'Stratégie Vertex'
    assert p.portfolio_min_positions == 8
    assert p.portfolio_max_positions == 10
    assert p.portfolio_max_drawdown_pct == -25
    assert p.stock_max_drawdown_pct == -20
    assert p.max_simultaneous_options == 3


def test_strategy_is_versioned():
    versions = C.list_versions()
    assert versions, 'au moins une version de la constitution doit exister'
    assert versions == sorted(versions)
    p = C.load_profile(version=versions[-1])
    assert p.version == versions[-1]


def test_only_allowed_final_decisions():
    p = C.load_profile()
    assert set(p.allowed_final_decisions) == {
        'ACHETER', 'RENFORCER', 'ATTENDRE', 'REDUIRE', 'REFUSER'}


def test_analysis_order_is_canonical():
    p = C.load_profile()
    assert p.analysis_order == C.ANALYSIS_ORDER
    assert p.analysis_order[0] == 'FUNDAMENTAL'
    assert p.analysis_order[-1] == 'FINAL_DECISION'


def test_options_profile_forbids_selling():
    p = C.load_profile()
    opt = p.options_profile
    assert opt['primary_direction'] == 'LONG_CALL'
    for feature in C.FORBIDDEN_OPTION_FEATURES:
        assert not opt.get(feature), f'{feature} doit rester désactivé'


def test_dte_preferences():
    p = C.load_profile()
    dte = p.dte
    assert dte.preferred_minimum == 90
    assert dte.preferred_maximum == 210
    assert dte.absolute_minimum == 60
    assert dte.absolute_maximum == 270


def test_dynamic_delta_range():
    p = C.load_profile()
    dyn = p.category('DYNAMIC')
    assert dyn['delta_min'] == 0.28 and dyn['delta_max'] == 0.45
    assert dyn.get('primary') is True
    bal = p.category('BALANCED')
    assert bal['delta_min'] == 0.40 and bal['delta_max'] == 0.60
    ultra = p.category('ULTRA_CONVEX')
    assert ultra['delta_min'] == 0.18 and ultra['delta_max'] == 0.30
    assert ultra.get('rare_setup_only') is True


def test_proposal_without_confirmation_writes_nothing(tmp_path):
    src = C.PROFILES_DIR / 'vertex_strategy_v1.json'
    (tmp_path / 'vertex_strategy_v1.json').write_text(src.read_text(encoding='utf-8'),
                                                      encoding='utf-8')
    result = C.propose_new_version({'max_stock_weight_pct': 12},
                                   confirm=False, profiles_dir=tmp_path)
    assert result['written'] is False
    assert result['proposed_version'] == 2
    assert any('max_stock_weight_pct' in d for d in result['diff'])
    assert not (tmp_path / 'vertex_strategy_v2.json').exists(), \
        'sans confirmation humaine, rien ne doit être écrit'


def test_confirmed_proposal_keeps_old_version(tmp_path):
    src = C.PROFILES_DIR / 'vertex_strategy_v1.json'
    (tmp_path / 'vertex_strategy_v1.json').write_text(src.read_text(encoding='utf-8'),
                                                      encoding='utf-8')
    result = C.propose_new_version({'max_stock_weight_pct': 12},
                                   confirm=True, profiles_dir=tmp_path)
    assert result['written'] is True
    assert (tmp_path / 'vertex_strategy_v1.json').exists(), \
        "l'ancienne version doit être conservée (restauration possible)"
    new = C.load_profile(profiles_dir=tmp_path)
    assert new.version == 2 and new.max_stock_weight_pct == 12
    old = C.load_profile(version=1, profiles_dir=tmp_path)
    assert old.max_stock_weight_pct == 15


def test_invalid_proposal_is_rejected(tmp_path):
    src = C.PROFILES_DIR / 'vertex_strategy_v1.json'
    (tmp_path / 'vertex_strategy_v1.json').write_text(src.read_text(encoding='utf-8'),
                                                      encoding='utf-8')
    with pytest.raises(C.ConstitutionError):
        C.propose_new_version({'options_profile': {'short_options': True}},
                              confirm=True, profiles_dir=tmp_path)
    assert not (tmp_path / 'vertex_strategy_v2.json').exists()
    with pytest.raises(C.ConstitutionError):
        C.propose_new_version({'allowed_final_decisions': ['ACHETER', 'VENDRE']},
                              confirm=True, profiles_dir=tmp_path)


def test_profile_file_matches_spec():
    raw = json.loads((C.PROFILES_DIR / 'vertex_strategy_v1.json').read_text(encoding='utf-8'))
    assert raw['target_annual_return_pct'] == 30
    assert raw['target_is_guarantee'] is False
    assert raw['preferred_stock_weight_pct'] == [8, 12]
    assert raw['benchmark'] == 'SPY'
    assert raw['style'] == 'OFFENSIVE_HIGH_CONVICTION'
