"""Balayage d'INTEGRITE des 35 vues sur les CINQ largeurs de la matrice :
identifiants dupliques, liens internes casses, erreurs de page, et debordement
horizontal (WCAG 1.4.10 a 320 px).

LOT 42 : l'outil ne mesurait que 1440 et 320 — les deux bouts. La matrice de
`VALIDATION.md` en demande cinq, et ce ne sont pas les extremites qui cassent :
les defauts de grille naissent aux BASCULES (1024 sidebar compacte, 768 rail
vers mobile, 390 une colonne). Un debordement qui n'existe qu'a 768 px passait
entre les deux mesures sans que rien ne le dise.

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
    vu_largeur = False
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
            #  TEMOIN DE LARGEUR. Un « 0 debordement a 768 px » ne vaut rien si
            #  la page a en realite ete rendue a 1440 : le detecteur serait
            #  propre pour la mauvaise raison. On verifie donc, sur la premiere
            #  vue de chaque largeur, que le navigateur a bien applique le
            #  gabarit — et on refuse de continuer sinon, plutot que de publier
            #  un vert qui ne prouve rien.
            if not vu_largeur:
                reelle = pg.evaluate('() => window.innerWidth')
                if reelle != largeur:
                    ctx.close()
                    nav.close()
                    raise SystemExit(
                        'AVEUGLE — largeur demandee %d px, largeur rendue %d px : '
                        'le releve de cette colonne ne mesurerait pas ce qu\'il '
                        'annonce.' % (largeur, reelle))
                vu_largeur = True
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


# LA MATRICE COMPLETE (VALIDATION.md), et pourquoi elle ne se resume pas a ses
# extremites. On ne mesurait que 1440 et 320 : les deux bouts. Or les defauts de
# grille naissent aux BASCULES — 1024 (sidebar compacte), 768 (rail -> mobile),
# 390 (une colonne, graphiques 280-340 px). Un debordement qui n'existe qu'a
# 768 px passait entre les deux mesures sans que rien ne le dise.
LARGEURS = ((1440, 900, 'INTEGRITE 1440'),
            (1024, 800, 'GRILLE 1024'),
            (768, 900, 'BASCULE 768'),
            (390, 844, 'MOBILE 390'),
            (320, 800, 'REFLOW 320'))   # WCAG 1.4.10

with sync_playwright() as pw:
    ok = True
    for largeur, hauteur, titre in LARGEURS:
        ok = balayer(pw, largeur, hauteur, titre) and ok
print('\n%s' % ('TOUT PROPRE' if ok else 'DEFAUTS TROUVES — voir ci-dessus'))
