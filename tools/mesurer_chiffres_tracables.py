"""tools/mesurer_chiffres_tracables.py — CHAQUE CHIFFRE PEINT VIENT-IL D'UNE SOURCE ?

Réserve SIGNAL-OS-60 §3 et §5.3, de ma main :

> L'outil détecte les hôtes qui **n'aboutissent pas**. Il ne sait pas reconnaître
> un hôte qui aboutit avec une valeur **inventée** ou **périmée**. […] C'est de
> loin le plus utile qui manque encore.

C'est le seul défaut qui, dans un terminal d'analyse, peut coûter de l'argent
plutôt que de la confiance : un chiffre plausible, affiché sans source.

## Le principe

1. On capture **tout ce que la page reçoit** — le corps de chaque réponse d'API.
2. On extrait **tout ce que la page affiche** — les nombres de `innerText`.
3. Pour chaque nombre peint, on demande : *ce nombre est-il dans ce qui est
   arrivé ?* Exactement, ou à l'arrondi près.

Un nombre peint absent de toute réponse est **inexpliqué**. Cela ne prouve pas
qu'il est inventé — il peut être dérivé (une somme, un pourcentage, un écart) —
mais tout chiffre inventé est nécessairement inexpliqué. L'outil réduit donc
l'espace à fouiller, il ne rend pas un verdict moral.

## Pourquoi la mesure vaut surtout SOUS PANNE

Nominal, presque tout s'explique et le bruit domine. Sous coupure d'une famille,
la question devient tranchante : **la page continue-t-elle d'afficher des
chiffres dont la source vient de mourir ?** C'est là qu'un fond de cache
présenté comme frais se voit.

## Ce que l'outil NE dit PAS

- Il ne distingue pas « dérivé » de « inventé ». Un écart, une somme, un
  pourcentage sont légitimement absents des réponses.
- Il ne juge pas la **fraîcheur** : un nombre présent dans une réponse périmée
  lui paraît tracé.
- Les nombres de **mise en page** (tailles, viewBox SVG) sont exclus par
  construction — on ne lit que `innerText`, jamais les attributs.

Dire cela n'affaiblit pas l'outil : cela empêche de lire son silence comme une
garantie.

## Anti-vacuité

Trois témoins, et l'outil rend 2 si l'un manque :

1. il doit **capturer au moins une réponse** — sans corpus, tout serait
   « inexpliqué » et le compte serait absurde ;
2. il doit **expliquer au moins un nombre** — si rien ne s'explique, c'est son
   appariement qui est cassé, pas le produit ;
3. **`--temoin` fabrique un chiffre sans source** et exige que l'outil le
   dénonce. Un détecteur qui ne trouve rien ne prouve rien tant qu'on ne l'a pas
   vu se déclencher : « zéro inexpliqué » et « je ne sais pas voir » rendent le
   même chiffre.

Usage : python tools/mesurer_chiffres_tracables.py [--base http://127.0.0.1:5002]
        [--espace /markets] [--couper-une market] [--tous] [--temoin]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mesurer_blocs_peints import _INTERDITS, _chromium  # noqa: E402
from tools.mesurer_hotes_resolus import espaces  # noqa: E402

#  Un nombre peint : chiffres, séparateurs français ou anglais, signe optionnel.
#  DEUX PIEGES MESURES AU PREMIER PASSAGE, tous deux fabriquant de faux
#  « inexpliques » a partir de mon propre decoupage :
#   - l'espace comme separateur de milliers ne vaut QUE s'il groupe
#     exactement TROIS chiffres. Sans cette regle, « 2026 12 » (une date)
#     devenait un seul nombre de mon invention, absent de toute reponse
#     par construction ;
#   - un nombre suivi de « .chiffre » appartient a une adresse ou a une
#     version (127.0.0.1). Le couper en morceaux cree des valeurs que
#     personne n'a jamais affichees comme nombres.
_ESP = '[   ]'
_NOMBRE = re.compile(r'-?\d{1,3}(?:' + _ESP + r'\d{3})+(?:[.,]\d+)?'
                     r'|-?\d+(?:[.,]\d+)?')


def _dans_une_suite_pointee(texte, fin):
    """Le nombre est-il un morceau de `127.0.0.1` ou de `1.2.3` ?"""
    return (fin + 1 < len(texte) and texte[fin] == '.'
            and texte[fin + 1].isdigit())

#  Nombres qu'on n'interroge pas, et chacun pour une raison mesurée :
#  - 0 et 1 apparaissent partout et n'apprennent rien ;
#  - les entiers ≤ 31 sont massivement des dates, des rangs, des compteurs
#    d'éléments affichés — la page les calcule elle-même, légitimement.
def _interessant(v, brut):
    if v in (0.0, 1.0):
        return False
    if float(v).is_integer() and abs(v) <= 31:
        return False
    return True


def _nombres_peints(texte):
    """Les nombres que l'écran montre, normalisés en flottants."""
    vus = {}
    for m in _NOMBRE.finditer(texte):
        if _dans_une_suite_pointee(texte, m.end()):
            continue
        brut = m.group(0).strip()
        net = (brut.replace(' ', '').replace(' ', '')
               .replace(' ', '').replace(',', '.'))
        if net.count('.') > 1 or net in ('-', ''):
            continue
        try:
            v = float(net)
        except ValueError:
            continue
        if _interessant(v, brut):
            vus.setdefault(round(v, 6), brut)
    return vus


