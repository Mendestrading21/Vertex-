"""Verifie que chaque lien interne mene quelque part, et qu'aucun id ne double.

Deux defauts que rien ne mesurait, et qui se ressemblent : ils sont invisibles
tant qu'on ne clique pas, ou tant que le script ne cherche pas le mauvais
element.

## 1. Liens internes

Un `href` interne doit rendre une PAGE. Trois facons de rater :

  · **404** -- la route n'existe pas (ou plus) ;
  · **JSON** -- la route existe mais sert de l'API : c'est exactement le
    defaut de la collision `/options/:sym`, ou neuf liens deversaient du JSON
    brut dans le navigateur ;
  · **redirection en boucle** -- l'application repond 302 vers elle-meme,
    ce qui arrive quand le rendu leve.

## 2. Identifiants dupliques

`getElementById` rend le PREMIER. Deux elements portant le meme id, et la
moitie du code ecrit dans le mauvais -- sans erreur, sans trace. C'est le
genre de panne qui se lit comme « la donnee n'arrive pas ».

Usage :
    python tools/vertex_2_0_liens.py --routes / /markets /options
"""
from __future__ import annotations

import argparse
import urllib.parse

_JS_LIENS = r"""() => {
  const vus = new Set(), out = [];
  document.querySelectorAll('a[href]').forEach(a => {
    const h = a.getAttribute('href') || '';
    if (!h || h.startsWith('#') || h.startsWith('mailto:')
        || h.startsWith('tel:') || h.startsWith('javascript:')) return;
    if (/^https?:\/\//i.test(h) && !h.startsWith(location.origin)) return;  // externe
    const u = new URL(h, location.href);
    const cle = u.pathname + u.search;
    if (vus.has(cle)) return;
    vus.add(cle);
    out.push({ url: cle, texte: (a.innerText || '').trim().slice(0, 40) });
  });
  return out;
}"""

_JS_IDS = r"""() => {
  const compte = {};
  document.querySelectorAll('[id]').forEach(e => {
    compte[e.id] = (compte[e.id] || 0) + 1;
  });
  return Object.entries(compte).filter(([, n]) => n > 1)
    .map(([id, n]) => ({ id: id, n: n }));
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--routes', nargs='+', required=True)
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ap.add_argument('--wait', type=int, default=2300)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    cibles: dict[str, list[str]] = {}
    doublons = 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=args.exe)
        ctx = nav.new_context(viewport={'width': 1440, 'height': 1000})
        page = ctx.new_page()

        print('-- Identifiants dupliques --')
        for route in args.routes:
            page.goto(args.base + route, wait_until='domcontentloaded')
            page.wait_for_timeout(args.wait)
            for d in page.evaluate(_JS_IDS):
                doublons += 1
                print('  %-38s #%s  x%d' % (route, d['id'], d['n']))
            for lien in page.evaluate(_JS_LIENS):
                cibles.setdefault(lien['url'], []).append(route)
        if not doublons:
            print('  aucun')

        # Les cibles sont visitees une seule fois, meme si dix pages y menent.
        # On les demande en HTTP plutot qu'en navigation : un lien d'export
        # declenche un telechargement, et `goto` leve dessus. Ce qu'on veut
        # savoir -- le statut et le type -- tient dans la reponse.
        print('\n-- Liens internes (%d cible(s) distincte(s)) --' % len(cibles))
        casses, exports = 0, 0
        for url in sorted(cibles):
            depuis = ', '.join(sorted(set(cibles[url]))[:3])
            try:
                rep = ctx.request.get(args.base + url, max_redirects=3)
            except Exception as exc:
                casses += 1
                print('  %-42s %s   (depuis %s)' % (url, str(exc)[:40], depuis))
                continue
            typ = (rep.headers.get('content-type', '') or '').split(';')[0]
            if rep.status >= 400:
                casses += 1
                print('  %-42s HTTP %d   (depuis %s)' % (url, rep.status, depuis))
            elif 'json' in typ or 'csv' in typ or 'octet-stream' in typ:
                # Une PAGE doit rendre du HTML. Un lien vers /api/... qui sert
                # un fichier est un EXPORT assume, pas une panne ; ailleurs,
                # c'est le defaut de collision de route -- l'API gagne, et
                # l'utilisateur recoit des accolades.
                if url.startswith('/api/'):
                    exports += 1
                else:
                    casses += 1
                    print('  %-42s sert du %s au lieu d une page   (depuis %s)'
                          % (url, typ, depuis))
        if not casses:
            print('  aucun')
        if exports:
            print('  (%d lien(s) d export vers /api/ -- volontaires, non comptes)' % exports)
        nav.close()

    print('\nTOTAL : %d id(s) duplique(s) · %d lien(s) casse(s)' % (doublons, casses))
    return 1 if (doublons or casses) else 0


if __name__ == '__main__':
    raise SystemExit(main())
