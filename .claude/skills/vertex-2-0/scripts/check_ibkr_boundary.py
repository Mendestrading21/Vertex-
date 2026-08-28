#!/usr/bin/env python3
"""Inventorie les capacités IBKR interdites ; --enforce échoue sur tout hit."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DENIED = (
    "managedAccounts", "accountSummary", "accountValues", "accountUpdates",
    "positions", "reqPositions", "portfolio", "reqPnL", "reqPnLSingle",
    "openOrders", "openTrades", "completedOrders", "executions", "fills",
    "placeOrder", "cancelOrder",
)


def files() -> list[Path]:
    result = [ROOT / "terminal.py"]
    result.extend((ROOT / "vertex").rglob("*.py"))
    result.extend((ROOT / "tools").rglob("*.py"))
    return sorted(path for path in result if path.is_file())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    hits: list[tuple[Path, int, str]] = []
    for path in files():
        source = path.read_text(encoding="utf-8", errors="ignore")
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr in DENIED:
                hits.append((path.relative_to(ROOT), node.lineno, node.func.attr))

    if hits:
        print(f"Capacités IBKR sensibles détectées: {len(hits)}")
        for path, number, method in hits:
            print(f"- {path}:{number}: {method}()")
        print("À classifier puis supprimer derrière MarketDataGateway au lot 2.")
        return 1 if args.enforce else 0
    print("OK: aucun appel IBKR sensible détecté dans le périmètre runtime/outils.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
