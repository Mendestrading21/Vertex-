"""Garde la preuve G6 exécutable dans le clone superficiel de GitHub Actions."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ci_recupere_la_reference_canonique_avant_la_suite_complete():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    fetch = "git fetch origin '+refs/heads/*:refs/remotes/origin/*' --depth=1 --no-tags"
    assert fetch in workflow, (
        "G6 exige origin/main et le gardien de depot exige les branches "
        "distantes ; le checkout superficiel ne fournit aucune de ces preuves"
    )
    assert workflow.index(fetch) < workflow.index("python -m pytest -q")
