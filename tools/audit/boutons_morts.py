"""Detecte les BOUTONS MORTS en les CLIQUANT, et en regardant s il se passe
quelque chose.

La doctrine produit interdit la « fausse fonctionnalite » : un bouton qui
invite au clic et ne peut rien produire. Rien ne la mesurait -- un bouton
inerte a exactement la meme apparence qu un bouton qui marche.

## Pourquoi on ne lit pas les ecouteurs

Premiere version de cet outil : interroger `DOMDebugger.getEventListeners` sur
le bouton puis sur chacun de ses ancetres, `document` et `window` compris, pour
tenir compte de la delegation. Contre-epreuve : un bouton temoin, sans le
moindre gestionnaire, insere dans la coque. **L outil ne l a pas vu.**

La raison est structurelle : la coque pose un ecouteur de clic sur `document`.
Tout bouton a donc un ancetre qui « ecoute », et la mesure repond toujours
« vivant ». Elle n aurait jamais rien trouve -- un zero rassurant et faux.

## Ce qu on mesure a la place

On clique, et on regarde s il se passe QUOI QUE CE SOIT :

  · une mutation du DOM (MutationObserver sur tout le document) ;
  · une requete reseau ;
  · une tentative de navigation ;
  · une ecriture dans `localStorage` / `sessionStorage` ;
  · un DEFILEMENT de la page.

Aucun des cinq : le bouton n a rien produit.

Le defilement a ete ajoute apres coup : sur la page d accueil, les pastilles
d ancre ne font QUE defiler vers un bloc. Sans cette mesure, l outil declarait
morte une commande qui marche.

Troisieme correction, meme lecon : les boutons d un `<details>` REPLIE gardent
une boite de mise en page dans Chromium. L outil les cliquait de force, a des
coordonnees ou il n y a rien, et lisait le silence comme une panne. On ne force
plus le clic -- si Playwright refuse d atteindre un element, l utilisateur ne
l atteindrait pas non plus, et la question ne se pose pas.

Trois faux positifs, trois fois ecartes AVANT qu une ligne de produit ne soit
touchee. On ne corrige pas ce qu un outil n a pas prouve.

## Sûreté

Vertex est en lecture seule, mais on ne s en remet pas a ca :

  · toute requete non-GET est **bloquee** avant de partir -- elle compte
    comme un effet, sans etre executee ;
  · toute navigation est **bloquee** -- elle compte comme un effet ;
  · l etat est recharge entre chaque bouton, donc un clic ne peut pas
    influencer le suivant.

Usage :
    python tools/audit/boutons_morts.py --routes / /markets
"""
from __future__ import annotations

import argparse

_JS_CANDIDATS = r"""() => {
  const out = [];
  document.querySelectorAll('button, [role="button"], .vx-btn, .vx2-btn')
    .forEach((b, i) => {
      const r = b.getBoundingClientRect();
      if (r.width < 4 || r.height < 4) return;                 // invisible
      // Un `<details>` REPLIE garde, dans Chromium, les boites de mise en page
      // de son contenu : ses boutons ont une largeur et une hauteur alors que
      // personne ne les voit. `vertex_2_0_etats_vides.py` avait deja releve ce
      // piege ; cet outil l'ignorait, et declarait morts six boutons de la
      // fiche Options qui vivent simplement dans un repli ferme.
      if (b.closest('details:not([open])')) return;
      if (b.disabled || b.getAttribute('aria-disabled') === 'true') return;
      if (b.tagName === 'A' && b.getAttribute('href')) return;  // c'est un lien
      const t = (b.getAttribute('type') || '').toLowerCase();
      if ((t === 'submit' || t === 'reset') && b.closest('form')) return;
      b.setAttribute('data-vx-sonde', String(i));
      out.push({ sonde: String(i),
                 texte: (b.innerText || b.getAttribute('aria-label') || '')
                          .trim().slice(0, 44),
                 id: b.id || '' });
    });
  return out;
}"""