def _nombres_recus(corpus):
    """Les nombres présents dans ce que la page a REÇU."""
    vus = set()
    for corps in corpus:
        for m in _NOMBRE.finditer(corps):
            net = m.group(0).strip().replace(',', '.')
            if net.count('.') > 1 or net in ('-', ''):
                continue
            try:
                vus.add(round(float(net), 6))
            except ValueError:
                continue
    return vus


def _explique(v, recus):
    """Le nombre peint se retrouve-t-il dans ce qui est arrivé ?

    À L'ARRONDI PRÈS, et ce n'est pas une complaisance : la page affiche
    `198,00` pour un `198.0031` reçu. Exiger l'égalité stricte rendrait
    « inexpliqué » la quasi-totalité des prix, et l'outil serait inutilisable.
    On accepte donc qu'un reçu s'arrondisse au peint, à la précision du peint.
    """
    if v in recus:
        return True
    for dec in (0, 1, 2, 3):
        cible = round(v, dec)
        for r in recus:
            if round(r, dec) == cible and abs(r - v) < 10 ** (-dec) * 5:
                return True
    #  Pourcentage : la page montre 12,5 pour un 0.125 reçu (ou l'inverse).
    for r in recus:
        if r and (abs(r * 100 - v) < 0.05 or abs(r / 100 - v) < 0.0005):
            return True
    return False


