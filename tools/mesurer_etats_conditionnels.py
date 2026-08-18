"""tools/mesurer_etats_conditionnels.py — LES ÉTATS QUE L'ÉCRAN D'ACCUEIL NE MONTRE PAS.

La même réserve revient dans **trois** rapports — 41 §6.1, 46 §4.3, 47 §5.1 :

> Les états conditionnels (tiroir ouvert, bandeau d'erreur, watchlist remplie)
> restent hors du relevé navigateur.

Une réserve qui revient trois fois est une dette, pas une nuance. Cet outil la
paie : il conduit le produit dans ces états, puis y relance la sonde à
pictogrammes du lot 47 — celle qui lit le texte **et** les pseudo-éléments.

## La règle qui commande le montage

Chaque état doit être **atteint par le chemin du produit**, pas fabriqué.

- La watchlist se remplit par `VXEntities.toggleFavorite`, la fonction
  qu'appelle « Ajouter aux favoris ». Écrire `localStorage` avant le
  chargement ne marche pas — mesuré : l'hydratation de démarrage rapatrie le
  blob du serveur et écrase la clé. Le magasin n'est pas le chemin.
- Le menu d'entité s'ouvre en **cliquant** le bouton `[data-entity-menu]` de la
  page, avec son contenu réel.
- Le bandeau d'erreur apparaît en coupant les points de données, comme
  `mesurer_degradation.py` — pas en injectant un faux bandeau.

Ouvrir une surcouche avec un contenu d'essai — ce que fait le banc du clavier,
et c'est correct pour ce qu'il mesure — ne conviendrait PAS ici : on mesurerait
les pictogrammes de mon propre échafaudage. C'est la faute du lot 38 sous un
énième déguisement.

## Anti-vacuité, état par état

Un relevé « 0 emoji dans le tiroir » ne vaut rien si le tiroir ne s'est pas
ouvert. Chaque état porte donc sa **preuve d'atteinte** — un fait vérifié dans
la page — et l'outil refuse de conclure sur un état qu'il n'a pas su atteindre :
il le compte NON ATTEINT et sort en 2.

Usage : python tools/mesurer_etats_conditionnels.py [--base http://127.0.0.1:5002]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mesurer_pictogrammes import (  # noqa: E402  (chemin ajouté ci-dessus)
    SONDE, TEMOIN, _chromium, est_emoji, est_pictogramme)

#  Points de données coupés pour faire naître un bandeau d'erreur — même
#  périmètre que `mesurer_degradation.py`, et jamais le HTML/CSS/JS (sinon on
#  mesurerait un navigateur en panne, pas un produit qui dégrade).
_DONNEES = '**/{api,scan,cal-feed,news-feed}**'

#  Consigne de session : jamais appelés, même le réseau coupé.
_INTERDITS = ('**/api/ticker/**', '**/api/analyst/**', '**/api/correlations/**',
              '**/api/options-for/**', '**/options/*', '**/desc/**')


def _page(nav, base, url, avant=None, couper=False):
    #  SERVICE WORKER BLOQUÉ, et ce n'est pas un détail. Sans cela, le SW
    #  répond depuis son cache et la panne simulée n'atteint jamais la page :
    #  mesuré au premier jet, l'écran affichait « Analyse à jour » sous une
    #  coupure totale. Je mesurais un cache, pas une dégradation.
    ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                          service_workers='block')
    page = ctx.new_page()
    for motif in _INTERDITS:
        page.route(motif, lambda r: r.abort())
    if couper:
        page.route(_DONNEES, lambda r: r.fulfill(
            status=500, content_type='application/json',
            body='{"error":"panne simulee"}'))
    if avant:
        page.add_init_script(avant)
    page.goto(base + url, wait_until='domcontentloaded', timeout=45000)
    page.wait_for_timeout(3500)
    return ctx, page


def etat_watchlist(nav, base):
    """La watchlist REMPLIE — par la fonction du produit, pas par le magasin.

    Premier jet : j'écrivais `myFavs` dans `localStorage` avant le chargement.
    Mesure : la clé revenait à `[]`. L'hydratation de démarrage rapatrie le
    blob du serveur et **écrase** ce qui a été posé avant elle. Écrire le
    magasin n'est donc pas le chemin du produit ; `VXEntities.toggleFavorite`
    l'est — c'est ce qu'appelle « Ajouter aux favoris »."""
    ctx, page = _page(nav, base, '/portfolio?view=watchlist')
    #  ATTENDRE LA CONDITION, PAS LE CHRONOMÈTRE. Mesuré : à 3,5 s le premier
    #  jet posait bien les deux favoris, puis l'hydratation de démarrage
    #  arrivait ENSUITE et les effaçait — l'état paraissait tantôt atteint,
    #  tantôt non, selon la charge de la machine. Une attente fixe transforme
    #  une course en tirage au sort. On repose donc le geste jusqu'à ce qu'il
    #  tienne, et on renonce franchement s'il ne tient jamais.
    atteint = False
    for _ in range(6):
        page.wait_for_timeout(1500)
        if not page.evaluate('() => !!window.VXEntities'):
            continue
        page.evaluate("() => { if (!VXEntities.isFavorite('ABNB'))"
                      " VXEntities.toggleFavorite('ABNB');"
                      " if (!VXEntities.isFavorite('ALL'))"
                      " VXEntities.toggleFavorite('ALL'); }")
        page.wait_for_timeout(1200)
        if page.evaluate('() => VXEntities.favorites().length >= 2'):
            atteint = True
            break
    return ctx, page, atteint, 'deux favoris poses par la fonction du produit'