_JS_ARMER = r"""() => {
  // Le defilement EST un effet : plusieurs commandes de la page d'accueil ne
  // font que cela (les pastilles d'ancre menent a un bloc). Sans cette
  // mesure, l'outil les declarait mortes.
  //  REMPLIR UN CHAMP EST UN EFFET, et c'est meme le plus courant dans un
  //  produit fait de filtres et de formulaires. Une `value` d'input est une
  //  PROPRIETE, pas un attribut : le MutationObserver ne la voit pas, aucun
  //  reseau ne part, rien ne defile. L'outil declarait donc morts des boutons
  //  qui marchent.
  //
  //  Mesure : sur `/intelligence`, NEUF boutons sur seize — les quatre
  //  exemples de questions (« La these tient-elle apres les resultats ? »…)
  //  et les cinq pastilles de tickers. Leur handler fait exactement
  //  `$('vx-analyst-q').value = …` puis `focus()`. Ils remplissent le
  //  formulaire de l'analyste, et l'outil les enterrait.
  const champs = () => [...document.querySelectorAll('input, select, textarea')]
    .map(c => (c.type === 'checkbox' || c.type === 'radio')
                ? (c.checked ? '1' : '0') : String(c.value == null ? '' : c.value))
    .join('\u0001');
  window.__vxChamps = champs;
  window.__vxEffet = { dom: 0, stockage: 0, defile: 0, champs: 0,
                       c0: champs(),
                       y0: window.scrollY, x0: window.scrollX };
  window.__vxObs = new MutationObserver(m => { window.__vxEffet.dom += m.length; });
  window.__vxObs.observe(document.documentElement,
    { childList: true, subtree: true, attributes: true, characterData: true });
  ['localStorage', 'sessionStorage'].forEach(nom => {
    const s = window[nom];
    if (!s || s.__vxPatche) return;
    const brut = s.setItem.bind(s);
    s.setItem = function (k, v) { window.__vxEffet.stockage++; return brut(k, v); };
    try { Object.defineProperty(s, '__vxPatche', { value: true }); } catch (e) {}
  });
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--routes', nargs='+', required=True)
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ap.add_argument('--wait', type=int, default=2400)
    ap.add_argument('--apres', type=int, default=400,
                    help='delai laisse au bouton pour produire son effet, en ms')
    ap.add_argument('--budget', type=int, default=90,
                    help='secondes accordees a une route ; au-dela elle est '
                         'declaree NON COUVERTE plutot que de bloquer le releve')
    args = ap.parse_args()

    import time

    from playwright.sync_api import sync_playwright

    total, non_couvertes = 0, []
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=args.exe)
        ctx = nav.new_context(viewport={'width': 1440, 'height': 1000})
        page = ctx.new_page()

        effets = {'reseau': 0, 'navigation': 0}

        def _route(route, requete):
            if requete.method != 'GET':
                effets['reseau'] += 1
                route.abort()                       # on ne LAISSE PAS partir
                return
            if requete.is_navigation_request() and requete.frame is page.main_frame:
                effets['navigation'] += 1
                route.abort()
                return
            effets['reseau'] += 1
            route.continue_()

        for route_url in args.routes:
            page.goto(args.base + route_url, wait_until='domcontentloaded')
            page.wait_for_timeout(args.wait)
            candidats = page.evaluate(_JS_CANDIDATS)
            morts, instables = [], []
            debut, testes = time.monotonic(), 0
            for cand in candidats:
                # Une route lente ne doit pas faire taire tout le releve : on
                # borne son temps et on DIT ce qui n'a pas ete teste, plutot que
                # de rendre une couverture partielle en la presentant comme
                # complete.
                if time.monotonic() - debut > args.budget:
                    break
                testes += 1
                page.goto(args.base + route_url, wait_until='domcontentloaded')
                page.wait_for_timeout(args.wait)
                page.evaluate(_JS_CANDIDATS)        # repose les sondes
                page.evaluate(_JS_ARMER)
                effets['reseau'] = effets['navigation'] = 0
                page.route('**/*', _route)
                cible = page.locator('[data-vx-sonde="%s"]' % cand['sonde']).first
                url_avant = page.url

                #  LE MEME BOUTON, OU UN AUTRE ? Les sondes sont reposees a
                #  chaque re-navigation, dans l'ordre du DOM. Une page qui rend
                #  en plusieurs temps n'a pas le meme DOM a 2,4 s qu'a 6 s : la
                #  sonde N peut alors designer un AUTRE element, ou le meme
                #  avant son remplissage. Cliquer la ne mesure plus rien.
                #
                #  Mesure qui a impose ce garde-fou : sur `/`, cinq tuiles
                #  d'options ont ete declarees mortes. Leur propre trace le
                #  disait — « strike 205 · prime  », la prime VIDE — alors
                #  qu'une page stabilisee affiche « prime 43,84 $ » et que le
                #  clic navigue bien vers /options/dossier/ACN. Cinq faux
                #  morts, et un instrument qui crie faux finit par ne plus
                #  etre cru : c'est alors le vrai bouton mort qu'on rate.
                #  L'identite se lit AVEC LA MEME REGLE que `_JS_CANDIDATS` :
                #  `innerText` SINON `aria-label`. Premiere version : elle ne
                #  lisait que `innerText`, et ecartait donc les quatre boutons
                #  a icone de la coque — Connexions, Notifications, Actualiser,
                #  Reduire la navigation — sur les DOUZE routes. Un garde-fou
                #  qui retire 48 boutons du releve coute plus qu'il ne protege.
                _LIRE = ("el => (el.innerText || el.getAttribute('aria-label')"
                         " || '').trim().slice(0, 44)")
                try:
                    texte_courant = cible.evaluate(_LIRE, timeout=1500)
                except Exception:
                    texte_courant = None
                if texte_courant is not None and texte_courant != cand['texte']:
                    page.wait_for_timeout(args.apres * 3)   # laisse finir le rendu
                    try:
                        texte_courant = cible.evaluate(_LIRE, timeout=1500)
                    except Exception:
                        texte_courant = None
                if texte_courant is not None and texte_courant != cand['texte']:
                    page.unroute('**/*', _route)
                    instables.append(cand)
                    continue

                try:
                    # PAS de `force` : on veut que Playwright refuse un element
                    # que l'utilisateur ne pourrait pas atteindre. Forcer le clic
                    # l'envoyait a des coordonnees ou il n'y a rien, et le silence
                    # qui suivait se lisait comme un bouton mort.
                    cible.click(timeout=2500)
                except Exception:
                    page.unroute('**/*', _route)
                    continue                        # non cliquable : hors sujet
                page.wait_for_timeout(args.apres)
                page.unroute('**/*', _route)
                #  LA NAVIGATION SE LIT SUR L'URL, PAS SUR UNE EXCEPTION.
                #
                #  Le releve d'en dessous supposait qu'une page qui navigue
                #  ferait LEVER `page.evaluate`. Elle ne leve pas : l'appel
                #  reussit sur le NOUVEAU document, ou `window.__vxEffet`
                #  n'existe pas, et le repli `{dom:0, stockage:0, …}` rendait
                #  alors « aucun effet ». Tout bouton qui navigue par
                #  `location.href` etait donc declare MORT.
                #
                #  Mesure : sur `/`, cinq tuiles d'options. Verifie une par une
                #  — meme sequence, memes 2,4 s, meme interception — l'URL
                #  passe de `/` a `/options/dossier/ACN`. Elles marchent, et
                #  l'outil disait le contraire. Cinq faux morts sur 45.
                if page.url != url_avant:
                    continue                        # a navigue : c'est un effet
                try:
                    interne = page.evaluate(
                        '() => { const e = window.__vxEffet'
                        ' || {dom:0,stockage:0,defile:0,champs:0,y0:0,x0:0};'
                        ' if (window.scrollY !== e.y0 || window.scrollX !== e.x0)'
                        '   e.defile = 1;'
                        ' if (window.__vxChamps && e.c0 !== undefined'
                        '     && window.__vxChamps() !== e.c0) e.champs = 1;'
                        ' return e; }')
                except Exception:
                    continue                        # la page a navigue : c'est un effet
                rien = (not interne.get('dom') and not interne.get('stockage')
                        and not interne.get('defile') and not interne.get('champs')
                        and not effets['reseau'] and not effets['navigation'])
                if rien:
                    morts.append(cand)
            total += len(morts)
            reste = len(candidats) - testes
            if reste > 0:
                non_couvertes.append(route_url)
                etat = 'BUDGET DEPASSE (%ds) - %d/%d teste(s)' % (
                    args.budget, testes, len(candidats))
            elif morts:
                etat = '%d mort(s) sur %d' % (len(morts), len(candidats))
            else:
                etat = 'OK (%d bouton(s) teste(s))' % len(candidats)
            if instables:
                etat += ' · %d non stabilise(s)' % len(instables)
            print('%-40s %s' % (route_url, etat))
            for m in morts:
                print('     « %s »%s' % (m['texte'] or '(sans texte)',
                                         '  #' + m['id'] if m['id'] else ''))
            #  DITS, PAS TUS : un bouton non stabilise n'est ni sain ni mort,
            #  il n'a pas ete juge. Le taire rendrait une couverture partielle
            #  pour une couverture complete.
            for m in instables:
                print('     ~ non stabilise : « %s »' % (m['texte'] or '(sans texte)'))
        nav.close()
    print('\nTOTAL : %d bouton(s) mort(s) sur %d route(s)'
          % (total, len(args.routes)))
    if non_couvertes:
        print('COUVERTURE INCOMPLETE sur %d route(s) : %s'
              % (len(non_couvertes), ', '.join(non_couvertes)))
    return 1 if total else 0


if __name__ == '__main__':
    raise SystemExit(main())
