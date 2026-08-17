"""Operabilite CLAVIER : controles non natifs, et contrat de focus des surcouches.

Deux mesures qu'aucun test de la suite ne peut faire, parce qu'elles exigent un
vrai navigateur qui appuie sur de vraies touches.

## 1. Les controles non natifs sont-ils ACTIVABLES ?

Un `role="button"` sur un span, une ligne de tableau cliquable : le navigateur
ne les active PAS tout seul — il ne le fait que pour button, a[href], input,
select. Sonde : focus, touche, et on regarde si un clic part.

Les DEUX touches sont testees (Entree et Espace) et TOUS les controles de
chaque vue. Le lot 27 n'en echantillonnait que six par vue et ne testait
qu'Entree ; le lot 28 a leve cette reserve — 45 controles au lieu de 18, meme
resultat.

## 2. Les surcouches tiennent-elles le focus ?

Six criteres par surcouche : ouverture, focus deplace dedans, focus PIEGE
(25 Tab restent dedans), Echap ferme, `inert` repose, et focus RENDU au
declencheur.

## Le faux positif a NE PAS corriger

`.vx-heatmap-scroll` ressort toujours « muet », et c'est correct : il porte
`role="region"` et un libelle qui annonce le defilement horizontal. Un
conteneur defilable focusable est un motif legitime ou Entree ne doit rien
faire. Lui donner `role="button"` pour faire taire cet outil transformerait une
region lisible au clavier en un controle qui ne fait rien.

Lancer :
    DEMO=1 NO_IBKR=1 START_ON_IMPORT=1 python terminal.py &
    python tools/mesurer_clavier.py
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


def _vues(fichier, symbole='_VIEWS'):
    src = io.open(os.path.join(_PAGES_DIR, fichier), encoding='utf-8').read()
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

# Les controles NON NATIFS uniquement : un <button> est active par le
# navigateur, il n'y a rien a verifier.
_COLLECTE = """() => {
  const vis = (e) => {
    const r = e.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return false;
    let n = e;
    while (n) {
      if (n.tagName === 'DETAILS' && !n.open) return false;
      const c = getComputedStyle(n);
      if (c.display === 'none' || c.visibility === 'hidden') return false;
      n = n.parentElement;
    }
    return true;
  };
  window.__vxCand = [...document.querySelectorAll(
    '#vx-content [role="button"], #vx-content [data-clickable], #vx-content [tabindex="0"]')]
    .filter(e => !['BUTTON','A','INPUT','SELECT','TEXTAREA','SUMMARY'].includes(e.tagName))
    .filter(vis);
  window.__vxClics = 0;
  document.addEventListener('click', () => { window.__vxClics++; }, true);
  return window.__vxCand.length;
}"""


def mesurer_controles(pg, touche):
    muets, testes = {}, 0
    for route, vues in PAGES:
        for v in vues:
            url = route + (('?view=' + v) if v else '')
            pg.goto(BASE + url, wait_until='domcontentloaded')
            pg.wait_for_timeout(2500)
            n = pg.evaluate(_COLLECTE)
            for i in range(n):
                info = pg.evaluate("""(i) => {
                  const e = window.__vxCand && window.__vxCand[i];
                  if (!e) return null;
                  e.focus(); window.__vxClics = 0;
                  return { ok: document.activeElement === e, tag: e.tagName,
                    cls: (e.className||'').toString().slice(0,36),
                    attrs: [...e.attributes].map(a=>a.name)
                      .filter(a=>a.startsWith('data-')||a==='role'||a==='tabindex').join(',') };
                }""", i)
                if not info or not info['ok']:
                    continue
                testes += 1
                pg.keyboard.press(touche)
                pg.wait_for_timeout(110)
                if pg.evaluate('() => window.__vxClics') == 0:
                    k = '%s .%s [%s]' % (info['tag'], info['cls'], info['attrs'])
                    muets[k] = muets.get(k, 0) + 1
                if pg.url != BASE + url:          # la touche a navigue
                    pg.goto(BASE + url, wait_until='domcontentloaded')
                    pg.wait_for_timeout(2200)
                    pg.evaluate(_COLLECTE)
    print('  touche %-6s : %d controles non natifs testes, %d muet(s)'
          % (repr(touche), testes, len(muets)))
    for k, c in muets.items():
        print('      %s x%d' % (k, c))
    return muets


def mesurer_surcouche(pg, url, genre):
    pg.goto(BASE + url, wait_until='domcontentloaded')
    pg.wait_for_timeout(2500)
    if not pg.evaluate("""() => {
        const e = document.querySelector('button');
        if (!e) return false; e.focus(); window.__vxDecl = e; return true; }"""):
        print('  %-28s aucun bouton sur la page' % genre)
        return False
    pg.evaluate("""(g) => { g === 'modale'
      ? VX.shell.openModal('Essai', '<button id="a">A</button><button id="b">B</button>', '<button id="c">C</button>')
      : VX.shell.openDrawer('Essai', '<button id="a">A</button><button id="b">B</button>'); }""", genre)
    pg.wait_for_timeout(700)
    ouvert = pg.evaluate(_ETAT)
    for _ in range(25):
        pg.keyboard.press('Tab')
    piege = pg.evaluate(_ETAT)
    pg.keyboard.press('Escape')
    pg.wait_for_timeout(500)
    ferme = pg.evaluate(_ETAT)
    retour = pg.evaluate('() => document.activeElement === window.__vxDecl')
    crit = {
        'ouverture': ouvert['ouvert'],
        'focus dedans': ouvert['dedans'],
        'focus piege': piege['dedans'],
        'Echap ferme': not ferme['ouvert'],
        'inert repose': ferme['inert'],
        'focus rendu': retour,
    }
    print('  %-28s %s' % (genre + ' (' + url + ')',
                          ' · '.join('%s=%s' % (k, 'oui' if v else 'NON')
                                     for k, v in crit.items())))
    return all(crit.values())


_ETAT = """() => {
  const a = document.activeElement;
  const m = document.getElementById('vx-modal'), d = document.getElementById('vx-drawer');
  const ouv = (x) => x && x.dataset.open === '1';
  return { ouvert: !!(ouv(m) || ouv(d)),
           dedans: !!((m && m.contains(a)) || (d && d.contains(a))),
           inert: !!(m && m.hasAttribute('inert') && d && d.hasAttribute('inert')) };
}"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(
        executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                          service_workers='block')
    pg = ctx.new_page()
    for motif in _INTERDITS:
        pg.route(motif, lambda r: r.abort())

    print('=== CONTROLES NON NATIFS')
    m1 = mesurer_controles(pg, 'Enter')
    m2 = mesurer_controles(pg, ' ')
    print('=== CONTRAT DE FOCUS DES SURCOUCHES')
    ok = mesurer_surcouche(pg, '/portfolio', 'modale')
    ok = mesurer_surcouche(pg, '/journal', 'tiroir') and ok
    ctx.close()
    nav.close()

# Le conteneur defilable est ATTENDU muet : c'est une region, pas un bouton.
reste = {k for k in list(m1) + list(m2) if 'vx-heatmap-scroll' not in k}
print('\n%s' % ('TOUT PROPRE (le conteneur defilable reste muet, et c\'est correct)'
                if ok and not reste else 'DEFAUTS TROUVES — voir ci-dessus'))
