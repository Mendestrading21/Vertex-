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
  /* DEBORDEMENT HORIZONTAL — et pourquoi `documentElement` ne peut PAS le dire
     ici. Mesure du lot 66 : `html` et `body` portent `overflow-x: clip`. Dans ce
     mode, `documentElement.scrollWidth` ne depasse JAMAIS `clientWidth` — il
     reste colle a la largeur du gabarit meme avec un element 400 px trop large
     (verifie : injecte 1840 px de contenu, `doc.scrollWidth` rendait toujours
     1440, `body.scrollWidth` rendait 1840).

     Le detecteur d'origine etait donc structurellement incapable de se
     declencher, et son « 0 debordement » sur cinq largeurs, publie depuis le
     lot 26, ne prouvait rien. Meme famille d'erreur que le lot 64 : une mesure
     qui ne peut pas rendre de resultat positif.

     On lit donc `body.scrollWidth` — que `clip` n'ecrase pas — et on nomme EN
     PLUS les elements dont le bord droit sort du gabarit, parce qu'un total ne
     dit pas QUOI corriger. `clip` a une consequence produit : rien ne defile,
     donc un element trop large est coupe en silence pour l'utilisateur aussi. */
  const vp = window.innerWidth;
  const coupables = [];
  /* ON BALAIE `body`, PAS `#vx-content`. Le premier relevé rendait « élément non
     identifié » sur 36 vues : le coupable est `.vx-topbar-right`, qui vit dans
     le SHELL, hors de la zone de contenu. Restreindre la recherche au contenu
     revenait à chercher la clé sous le lampadaire. */
  document.querySelectorAll('body *').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (r.right <= vp + 2) return;
    const cs = getComputedStyle(e);
    if (cs.position === 'fixed') return;      // overlays hors flux
    /* CE QUI DEPASSE N'EST PAS FORCEMENT PERDU. Une table large dans un
       conteneur `overflow-x:auto` sort du gabarit et reste ATTEIGNABLE : on
       fait defiler. L'accuser noierait le signal reel sous le patron le plus
       courant du produit — c'est l'exclusion `.vx-sr-only` de
       `mesurer_rognage_silencieux.py`, transposee. On ne retient donc que ce
       qu'AUCUN ancetre defilant ne rattrape. */
    let a = e.parentElement, rattrape = false;
    while (a && a !== document.body) {
      const ca = getComputedStyle(a);
      const peutDefiler = (ca.overflowX === 'auto' || ca.overflowX === 'scroll'
                           || ca.overflow === 'auto' || ca.overflow === 'scroll');
      if (peutDefiler && a.scrollWidth - a.clientWidth > 2) { rattrape = true; break; }
      a = a.parentElement;
    }
    if (rattrape) return;
    coupables.push({ cls: (e.className || '').toString().slice(0, 36),
                     tag: e.tagName, depasse: Math.round(r.right - vp) });
  });
  return { dbl: [...dbl], hrefs: [...new Set(hrefs)],
           debordeH: Math.max(0, document.body.scrollWidth - vp),
           coupables: coupables.slice(0, 6) };
}"""


# LE TEMOIN DE DETECTION — a ne pas confondre avec le temoin de LARGEUR qui
# existait deja plus bas. Celui-la prouve que le navigateur a applique le
# gabarit ; il ne prouve pas que les DETECTEURS mordent. « TOUT PROPRE » sur
# quatre detecteurs jamais mis a l'epreuve et « je ne sais pas voir » rendent
# exactement le meme resultat.
#
# On fabrique donc dans la page les trois defauts que l'outil pretend trouver —
# un id duplique, un debordement horizontal, un lien interne casse — et on exige
# qu'il les denonce tous les trois. Rien n'est ecrit sur le disque.
_TEMOIN_ID = 'vx-temoin-id-duplique'
_TEMOIN_LIEN = '/vx-cette-route-nexiste-pas-temoin'
_TEMOIN_JS = """() => {
  const hote = document.body;
  for (let i = 0; i < 2; i++) {
    const d = document.createElement('div');
    d.id = '%s';
    hote.appendChild(d);
  }
  const large = document.createElement('div');
  large.style.cssText = 'width:' + (window.innerWidth + 400) + 'px;height:4px';
  hote.appendChild(large);
  const a = document.createElement('a');
  a.setAttribute('href', '%s');
  a.textContent = 'temoin';
  hote.appendChild(a);
  return true;
}""" % (_TEMOIN_ID, _TEMOIN_LIEN)


def _navigateur(pw):
    """Chemin par glob : la version epinglee en dur casse des que l'image change."""
    import glob
    for motif in ('/opt/pw-browsers/chromium-*/chrome-linux/chrome',
                  '/opt/pw-browsers/chromium'):
        trouves = sorted(glob.glob(motif))
        if trouves:
            return pw.chromium.launch(executable_path=trouves[-1], args=['--no-sandbox'])
    return pw.chromium.launch(args=['--no-sandbox'])


def balayer(pw, largeur, hauteur, etiquette, temoin=False):
    nav = _navigateur(pw)
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
            if temoin:
                pg.evaluate(_TEMOIN_JS)
            r = pg.evaluate(JS)
            pg.remove_listener('console', _console)

            if r['dbl']:
                ids_dbl[url] = r['dbl']
            liens.update(r['hrefs'])
            if errs:
                erreurs[url] = sorted(set(errs))[:3]
            if r['debordeH'] > 2:
                qui = ', '.join('%s.%s +%dpx' % (c['tag'], c['cls'], c['depasse'])
                                for c in r['coupables']) or 'element non identifie'
                reflow.append('%s (+%d px) — %s' % (url, r['debordeH'], qui))

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

    if temoin:
        #  LES TROIS DEFAUTS FABRIQUES DOIVENT AVOIR ETE DENONCES. Si l'un
        #  d'eux passe inapercu, le detecteur correspondant est aveugle et son
        #  « 0 » de la vraie mesure ne veut rien dire.
        vus = {
            'id duplique': any(_TEMOIN_ID in v for v in ids_dbl.values()),
            'debordement H': bool(reflow),
            'lien casse': any(_TEMOIN_LIEN in c for c in casses),
        }
        for quoi, vu in vus.items():
            print('  TEMOIN %-16s %s' % (quoi, 'DENONCE — le detecteur mord'
                                         if vu else '*** PASSE INAPERCU ***'))
        ctx.close()
        nav.close()
        return all(vus.values())

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

def main(argv=None):
    import sys
    argv = list(sys.argv[1:] if argv is None else argv)
    temoin = '--temoin' in argv
    #  Le temoin n'a besoin que d'UNE largeur : il eprouve les detecteurs, pas
    #  la mise en page. Le faire tourner cinq fois couterait cinq balayages
    #  complets pour la meme preuve.
    largeurs = (LARGEURS[0],) if temoin else LARGEURS
    with sync_playwright() as pw:
        ok = True
        for largeur, hauteur, titre in largeurs:
            ok = balayer(pw, largeur, hauteur, titre, temoin=temoin) and ok
    if temoin:
        print('\n%s' % ('TEMOIN OK — les trois detecteurs mordent' if ok
                        else 'AVEUGLE — un detecteur au moins ne voit pas'))
        return 0 if ok else 2
    print('\n%s' % ('TOUT PROPRE' if ok else 'DEFAUTS TROUVES — voir ci-dessus'))
    return 0 if ok else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
