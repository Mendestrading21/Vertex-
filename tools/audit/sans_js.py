"""Mesure ce que Vertex rend quand JavaScript est ENTIEREMENT desactive.

Le controle 075 demande un repli utilisable quand Canvas, WebGL ou JS
echouent. Deux tiers etaient verifies -- `@supports not (backdrop-filter)`
rend un graphite plein, et les tables equivalentes sont du HTML donc lisibles
sans Canvas. Le cas « JS entierement desactive » etait declare NON MESURE.

Il est mesurable ici : Playwright sert la page avec le moteur JS coupe. On
regarde alors les trois questions qui decident si un repli est utilisable :

  1. La page repond-elle, et rend-elle sa COQUE (navigation, titre, contenu) ?
  2. Reste-t-il un SQUELETTE de chargement -- une promesse qu'aucun script ne
     tiendra jamais ? C'est le pire cas : l'ecran ment en silence.
  3. La navigation reste-t-elle praticable -- des liens `href` reels, pas des
     boutons qui attendent un gestionnaire ?

L'outil ne juge pas la richesse du repli : sans JS, aucune donnee ne se
charge, et c'est normal. Il verifie que l'absence est LISIBLE plutot que
deguisee en attente.

Usage :
    python tools/audit/sans_js.py --routes / /markets /options
"""
from __future__ import annotations

import argparse

_JS_LECTURE = None  # aucun script cote page : tout est lu via les API Playwright


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--routes', nargs='+', required=True)
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    total = 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=args.exe)
        ctx = nav.new_context(viewport={'width': 1440, 'height': 1000},
                              java_script_enabled=False)
        page = ctx.new_page()
        for route in args.routes:
            rep = page.goto(args.base + route, wait_until='domcontentloaded')
            page.wait_for_timeout(500)
            faits = []
            if not rep or rep.status != 200:
                faits.append('reponse HTTP %s' % (rep.status if rep else 'aucune'))
            # 1. La coque est-elle la ?
            for quoi, sel in (('navigation', 'nav a[href], aside a[href]'),
                              ('titre de page', 'h1'),
                              ('zone de contenu', '#vx-content')):
                if page.locator(sel).count() == 0:
                    faits.append('%s absente' % quoi)
            # 2. Squelettes perpetuels : une promesse qu'aucun script ne tiendra.
            #    On compte ceux qui se VOIENT : la coque en masque desormais la
            #    totalite via un <noscript><style>, et un squelette present mais
            #    invisible ne promet rien a personne.
            sq = page.locator('.vx-skeleton:visible, .vx2-skeleton:visible').count()
            if sq:
                faits.append('%d squelette(s) VISIBLE(s) sans script pour les resoudre' % sq)
            # 3. Le bandeau doit dire pourquoi l'ecran est muet.
            if page.locator('.vx2-noscript:visible').count() == 0:
                faits.append('aucun bandeau n\'explique l\'absence de donnees')
            # 4. Navigation praticable : des liens, pas seulement des boutons.
            liens = page.locator('#vx-app a[href]:not([href="#"]):not([href^="javascript"])').count()
            if liens < 5:
                faits.append('%d lien(s) navigables seulement' % liens)
            total += len(faits)
            print('%-34s %s' % (route, 'OK' if not faits else ' · '.join(faits)))
        nav.close()
    print('\nTOTAL : %d constat(s) sur %d route(s)' % (total, len(args.routes)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
