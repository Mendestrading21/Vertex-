#!/usr/bin/env python3
"""Valide l'autorité Claude unique de Vertex sans dépendance externe."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SKILLS = ROOT / ".claude" / "skills"
MASTER = SKILLS / "vertex-2-0"
EXPECTED_AGENTS = {
    "vertex-data-auditor.md",
    "vertex-decision-auditor.md",
    "vertex-performance-auditor.md",
    "vertex-product-auditor.md",
    "vertex-qa-auditor.md",
    "vertex-ui-auditor.md",
}
OLD_COMMAND = re.compile(
    r"/vertex-(?:1-0|maximum|design-2-0|redesign[^\s`]*|skyler[^\s`]*|total-rebuild)"
)


def main() -> int:
    errors: list[str] = []
    active = sorted(
        path.name for path in SKILLS.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if active != ["vertex-2-0"]:
        errors.append(f"skills actifs={active!r}, attendu=['vertex-2-0']")

    skill = (MASTER / "SKILL.md").read_text(encoding="utf-8")
    for rel in re.findall(r"\]\((references/[^)#]+\.md)\)", skill):
        if not (MASTER / rel).is_file():
            errors.append(f"référence absente: {rel}")

    audit = (MASTER / "references" / "audit-150.md").read_text(encoding="utf-8")
    numbers = [int(n) for n in re.findall(r"(?m)^(\d{3})\. ", audit)]
    if numbers != list(range(1, 151)):
        errors.append("audit-150 non continu ou différent de 150 contrôles")

    agents_dir = ROOT / ".claude" / "agents"
    agents = {path.name for path in agents_dir.glob("*.md")}
    if agents != EXPECTED_AGENTS:
        errors.append(
            f"agents inattendus={sorted(agents ^ EXPECTED_AGENTS)!r}"
        )
    for path in agents_dir.glob("*.md"):
        body = path.read_text(encoding="utf-8")
        if not body.startswith("---\n") or "permissionMode: plan" not in body:
            errors.append(f"agent non borné: {path.relative_to(ROOT)}")

    governance = [ROOT / "CLAUDE.md", ROOT / "README.md"]
    governance += list((ROOT / ".claude" / "rules").glob("*.md"))
    governance += list(agents_dir.glob("*.md"))
    for path in governance:
        for match in OLD_COMMAND.finditer(path.read_text(encoding="utf-8")):
            errors.append(
                f"ancienne commande dans {path.relative_to(ROOT)}: {match.group(0)}"
            )

    if errors:
        print("ÉCHEC surface Claude Vertex:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: 1 skill Vertex, 6 auditeurs, références résolues, audit 001–150.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
