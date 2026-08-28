"""Gardiens de la source de vérité Vertex 1.0."""

from pathlib import Path

import vertex
from vertex.app.config import ANALYSIS_ONLY, READONLY
from vertex.product import (
    CANONICAL_SPACES,
    DAILY_INTELLIGENCE_MANDATE,
    EQUITY_MANDATE,
    OPTIONS_MANDATE,
    ORDER_EXECUTION,
)
from vertex.strategy.constitution import list_versions, load_profile
from vertex.strategy.release import list_release_versions, load_release_profile


ROOT = Path(__file__).resolve().parents[1]


def test_product_version_and_analysis_only_invariant():
    assert vertex.__version__ == "1.0.0rc1"
    assert vertex.RELEASE_CHANNEL == "release-candidate"
    assert READONLY is True
    assert ANALYSIS_ONLY is True
    assert ORDER_EXECUTION == "disabled-by-design"


def test_canonical_information_architecture_has_eight_spaces():
    assert CANONICAL_SPACES == (
        "today", "markets", "opportunities", "analysis",
        "portfolio", "options", "journal", "system",
    )


def test_release_profile_v4_is_explicit_and_legacy_history_is_unchanged():
    assert list_versions() == [1, 2, 3]
    assert load_profile().version == 3
    assert list_release_versions() == [1, 2, 3, 4]
    profile = load_release_profile()
    assert profile.version == 4
    assert profile.strategy_id == "vertex_strategy_v4"


def test_active_release_strategy_matches_user_horizons():
    profile = load_release_profile()
    assert profile.holding.preferred_minimum == 10
    assert profile.holding.preferred_maximum == 30
    assert profile.dte.preferred_minimum == 120
    assert profile.dte.preferred_maximum == 240
    assert profile.options_profile["target_dte"] == 180
    assert profile.options_profile["swing_3_6m"]["holding_plan_weeks"] == [2, 4, 6]
    assert profile.raw["equity_profile"]["decision_horizons_months"] == [3, 6, 12]


def test_product_constants_match_release_strategy_profile():
    profile = load_release_profile()
    assert OPTIONS_MANDATE["holding_weeks"] == (2, 4, 6)
    assert OPTIONS_MANDATE["preferred_dte"] == (
        profile.dte.preferred_minimum,
        profile.dte.preferred_maximum,
    )
    assert OPTIONS_MANDATE["target_dte"] == profile.options_profile["target_dte"]
    assert EQUITY_MANDATE["decision_horizons_months"] == (3, 6, 12)
    assert DAILY_INTELLIGENCE_MANDATE["source_name"] == "WMB Brief"
    assert DAILY_INTELLIGENCE_MANDATE["may_supply_market_prices"] is False


def test_one_active_claude_skill_and_canonical_docs():
    skills_root = ROOT / ".claude/skills"
    skills = sorted(
        path.name for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    assert skills == ["vertex-2-0"]

    active = (skills_root / "vertex-2-0/SKILL.md").read_text(encoding="utf-8")
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    assert "IBKR fournit uniquement" in active
    assert "portefeuille" in active.lower() and "déclar" in active.lower()
    assert "/vertex-2-0" in claude
    assert "/vertex-1-0" not in claude
    assert (ROOT / "docs/vertex-1.0/ARCHITECTURE.md").is_file()
    assert (ROOT / "docs/vertex-1.0/RELEASE_CHECKLIST.md").is_file()


def test_launch_and_deployment_use_canonical_entrypoint():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    render = (ROOT / "render.yaml").read_text(encoding="utf-8")
    windows = (ROOT / "Lancer_VERTEX.bat").read_text(encoding="utf-8")
    macos = (ROOT / "Lancer_VERTEX.command").read_text(encoding="utf-8")
    runtime = (ROOT / "vertex/runtime.py").read_text(encoding="utf-8")
    assert "python -m vertex" in readme
    assert "gunicorn vertex.runtime:app" in render
    assert "-m vertex" in windows
    assert "-m vertex" in macos
    assert "activate_release_profile" in runtime
