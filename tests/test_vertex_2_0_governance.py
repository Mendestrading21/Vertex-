"""Gardiens de la doctrine Claude Vertex 2.0."""

import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude/skills/vertex-2-0"


def test_skill_links_resolve_inside_the_canonical_skill():
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    links = re.findall(r"\]\((references/[^)#]+\.md)\)", body)
    assert links
    missing = [link for link in links if not (SKILL / link).is_file()]
    assert missing == []


def test_final_audit_contains_exactly_150_contiguous_checks():
    body = (SKILL / "references/audit-150.md").read_text(encoding="utf-8")
    numbers = [int(value) for value in re.findall(r"(?m)^(\d{3})\. ", body)]
    assert numbers == list(range(1, 151))


def test_privacy_contract_is_market_data_only_and_portfolio_is_manual():
    ibkr = (SKILL / "references/ibkr-market-data-only.md").read_text(
        encoding="utf-8"
    )
    portfolio = (SKILL / "references/manual-portfolio.md").read_text(
        encoding="utf-8"
    )
    for forbidden in ("managedAccounts", "accountSummary", "positions", "reqPnL"):
        assert forbidden in ibkr
    assert "Interdit" in ibkr
    assert "déclaration volontaire" in portfolio


def test_only_six_subordinate_read_only_auditors_remain():
    agents = sorted(path.name for path in (ROOT / ".claude/agents").glob("*.md"))
    assert agents == [
        "vertex-data-auditor.md",
        "vertex-decision-auditor.md",
        "vertex-performance-auditor.md",
        "vertex-product-auditor.md",
        "vertex-qa-auditor.md",
        "vertex-ui-auditor.md",
    ]
    for name in agents:
        body = (ROOT / ".claude/agents" / name).read_text(encoding="utf-8")
        assert "permissionMode: plan" in body
        assert ".claude/skills/vertex-2-0" in body or "skill maître" in body


def test_runtime_manifest_distinguishes_current_pages_from_target_pages():
    manifest = (SKILL / "references/runtime-page-manifest.md").read_text(
        encoding="utf-8"
    )
    for fact in (
        "204 règles Flask",
        "199 endpoints",
        "Calendrier `/calendar` | 301",
        "Simulateur `/simulator` | 404",
        "Suivi `/follow-up` | 404",
        "GET /options/<sym>",
        "GET /api/anomalies/<sym>",
    ):
        assert fact in manifest
    assert "ne prouvent pas qu'un\n  widget est connecté" in manifest


def test_runtime_auditor_has_twelve_target_pages_and_is_valid_python():
    script = SKILL / "scripts/audit_runtime.py"
    tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    assignment = next(
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "TARGET_PAGES"
                for target in node.targets)
    )
    pages = ast.literal_eval(assignment.value)
    assert len(pages) == 12
    assert [page[0] for page in pages] == [
        "Aujourd'hui", "Calendrier", "Marchés", "Opportunités", "Analyse",
        "Options", "Simulateur", "Portefeuille", "Suivi", "Performance",
        "Vertex IA", "Système",
    ]


def test_autopilot_requires_runtime_truth_before_page_cutover():
    prompt = (SKILL / "templates/claude-autopilot-prompt.md").read_text(
        encoding="utf-8"
    )
    assert "scripts/audit_runtime.py" in prompt
    assert "une redirection ou une 404" in prompt
    assert "Ne supprime Journal" in prompt


def test_autopilot_requires_page_strategy_and_connection_contracts():
    prompt = (SKILL / "templates/claude-autopilot-prompt.md").read_text(
        encoding="utf-8"
    )
    for contract in (
        "WORK_MANIFEST",
        "PAGE_CONTRACT",
        "point-in-time",
        "walk-forward",
        "N'ajoute ni Redis",
        "Chaque dépendance ou méthode GitHub est une candidature",
    ):
        assert contract in prompt


def test_page_blueprint_covers_the_twelve_target_pages():
    blueprint = (
        SKILL / "references/page-widget-intelligence-blueprint.md"
    ).read_text(encoding="utf-8")
    for page in (
        "Aujourd'hui", "Calendrier", "Marchés", "Opportunités", "Analyse",
        "Options", "Simulateur", "Portefeuille", "Suivi", "Performance",
        "Vertex IA", "Système",
    ):
        assert f"| {page} |" in blueprint


def test_strategy_lab_is_research_only_and_anti_leakage():
    lab = (SKILL / "references/strategy-research-lab.md").read_text(
        encoding="utf-8"
    )
    for invariant in (
        "point-in-time",
        "look-ahead",
        "survivorship",
        "walk-forward",
        "purger/embargo",
        "transforme aucun backtest en ordre",
    ):
        assert invariant in lab