def une_page(base, url, famille=None, temoin=False):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('AVEUGLE — Playwright absent. Refus de conclure.')
        return 2

    corpus, coupees = [], []
    with sync_playwright() as pw:
        nav = _chromium(pw)
        ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                              service_workers='block')
        page = ctx.new_page()
        for motif in _INTERDITS:
            page.route(motif, lambda r: r.abort())
        if famille:
            def _partielle(route):
                if famille in route.request.url.split('?')[0]:
                    coupees.append(route.request.url)
                    route.fulfill(status=500, content_type='application/json',
                                  body='{"error":"panne partielle simulee"}')
                else:
                    route.continue_()
            page.route('**/{api,scan,cal-feed,news-feed}**', _partielle)

        def _garder(rep):
            u = rep.url.split('?')[0]
            if '/api/' in u or '/scan' in u or '-feed' in u:
                try:
                    corpus.append(rep.text())
                except Exception:
                    pass
        page.on('response', _garder)
        page.goto(base + url, wait_until='domcontentloaded', timeout=45000)
        page.wait_for_timeout(6000)
        if temoin:
            #  UN CHIFFRE FABRIQUE, qui n'est dans aucune reponse. Si l'outil ne
            #  le denonce pas, son silence sur le produit ne vaut rien.
            page.evaluate("() => {const s=document.createElement('div');"
                          "s.textContent='987654,321';document.body.appendChild(s);}")
        #  Ouvrir les replis : un chiffre cache est un chiffre non mesure.
        for _ in range(3):
            fermees = [d for d in page.query_selector_all('details')
                       if not d.get_attribute('open')]
            if not fermees:
                break
            for d in fermees:
                som = d.query_selector('summary')
                if som:
                    try:
                        som.click(timeout=2000)
                    except Exception:
                        pass
            page.wait_for_timeout(300)
        page.wait_for_timeout(1500)
        texte = page.evaluate('() => document.body.innerText')
        nav.close()

    if famille and not coupees:
        print('HORS PORTEE — la famille « %s » n\'est appelee par aucune requete '
              'de cette page.' % famille)
        return 3
    if not corpus:
        print('AVEUGLE — aucune reponse d\'API capturee : tout paraitrait '
              'inexplique, et ce compte ne voudrait rien dire.')
        return 2

    peints = _nombres_peints(texte)
    recus = _nombres_recus(corpus)
    expliques = {v: b for v, b in peints.items() if _explique(v, recus)}
    inexpliques = {v: b for v, b in peints.items() if v not in expliques}

    if not expliques:
        print('AVEUGLE — AUCUN des %d nombres peints ne se retrouve dans les %d '
              'reponses capturees. C\'est l\'appariement qui est casse, pas le '
              'produit.' % (len(peints), len(corpus)))
        return 2

    if temoin:
        vu = 987654.321 in inexpliques
        print('  TEMOIN : chiffre fabrique %s'
              % ('DENONCE — le detecteur mord' if vu
                 else 'PASSE INAPERCU — le detecteur est aveugle'))
        if not vu:
            return 2
    print('  reponses capturees : %d · nombres peints : %d'
          % (len(corpus), len(peints)))
    print('  traces : %d · inexpliques : %d'
          % (len(expliques), len(inexpliques)))
    if famille:
        print('  panne partielle : %d requete(s) coupee(s)' % len(coupees))
    if inexpliques:
        #  AVEC LEUR CONTEXTE. Un nombre inexplique sans sa phrase n'est pas
        #  exploitable : « 58 » ne dit rien, « Fraicheur 58 s » dit tout.
        montres = sorted(inexpliques.items(), key=lambda kv: -abs(kv[0]))[:12]
        print('  inexpliques :')
        for _, brut in montres:
            i = texte.find(brut)
            autour = texte[max(0, i - 45):i + len(brut) + 25].replace('\n', ' / ')
            print('    %-12s … %s …' % (brut, autour.strip()))
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    base = 'http://127.0.0.1:5002'
    sym = 'ACN'
    famille = argv[argv.index('--couper-une') + 1] if '--couper-une' in argv else None
    temoin = '--temoin' in argv
    if '--base' in argv:
        base = argv[argv.index('--base') + 1]
    if '--sym' in argv:
        sym = argv[argv.index('--sym') + 1]

    if '--tous' in argv:
        pire = 0
        for ident, href in espaces():
            url = href if href != '/analysis' else '/analysis/%s' % sym
            print('\n=== %s (%s)%s ===' % (ident.upper(), url,
                                           '  [PANNE %s]' % famille if famille else ''))
            code = une_page(base, url, famille, temoin)
            pire = max(pire, 0 if code == 3 else code)
        return pire

    url = '/analysis/%s' % sym
    if '--espace' in argv:
        url = argv[argv.index('--espace') + 1]
    return une_page(base, url, famille, temoin)


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
