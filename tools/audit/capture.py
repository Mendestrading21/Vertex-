"""Capture d'écran réelle de Vertex pour les preuves de refonte visuelle 2.0.

Lance un navigateur Chromium sur l'application RÉELLEMENT exécutée et
enregistre une capture par largeur cible. Aucune maquette externe.

Les trois largeurs par defaut sont celles qu'exige le skill maitre Vertex 2.0 :
**1600** (desktop de reference), **1024** (tablette) et **390** (mobile). Elles
restaient auparavant figees a 1440/390 : la tablette n'etait jamais capturee,
et c'est precisement la largeur ou deux fautes ont ete trouvees (les titres de
groupe coupes de la barre laterale, et le raccourci clavier pose sur le texte).
`--largeurs` permet d'en demander d'autres sans toucher au code.

Usage :
    python tools/audit/capture.py --base http://127.0.0.1:8099 \
        --out captures/avant \
        --routes / /opportunities /analysis
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

#: Largeur -> hauteur de fenetre, et nom du fichier produit.
LARGEURS_SKILL = {
    1600: (1000, 'desktop'),
    1024: (768, 'tablette'),
    390: (844, 'mobile'),
}
#: En dessous de ce seuil, on emule un vrai appareil tactile : sans cela, les
#: surcharges `@media (hover:none)` et les cibles de 44 px ne s'exercent pas.
SEUIL_TACTILE = 430


def slug(route: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9]+', '-', route).strip('-')
    return s or 'accueil'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--largeurs', type=int, nargs='+', default=sorted(LARGEURS_SKILL, reverse=True),
                    help='largeurs a capturer ; defaut 1600 1024 390 (skill maitre)')
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
            for w in args.largeurs:
                h, name = LARGEURS_SKILL.get(w, (1000, str(w)))
                tactile = w <= SEUIL_TACTILE
                ctx = browser.new_context(
                    viewport={'width': w, 'height': h},
                    device_scale_factor=2,
                    is_mobile=tactile,
                    has_touch=tactile,
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
