"""Capture d'écran réelle de Vertex pour les preuves de refonte visuelle 2.0.

Lance un navigateur Chromium sur l'application RÉELLEMENT exécutée et
enregistre desktop 1440x1000 + mobile 390x844. Aucune maquette externe.

Usage :
    python tools/vertex_2_0_capture.py --base http://127.0.0.1:8099 \
        --out docs/vertex-2-0/preuves/lot-00-avant \
        --routes / /opportunities /analysis
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DESKTOP = (1440, 1000)
MOBILE = (390, 844)


def slug(route: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9]+', '-', route).strip('-')
    return s or 'accueil'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--out', required=True)
    ap.add_argument('--routes', nargs='+', required=True)
    ap.add_argument('--full-page', action='store_true')
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                    help='binaire Chromium pré-installé (pas de téléchargement)')
    ap.add_argument('--wait', type=int, default=2500)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    report: list[dict] = []

    with sync_playwright() as pw:
        launch_kw = {'args': ['--force-color-profile=srgb']}
        if args.exe and Path(args.exe).exists():
            launch_kw['executable_path'] = args.exe
        browser = pw.chromium.launch(**launch_kw)
        for route in args.routes:
            entry = {'route': route, 'console': [], 'pageerrors': [], 'shots': {}}
            for name, (w, h) in (('desktop', DESKTOP), ('mobile', MOBILE)):
                ctx = browser.new_context(
                    viewport={'width': w, 'height': h},
                    device_scale_factor=2,
                    is_mobile=(name == 'mobile'),
                    has_touch=(name == 'mobile'),
                    locale='fr-FR',
                    timezone_id='Europe/Zurich',
                )
                page = ctx.new_page()
                page.on('console', lambda m, e=entry: (
                    e['console'].append({'type': m.type, 'text': m.text[:400]})
                    if m.type in ('error', 'warning') else None))
                page.on('pageerror', lambda err, e=entry: e['pageerrors'].append(str(err)[:400]))
                try:
                    page.goto(args.base + route, wait_until='networkidle', timeout=45000)
                except Exception as exc:  # noqa: BLE001
                    entry['pageerrors'].append(f'goto: {exc}'[:400])
                    try:
                        page.goto(args.base + route, wait_until='domcontentloaded', timeout=30000)
                    except Exception as exc2:  # noqa: BLE001
                        entry['pageerrors'].append(f'goto2: {exc2}'[:400])
                page.wait_for_timeout(args.wait)
                # Débordement horizontal global (contrôle 133).
                try:
                    entry.setdefault('overflow', {})[name] = page.evaluate(
                        'Math.max(0, document.documentElement.scrollWidth'
                        ' - document.documentElement.clientWidth)')
                except Exception:  # noqa: BLE001
                    pass
                shot = out / f'{slug(route)}-{name}.png'
                page.screenshot(path=str(shot), full_page=args.full_page)
                entry['shots'][name] = str(shot)
                ctx.close()
            report.append(entry)
            errs = len(entry['pageerrors'])
            ov = entry.get('overflow', {})
            print(f"{route:<22} erreurs={errs} overflow={ov}", flush=True)
        browser.close()

    (out / 'rapport.json').write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
