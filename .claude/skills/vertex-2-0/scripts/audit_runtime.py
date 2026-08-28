#!/usr/bin/env python3
"""Mesure le runtime Flask et le cutover des pages Vertex 2.0.

Le script ne contacte ni IBKR ni un fournisseur de marche. Il construit
l'application en mode demo, interroge seulement les pages HTML de shell et
signale les collisions de routes telles que Flask les resout reellement.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DEMO", "1")
os.environ.setdefault("NO_IBKR", "1")
os.environ.setdefault("START_ON_IMPORT", "0")
os.environ.setdefault("VERTEX_LAN", "0")
os.environ.setdefault("AUTH_ON", "0")
os.environ.setdefault("VERTEX_CODE", "")


TARGET_PAGES = (
    ("Aujourd'hui", "/", "conserver_renommer"),
    ("Calendrier", "/calendar", "extraire"),
    ("Marchés", "/markets", "restaurer"),
    ("Opportunités", "/opportunities", "conserver"),
    ("Analyse", "/analysis", "conserver"),
    ("Options", "/options", "conserver"),
    ("Simulateur", "/simulator", "creer_apres_moteur"),
    ("Portefeuille", "/portfolio", "conserver"),
    ("Suivi", "/follow-up", "migrer_tracking"),
    ("Performance", "/performance", "separer_du_journal"),
    ("Vertex IA", "/intelligence", "promouvoir"),
    ("Système", "/system", "conserver"),
)

INTERNAL_PAGES = (
    "/journal",
    "/tracking",
    "/design-system",
    "/system/design-system",
    "/widget-lab",
)


def _title(body: str) -> str | None:
    match = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else None


def _probe(client, path: str) -> dict:
    started = time.perf_counter()
    response = client.get(path, follow_redirects=False)
    elapsed = round((time.perf_counter() - started) * 1000, 1)
    body = response.get_data(as_text=True)
    return {
        "path": path,
        "status": response.status_code,
        "redirect": response.headers.get("Location"),
        "content_type": response.content_type,
        "bytes": len(response.data),
        "render_ms": elapsed,
        "title": _title(body),
    }


def _collisions(app) -> list[dict]:
    owners: dict[tuple[str, str], list[str]] = defaultdict(list)
    for rule in app.url_map.iter_rules():
        for method in sorted(rule.methods - {"HEAD", "OPTIONS"}):
            owners[(rule.rule, method)].append(rule.endpoint)
    return [
        {"path": path, "method": method, "owners": endpoints}
        for (path, method), endpoints in sorted(owners.items())
        if len(endpoints) > 1
    ]


def collect() -> dict:
    from vertex.runtime import create_app
    from vertex.ui.shell import PRIMARY_NAV

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    pages = []
    for label, path, transition in TARGET_PAGES:
        item = _probe(client, path)
        item.update({"label": label, "transition": transition})
        pages.append(item)
    internal = [_probe(client, path) for path in INTERNAL_PAGES]
    root = client.get("/").get_data(as_text=True)
    styles = re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', root, re.I)
    scripts = re.findall(r'<script[^>]+src="([^"]+)"', root, re.I)
    fonts = re.findall(r'<link[^>]+as="font"[^>]+href="([^"]+)"', root, re.I)
    rules = list(app.url_map.iter_rules())
    return {
        "runtime": {
            "app": app.name,
            "rules": len(rules),
            "endpoints": len({rule.endpoint for rule in rules}),
            "blueprints": len(app.blueprints),
        },
        "primary_navigation": [dict(item) for item in PRIMARY_NAV],
        "target_pages": pages,
        "internal_and_legacy_pages": internal,
        "collisions": _collisions(app),
        "shell": {
            "stylesheets": len(styles),
            "scripts": len(scripts),
            "router_loaded": "/static/vertex/js/vx-router.js" in scripts,
            "fonts": fonts,
        },
    }


def render_markdown(report: dict) -> str:
    runtime = report["runtime"]
    lines = [
        "# Audit runtime Vertex",
        "",
        f"- Flask : {runtime['rules']} regles, {runtime['endpoints']} endpoints, "
        f"{runtime['blueprints']} blueprints.",
        f"- Navigation principale : {len(report['primary_navigation'])} entrees.",
        f"- Shell : {report['shell']['stylesheets']} CSS, "
        f"{report['shell']['scripts']} scripts, routeur persistant charge : "
        f"{'oui' if report['shell']['router_loaded'] else 'non'}.",
        "",
        "| Page cible | Route | HTTP | Redirection | Transition |",
        "|---|---|---:|---|---|",
    ]
    for page in report["target_pages"]:
        lines.append(
            f"| {page['label']} | `{page['path']}` | {page['status']} | "
            f"{page['redirect'] or '—'} | `{page['transition']}` |"
        )
    lines.extend(["", "## Collisions"])
    for collision in report["collisions"]:
        lines.append(
            f"- `{collision['method']} {collision['path']}` : "
            + ", ".join(f"`{owner}`" for owner in collision["owners"])
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="sortie JSON")
    parser.add_argument(
        "--enforce-target",
        action="store_true",
        help="echoue tant qu'une page cible redirige/manque, qu'une route collisionne "
        "ou que le routeur du shell n'est pas charge",
    )
    args = parser.parse_args()
    report = collect()
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else render_markdown(report))
    if not args.enforce_target:
        return 0
    target_unready = [page for page in report["target_pages"] if page["status"] != 200]
    return int(bool(target_unready or report["collisions"] or not report["shell"]["router_loaded"]))


if __name__ == "__main__":
    raise SystemExit(main())
