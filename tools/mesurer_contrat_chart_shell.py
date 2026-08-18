"""tools/mesurer_contrat_chart_shell.py — LE CONTRAT DU CHART SHELL EST-IL TENU ?

Réserve SIGNAL-OS-63 §6.4, de ma main :

> `VXCharts.freshnessBadge()` n'est appelé avec une valeur par personne :
> `opts.freshness` n'est passé par aucun appelant de `VXCharts.card`. Le « badge
> de fraîcheur canonique » du Chart Shell est donc du **code mort**.

Je l'avais lu au `grep`. Ce n'est pas une mesure : un `grep` ne voit pas un objet
construit ailleurs, ni une clé passée depuis une variable. Cet outil compare les
deux côtés du contrat, et il y a **deux façons** de le rompre — l'une bien plus
grave que l'autre.

## Les deux directions, et pourquoi la seconde est pire

| direction | ce que ça veut dire |
| --- | --- |
| **lue, jamais passée** | le composant sait faire une chose que personne ne lui demande — du **code mort**, et une promesse de contrat qui n'est pas tenue |
| **passée, jamais lue** | une page **croit dire quelque chose** et le composant l'ignore en silence |

La seconde est la vraie trouvaille possible : une page qui passe `source:` en
pensant nommer sa source, et rien ne s'affiche. C'est un défaut d'honnêteté, pas
d'hygiène — et il est **invisible à la lecture des deux fichiers séparément**.

## Anti-vacuité : deux témoins, un par direction

Un détecteur qui trouve zéro dans les deux sens et qui est simplement aveugle
rend exactement le même résultat qu'un produit parfait.

- `--temoin-lu` insère `opts.__temoin_jamais_passe` dans un builder : l'outil
  DOIT le dénoncer comme lu-jamais-passé ;
- `--temoin-passe` insère `__temoin_jamais_lu:1` sur un site d'appel : l'outil
  DOIT le dénoncer comme passé-jamais-lu.

Les deux témoins écrivent sur une **copie en mémoire**, jamais sur le disque.

## Ce que l'outil ne sait pas faire, et qu'il déclare

Il lit le **texte** des sources. Une clé passée via une variable
(`VXCharts.card(h, cfg)`) ou par diffusion (`{...base}`) lui échappe : ces sites
sont **comptés et annoncés** comme non analysables, jamais silencieusement
ignorés. Une limite tue transformerait son silence en garantie.

Usage : python tools/mesurer_contrat_chart_shell.py [--temoin-lu] [--temoin-passe]
"""
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CHARTS = os.path.join(RACINE, 'vertex', 'static', 'vertex', 'js', 'charts')

#  Clés utilitaires du shell que les appelants n'ont aucune raison de passer :
#  elles sont posées par le composant lui-même en cours de route.
_INTERNES = {'constructor', 'length', 'name'}

_DEF = re.compile(r'^  C\.([A-Za-z][A-Za-z0-9_]*) = function\s*\(([^)]*)\)', re.M)


def _sources_charts(mut_lu=False):
    """Rend {chemin: texte} pour les builders. `mut_lu` insère le témoin."""
    out = {}
    for nom in sorted(os.listdir(_CHARTS)):
        if not nom.endswith('.js'):
            continue
        p = os.path.join(_CHARTS, nom)
        with open(p, encoding='utf-8') as f:
            t = f.read()
        out[nom] = t
    if mut_lu:
        #  Le témoin est planté DANS le corps de `C.card`, le composant même dont
        #  la réserve parle — jamais sur le disque.
        cle = 'chart-core.js'
        out[cle] = out[cle].replace(
            '  C.card = function (host, opts) {',
            '  C.card = function (host, opts) {\n    var _t = opts.__temoin_jamais_passe;', 1)
    return out


def _cles_destructurees(bloc):
    """Les NOMS d'une déstructuration, sans les valeurs par défaut.

    MA PREMIÈRE VERSION ACCUSAIT `false` ET `true` D'ÊTRE DES OPTIONS. Elle
    coupait `horizontal = false, fill = true` sur les virgules ET les `=`, et
    ramassait donc les valeurs comme des clés. Un artefact de mon découpage
    présenté comme une trouvaille — exactement les `2026 12` et `127.0` du
    lot 61. On ne garde que ce qui précède un `=` ou une virgule."""
    cles, prof, courant, saute = set(), 0, '', False
    for c in bloc + ',':
        if c in '{([':
            prof += 1
        elif c in '})]':
            prof -= 1
        if prof == 0 and c in ',=':
            if not saute:
                m = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*$', courant)
                if m:
                    cles.add(m.group(1))
            saute = (c == '=')      # après un `=`, on saute la valeur par défaut
            courant = ''
            continue
        courant += c
    return cles


