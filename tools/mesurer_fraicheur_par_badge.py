"""tools/mesurer_fraicheur_par_badge.py — COMBIEN D'ÉTIQUETTES SONT DES CONSTANTES ?

Le lot 62 a trouvé une étiquette de fraîcheur **constante** sur Aujourd'hui et l'a
corrigée. Puis il a rendu « sans vocabulaire » sur Options. **Ce verdict était
faux** : Options porte bien une étiquette, dans une **troisième** grammaire que
mon instrument ne connaissait pas — et cette étiquette est exactement la même
constante que celle que je venais de corriger.

Deux fautes de méthode à réparer, pas une :

1. **Mon inventaire des grammaires était incomplet.** Il y en a *trois*, pas deux.
2. **Ma granularité était la page.** L'outil du lot 62 rendait « DIT » dès qu'**une**
   étiquette réagissait. Une page qui porte un badge honnête *et* un badge
   constant était donc déclarée saine. *Un verdict par page masque un défaut par
   badge.*

## Les trois grammaires, mesurées

| sélecteur | émis par | où |
| --- | --- | --- |
| `.vx-fresh-chip[data-state]` | `VX.freshness.chip()` | Analyse, Marchés, Opportunités, Portefeuille, Système |
| `.vx-freshness[data-live]` | `freshBadge()` / `VXCharts.freshnessBadge()` | Aujourd'hui, Analyse, Opportunités |
| `.vx-freshness[data-state]` | à la main | Options, Portefeuille, Système |

## L'expérience : la même qu'au lot 62, mais par badge

Chaque espace est chargé **deux fois** — nominal, puis avec les réponses
**vieillies en vol** (`age_s`, `scan_age`, `ts` réécrits à 2 h). On identifie
chaque étiquette par son **chemin DOM** (stable entre deux chargements de la même
page) et on compare son état et son texte.

- l'étiquette change → **RÉAGIT** ;
- l'étiquette ne bouge pas alors que *tout* a vieilli de deux heures →
  **CONSTANTE**.

## Anti-vacuité : un témoin POSITIF pris dans le produit

Le témoin n'est pas fabriqué : c'est l'étiquette d'Aujourd'hui, dont le lot 62 a
**mesuré** qu'elle réagit (`scan_age` 10 → Live, 600 → Différé, 7 200 → Périmé).
Si l'instrument ne la voit pas bouger, il est aveugle et rend 2 — « aucune
constante trouvée » ne voudrait alors rien dire.

Un témoin pris dans le produit vaut mieux qu'un témoin fabriqué : il prouve la
chaîne entière — interception, vieillissement, identification, comparaison — dans
les conditions exactes de la mesure.

Usage : python tools/mesurer_fraicheur_par_badge.py [--base http://127.0.0.1:5002]
        [--espace /options] [--age 7200] [--sym ACN]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mesurer_blocs_peints import _INTERDITS, _chromium  # noqa: E402
from tools.mesurer_fraicheur_dite import _vieillir  # noqa: E402
from tools.mesurer_hotes_resolus import espaces  # noqa: E402

#  L'ESPACE QUI SERT DE TÉMOIN, et l'ancre de son étiquette. Mesuré au lot 62 :
#  cette étiquette PASSE de « Différé » à « Périmé » quand la donnée vieillit.
_TEMOIN_URL = '/'
_TEMOIN_ANCRE = 'vx-hero-fresh'

#  LES TROIS GRAMMAIRES DE FRAÎCHEUR — relevées dans le code servi, pas
#  supposées. La troisième (`.vx-freshness[data-state]`) est celle que le lot 62
#  ignorait, ce qui lui a fait rendre « sans vocabulaire » sur une page qui porte
#  bel et bien une etiquette.
_RECOLTE = """() => {
  const out = [];
  const chemin = (e) => {
    const p = [];
    for (let n = e; n && n.nodeType === 1 && p.length < 12; n = n.parentElement) {
      if (n.id) { p.unshift('#' + n.id); break; }
      const f = n.parentElement
        ? Array.prototype.indexOf.call(n.parentElement.children, n) : 0;
      p.unshift(n.tagName.toLowerCase() + ':' + f);
    }
    return p.join('>');
  };
  const prendre = (e, grammaire, etat) => {
    //  ON NE GARDE QUE CE QUI EST MONTRÉ. Une étiquette dans un bloc replié ne
    //  dit rien à l'utilisateur — et n'a donc rien à démentir.
    if (e.getBoundingClientRect().height <= 0) return;
    out.push({chemin: chemin(e), grammaire: grammaire, etat: etat,
              texte: (e.innerText || '').trim().slice(0, 40)});
  };
  for (const e of document.querySelectorAll('.vx-fresh-chip[data-state]'))
    prendre(e, 'chip', e.getAttribute('data-state'));
  for (const e of document.querySelectorAll('.vx-freshness[data-live]'))
    prendre(e, 'badge-live', e.getAttribute('data-live'));
  for (const e of document.querySelectorAll('.vx-freshness[data-state]'))
    prendre(e, 'badge-state', e.getAttribute('data-state'));
  return out;
}"""


def _hors_demo(charge):
    """Force la branche NON-DÉMO. Rend le nombre de drapeaux abaissés.

    LE TÉMOIN M'A REPRIS DÈS LE PREMIER PASSAGE, et il avait raison : en mode
    démonstration, les pages court-circuitent l'évaluation de fraîcheur
    (`if(demo){…DÉMO…}`) — c'est honnête, mais le chemin que je veux mesurer
    n'est alors **jamais exercé**, et toute étiquette paraît constante. C'est
    exactement la leçon §3.1 du lot 62, et je venais de la re-commettre.

    L'instrument abaisse donc `demo` dans les réponses, **sur les DEUX visites**
    — sans quoi le nominal dirait « Démo » et le vieilli autre chose, et tout
    paraîtrait « réagir » pour la mauvaise raison. C'est une intervention sur la
    mesure, pas sur le produit : elle est déclarée ici et dans le rapport.
    """
    n = 0

    def parcourir(o):
        nonlocal n
        if isinstance(o, dict):
            for cle, val in list(o.items()):
                if cle == 'demo' and val is True:
                    o[cle] = False
                    n += 1
                else:
                    parcourir(val)
        elif isinstance(o, list):
            for v in o:
                parcourir(v)

    parcourir(charge)
    return n


def _une_visite(nav, base, url, age=None):
    """Charge la page ; si `age` est donné, vieillit les réponses en vol.

    Les deux visites passent par la même interception : seule la présence de
    `age` les distingue."""
    import time
    modifiees = [0]
    ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                          service_workers='block')
    page = ctx.new_page()
    for motif in _INTERDITS:
        page.route(motif, lambda r: r.abort())

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
        _hors_demo(charge)
        if age is not None:
            charge, n = _vieillir(charge, age, maintenant)
            modifiees[0] += n
        route.fulfill(response=rep, body=json.dumps(charge),
                      headers={**rep.headers, 'content-type': 'application/json'})
    page.route('**/{api,scan,cal-feed,news-feed}**', _rajeunir_pas)

    page.goto(base + url, wait_until='domcontentloaded', timeout=45000)
    page.wait_for_timeout(6500)
    badges = page.evaluate(_RECOLTE)
    ctx.close()
    return badges, modifiees[0]


def _comparer(avant, apres):
    """Apparie les étiquettes par leur chemin DOM et rend (reagissent, constantes)."""
    a = {b['chemin']: b for b in avant}
    p = {b['chemin']: b for b in apres}
    reagissent, constantes = [], []
    for chemin, badge in a.items():
        autre = p.get(chemin)
        if autre is None:
            #  DISPARUE : ce n'est ni une réaction ni une constante — la page a
            #  changé de forme sous vieillissement. On ne conclut rien dessus.
            continue
        if (autre['etat'], autre['texte']) != (badge['etat'], badge['texte']):
            reagissent.append((chemin, badge, autre))
        else:
            constantes.append((chemin, badge))
    return reagissent, constantes


def une_page(nav, base, url, age, bavard=True):
    avant, _ = _une_visite(nav, base, url)
    apres, modifiees = _une_visite(nav, base, url, age=age)
    reagissent, constantes = _comparer(avant, apres)

    if bavard:
        if not avant:
            print('  aucune etiquette de fraicheur affichee sur cette page.')
        if not modifiees:
            print('  AVEUGLE — aucune reponse vieillie : « rien ne change » ne '
                  'prouverait rien ici.')
            return None, None
        for chemin, b, a2 in reagissent:
            print('  REAGIT     [%s] %s : %s « %s » -> %s « %s »'
                  % (b['grammaire'], chemin[-46:], b['etat'], b['texte'],
                     a2['etat'], a2['texte']))
        for chemin, b in constantes:
            print('  CONSTANTE  [%s] %s : reste %s « %s » alors que TOUT a '
                  'vieilli de %d s' % (b['grammaire'], chemin[-46:], b['etat'],
                                       b['texte'], age))
    return reagissent, constantes


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    base = 'http://127.0.0.1:5002'
    sym = 'ACN'
    age = int(argv[argv.index('--age') + 1]) if '--age' in argv else 7200
    if '--base' in argv:
        base = argv[argv.index('--base') + 1]
    if '--sym' in argv:
        sym = argv[argv.index('--sym') + 1]

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('AVEUGLE — Playwright absent. Refus de conclure.')
        return 2

    liste = [(i, h if h != '/analysis' else '/analysis/%s' % sym)
             for i, h in espaces()]
    if '--espace' in argv:
        liste = [('espace', argv[argv.index('--espace') + 1])]

    with sync_playwright() as pw:
        nav = _chromium(pw)

        #  LE TÉMOIN D'ABORD — et sans lui, rien de ce qui suit ne vaut. On exige
        #  que l'étiquette d'Aujourd'hui, MESURÉE réactive au lot 62, soit vue
        #  bouger par cet instrument-ci.
        print('=== TEMOIN (%s) ===' % _TEMOIN_URL)
        reagissent, _ = une_page(nav, base, _TEMOIN_URL, age)
        if reagissent is None:
            nav.close()
            return 2
        if not any(_TEMOIN_ANCRE in c for c, _, _ in reagissent):
            print('AVEUGLE — le temoin n\'a PAS bouge. L\'etiquette d\'Aujourd\'hui '
                  'est pourtant mesuree reactive (lot 62). L\'instrument ne voit '
                  'donc pas ce qu\'il pretend voir : « aucune constante » ne '
                  'voudrait rien dire.')
            nav.close()
            return 2
        print('  temoin OK — l\'instrument voit une etiquette reagir.')

        total = []
        for ident, url in liste:
            print('\n=== %s (%s) ===' % (ident.upper(), url))
            reagissent, constantes = une_page(nav, base, url, age)
            if constantes:
                total.extend((ident, c[1]) for c in constantes)
        nav.close()

    print('\n%s\nRESUME — etiquettes de fraicheur CONSTANTES\n%s' % ('=' * 62, '=' * 62))
    if not total:
        print('  aucune. Toutes les etiquettes affichees reagissent a l\'age.')
        return 0
    for ident, b in total:
        print('  %-14s [%s] %s « %s »' % (ident, b['grammaire'], b['etat'], b['texte']))
    print('\n%d etiquette(s) occupent la place d\'un indicateur de fraicheur sans '
          'porter la moindre information d\'age.' % len(total))
    return 1


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
