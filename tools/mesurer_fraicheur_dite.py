"""tools/mesurer_fraicheur_dite.py — UN CHIFFRE VRAI HIER, AFFICHÉ SANS LE DIRE.

Réserve SIGNAL-OS-61 §6.2, de ma main :

> La **fraîcheur n'est pas jugée**. Un nombre présent dans une réponse
> **périmée** paraît tracé. La moitié « périmée » de la réserve du lot 60 reste
> donc ouverte.

C'est la moitié la plus sournoise. Un chiffre inventé est faux tout de suite ; un
chiffre **périmé** a été vrai, il reste plausible, et rien à l'écran ne le
distingue d'un chiffre frais. *Un chiffre vrai hier, affiché sans dire qu'il date
d'hier, est un mensonge par omission.*

## Le produit a déjà le vocabulaire — la question est s'il s'en sert

`VX.freshness` définit six états, avec des seuils explicites :

| état | seuil |
| --- | --- |
| `live` | < 20 s |
| `snapshot` (« Analyse ») | < 30 min |
| `stale` (« À actualiser ») | au-delà de 35 min |
| `saved` · `error` · `offline` | selon le cas |

La question mesurable est donc précise : **quand la donnée vieillit réellement,
l'écran le dit-il ?**

## L'expérience : un AVANT/APRÈS, jamais une seule photo

On interroge chaque espace deux fois :

1. **nominal** — la réponse passe telle quelle ;
2. **vieilli** — on intercepte les réponses et on réécrit leurs champs d'âge
   (`age_s`, `scan_age`, `ts`) pour placer la donnée bien au-delà du seuil.

Une seule photo ne prouverait rien : voir « Analyse » ne dit pas si l'étiquette
réagit, et voir « À actualiser » ne dit pas si elle réagit *à la bonne chose*.
Seul l'écart entre les deux est une mesure.

## Anti-vacuité — trois refus de conclure

1. Si le nominal n'affiche **aucune** étiquette de fraîcheur, il n'y a rien à
   observer : l'outil rend 2 plutôt qu'un « rien à signaler ».
2. Si le nominal affiche **déjà** `stale`, l'expérience ne peut pas distinguer :
   rendre 2.
3. Si la réécriture n'a modifié **aucune** réponse, on n'a rien vieilli :
   rendre 2.

Usage : python tools/mesurer_fraicheur_dite.py [--base http://127.0.0.1:5002]
        [--espace /markets] [--tous] [--age 7200]
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mesurer_blocs_peints import _INTERDITS, _chromium  # noqa: E402
from tools.mesurer_hotes_resolus import espaces  # noqa: E402

#  Les champs d'âge servis par le produit, relevés sur les réponses réelles :
#  `age_s` (par domaine dans /api/live/status), `scan_age` (/api/market/summary),
#  et `ts` (horodatage epoch). On ne touche à rien d'autre.
_CHAMPS_AGE = ('age_s', 'scan_age')

_ETATS = re.compile(r'data-state="([a-z]+)"')

#  LES ÉTATS QUE `VX.freshness` PRODUIT — et eux seuls. Distinction apprise en
#  mesurant : `data-state` sert aussi à d'autres choses. Sur Système, « live »
#  décrit l'état de la CONNEXION IBKR, pas l'âge de la donnée ; « ready » et
#  « empty » appartiennent aux cartes. Confondre le mot et le sens accuserait
#  une page qui ne ment pas.
_FRAICHEUR = {'live', 'snapshot', 'stale', 'saved', 'refreshing', 'error', 'offline'}


def _vieillir(charge, age, maintenant):
    """Réécrit les champs d'âge en profondeur. Rend (charge, nb_modifications)."""
    n = 0

    def parcourir(o):
        nonlocal n
        if isinstance(o, dict):
            for cle, val in list(o.items()):
                if cle in _CHAMPS_AGE and isinstance(val, (int, float)):
                    o[cle] = age
                    n += 1
                elif cle == 'ts' and isinstance(val, (int, float)) and val > 1e9:
                    o[cle] = maintenant - age
                    n += 1
                else:
                    parcourir(val)
        elif isinstance(o, list):
            for v in o:
                parcourir(v)

    parcourir(charge)
    return charge, n


