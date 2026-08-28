#!/usr/bin/env python3
"""Produit une baseline JSON légère du dépôt courant."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]


def main() -> None:
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    suffixes = Counter(path.suffix or "[sans extension]" for path in files)
    py_files = [path for path in files if path.suffix == ".py"]
    route_pattern = re.compile(r"@\w+\.(?:route|get|post|put|patch|delete)\s*\(")
    routes = broad = silent = 0
    for path in py_files:
        body = path.read_text(encoding="utf-8", errors="ignore")
        routes += len(route_pattern.findall(body))
        broad += body.count("except Exception")
        silent += len(re.findall(r"except[^:]*:\s*(?:#.*\n\s*)?(?:pass|continue)\b", body))
    payload = {
        "files": len(files),
        "suffixes": dict(suffixes.most_common()),
        "python_files": len(py_files),
        "test_files": len(list((ROOT / "tests").rglob("test_*.py"))),
        "route_decorators_approx": routes,
        "except_exception_approx": broad,
        "silent_except_approx": silent,
        "active_skills": sorted(
            path.parent.name for path in (ROOT / ".claude" / "skills").glob("*/SKILL.md")
        ),
        "auditors": sorted(path.name for path in (ROOT / ".claude" / "agents").glob("*.md")),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
