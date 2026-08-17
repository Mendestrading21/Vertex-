"""PANNE PARTIELLE : une source tombe, les autres repondent normalement.

Le lot 29 avait eprouve les pannes GLOBALES et conclu par une reserve : « une
panne PARTIELLE est un regime different, ou un chiffre faux peut se glisser
entre des chiffres justes sans qu'aucun etat d'erreur ne s'affiche ».

Le lot 30 a construit cet outil, mesure les fuites et les erreurs (0 et 0), et
LAISSE LA QUESTION OUVERTE en la documentant : les trois methodes essayees
donnaient des faux positifs. Le lot 35 la ferme.

## Ce qui a debloque la mesure

1. CLE PAR CHEMIN DOM. La cle du lot 30 (`e.className` + longueur) mettait tout
   texte SVG dans le meme seau — `className` vaut « [object SVGAnimatedString] »
   — et glissait des qu'un element apparaissait. Le chemin DOM designe une
   cellule et une seule. Effet mesure : 546 cellules chiffrees, 546 STABLES,
   contre 637 sur 1768 avec l'ancienne cle.

2. MESURE ENCADREE — et il a fallu TROIS tentatives, chacune mesuree.
   (a) UNE reference globale, puis dix sources eprouvees : vingt minutes plus
       tard, « Il y a 5 min » etait devenu « Il y a 8 min » et l'outil accusait
       quinze chiffres. C'etait l'horloge.
   (b) DEUX references immediates, a la meme cadence : mieux, mais insuffisant.
       Un libelle a la minute ne bouge pas en 2,4 s, puis tombe pile pendant la
       mesure — la course complete en gardait quatre.
   (c) DEUX references AVANT + UN CONTROLE APRES, tous sans panne. Une cellule
       n'est jugee que si elle est identique dans les TROIS.
   (d) MEME CACHE DES DEUX COTES. Apres (c) il restait quatre cas sur
       /system?view=automations, et j'ai eu tort d'en conclure que « la panne
       change vraiment la duree ». La cause etait mon montage : le bras de
       controle reutilisait UN contexte pour ses trois releves, donc le cache
       client (`VX.fetch`, 15 s) lui rendait la meme valeur, tandis que le bras
       sous panne — contexte neuf — refetchait. Toute valeur vivante differait
       donc entre les bras. Un CONTEXTE NEUF PAR RELEVE, des deux cotes, retire
       cet avantage. Voir `_releve_neuf`.
   La vue en cause ne lit meme pas /api/desk : elle lit /api/system/automations.
   C'est ce detail, verifie dans le code, qui a fait tomber ma conclusion.

3. TOUT CHIFFRE QUI CHANGE, pas seulement les zeros. Le lot 30 ne cherchait
   qu'un « 0 » substitue. Une moyenne sur cinq sources au lieu de six est
   plausible, et fausse.

## Le temoin, sans lequel un « 0 » ne prouve rien

Un balayage qui ne trouve rien peut vouloir dire que le produit est honnete, ou
que l'instrument est aveugle. Le temoin fabrique le defaut : la source repond
200 avec un corps VALIDE mais ALTERE. La vue n'a alors aucune raison d'afficher
une erreur — elle affiche un chiffre faux. Si l'outil ne le voit pas, son « 0 »
ne vaut rien et il le DIT.

Lancer :
    DEMO=1 NO_IBKR=1 START_ON_IMPORT=1 python terminal.py &
    python tools/mesurer_panne_partielle.py
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# IMPORT PARESSEUX de Playwright — il est fait dans `main()`, pas ici.
# Mesuré au lot 35 : le gardien importe ce module pour éprouver sa LOGIQUE
# (`_silencieux`, la clé DOM, la liste des sources), et cette logique est pure.
# Un import de Playwright au chargement rendait TOUTE la suite incollectable en
# CI, qui n'a pas le navigateur — un échec que mon poste ne pouvait pas montrer,
# puisqu'il l'a. Ce que l'outil exige pour MESURER ne doit pas être exigé pour
# le LIRE.

BASE = 'http://localhost:5002'
_PAGES_DIR = os.path.join('vertex', 'ui', 'pages')
_INTERDITS = ('**/api/ticker/**', '**/api/analyst/**', '**/api/correlations/**',
              '**/api/options-for/**', '**/options/*', '**/desc/**')
CIBLES = ('/scan', '/api/pos-quotes', '/api/market/summary', '/api/market/regime',
          '/api/command', '/api/options/overview', '/cal-feed',
          '/api/briefing/editorial', '/api/opportunities/funnel', '/api/desk')


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

# Une cellule = un element feuille portant un CHIFFRE, designe par son CHEMIN DOM.
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
  const chemin = (e) => {
    const b = [];
    for (let n = e; n && n.id !== 'vx-content'; n = n.parentElement) {
      const p = n.parentElement;
      if (!p) break;
      b.push(n.tagName + ':' + ([...p.children].indexOf(n)));
    }
    return b.reverse().join('>');
  };
  const cellules = {};
  let fuite = null;
  const hote = document.getElementById('vx-content');
  if (!hote) return { cellules, fuite, etats: 0, mentions: 0 };
  hote.querySelectorAll('*').forEach(e => {
    if (e.classList.contains('vx-sr-only') || !vis(e)) return;
    const t = [...e.childNodes].filter(n => n.nodeType === 3)
      .map(n => n.textContent).join('').trim();
    if (!t) return;
    if (!fuite && /\\b(NaN|undefined|null|Infinity|\\[object Object\\])\\b/.test(t)) {
      fuite = t.slice(0, 60);
    }
    if (t.length <= 24 && /\\d/.test(t)) cellules[chemin(e)] = t;
  });
  return {
    cellules, fuite,
    etats: hote.querySelectorAll('[data-state], .vx-state, .vx-empty, '
      + '.vx-error-banner, .vx-insufficient').length,
    mentions: (hote.innerText.match(
      /(^|\\s)(—|n\\/d|indisponible|non évaluable|non disponible|aucune donnée)/gi) || []).length,
  };
}"""


