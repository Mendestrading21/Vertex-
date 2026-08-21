#!/usr/bin/env python3
"""Vertex 1.0 — LES 59 MOTEURS ATTEIGNENT-ILS UN ÉCRAN ?

La mission demande un **audit des moteurs de décision** avant d'en créer un
nouveau. La question naturelle — « que calcule chaque moteur ? » — n'est pas la
plus utile. Celle qui l'est :

    **ce que ce moteur calcule sort-il quelque part ?**

Le lot précédent a montré pourquoi. `track_record.evaluate()` tournait, ne
plantait pas, et rendait `resolved: 0` sur toutes les entrées : un moteur
parfaitement vivant dont le résultat était vide, sous un test vert. Un moteur
qu'aucune route n'atteint est le cas dégénéré du même problème.

## Ce que l'outil mesure

Pour chaque module de `vertex/engines/`, il construit le graphe d'imports du
dépôt et cherche un chemin jusqu'à une **surface servie** :

- une route (`vertex/app/routes/**`, ou une page `vertex/ui/pages/**`) ;
- en partant de ces surfaces, il remonte les imports de proche en proche.

Trois statuts :

- `SERVI`      — un chemin d'import mène du moteur à une surface servie ;
- `INDIRECT`   — atteint seulement via un autre moteur lui-même servi ;
- `INATTEINT`  — aucun chemin. Le moteur peut être excellent : personne ne le lit.

## Ce que l'outil NE mesure pas, et il faut le dire

Un chemin d'import prouve la **portée**, pas la **sortie**. Un module importé
dont on n'appelle aucune fonction reste « SERVI » ici. C'est la limite exacte
qu'un lot précédent a nommée — *« une portée n'est pas une sortie »* — et cet
outil s'arrête volontairement à la portée : franchir le pas demanderait de
suivre les appels, ce qu'un `import *` et des appels indirects rendent
incomplet (mesuré : `terminal.py` fait `from vertex.data.universe import *`).

Un `INATTEINT` est donc un fait **solide** — aucun chemin n'existe. Un `SERVI`
est un fait **faible** : il ne dit pas que le résultat est affiché.

## Les témoins

1. **positif** — un moteur notoirement servi (`decision_stack`, cité par le
   guide comme « vérité des verdicts ») doit ressortir atteint ;
2. **négatif** — un module fabriqué, importé par personne, doit ressortir
   `INATTEINT`. S'il ressortait servi, le graphe relierait n'importe quoi.

Usage :
    python tools/vertex_1_0/mesurer_moteurs.py [--json]
Sorties : 0 = mesuré, 2 = témoin muet.
"""
from __future__ import annotations

import ast
import json
import pathlib
import sys
from collections import defaultdict, deque

RACINE = pathlib.Path(__file__).resolve().parents[2]

#: Les surfaces d'où part la remontée. « Servi » ne veut pas dire « déclare une
#: route » : le scan tourne dans les **boucles de fond** de `terminal.py`, qui
#: remplissent `scan_state` — l'état que toutes les routes servent ensuite. Un
#: moteur du pipeline de scan est donc aussi lu par l'utilisateur qu'un moteur
#: appelé depuis une vue.
#:
#: ⚠ PREMIÈRE VERSION : `routes/` et `pages/` seulement. Elle rendait
#: `analysis` (336 lignes, producteur des séries de prix de tout le produit)
#: « INATTEINT ». L'hypothèse « surface = route » avait été invalidée par le
#: chantier #779 lui-même, qui a fait passer `terminal.py` de 14 routes à 0 :
#: le monolithe a cessé de déclarer des routes sans cesser d'être servi. Un
#: instrument qui encode une hypothèse périmée mesure le passé.
SURFACES = ('vertex/app/routes/', 'vertex/ui/pages/', 'vertex/scanner/',
            'vertex/runtime.py', 'terminal.py')

#: Témoin négatif : un module que le dépôt ne peut pas importer.
TEMOIN_ABSENT = 'vertex/engines/_temoin_moteur_inexistant.py'

#: Témoin positif : le guide le nomme « vérité des verdicts ».
TEMOIN_SERVI = 'decision_stack'


def _modules():
    """{chemin relatif -> nom de module pointé} pour tout le paquet + le monolithe."""
    out = {}
    for p in sorted((RACINE / 'vertex').rglob('*.py')):
        if '__pycache__' in str(p):
            continue
        rel = p.relative_to(RACINE).as_posix()
        out[rel] = rel[:-3].replace('/', '.').removesuffix('.__init__')
    out['terminal.py'] = 'terminal'
    return out


