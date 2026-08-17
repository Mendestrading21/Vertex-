"""La DEGRADATION HONNETE, eprouvee : que montre le produit quand ses sources
tombent ?

`CLAUDE.md` pose l'invariant le plus important du produit — « donnee absente ->
mention honnete, jamais un chiffre invente ». Personne ne l'avait EPROUVE : on
l'avait lu dans le code, jamais provoque.

Trois pannes simulees, sur les points de DONNEES uniquement — jamais le HTML,
le CSS ni le JS, sinon on mesurerait un navigateur en panne et non un produit
qui degrade :

  * erreur 500 ;
  * reponse 200 mais vide (`{}`) ;
  * JSON malforme.

Ce qu'un utilisateur ne doit JAMAIS lire : NaN, undefined, null, Infinity,
[object Object]. Ces mots ne sont pas des donnees absentes, ce sont des fuites
de plomberie — et ils ressemblent assez a du texte pour passer inapercus.

Releve du lot 29 (33 vues x 3 pannes, serveur td-shell-v233) : 0 erreur de
page, 0 fuite technique sur les trois pannes.

## Le faux positif a NE PAS corriger

Le compteur « vues sans etat honnete » signale `/journal?view=progression` et
`/system?view=settings`. Ce sont des vues STATIQUES — le relais pose au lot 11
et un formulaire de reglages — dont le contenu ne vient d'AUCUNE source. Leurs
seuls chiffres sont des valeurs de filtre. Une vue qui n'affiche pas de donnee
n'a pas d'etat de donnee a montrer.

Lancer :
    DEMO=1 NO_IBKR=1 START_ON_IMPORT=1 python terminal.py &
    python tools/mesurer_degradation.py
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
_DONNEES = '**/{api,scan,cal-feed,news-feed}**'
_FUITES = re.compile(r'\b(NaN|undefined|null|Infinity|\[object Object\])\b')
# Vues STATIQUES : elles n'affichent aucune donnee, donc aucun etat de donnee.
_SANS_DONNEE = ('/journal?view=progression', '/system?view=settings')


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

PANNES = {
    'erreur 500': dict(status=500, body='{"error":"panne simulee"}'),
    'reponse vide': dict(status=200, body='{}'),
    'json malforme': dict(status=200, body='{ceci nest pas du json'),
}

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
  const mots = [];
  document.querySelectorAll('#vx-content *').forEach(e => {
    if (e.classList.contains('vx-sr-only') || !vis(e)) return;
    const propre = [...e.childNodes].filter(n => n.nodeType === 3)
      .map(n => n.textContent).join('').trim();
    if (propre) mots.push({ t: propre.slice(0, 70), c: (e.className||'').toString().slice(0,30) });
  });
  const etat = document.querySelectorAll(
    '#vx-content [data-state], #vx-content .vx-state, #vx-content .vx-empty, '
    + '#vx-content .vx-error-banner, #vx-content .vx-skeleton').length;
  return { mots, etat, texte: (document.getElementById('vx-content')||{}).innerText || '' };
}"""

propre_partout = True
with sync_playwright() as pw:
    nav = pw.chromium.launch(
        executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for nom, panne in PANNES.items():
        ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                              service_workers='block')
        pg = ctx.new_page()
        for motif in _INTERDITS:
            pg.route(motif, lambda r: r.abort())
        # Fabrique de gestionnaire : Playwright passe `request` en SECOND
        # argument positionnel, ce qui ecrasait un defaut `p=panne` et rendait
        # « 'Request' object is not subscriptable ». La closure ne prend donc
        # qu'un parametre.
        def _gestionnaire(p):
            def _f(r):
                r.fulfill(status=p['status'], content_type='application/json',
                          body=p['body'])
            return _f
        pg.route(_DONNEES, _gestionnaire(panne))

        fuites, sans_etat, erreurs, n_vues = {}, [], {}, 0
        for route, vues in PAGES:
            for v in vues:
                url = route + (('?view=' + v) if v else '')
                errs = []
                pg.on('pageerror', lambda e, _e=errs: _e.append(str(e)[:90]))
                pg.goto(BASE + url, wait_until='domcontentloaded')
                pg.wait_for_timeout(2500)
                n_vues += 1
                r = pg.evaluate(JS)
                for m in r['mots']:
                    f = _FUITES.search(m['t'])
                    if f:
                        k = '%s dans .%s' % (f.group(0), m['c'])
                        fuites.setdefault(k, {'ex': m['t'], 'ou': url, 'n': 0})
                        fuites[k]['n'] += 1
                if r['etat'] == 0 and len(r['texte'].strip()) > 400 and url not in _SANS_DONNEE:
                    sans_etat.append(url)
                if errs:
                    erreurs[url] = sorted(set(errs))[:2]
        print('=== PANNE : %s  (%d vues)' % (nom, n_vues))
        print('  fuites techniques a l\'ecran : %d' % len(fuites))
        for k, d in fuites.items():
            print('      %s  ex: « %s »  [%s] x%d' % (k, d['ex'], d['ou'], d['n']))
        print('  vues sans etat honnete : %s' % (', '.join(sans_etat) or 0))
        print('  erreurs de page : %s' % (erreurs or 0))
        if fuites or sans_etat or erreurs:
            propre_partout = False
        ctx.close()
    nav.close()
print('\n%s' % ('TOUT PROPRE — le produit degrade honnetement'
                if propre_partout else 'DEFAUTS TROUVES — voir ci-dessus'))