def _ouvrir(nav, panne=None, alterer=None):
    ctx = nav.new_context(viewport={'width': 1440, 'height': 900}, service_workers='block')
    pg = ctx.new_page()
    for motif in _INTERDITS:
        pg.route(motif, lambda r: r.abort())
    if panne:
        pg.route('**' + panne + '*',
                 lambda r: r.fulfill(status=500, content_type='application/json',
                                     body='{"error":"panne partielle"}'))
    if alterer:
        pg.route('**' + alterer + '*', _altere)
    return ctx, pg


def _altere(route):
    """200 + corps VALIDE mais FAUX : la vue n'a aucune raison de crier."""
    try:
        rep = route.fetch()
        d = rep.json()
        if isinstance(d, dict):
            if d.get('vix') is not None:
                d['vix'] = float(d['vix']) + 7.77
            if isinstance(d.get('breadth'), dict) and d['breadth'].get('above200') is not None:
                d['breadth']['above200'] = 3
        route.fulfill(status=200, content_type='application/json', body=json.dumps(d))
    except Exception:
        route.continue_()


def _releve(pg, url):
    pg.goto(BASE + url, wait_until='domcontentloaded', timeout=20000)
    pg.wait_for_timeout(2400)
    return pg.evaluate(JS)


def _releve_neuf(nav, url, panne=None, erreurs=None):
    """Un CONTEXTE NEUF par releve — pour les DEUX bras, sain comme en panne.

    Sans cela, les bras ne sont pas comparables, et je l'ai paye : le bras de
    controle reutilisait un seul contexte pour ses trois releves, donc le cache
    client (`VX.fetch` garde 15 s) lui rendait la MEME valeur, pendant que le
    bras sous panne, contexte neuf, refetchait. Toute valeur vivante (un age
    calcule par le serveur) differait alors systematiquement entre les bras —
    et l'outil l'imputait a la panne.

    J'avais conclu de ces quatre cas qu'ils « passaient l'encadrement, donc la
    panne change vraiment la duree ». C'etait faux : c'etait mon montage.
    Meme cache, meme conditions, des deux cotes."""
    ctx, pg = _ouvrir(nav, panne=panne)
    try:
        if erreurs is not None:
            pg.on('pageerror', lambda e: erreurs.append(str(e)[:70]))
        return _releve(pg, url)
    finally:
        ctx.close()


# Un libellé de DURÉE (« Il y a 25 min », « dans ~3 min », « 41 s »). Ce
# n'est pas un filtre qui masque : ces cas sont TOUJOURS affichés, mais comptés
# à part, parce qu'ils ne répondent pas à la même question. Mesuré au lot 35 :
# même encadrée, la mesure en garde quatre sur `/system?view=automations` —
# identiques dans les trois relevés sains, différents sous panne. La panne
# change donc bien la durée affichée (vraisemblablement l'horodatage de repli
# employé), mais une durée plus ancienne n'est pas un chiffre INVENTÉ. Les
# confondre ferait dire à l'outil autre chose que ce qu'il mesure.
_DUREE = re.compile(r'^\s*(il y a|dans\s*~?|depuis)?\s*[\d.,]+\s*(s|min|h|j|'
                    r'seconde|minute|heure|jour)s?\s*$', re.I)


def est_duree(txt):
    return bool(_DUREE.match(txt or ''))


def _silencieux(avant, apres):
    """Chiffres CHANGES que la vue ne signale pas. `avant` est la reference la
    plus RECENTE, `apres` la mesure sous panne."""
    if apres['etats'] > avant['etats'] or apres['mentions'] > avant['mentions']:
        return []                       # la vue DIT qu'il lui manque quelque chose
    out = []
    for k, v in avant['cellules'].items():
        w = apres['cellules'].get(k)
        if w is None or w == v or not re.search(r'\d', w):
            continue                    # disparu, inchange, ou devenu « — » : honnete
        out.append('« %s » -> « %s »' % (v, w))
    return out