def _graphe(modules):
    """`importe[A] = {B, …}` : A importe B. Les deux sens servent."""
    par_nom = {nom: rel for rel, nom in modules.items()}
    importe = defaultdict(set)
    for rel in modules:
        try:
            arbre = ast.parse((RACINE / rel).read_text(encoding='utf-8', errors='replace'))
        except (SyntaxError, OSError):
            continue
        cibles = set()
        for n in ast.walk(arbre):
            if isinstance(n, ast.ImportFrom) and n.module:
                cibles.add(n.module)
                for a in n.names:                    # `from vertex.engines import x`
                    cibles.add('%s.%s' % (n.module, a.name))
            elif isinstance(n, ast.Import):
                for a in n.names:
                    cibles.add(a.name)
        for c in cibles:
            if c in par_nom:
                importe[rel].add(par_nom[c])
    return importe


def _appels(modules, importe):
    """{moteur -> nombre de sites d'appel} dans la PRODUCTION (tests exclus).

    Un moteur importé dont aucune fonction n'est appelée est le cas exact que
    « une portée n'est pas une sortie » désigne. On compte les `X.f(...)` où `X`
    est l'alias sous lequel le moteur a été importé — c'est la forme employée
    partout dans le dépôt.

    ⚠ Cette mesure est BORNÉE PAR LE BAS : un appel indirect (attribut stocké,
    `getattr`, passage en argument) n'est pas vu. Zéro appel compté n'est donc
    pas une preuve d'inutilité — c'est une raison de regarder.
    """
    par_nom = {nom: rel for rel, nom in modules.items()}
    compte = defaultdict(int)
    for rel in modules:
        try:
            arbre = ast.parse((RACINE / rel).read_text(encoding='utf-8', errors='replace'))
        except (SyntaxError, OSError):
            continue
        #  alias local -> chemin du moteur importé
        alias = {}
        for n in ast.walk(arbre):
            if isinstance(n, ast.ImportFrom) and n.module:
                for a in n.names:
                    cible = par_nom.get('%s.%s' % (n.module, a.name))
                    if cible and cible.startswith('vertex/engines/'):
                        alias[a.asname or a.name] = cible
            elif isinstance(n, ast.Import):
                for a in n.names:
                    cible = par_nom.get(a.name)
                    if cible and cible.startswith('vertex/engines/'):
                        alias[(a.asname or a.name).split('.')[0]] = cible
        if not alias:
            continue
        for n in ast.walk(arbre):
            #  (a) appel direct : `X.f(...)`
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and isinstance(n.func.value, ast.Name)
                    and n.func.value.id in alias):
                compte[alias[n.func.value.id]] += 1
            #  (b) LIAISON D'ATTRIBUT : `f = X.f`, puis `f(...)` ailleurs.
            #
            #  ⚠ Oublier cette forme donnait CINQ faux positifs, dont
            #  `analysis` — le producteur des séries de prix de tout le produit,
            #  lié par `analyse = _analysis.analyse` dans `terminal.py`. C'est
            #  l'idiome employé partout dans le dépôt, y compris par les façades
            #  posées au chantier #779 (`_sync_ibkr_state = _ibkr_state.sync`).
            #  Un détecteur qui l'ignore mesure un dépôt qui n'existe pas.
            elif isinstance(n, ast.Assign) and isinstance(n.value, ast.Attribute) \
                    and isinstance(n.value.value, ast.Name) \
                    and n.value.value.id in alias:
                compte[alias[n.value.value.id]] += 1
    return compte


def mesurer() -> dict:
    modules = _modules()
    importe = _graphe(modules)

    #  Remontée depuis les surfaces servies : qui est atteignable.
    atteints, file = set(), deque(
        rel for rel in modules if rel.startswith(SURFACES))
    depart = set(file)
    while file:
        rel = file.popleft()
        for cible in importe.get(rel, ()):
            if cible not in atteints:
                atteints.add(cible)
                file.append(cible)

    moteurs = sorted(rel for rel in modules
                     if rel.startswith('vertex/engines/')
                     and not rel.endswith('__init__.py'))
    appels = _appels(modules, importe)
    lignes = []
    for rel in moteurs:
        direct = any(rel in importe.get(s, ()) for s in depart)
        lignes.append({
            'moteur': pathlib.Path(rel).stem,
            'chemin': rel,
            'statut': ('SERVI' if direct else
                       'INDIRECT' if rel in atteints else 'INATTEINT'),
            'appels_production': appels.get(rel, 0),
            'lignes': len((RACINE / rel).read_text(encoding='utf-8',
                                                   errors='replace').splitlines()),
        })
    return {
        'total': len(lignes),
        'servis': sum(1 for l in lignes if l['statut'] == 'SERVI'),
        'indirects': sum(1 for l in lignes if l['statut'] == 'INDIRECT'),
        'inatteints': sum(1 for l in lignes if l['statut'] == 'INATTEINT'),
        'atteints_sans_appel': sorted(
            l['moteur'] for l in lignes
            if l['statut'] != 'INATTEINT' and l['appels_production'] == 0),
        'moteurs': lignes,
        'surfaces_de_depart': len(depart),
    }