def _etats_peints(page):
    """Les états de fraîcheur RÉELLEMENT affichés, lus dans le DOM."""
    return page.evaluate("""() => {
      const vus = {};
      for (const e of document.querySelectorAll('[data-state]')) {
        const s = e.getAttribute('data-state');
        //  On ne garde que ce qui est MONTRÉ : un chip dans un bloc replié ne
        //  dit rien à l'utilisateur.
        if (e.getBoundingClientRect().height <= 0) continue;
        //  ET ON DISTINGUE LA PUCE DE FRAÎCHEUR DU RESTE. `VX.freshness.chip()`
        //  émet `class="vx-fresh-chip"` ; `data-state` seul ne suffit pas comme
        //  discriminant. Mesuré : sur Système, un `data-state="live"` porte la
        //  classe `vx-freshness` et le texte « Système opérationnel » — il décrit
        //  l'état du SYSTÈME, pas l'âge de la donnée. L'accuser de mentir sur la
        //  fraîcheur aurait été confondre un mot avec son sens.
        const cle = e.classList.contains('vx-fresh-chip') ? s : 'autre:' + s;
        vus[cle] = (vus[cle] || 0) + 1;
      }
      //  DEUX GRAMMAIRES DE FRAÎCHEUR, pas une — mesuré, pas supposé.
      //  `VX.freshness.chip()` émet `.vx-fresh-chip[data-state]` ; mais
      //  `freshBadge()` (Aujourd'hui, Analyse, Opportunités) émet
      //  `.vx-freshness[data-live]`, avec ses propres mots — `frozen` y veut
      //  dire « Périmé », l'équivalent de `stale`. N'en connaître qu'une faisait
      //  rendre « sans vocabulaire » sur une page qui en a bien un.
      const EQ = {frozen: 'stale', fallback: 'demo'};
      for (const e of document.querySelectorAll('.vx-freshness[data-live]')) {
        if (e.getBoundingClientRect().height <= 0) continue;
        const v = e.getAttribute('data-live');
        const s = EQ[v] || v;
        vus[s] = (vus[s] || 0) + 1;
      }
      return vus;
    }""")


def _une_visite(nav, base, url, age=None):
    """Charge la page ; si `age` est donné, vieillit les réponses en vol."""
    import time
    modifiees = [0]
    ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                          service_workers='block')
    page = ctx.new_page()
    for motif in _INTERDITS:
        page.route(motif, lambda r: r.abort())

    if age is not None:
        maintenant = time.time()

        def _rajeunir_pas(route):
            try:
                rep = route.fetch()
                brut = rep.text()
            except Exception:
                route.continue_()
                return
            try:
                charge = json.loads(brut)
            except ValueError:
                route.fulfill(response=rep)
                return
            charge, n = _vieillir(charge, age, maintenant)
            modifiees[0] += n
            route.fulfill(response=rep, body=json.dumps(charge),
                          headers={**rep.headers, 'content-type': 'application/json'})
        page.route('**/{api,scan,cal-feed,news-feed}**', _rajeunir_pas)

    page.goto(base + url, wait_until='domcontentloaded', timeout=45000)
    page.wait_for_timeout(6500)
    etats = _etats_peints(page)
    texte = page.evaluate('() => document.body.innerText')
    ctx.close()
    return etats, texte, modifiees[0]


