"""Balayage d'INTEGRITE des 35 vues : identifiants dupliques, liens internes
casses, erreurs de page, et debordement horizontal a 320 px (WCAG 1.4.10).

Quatre invariants qu'aucun test de la suite ne peut tenir : ils n'existent
qu'une fois la page rendue et hydratee. Un id duplique ne casse rien
visiblement, un lien mort ne se voit qu'au clic, et le reflow a 320 px ne se
mesure qu'a 320 px.

Comme `mesurer_rognage_silencieux.py`, cet outil a besoin d'un navigateur ET
d'un serveur, donc il ne tourne pas dans pytest. Lancer :

    DEMO=1 NO_IBKR=1 START_ON_IMPORT=1 python terminal.py &
    python tools/mesurer_integrite_pages.py

Releve du lot 26 (serveur td-shell-v231) : 0 id duplique, 0 erreur de page,
0 lien casse sur 65 distincts, 0 debordement horizontal a 1440 NI a 320.

## Deux pieges que cet outil evite, et que j'ai payes pour connaitre

1. Les erreurs console `net::ERR_FAILED` sont les avortements des points
   d'entree INTERDITS dans cet environnement — les miens, pas ceux du produit.
   Les compter rendait 4 « erreurs » par page qui n'existent pas en vrai.
2. Un lien vers un point d'entree interdit ne doit jamais etre SUIVI. La liste
   `_INTERDITS` sert donc deux fois : a avorter les requetes du navigateur, et
   a filtrer les liens que l'outil verifie lui-meme.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from playwright.sync_api import sync_playwright   # noqa: E402

BASE = 'http://localhost:5002'
_NAV = os.path.join('vertex', 'ui', 'pages')

# Avortes au NAVIGATEUR : la requete ne part pas, donc le serveur ne sort pas.
_INTERDITS = ('**/api/ticker/**', '**/api/analyst/**', '**/api/correlations/**',
              '**/api/options-for/**', '**/options/*', '**/desc/**')
_INTERDIT_RE = re.compile(
    r'/api/(ticker|analyst|correlations|options-for)/|/desc/|^/options/[^/]+$')


def _vues(fichier, symbole='_VIEWS'):
    """Les vues DECLAREES, derivees de la source (lecon du lot 14 : une URL
    fabriquee retombe sur la vue par defaut sans erreur, donc on mesurerait
    deux fois la meme page en croyant en couvrir deux)."""
    src = io.open(os.path.join(_NAV, fichier), encoding='utf-8').read()
    m = (re.search(symbole + r'\s*=\s*\((.*?)\n\)', src, re.S)
         or re.search(symbole + r'\s*=\s*\((.*?)\)\s*\n\n', src, re.S))
    return re.findall(r"\('([a-z0-9-]+)'\s*,", m.group(1)) if m else ['']


PAGES = [('/', ['']),
         ('/markets', _vues('markets_page.py')),
         ('/opportunities', _vues('opportunities_page.py')),
         ('/analysis', ['']),
         ('/analysis/ACN', ['']),
         ('/portfolio', _vues('portfolio_page.py')),
         ('/options', _vues('options_intel_page.py')),
         ('/journal', _vues('performance_page.py')),
         ('/system', _vues('system_page.py', 'VIEWS'))]

JS = """() => {
  const ids = [...document.querySelectorAll('[id]')].map(e => e.id).filter(Boolean);
  const vus = new Set(), dbl = new Set();
  for (const i of ids) { if (vus.has(i)) dbl.add(i); vus.add(i); }
  const hrefs = [...document.querySelectorAll('a[href]')]
    .map(a => a.getAttribute('href'))
    .filter(h => h && !h.startsWith('#') && !h.startsWith('mailto:')
              && !h.startsWith('http') && !h.startsWith('javascript:'));
  const doc = document.documentElement;
  return { dbl: [...dbl], hrefs: [...new Set(hrefs)],
           debordeH: doc.scrollWidth - doc.clientWidth };
}"""


def balayer(pw, largeur, hauteur, etiquette):
    nav = pw.chromium.launch(
        executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = nav.new_context(viewport={'width': largeur, 'height': hauteur},
                          service_workers='block')
    pg = ctx.new_page()
    for motif in _INTERDITS:
        pg.route(motif, lambda r: r.abort())

    ids_dbl, liens, erreurs, reflow = {}, set(), {}, []
    for route, vues in PAGES:
        for v in vues:
            url = route + (('?view=' + v) if v else '')
            errs = []
            pg.on('pageerror', lambda e: errs.append('pageerror: %s' % e))

            def _console(m, _e=errs):
                if m.type != 'error':
                    return
                # MES avortements, pas des defauts du produit.
                if 'ERR_FAILED' in m.text or 'Failed to load resource' in m.text:
                    return
                _e.append('console: ' + m.text)
            pg.on('console', _console)

            pg.goto(BASE + url, wait_until='domcontentloaded')
            pg.wait_for_timeout(2600)
            r = pg.evaluate(JS)
            pg.remove_listener('console', _console)

            if r['dbl']:
                ids_dbl[url] = r['dbl']
            liens.update(r['hrefs'])
            if errs:
                erreurs[url] = sorted(set(errs))[:3]
            if r['debordeH'] > 2:
                reflow.append('%s (+%d px)' % (url, r['debordeH']))

    print('=== %s (%d px)' % (etiquette, largeur))
    print('  ids dupliques   : %s' % (ids_dbl or 0))
    print('  erreurs de page : %s' % (erreurs or 0))
    print('  debordement H   : %s' % (', '.join(reflow) or 0))

    casses = []
    for h in sorted(liens):
        if _INTERDIT_RE.search(h):
            print('  (lien non suivi, point d\'entree interdit) %s' % h)
            continue
        try:
            rep = pg.request.get(BASE + h, max_redirects=5)
            if rep.status >= 400:
                casses.append('%s -> %d' % (h, rep.status))
        except Exception as e:
            casses.append('%s -> %s' % (h, type(e).__name__))
    print('  liens internes  : %d distincts, casses : %s'
          % (len(liens), ', '.join(casses) or 0))
    ctx.close()
    nav.close()
    return not (ids_dbl or erreurs or reflow or casses)


with sync_playwright() as pw:
    ok = balayer(pw, 1440, 900, 'INTEGRITE')
    # WCAG 1.4.10 : 320 px de large sans defilement horizontal.
    ok = balayer(pw, 320, 800, 'REFLOW 320') and ok
print('\n%s' % ('TOUT PROPRE' if ok else 'DEFAUTS TROUVES — voir ci-dessus'))