def _temoins(r: dict) -> list:
    echecs = []
    par_nom = {l['moteur']: l for l in r['moteurs']}
    positif = par_nom.get(TEMOIN_SERVI)
    if not positif:
        echecs.append('temoin positif absent du recensement : %s' % TEMOIN_SERVI)
    elif positif['statut'] == 'INATTEINT':
        echecs.append(
            'TEMOIN POSITIF MUET : « %s » ressort INATTEINT alors que le guide '
            'le nomme verite des verdicts — le graphe d\'imports est casse'
            % TEMOIN_SERVI)
    if TEMOIN_ABSENT in {l['chemin'] for l in r['moteurs']}:
        echecs.append('le temoin negatif existe sur disque : il ne temoigne plus')
    if not r['surfaces_de_depart']:
        echecs.append('aucune surface servie trouvee : la remontee part de rien')
    #  Témoin négatif VIVANT : un moteur fabriqué, importé par personne, doit
    #  ressortir INATTEINT. Sans lui, « 1 seul inatteint » pourrait aussi bien
    #  vouloir dire « le detecteur ne sait plus reconnaitre l'absence ».
    modules = _modules()
    modules[TEMOIN_ABSENT] = 'vertex.engines._temoin_moteur_inexistant'
    importe = _graphe(modules)
    atteints, file = set(), deque(rel for rel in modules if rel.startswith(SURFACES))
    while file:
        rel = file.popleft()
        for cible in importe.get(rel, ()):
            if cible not in atteints:
                atteints.add(cible)
                file.append(cible)
    if TEMOIN_ABSENT in atteints:
        echecs.append(
            'TEMOIN NEGATIF ROMPU : un moteur que PERSONNE n\'importe ressort '
            'atteignable — le graphe relie n\'importe quoi')
    if positif and positif['appels_production'] == 0:
        echecs.append(
            'TEMOIN D\'APPEL MUET : « %s » ne compte aucun appel en production '
            'alors qu\'il porte les verdicts — le detecteur d\'appels est casse'
            % TEMOIN_SERVI)
    return echecs


def rendre_texte(r: dict) -> str:
    out = ['LES MOTEURS ATTEIGNENT-ILS UN ECRAN ?',
           '=' * 62,
           'moteurs      : %d' % r['total'],
           'SERVI        : %d  (importes directement par une route ou une page)'
           % r['servis'],
           'INDIRECT     : %d  (atteints via un autre module servi)' % r['indirects'],
           'INATTEINT    : %d  (aucun chemin d\'import depuis une surface)'
           % r['inatteints'],
           'surfaces     : %d' % r['surfaces_de_depart'],
           '']
    sans_appel = r['atteints_sans_appel']
    if sans_appel:
        out.append('ATTEINTS MAIS SANS AUCUN APPEL MESURE (%d) :' % len(sans_appel))
        out += ['   ' + m for m in sans_appel]
        out.append('   (borne PAR LE BAS : un appel indirect n\'est pas vu —')
        out.append('    zero appel n\'est pas une preuve, c\'est une raison de regarder)')
        out.append('')
    inatteints = [l for l in r['moteurs'] if l['statut'] == 'INATTEINT']
    if inatteints:
        out.append('INATTEINTS (%d) — aucun ecran ne peut les lire :' % len(inatteints))
        for l in sorted(inatteints, key=lambda x: -x['lignes']):
            out.append('   %-34s %5d lignes' % (l['moteur'], l['lignes']))
        out.append('')
        out.append('RAPPEL : ce statut dit qu\'aucun CHEMIN D\'IMPORT n\'existe.')
        out.append('C\'est un fait solide. L\'inverse (« SERVI ») est faible :')
        out.append('un module importe sans etre appele compte comme servi ici.')
    return '\n'.join(out)


def main() -> int:
    r = mesurer()
    echecs = _temoins(r)
    if echecs:
        for e in echecs:
            print('TEMOIN MUET : %s' % e, file=sys.stderr)
        return 2
    print(json.dumps(r, indent=2, ensure_ascii=False) if '--json' in sys.argv
          else rendre_texte(r))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