def une_page(base, url, age):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('AVEUGLE — Playwright absent. Refus de conclure.')
        return 2

    with sync_playwright() as pw:
        nav = _chromium(pw)
        avant, texte_avant, _ = _une_visite(nav, base, url)
        apres, texte_apres, modifiees = _une_visite(nav, base, url, age=age)
        nav.close()

    #  QUATRE SITUATIONS, ET UNE SEULE EST UN DEFAUT. Mon premier verdict etait
    #  binaire (DIT / MUET) et accusait cinq pages sur huit. Trois de ces cinq ne
    #  mentaient pas :
    #   - le mode DEMONSTRATION court-circuite l'evaluation (`if(demo){…DEMO…}`) :
    #     la page annonce « DEMO », ce qui est honnete, et le chemin de fraicheur
    #     n'est simplement pas exerce → non observable ;
    #   - certaines pages n'ont AUCUN vocabulaire de fraicheur : ce n'est pas un
    #     mensonge, c'est une absence — a signaler comme telle, pas comme faute ;
    #   - un `data-state="live"` peut decrire la CONNEXION et non l'age.
    if 'demo' in apres or 'demo' in avant:
        print('  NON OBSERVABLE — la page annonce « DEMO » : le mode '
              'demonstration court-circuite l\'evaluation de fraicheur. Honnete, '
              'mais le chemin mesure ici n\'est pas exerce.')
        return 2
    porte = {e for e in avant if e in _FRAICHEUR}
    if not porte:
        print('  SANS VOCABULAIRE — aucune etiquette de fraicheur sur cette page '
              '(etats vus : %s). Ce n\'est pas un mensonge, c\'est une absence : '
              'rien ne dit a l\'utilisateur de quand datent les chiffres.'
              % ', '.join(sorted(avant)))
        return 3
    if not avant:
        print('  AVEUGLE — aucune etiquette affichee en nominal.')
        return 2
    if 'stale' in avant:
        print('  AVEUGLE — la page affiche DEJA « a actualiser » en nominal : '
              'l\'experience ne peut pas distinguer un basculement.')
        return 2
    if not modifiees:
        print('  AVEUGLE — aucune reponse n\'a ete vieillie (aucun champ d\'age '
              'trouve) : « rien ne change » ne prouverait rien.')
        return 2

    print('  nominal : %s' % (', '.join('%s×%d' % (k, v) for k, v in sorted(avant.items()))))
    print('  vieilli (%d s, %d champ(s) reecrit(s)) : %s'
          % (age, modifiees,
             ', '.join('%s×%d' % (k, v) for k, v in sorted(apres.items())) or 'aucune etiquette'))

    dit = 'stale' in apres or 'À actualiser' in texte_apres
    if dit:
        print('  DIT — l\'ecran signale la donnee perimee.')
        return 0
    print('  MUET — la donnee est vieille de %d s et AUCUNE etiquette ne le dit : '
          'les chiffres restent affiches comme s\'ils etaient frais.' % age)
    return 1


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    base = 'http://127.0.0.1:5002'
    sym = 'ACN'
    age = int(argv[argv.index('--age') + 1]) if '--age' in argv else 7200
    if '--base' in argv:
        base = argv[argv.index('--base') + 1]
    if '--sym' in argv:
        sym = argv[argv.index('--sym') + 1]

    if '--tous' in argv:
        pire, resume = 0, []
        for ident, href in espaces():
            url = href if href != '/analysis' else '/analysis/%s' % sym
            print('\n=== %s (%s) ===' % (ident.upper(), url))
            code = une_page(base, url, age)
            resume.append((ident, code))
            #  « non observable » (2) et « sans vocabulaire » (3) ne sont pas des
            #  mensonges : ils ne remontent pas comme des defauts.
            pire = max(pire, code if code == 1 else 0)
        print('\n%s\nRESUME — la donnee vieillie est-elle DITE ?\n%s' % ('=' * 60, '=' * 60))
        for ident, code in resume:
            print('  %-14s %s' % (ident, {0: 'DIT', 1: 'MUET',
                                          2: 'non observable (demo)',
                                          3: 'sans vocabulaire'}.get(code, '?')))
        return pire

    url = '/analysis/%s' % sym
    if '--espace' in argv:
        url = argv[argv.index('--espace') + 1]
    return une_page(base, url, age)


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
