"""tools/mesurer_actifs_charges.py — QUELS FICHIERS STATIQUES SONT VRAIMENT CHARGÉS ?

`PAGES.md`, passe finale : « suppression CSS/JS legacy devenu inutile ». Et la
gouvernance est explicite : *aucun fichier supprimé sans preuve d'inutilisation*.
Cet outil produit cette preuve — ou refuse de la produire.

## La preuve, et ce qu'elle exige

Un fichier n'est « inutile » que si **aucune vue** ne le demande. Une mesure qui
ne visiterait que les huit écrans d'accueil déclarerait morts des fichiers qui
ne se chargent que sur `/options?view=gex` ou `/analysis/<sym>` — et une
suppression fondée sur elle casserait le produit. La liste des vues n'est donc
pas écrite ici : elle est **dérivée des modules de page** (même source que
`mesurer_degradation.py`), et les fiches par symbole sont ajoutées.

Le navigateur est indispensable : un `<script src>` peut être injecté par le
shell, un `@import` peut tirer une feuille depuis une autre, et le service
worker peut resservir un fichier qu'aucune balise ne nomme. Seule la liste des
requêtes réellement émises fait foi. Le service worker est donc **bloqué**
(`service_workers='block'`) : on veut ce que la page demande, pas ce qu'un cache
lui rend.

## Anti-vacuité

Si le relevé ne voit aucune requête `/static`, c'est la sonde qui est morte, pas
le produit : l'outil rend 2 plutôt qu'un inventaire de fichiers « inutiles ».

Usage : python tools/mesurer_actifs_charges.py [--base http://127.0.0.1:5002]
"""
import os
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE))

STATIQUES = RACINE / 'vertex' / 'static'


def _vues(module):
    """Les vues d'une page, LUES dans son module — jamais recopiées ici.

    Même règle que `mesurer_degradation.py` : une liste recopiée diverge, et
    une vue oubliée transforme un fichier vivant en fichier « mort ».
    Le nom de la table varie (`VIEWS` chez Système, `_VIEWS` ailleurs) : on
    accepte les deux, et une page sans table n'a qu'une vue."""
    src = (RACINE / 'vertex' / 'ui' / 'pages' / module).read_text(encoding='utf-8')
    for nom in ('_VIEWS', 'VIEWS'):
        m = (re.search(nom + r'\s*=\s*\((.*?)\n\)', src, re.S)
             or re.search(nom + r'\s*=\s*\((.*?)\)\s*\n\n', src, re.S))
        if m:
            vues = re.findall(r"\('([a-z0-9_-]+)'\s*,", m.group(1))
            if vues:
                return [''] + vues
    return ['']


def urls():
    pages = [('/', ['']),
             ('/markets', _vues('markets_page.py')),
             ('/opportunities', _vues('opportunities_page.py')),
             ('/analysis', _vues('analysis_page.py')),
             ('/portfolio', _vues('portfolio_page.py')),
             ('/options', _vues('options_intel_page.py')),
             ('/journal', _vues('performance_page.py')),
             ('/system', _vues('system_page.py')),
             #  LES PAGES QUI NE SONT PAS DANS LES HUIT ESPACES, et sans
             #  lesquelles le verdict serait faux. Premier relevé : trois
             #  fichiers « jamais demandés » — dont `js/pages/tracking.js`,
             #  qui n'est servi que par `/tracking`, une route que je ne
             #  visitais pas. Déclarer mort un fichier parce qu'on n'a pas
             #  ouvert sa page, c'est fabriquer la preuve qu'on cherchait.
             ('/intelligence', _vues('intelligence_page.py')),
             ('/tracking', ['']),
             ('/system/design-system', ['']),
             ('/widget-lab', [''])]
    out = []
    for route, vues in pages:
        for v in dict.fromkeys(vues):
            out.append(route + (('?view=' + v) if v else ''))
    return out


