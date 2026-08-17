"""PANNE PARTIELLE : une source tombe, les autres repondent normalement.

Le lot 29 avait eprouve les pannes GLOBALES — toutes les sources en meme temps
— et conclu par une reserve : « une panne PARTIELLE est un regime different, ou
un chiffre faux peut se glisser entre des chiffres justes sans qu'aucun etat
d'erreur ne s'affiche ». Cet outil eprouve ce regime-la.

## Ce qu'il mesure de facon SURE

Pour chaque source, il fait d'abord la carte de QUI L'APPELLE (mesure, pas
supposition), puis ne juge que les vues concernees :

  * fuites techniques a l'ecran (NaN, undefined, null, Infinity, [object Object]) ;
  * erreurs de page.

Releve du lot 30, six sources isolees : 0 fuite, 0 erreur.

## Ce qu'il NE PEUT PAS decider, et pourquoi c'est dit ici

« Un chiffre faux se glisse-t-il entre des chiffres justes ? » n'est pas
decidable sur le jeu de donnees de demonstration. J'ai essaye trois methodes,
et les trois ont produit des FAUX POSITIFS que j'ai du refuter une par une :

  1. comparer toutes les cellules avant/apres : la cle `e.className` vaut
     « [object SVGAnimatedString] » pour TOUT texte SVG, donc des valeurs sans
     rapport tombaient dans le meme seau ;
  2. ajouter un rang de fratrie a la cle : la cle glisse des que l'ordre de
     rendu change, et desigme une autre cellule ;
  3. exiger qu'une vue « signale » son manque : plusieurs sources n'apportent
     RIEN en demo (aucune position a valoriser pour /api/pos-quotes), donc leur
     panne ne peut rien changer — l'absence de signal n'y prouve rien.

Le seul candidat concret trouve — une KPI de Systeme passant de « 8/8 » a
« 0 » — a ete REFUTE en regardant l'ecran : la valeur est identique avec et
sans panne.

Conclure « propre » sur cette question serait affirmer plus que ce que la
mesure permet. Elle reste ouverte, et elle demande un jeu de donnees ou chaque
source apporte une valeur observable.

Lancer :
    DEMO=1 NO_IBKR=1 START_ON_IMPORT=1 python terminal.py &
    python tools/mesurer_panne_partielle.py
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from playwright.sync_api import sync_playwright   # noqa: E402

BASE = 'http://localhost:5002'
_PAGES_DIR = os.path.join('vertex', 'ui', 'pages')
_INTERDITS = ('**/api/ticker/**', '**/api/analyst/**', '**/api/correlations/**',
              '**/api/options-for/**', '**/options/*', '**/desc/**')
CIBLES = ('/scan', '/api/pos-quotes', '/api/market/summary', '/api/command',
          '/api/portfolio/team', '/api/options/overview')


def _vues(fichier, symbole='_VIEWS'):
    src = io.open(os.path.join(_PAGES_DIR, fichier), encoding='utf-8').read()
    m = (re.search(symbole + r'\s*=\s*\((.*?)\n\)', src, re.S)
         or re.search(symbole + r'\s*=\s*\((.*?)\)\s*\n\n', src, re.S))
    return re.findall(r"\('([a-z0-9-]+)'\s*,", m.group(1)) if m else ['']


PAGES = [('/', ['']),
         ('/markets', _vues('markets_page.py')),
         ('/opportunities', _vues('opportunities_page.py')),
         ('/portfolio', _vues('portfolio_page.py')),
         ('/options', _vues('options_intel_page.py')),
         ('/journal', _vues('performance_page.py')),
         ('/system', _vues('system_page.py', 'VIEWS'))]

JS = """() => {
  const vis = (e) => {
    const q = e.getBoundingClientRect();
    if (q.width < 2 || q.height < 2) return false;
    let n = e;
    while (n) {
      if (n.tagName === 'DETAILS' && !n.open) return false;
      const c = getComputedStyle(n);
      if (c.display === 'none' || c.visibility === 'hidden') return false;
      n = n.parentElement;
    }
    return true;
  };
  let fuite = null;
  document.querySelectorAll('#vx-content *').forEach(e => {
    if (fuite || e.classList.contains('vx-sr-only') || !vis(e)) return;
    const t = [...e.childNodes].filter(n => n.nodeType === 3)
      .map(n => n.textContent).join('').trim();
    if (t && /\\b(NaN|undefined|null|Infinity|\\[object Object\\])\\b/.test(t)) fuite = t.slice(0,60);
  });
  return { fuite };
}"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(
        executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')

    # 1. La carte QUI APPELLE QUOI, mesuree.
    ctx = nav.new_context(viewport={'width': 1440, 'height': 900}, service_workers='block')
    pg = ctx.new_page()
    for motif in _INTERDITS:
        pg.route(motif, lambda r: r.abort())
    usage = {}
    for route, vues in PAGES:
        for v in vues:
            url = route + (('?view=' + v) if v else '')
            vus = set()

            def _req(r, _v=vus):
                u = r.url.replace(BASE, '').split('?')[0]
                for c in CIBLES:
                    if u == c or u.startswith(c + '/'):
                        _v.add(c)
            pg.on('request', _req)
            pg.goto(BASE + url, wait_until='domcontentloaded')
            pg.wait_for_timeout(2400)
            pg.remove_listener('request', _req)
            usage[url] = vus
    ctx.close()
    print('=== QUI APPELLE QUOI (mesure)')
    for c in CIBLES:
        q = [u for u, s in usage.items() if c in s]
        print('  %-24s %d vue(s)' % (c, len(q)))

    # 2. Une source en panne a la fois — SEULES les vues concernees sont jugees.
    propre = True
    for cible in CIBLES:
        concernees = [u for u, s in usage.items() if cible in s]
        if not concernees:
            print('--- %s : aucune vue concernee' % cible)
            continue
        ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                              service_workers='block')
        pg = ctx.new_page()
        for motif in _INTERDITS:
            pg.route(motif, lambda r: r.abort())

        def _panne(r):
            r.fulfill(status=500, content_type='application/json',
                      body='{"error":"panne partielle"}')
        pg.route('**' + cible + '*', _panne)

        fuites, erreurs = [], []
        for url in concernees:
            errs = []
            pg.on('pageerror', lambda e, _e=errs: _e.append(str(e)[:70]))
            pg.goto(BASE + url, wait_until='domcontentloaded')
            pg.wait_for_timeout(2500)
            r = pg.evaluate(JS)
            if r['fuite']:
                fuites.append('%s :: %s' % (url, r['fuite']))
            if errs:
                erreurs.append('%s :: %s' % (url, errs[0]))
        print('--- panne isolee : %-24s %d vue(s) · fuites %s · erreurs %s'
              % (cible, len(concernees), fuites or 0, erreurs or 0))
        if fuites or erreurs:
            propre = False
        ctx.close()
    nav.close()

print('\n%s' % ('AUCUNE FUITE NI ERREUR sous panne partielle. La question du '
                '« chiffre faux silencieux » reste OUVERTE — voir l\'en-tete.'
                if propre else 'DEFAUTS TROUVES — voir ci-dessus'))