def etat_menu_entite(nav, base):
    """Le menu d'entité OUVERT, avec son contenu réel — cliqué, pas fabriqué."""
    ctx, page = _page(nav, base, '/opportunities?view=stocks')
    ouvert = page.evaluate("""() => {
      const b = document.querySelector('[data-entity-menu]');
      if (!b) return 'aucun declencheur';
      b.click();
      return 'clique';
    }""")
    page.wait_for_timeout(1200)
    atteint = ouvert == 'clique' and page.evaluate(
        "() => !!document.querySelector('.vx-modal, .vx-drawer, [role=\"dialog\"]')")
    return ctx, page, atteint, 'une surcouche du produit est ouverte'


def etat_bandeau_erreur(nav, base):
    """Le bandeau d'erreur — points de données coupés, comme une vraie panne."""
    ctx, page = _page(nav, base, '/', couper=True)
    #  On cherche un ÉTAT HONNÊTE, pas le mot « erreur ». Le produit ne dit pas
    #  « erreur » à l'utilisateur : il dit « indisponible », « indéterminé ».
    #  Chercher un vocabulaire technique aurait déclaré l'état non atteint
    #  alors qu'il l'était — et fait passer une bonne pratique pour une panne.
    atteint = page.evaluate(
        "() => /indisponible|indetermin|indétermin|impossible/i"
        ".test(document.body.innerText)")
    return ctx, page, atteint, 'un etat honnete de donnee absente est peint'


ETATS = (('watchlist remplie', etat_watchlist),
         ('menu d\'entite ouvert', etat_menu_entite),
         ('bandeau d\'erreur', etat_bandeau_erreur))


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    base = argv[argv.index('--base') + 1] if '--base' in argv else 'http://127.0.0.1:5002'

    from playwright.sync_api import sync_playwright   # import PARESSEUX (lot 35)

    peints, non_atteints = {}, []
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=_chromium(), args=['--no-sandbox'])
        try:
            for nom, ouvrir in ETATS:
                ctx, page, atteint, preuve = ouvrir(nav, base)
                try:
                    if not atteint:
                        non_atteints.append('%s — %s : NON' % (nom, preuve))
                        print('  %-24s NON ATTEINT (%s)' % (nom, preuve))
                        continue
                    #  Témoin par état : la sonde doit voir CE rendu-ci.
                    page.evaluate(
                        "t => { const d = document.createElement('div');"
                        " d.textContent = t; document.body.appendChild(d); }",
                        TEMOIN)
                    page.wait_for_timeout(120)
                    vus = page.evaluate(SONDE)
                    if TEMOIN not in vus:
                        non_atteints.append('%s — sonde muette' % nom)
                        print('  %-24s SONDE MUETTE' % nom)
                        continue
                    n = 0
                    for ch, info in vus.items():
                        if ch == TEMOIN or not est_pictogramme(ch):
                            continue
                        n += 1
                        e = peints.setdefault(ch, {'n': 0, 'etats': set()})
                        e['n'] += info['n']
                        e['etats'].add(nom)
                    print('  %-24s atteint · %2d pictogrammes peints' % (nom, n))
                finally:
                    ctx.close()
        finally:
            nav.close()

    print('\nPICTOGRAMMES PEINTS DANS CES ETATS — %d distincts' % len(peints))
    for ch, e in sorted(peints.items(), key=lambda x: -x[1]['n']):
        print('  %s U+%04X ×%-4d %-6s %s'
              % (ch, ord(ch[0]), e['n'], 'EMOJI' if est_emoji(ch) else 'signe',
                 ' · '.join(sorted(e['etats']))))

    fautes = {c: e for c, e in peints.items() if est_emoji(c)}
    if fautes:
        print('\n%d EMOJI PEINT(S) dans un etat conditionnel :' % len(fautes))
        for ch, e in fautes.items():
            print('  %s ×%d  %s' % (ch, e['n'], ' · '.join(sorted(e['etats']))))
        return 1
    if non_atteints:
        print('\nAVEUGLE — %d etat(s) non atteint(s) : un zero ne prouve rien '
              'la ou le produit n\'est pas alle.' % len(non_atteints))
        for a in non_atteints:
            print('  … %s' % a)
        return 2
    print('\nAUCUN EMOJI PEINT DANS LES ETATS CONDITIONNELS.')
    return 0


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