def _aides(t):
    """Les fonctions internes du fichier et les clés qu'elles lisent de LEUR
    paramètre. C'est le « un saut » qui manquait : `C.card` ne lit pas
    `opts.height`, il appelle `chartHeightStyle(opts)` qui appelle
    `chartHeight(opts)`. Sans suivre ce chemin, l'outil accusait la page de
    passer une clé que le composant lit parfaitement."""
    aides = {}
    for m in re.finditer(r'function ([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)\s*\{', t):
        nom, param = m.group(1), m.group(2)
        corps = t[m.end():m.end() + 2500]
        aides[nom] = (param, set(re.findall(r'\b%s\.([A-Za-z_][A-Za-z0-9_]*)' % param, corps)),
                      set(re.findall(r'([A-Za-z_][A-Za-z0-9_]*)\(\s*%s\s*\)' % param, corps)))
    #  DEUXIÈME SAUT : une aide qui en appelle une autre avec le même objet.
    for nom, (param, cles, suivantes) in list(aides.items()):
        for s in suivantes:
            if s in aides and s != nom:
                cles |= aides[s][1]
        aides[nom] = (param, cles, suivantes)
    return aides


def _lues(textes):
    """Les clés que chaque builder LIT, par découpage du fichier aux définitions."""
    lues = {}
    for nom, brut in textes.items():
        #  ON ANALYSE LE TEXTE MASQUE, COMMENTAIRES COMPRIS. Mon gardien a
        #  echoue sur un fichier parfaitement correct : le commentaire qui
        #  EXPLIQUE le retrait de `opts.freshness` contient les mots
        #  `opts.freshness`, que la recherche reprenait comme une lecture reelle.
        #  C'est le mecanisme du gardien creux — une sous-chaine qui existe
        #  ailleurs — cette fois dans l'instrument lui-meme.
        t = _masque(brut)
        aides = _aides(t)
        bornes = [(m.group(1), m.start(), m.group(2)) for m in _DEF.finditer(t)]
        for i, (builder, deb, params) in enumerate(bornes):
            fin = bornes[i + 1][1] if i + 1 < len(bornes) else len(t)
            corps = t[deb:fin]
            #  Le paramètre d'options peut s'appeler `opts`, `o` ou `d`, ou être
            #  déstructuré dans la signature. On suit ce que la signature déclare
            #  plutôt que de supposer un nom — supposer un nom est exactement la
            #  faute d'inventaire des lots 55 à 58.
            noms = re.findall(r'\b([a-z][A-Za-z0-9_]*)\b\s*(?:=|,|\)|$)', params)
            cands = [n for n in noms if n in ('opts', 'o', 'd', 'options')]
            cles = set()
            for n in cands:
                cles |= set(re.findall(r'\b%s\.([A-Za-z_][A-Za-z0-9_]*)' % n, corps))
                #  UN SAUT : `chartHeightStyle(opts)` lit `opts.height` pour lui.
                for aide in re.findall(r'([A-Za-z_][A-Za-z0-9_]*)\(\s*%s\s*\)' % n, corps):
                    if aide in aides:
                        cles |= aides[aide][1]
            for bloc in re.findall(r'\{([^}]*)\}\s*=\s*\{\}', params):
                cles |= _cles_destructurees(bloc)
            lues.setdefault(builder, set()).update(cles - _INTERNES)
    return lues


def _fichiers_appelants():
    """Tout ce qui peut appeler un builder — `charts/*.js` COMPRIS (cf. _passees)."""
    out = []
    for base, _, noms in os.walk(os.path.join(RACINE, 'vertex')):
        if '__pycache__' in base:
            continue
        for n in noms:
            if n.endswith(('.py', '.js')):
                out.append(os.path.join(base, n))
    out.append(os.path.join(RACINE, 'terminal.py'))
    return out