def fiches(base, combien=2):
    """Des fiches par symbole — `/analysis/<sym>` charge des scripts que
    l'index ne charge pas. Symboles LUS dans le scan servi."""
    import json
    import urllib.request
    try:
        with urllib.request.urlopen(base + '/scan', timeout=30) as r:
            detail = (json.loads(r.read().decode('utf-8')) or {}).get('detail') or {}
    except Exception:
        return []
    return ['/analysis/%s' % s for s in sorted(detail)[:combien]]


def _chromium():
    import glob
    for c in sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome')):
        if os.path.exists(c):
            return c
    return None


def inventaire():
    return sorted(str(p.relative_to(STATIQUES)).replace(os.sep, '/')
                  for p in STATIQUES.rglob('*')
                  if p.is_file() and p.suffix in ('.js', '.css'))


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    base = argv[argv.index('--base') + 1] if '--base' in argv else 'http://127.0.0.1:5002'

    from playwright.sync_api import sync_playwright   # import PARESSEUX (lot 35)

    tous = inventaire()
    demandes, par_url = set(), {}
    visitees = urls() + fiches(base)

    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=_chromium(), args=['--no-sandbox'])
        ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                              service_workers='block')
        page = ctx.new_page()

        def _vu(req):
            #  MÊME BASE DES DEUX CÔTÉS, et ce n'est pas un détail de style :
            #  premier jet, l'inventaire était relatif à `vertex/static`
            #  (`vertex/css/tokens.css`) tandis que la requête était coupée à
            #  `/static/vertex/` (`css/tokens.css`). Les deux ensembles ne se
            #  croisaient jamais — l'outil annonçait 54 fichiers « jamais
            #  demandés » avec aplomb. On coupe donc à `/static/`, le seul
            #  point commun aux deux.
            u = req.url
            if '/static/' in u:
                chemin = u.split('/static/', 1)[1].split('?')[0]
                demandes.add(chemin)
                par_url.setdefault(chemin, set()).add(courante[0])

        courante = ['']
        page.on('request', _vu)
        for u in visitees:
            courante[0] = u
            try:
                page.goto(base + u, wait_until='domcontentloaded', timeout=45000)
                page.wait_for_timeout(2500)
            except Exception as e:
                print('  … %-34s NON VISITEE (%s)' % (u, type(e).__name__))
        ctx.close()
        nav.close()

    print('vues visitees : %d · fichiers statiques : %d' % (len(visitees), len(tous)))
    if not demandes:
        print('\nAVEUGLE — aucune requete /static observee : la sonde est morte, '
              'pas le produit. Refus de declarer quoi que ce soit inutile.')
        return 2

    #  LE TÉMOIN QUI MANQUAIT, et qui m'a coûté un verdict faux. Voir des
    #  requêtes ne suffit pas : encore faut-il qu'elles se RACCORDENT à
    #  l'inventaire. Une intersection vide ne veut pas dire « 54 fichiers
    #  morts », elle veut dire que les deux listes ne parlent pas de la même
    #  chose. L'outil refuse alors de conclure.
    croisement = set(tous) & demandes
    if not croisement:
        print('\nAVEUGLE — aucune requete ne correspond a un fichier de '
              'l\'inventaire (%d requetes, %d fichiers). Ce n\'est pas un '
              'produit sans actifs : c\'est un desaccord de chemins entre la '
              'sonde et le disque. Refus de declarer quoi que ce soit inutile.'
              % (len(demandes), len(tous)))
        return 2

    jamais = [f for f in tous if f not in demandes]
    poids = 0
    print('\nCHARGES AU MOINS UNE FOIS : %d' % (len(tous) - len(jamais)))
    print('\nJAMAIS DEMANDES PAR AUCUNE VUE : %d' % len(jamais))
    for f in jamais:
        o = (STATIQUES / f).stat().st_size
        poids += o
        print('  %8d o  %s' % (o, f))
    print('\npoids jamais demande : %d o (%.1f Ko)' % (poids, poids / 1024))
    inconnus = sorted(demandes - set(tous))
    if inconnus:
        print('\nDEMANDES MAIS ABSENTS DU DISQUE : %d' % len(inconnus))
        for f in inconnus:
            print('  %s' % f)
    return 0


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