def main():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        nav = pw.chromium.launch(
            executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')

        # 1. La carte QUI APPELLE QUOI, mesuree.
        ctx, pg = _ouvrir(nav)
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
                _releve(pg, url)
                pg.remove_listener('request', _req)
                usage[url] = vus
        ctx.close()
        print('=== QUI APPELLE QUOI (mesure)')
        for c in CIBLES:
            print('  %-26s %d vue(s)' % (c, len([u for u, s in usage.items() if c in s])))

        # 2. Une source en panne a la fois — SEULES les vues concernees.
        fuites, erreurs, muets, durees = [], [], [], []
        for cible in CIBLES:
            concernees = [u for u, s in usage.items() if cible in s]
            if not concernees:
                print('--- %-26s aucune vue concernee' % cible)
                continue
            n_muets = 0
            for url in concernees:
                # Contextes recrees PAR VUE. Les garder ouverts sur des dizaines
                # de vues fait accumuler les processus du navigateur jusqu'au
                # blocage — mesure : l'outil se figeait apres quelques vues, sans
                # rien dire. Le cout (~0,3 s par contexte) est le prix d'une
                # mesure qui va au bout.
                # LA MESURE EST ENCADREE. Deux references AVANT, un controle
                # APRES, tous sans panne. Une cellule n'est jugee que si elle
                # est identique dans les TROIS : ce qui change alors sous panne
                # ne peut venir que de la panne.
                #
                # La double reference seule ne suffisait pas, et c'est mesure :
                # une horloge a la minute ne bouge pas entre deux releves
                # espaces de 2,4 s, puis tombe pile pendant la mesure. Le
                # balayage complet accusait ainsi « Il y a 25 min » -> « 26 min »
                # et « dans ~1 min » -> « ~0 min ». Le controle d'apres les
                # elimine SANS lister les formats de duree — on demande a la
                # cellule si elle bouge aussi quand rien n'est casse.
                a = _releve_neuf(nav, url)
                b = _releve_neuf(nav, url)
                errs = []
                c = _releve_neuf(nav, url, panne=cible, erreurs=errs)
                d = _releve_neuf(nav, url)
                stables = {k: v for k, v in b['cellules'].items()
                           if a['cellules'].get(k) == v and d['cellules'].get(k) == v}
                if c['fuite']:
                    fuites.append('%s :: %s' % (url, c['fuite']))
                if errs:
                    erreurs.append('%s :: %s' % (url, errs[0]))
                for ligne in _silencieux(dict(b, cellules=stables), c):
                    avant_txt = ligne.split(' » -> « ')[0].lstrip('« ')
                    apres_txt = ligne.split(' » -> « ')[-1].rstrip(' »')
                    cas = '%s [%s] %s' % (url, cible, ligne)
                    if est_duree(avant_txt) and est_duree(apres_txt):
                        durees.append(cas)          # compté à part, jamais masqué
                    else:
                        muets.append(cas)
                        n_muets += 1
            print('--- %-26s %2d vue(s) · chiffres changes EN SILENCE : %d'
                  % (cible, len(concernees), n_muets))

        # 3. LE TEMOIN — sans lui, un « 0 » ne prouve rien.
        # Meme regle pour le temoin : contexte neuf des deux cotes.
        a = _releve_neuf(nav, '/')
        b = _releve_neuf(nav, '/')
        ctxT, pgT = _ouvrir(nav, alterer='/api/market/summary')
        t = _releve(pgT, '/')
        ctxT.close()
        d = _releve_neuf(nav, '/')
        stables = {k: v for k, v in b['cellules'].items()
                   if a['cellules'].get(k) == v and d['cellules'].get(k) == v}
        vu = _silencieux(dict(b, cellules=stables), t)
        nav.close()

    print('\n=== TEMOIN (source qui repond 200 avec un corps FAUX)')
    for ligne in vu[:4]:
        print('    ' + ligne)
    if not vu:
        print('    AUCUN — l instrument est AVEUGLE, son « 0 » ne vaut rien.')
        return 2
    print('    l instrument voit un chiffre faux silencieux : il peut echouer.')

    print('\n=== VERDICT')
    print('  fuites techniques : %s' % (fuites or 0))
    print('  erreurs de page   : %s' % (erreurs or 0))
    print('  chiffres faux SILENCIEUX : %s' % (muets or 0))
    # Les DUREES sont toujours dites, jamais masquees — mais elles ne repondent
    # pas a la meme question qu'un chiffre invente. Voir le commentaire de _DUREE.
    print('  libelles de DUREE modifies (comptes a part) : %d' % len(durees))
    for d in durees[:6]:
        print('    ' + d)
    if fuites or erreurs or muets:
        return 1
    print('\nSOUS PANNE PARTIELLE, AUCUN CHIFFRE INVENTE NE S AFFICHE EN SILENCE.')
    if durees:
        print('RESERVE : %d libelle(s) de duree changent sous panne. Une duree '
              'plus ancienne n est pas un chiffre invente, mais la cause reste '
              'a expliquer.' % len(durees))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