def _masque(t):
    """Copie de même longueur où le CONTENU des chaînes et des commentaires est
    remplacé par des espaces, la structure étant conservée.

    UN COMMENTAIRE M'A FAIT INVENTER UNE OPTION. Mon premier passage accusait
    `VXCharts.card` de recevoir une clé `coup` que personne ne lit. Elle n'existe
    pas : elle vient de « se lit d'un coup d'œil », un COMMENTAIRE dont les deux
    apostrophes ASCII désynchronisaient mon suivi des chaînes — après quoi
    n'importe quel mot suivi de `:` devenait une clé. Troisième fois de la série
    qu'un artefact de découpage se présente comme une trouvaille (lot 61 :
    `2026 12` et `127.0`). Masquer d'abord, analyser ensuite.

    ET LES GABARITS NE SONT PAS DES CHAÎNES ORDINAIRES. Ma première version
    masquait tout ce qui se trouve entre deux accents graves — or `${…}` y
    contient du **code réel**, et c'est là que `C.card` compose tout son en-tête.
    Une mutation l'a dit : remettre `opts.freshness` dans la condition de
    l'en-tête laissait le gardien vert, parce que la lecture était invisible.
    L'intérieur des interpolations est donc analysé comme du code."""
    out = list(t)
    n = len(t)
    i = 0
    #  Pile de contextes : 'code' | 'tpl' | ('interp', profondeur d'accolades)
    pile = ['code']

    def blanc(k):
        if t[k] != '\n':
            out[k] = ' '

    while i < n:
        c = t[i]
        haut = pile[-1]
        if haut == 'tpl':
            if c == '\\':
                blanc(i)
                if i + 1 < n:
                    blanc(i + 1)
                i += 2
                continue
            if c == '`':
                pile.pop()
                i += 1
                continue
            if c == '$' and i + 1 < n and t[i + 1] == '{':
                pile.append(['interp', 0])      # `${` reste visible : c'est du code
                i += 2
                continue
            blanc(i)
            i += 1
            continue
        #  contexte code (racine ou intérieur d'interpolation)
        if c == '/' and i + 1 < n and t[i + 1] == '*':
            j = t.find('*/', i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                blanc(k)
            i = j
            continue
        if c == '/' and i + 1 < n and t[i + 1] == '/':
            j = t.find('\n', i)
            j = n if j < 0 else j
            for k in range(i, j):
                blanc(k)
            i = j
            continue
        if c == '`':
            pile.append('tpl')
            i += 1
            continue
        if c in '"\'':
            j = i + 1
            while j < n:
                if t[j] == '\\':
                    j += 2
                    continue
                if t[j] == c or t[j] == '\n':
                    break
                j += 1
            for k in range(i + 1, min(j, n)):
                blanc(k)
            i = min(j, n) + 1
            continue
        if isinstance(haut, list):
            if c == '{':
                haut[1] += 1
            elif c == '}':
                if haut[1] == 0:
                    pile.pop()          # fin de `${…}` : retour au gabarit
                    i += 1
                    continue
                haut[1] -= 1
        i += 1
    return ''.join(out)


def _objets_dans_appel(m, i):
    """TOUS les littéraux objets de la liste d'arguments, sur le texte MASQUÉ.

    Prendre « le premier littéral de niveau 1 » ne suffisait pas : `C.cardState`
    transmet l'état par `C.card(host, Object.assign({}, opts, {state: …}))`, où
    le littéral est niché d'un cran. L'outil déclarait donc `state` « jamais
    passée » alors que c'est le chemin normal pour l'atteindre."""
    prof, acc, j, objets, pile = 0, 0, i, [], []
    #  RAMASSER TOUS LES LITTÉRAUX IMBRIQUÉS NOIE LA MESURE. Ma correction
    #  précédente attrapait les configurations Chart.js passées dans `render:` —
    #  des centaines de clés (`borderWidth`, `callbacks`, `datasets`…) qui ne
    #  sont pas des options du shell. On ne garde que les littéraux au niveau
    #  ARGUMENT (accolade encore fermée), plus ceux d'un `Object.assign`.
    while j < len(m) and j - i < 40000:
        c = m[j]
        if c in '([':
            prof += 1
        elif c in ')]':
            prof -= 1
            if prof <= 0:
                break
        elif c == '{':
            argument = (acc == 0 and (prof == 1 or (prof == 2 and 'Object.assign'
                                                    in m[max(0, j - 200):j])))
            pile.append((j, argument))
            acc += 1
        elif c == '}':
            acc -= 1
            if pile:
                deb, argument = pile.pop()
                if argument:
                    objets.append((deb, j + 1))
        j += 1
    return objets


def _cles_niveau1(m, deb, fin):
    """Les clés de premier niveau d'un littéral objet, sur le texte MASQUÉ."""
    obj = m[deb:fin]
    cles, prof, j, attente = set(), 0, 0, True
    while j < len(obj):
        c = obj[j]
        if c in '{([':
            prof += 1
        elif c in '})]':
            prof -= 1
        elif prof == 1 and attente:
            mm = re.match(r'\s*([A-Za-z_][A-Za-z0-9_]*)\s*:', obj[j:])
            if mm:
                cles.add(mm.group(1))
                j += mm.end()
                attente = False
                continue
        elif prof == 1 and c == ',':
            attente = True
        j += 1
    return cles


def _passees(mut_passe=False):
    """Rend (par_builder, non_analysables).

    LES BUILDERS SONT AUSSI DES APPELANTS, et l'oublier m'a fait accuser à tort.
    `C.cardState` transmet `state` à `C.card` par `Object.assign` : aucun
    appelant externe n'écrit `state:` dans un littéral, et l'outil déclarait donc
    `state` « jamais passée » alors que c'est le chemin normal pour l'atteindre.
    On balaie donc aussi `charts/*.js`, en reconnaissant la forme interne `C.x(`.
    """
    par, opaques = {}, []
    motif = re.compile(r'(?:VXCharts|C)\.([A-Za-z][A-Za-z0-9_]*)\s*\(')
    for chemin in _fichiers_appelants():
        try:
            with open(chemin, encoding='utf-8') as f:
                t = f.read()
        except (OSError, UnicodeDecodeError):
            continue
        if mut_passe and chemin.endswith('markets_page.py') and 'VXCharts.card(' in t:
            t = t.replace('VXCharts.card(', 'VXCharts.card(__H__,{__temoin_jamais_lu:1},', 1)
        masque = _masque(t)
        for m in motif.finditer(masque):
            builder = m.group(1)
            objets = _objets_dans_appel(masque, m.end() - 1)
            if not objets:
                opaques.append((os.path.relpath(chemin, RACINE), builder))
                continue
            for deb, fin in objets:
                par.setdefault(builder, set()).update(_cles_niveau1(masque, deb, fin))
    return par, opaques


def mesurer(mut_lu=False, mut_passe=False):
    """Rend (ignorees, mortes, opaques, lues, passees) ou lève si aveugle.

    Exposé pour qu'un gardien puisse APPELER la mesure au lieu d'épingler des
    chaînes : un gardien qui compare du texte se contente de la forme, celui-ci
    vérifie la propriété."""
    lues = _lues(_sources_charts(mut_lu=mut_lu))
    passees, opaques = _passees(mut_passe=mut_passe)
    if not lues or not passees:
        raise RuntimeError('AVEUGLE — un cote du contrat est vide '
                           '(lues=%d, passees=%d)' % (len(lues), len(passees)))
    mortes, ignorees = [], []
    for builder, cles in sorted(passees.items()):
        connues = lues.get(builder, set())
        if not connues:
            continue        # builder sans parametre d'options identifie
        for c in sorted(cles - connues):
            ignorees.append((builder, c))
    for builder in sorted(lues):
        if builder not in passees:
            continue        # builder jamais appele : autre sujet
        for c in sorted(lues[builder] - passees[builder]):
            mortes.append((builder, c))
    return ignorees, mortes, opaques, lues, passees


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    t_lu, t_passe = '--temoin-lu' in argv, '--temoin-passe' in argv

    try:
        ignorees, mortes, opaques, lues, passees = mesurer(t_lu, t_passe)
    except RuntimeError as e:
        print('%s. Refus de conclure.' % e)
        return 2

    if t_lu or t_passe:
        cible = ('__temoin_jamais_passe', mortes) if t_lu else ('__temoin_jamais_lu', ignorees)
        vu = any(c == cible[0] for _, c in cible[1])
        print('TEMOIN %s : %s' % (cible[0],
              'DENONCE — le detecteur mord' if vu else '*** PASSE INAPERCU ***'))
        return 0 if vu else 2

    print('=== PASSEES MAIS JAMAIS LUES — la page croit dire quelque chose ===')
    if not ignorees:
        print('  aucune.')
    for b, c in ignorees:
        print('  VXCharts.%-18s %s' % (b, c))

    print('\n=== LUES MAIS JAMAIS PASSEES — capacite que personne ne demande ===')
    if not mortes:
        print('  aucune.')
    for b, c in mortes:
        print('  VXCharts.%-18s %s' % (b, c))

    #  AUCUNE LIMITE TUE : un site non analysable est ANNONCE. Le taire
    #  transformerait le silence de l'outil en garantie.
    print('\n%d site(s) d\'appel non analysables (objet construit ailleurs) :' % len(opaques))
    for f, b in opaques[:12]:
        print('  %-46s VXCharts.%s' % (f, b))
    return 1 if (ignorees or mortes) else 0


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
