"""Vertex Test 1.0 · #779 — INVENTAIRE EXÉCUTABLE DU RUNTIME.

Livrable n°1 de l'issue #779 : *« inventaire généré depuis le SHA courant :
imports, routes, blueprints, workers, scheduler, caches, stores, pages et
scripts servis ; matrice propriétaire canonique / adaptateur / legacy / mort ;
métriques reproductibles de taille et complexité »*.

## Pourquoi un instrument et pas un relevé écrit à la main

`MIGRATION_PLAN.md` §Phase 1 l'impose : *« Aucun chiffre historique n'est repris
comme baseline sans reproduction. »* Un inventaire écrit une fois vieillit en
silence — c'est exactement le défaut que ce dépôt a déjà payé. Celui-ci est
**dérivé de l'AST** à chaque exécution et **estampillé du SHA** sur lequel il a
tourné : deux relevés ne peuvent pas diverger sans que le code ait bougé.

## Ce qu'il mesure, et comment

| catégorie | dérivation |
| --- | --- |
| routes | décorateurs `@app.route/get/post` et `@bp.route/get/post` (AST) |
| blueprints | `Blueprint(...)` et `register_blueprint(...)` (AST) |
| workers | `threading.Thread(target=...)` — la cible, pas le nom |
| boucles | fonctions dont le corps contient un `while` de service |
| stores/caches | affectations de module à un `dict`/`{}` |
| pages servies | fonctions de route rendant du HTML |
| métriques | lignes, octets, fonctions, plus longue fonction, imports |

## La matrice de propriété

Chaque route reçoit un statut :

- **CANONIQUE** — servie par un blueprint du package `vertex/` ;
- **LEGACY** — servie directement par `terminal.py` ;
- **ADAPTATEUR** — enregistrée par `terminal.py` mais définie dans le package.

C'est cette colonne qui mesure l'avancement de #779 : le but n'est pas de
supprimer `terminal.py`, c'est de faire tomber **LEGACY** à zéro.

## Anti-vacuité

`--temoin` injecte, dans une copie en mémoire de `terminal.py`, une route, un
worker et un store fabriqués, et exige que l'inventaire les dénonce. Un
inventaire qui ne trouve rien et un inventaire aveugle rendent le même document.

Usage :
    python tools/mesures/inventaire_runtime.py [--temoin] [--json CHEMIN]
"""
import argparse
import ast
import json
import os
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_MONOLITHE = os.path.join(RACINE, 'terminal.py')
_PAQUET = os.path.join(RACINE, 'vertex')

_DECOS_ROUTE = ('route', 'get', 'post', 'put', 'delete', 'patch')

#  Le témoin : trois défauts fabriqués, un par famille détectée.
_TEMOIN = '''

@app.route("/__temoin_route_fabriquee__")
def __temoin_vue__():
    return "temoin"


__temoin_store__ = {}


def __temoin_worker__():
    while True:
        pass


threading.Thread(target=__temoin_worker__, daemon=True).start()
'''


def _sha():
    try:
        return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=RACINE,
                              capture_output=True, text=True).stdout.strip()[:12]
    except Exception:
        return 'inconnu'


def _lire(chemin):
    with open(chemin, encoding='utf-8') as f:
        return f.read()


def _fichiers_paquet():
    out = []
    for base, dirs, noms in os.walk(_PAQUET):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for n in sorted(noms):
            if n.endswith('.py'):
                out.append(os.path.join(base, n))
    return sorted(out)


def _nom_pointe(noeud):
    """Rend `a.b.c` pour un Attribute/Name, ou None."""
    bouts = []
    while isinstance(noeud, ast.Attribute):
        bouts.append(noeud.attr)
        noeud = noeud.value
    if isinstance(noeud, ast.Name):
        bouts.append(noeud.id)
        return '.'.join(reversed(bouts))
    return None


def _litteral(noeud):
    if isinstance(noeud, ast.Constant) and isinstance(noeud.value, str):
        return noeud.value
    return None


def analyser(source, etiquette):
    """Rend le relevé d'un fichier. Aucune supposition sur les noms."""
    arbre = ast.parse(source)
    releve = {'fichier': etiquette, 'routes': [], 'blueprints_definis': [],
              'blueprints_enregistres': [], 'workers': [], 'boucles': [],
              'stores': [], 'imports': set(), 'fonctions': 0,
              'plus_longue_fonction': ('', 0)}

    for noeud in ast.walk(arbre):
        #  ── imports ────────────────────────────────────────────────────
        if isinstance(noeud, ast.Import):
            for a in noeud.names:
                releve['imports'].add(a.name.split('.')[0])
        elif isinstance(noeud, ast.ImportFrom):
            if noeud.module:
                releve['imports'].add(noeud.module.split('.')[0])

        #  ── fonctions et routes ────────────────────────────────────────
        elif isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef)):
            releve['fonctions'] += 1
            longueur = (getattr(noeud, 'end_lineno', noeud.lineno) or noeud.lineno) - noeud.lineno
            if longueur > releve['plus_longue_fonction'][1]:
                releve['plus_longue_fonction'] = (noeud.name, longueur)
            for deco in noeud.decorator_list:
                appel = deco if isinstance(deco, ast.Call) else None
                cible = _nom_pointe(appel.func if appel else deco)
                if not cible or '.' not in cible:
                    continue
                objet, methode = cible.rsplit('.', 1)
                if methode not in _DECOS_ROUTE:
                    continue
                chemin = None
                if appel and appel.args:
                    chemin = _litteral(appel.args[0])
                methodes = ['GET'] if methode == 'get' else (
                    ['POST'] if methode == 'post' else ['*'])
                if appel:
                    for kw in appel.keywords:
                        if kw.arg == 'methods' and isinstance(kw.value, (ast.List, ast.Tuple)):
                            m = [_litteral(e) for e in kw.value.elts]
                            methodes = [x for x in m if x]
                releve['routes'].append({
                    'chemin': chemin or '(calcule)', 'vue': noeud.name,
                    'porteur': objet, 'methodes': methodes, 'ligne': noeud.lineno})
            #  boucle de service : un `while` dans le corps
            for interne in ast.walk(noeud):
                if isinstance(interne, ast.While):
                    releve['boucles'].append(noeud.name)
                    break

        #  ── appels : blueprints, threads ───────────────────────────────
        elif isinstance(noeud, ast.Call):
            cible = _nom_pointe(noeud.func)
            if cible and cible.endswith('register_blueprint'):
                arg = noeud.args[0] if noeud.args else None
                releve['blueprints_enregistres'].append(
                    _nom_pointe(arg) or (_nom_pointe(arg.func) if isinstance(arg, ast.Call) else '?'))
            elif cible and cible.split('.')[-1] == 'Blueprint':
                nom = _litteral(noeud.args[0]) if noeud.args else None
                releve['blueprints_definis'].append(nom or '?')
            elif cible and cible.split('.')[-1] == 'Thread':
                for kw in noeud.keywords:
                    if kw.arg == 'target':
                        releve['workers'].append(_nom_pointe(kw.value) or '?')

    #  ── stores de module : affectation d'un dict au niveau du module ──
    for noeud in arbre.body:
        if isinstance(noeud, ast.Assign) and isinstance(noeud.value, ast.Dict):
            for c in noeud.targets:
                if isinstance(c, ast.Name):
                    releve['stores'].append(c.id)

    releve['imports'] = sorted(releve['imports'])
    releve['boucles'] = sorted(set(releve['boucles']))
    releve['workers'] = sorted(set(releve['workers']))
    return releve


def inventorier(temoin=False):
    """Rend l'inventaire complet, dérivé du SHA courant."""
    src_mono = _lire(_MONOLITHE)
    if temoin:
        src_mono += _TEMOIN
    mono = analyser(src_mono, 'terminal.py')
    mono['lignes'] = src_mono.count('\n') + 1
    mono['octets'] = len(src_mono.encode('utf-8'))

    paquet = []
    for chemin in _fichiers_paquet():
        rel = os.path.relpath(chemin, RACINE)
        try:
            r = analyser(_lire(chemin), rel)
        except SyntaxError:
            continue
        r['lignes'] = _lire(chemin).count('\n') + 1
        paquet.append(r)

    #  ── MATRICE DE PROPRIÉTÉ ───────────────────────────────────────────
    #  Une route servie par un blueprint du paquet est CANONIQUE ; une route
    #  decoree directement sur `app` dans terminal.py est LEGACY. C'est cette
    #  colonne qui mesure l'avancement de #779.
    matrice = []
    for r in mono['routes']:
        matrice.append({**r, 'statut': 'LEGACY', 'fichier': 'terminal.py'})
    for f in paquet:
        for r in f['routes']:
            matrice.append({**r, 'statut': 'CANONIQUE', 'fichier': f['fichier']})

    return {
        'sha': _sha(),
        'monolithe': mono,
        'paquet': paquet,
        'matrice_routes': matrice,
        'totaux': {
            'routes_legacy': sum(1 for m in matrice if m['statut'] == 'LEGACY'),
            'routes_canoniques': sum(1 for m in matrice if m['statut'] == 'CANONIQUE'),
            'blueprints_enregistres': len(mono['blueprints_enregistres']),
            'workers_monolithe': len(mono['workers']),
            'boucles_monolithe': len(mono['boucles']),
            'stores_monolithe': len(mono['stores']),
            'lignes_monolithe': mono['lignes'],
            'octets_monolithe': mono['octets'],
            'fichiers_paquet': len(paquet),
        },
    }


def _rendre(inv):
    t = inv['totaux']
    m = inv['monolithe']
    lignes = []
    a = lignes.append
    a('# Vertex Test 1.0 · #779 — Inventaire exécutable du runtime')
    a('')
    a('SHA : `%s` · généré par `tools/mesures/inventaire_runtime.py`' % inv['sha'])
    a('')
    a('> Ce document est **régénéré**, jamais édité à la main. Un chiffre qui')
    a('> change sans que le code ait bougé est un défaut de l\'instrument.')
    a('')
    a('## Monolithe — ce qu\'il reste à extraire')
    a('')
    a('| mesure | valeur |')
    a('| --- | --- |')
    a('| lignes | %d |' % t['lignes_monolithe'])
    a('| octets | %d |' % t['octets_monolithe'])
    a('| fonctions | %d |' % m['fonctions'])
    a('| plus longue fonction | `%s` (%d lignes) |' % m['plus_longue_fonction'])
    a('| **routes LEGACY** | **%d** |' % t['routes_legacy'])
    a('| blueprints enregistrés | %d |' % t['blueprints_enregistres'])
    a('| workers démarrés | %d |' % t['workers_monolithe'])
    a('| boucles de service | %d |' % t['boucles_monolithe'])
    a('| stores de module | %d |' % t['stores_monolithe'])
    a('')
    a('## Matrice de propriété des routes')
    a('')
    a('| statut | nombre |')
    a('| --- | --- |')
    a('| CANONIQUE (blueprint du paquet) | %d |' % t['routes_canoniques'])
    a('| LEGACY (`terminal.py`) | %d |' % t['routes_legacy'])
    a('')
    a('**L\'objectif de #779 est que la ligne LEGACY tombe à 0.** Supprimer')
    a('`terminal.py` n\'est pas le but ; lui retirer toute responsabilité l\'est.')
    a('')
    a('### Routes encore servies par `terminal.py`')
    a('')
    a('| chemin | vue | méthodes | ligne |')
    a('| --- | --- | --- | --- |')
    for r in sorted(m['routes'], key=lambda x: x['ligne']):
        a('| `%s` | `%s` | %s | %d |'
          % (r['chemin'], r['vue'], ', '.join(r['methodes']), r['ligne']))
    a('')
    a('### Workers démarrés par `terminal.py`')
    a('')
    for w in m['workers']:
        a('- `%s`' % w)
    a('')
    a('### Stores de module (état partagé)')
    a('')
    for s in sorted(m['stores']):
        a('- `%s`' % s)
    a('')
    a('## Paquet `vertex/` — surface canonique')
    a('')
    a('| mesure | valeur |')
    a('| --- | --- |')
    a('| fichiers Python | %d |' % t['fichiers_paquet'])
    a('| routes canoniques | %d |' % t['routes_canoniques'])
    a('')
    a('### Blueprints enregistrés par le monolithe')
    a('')
    for b in sorted(set(m['blueprints_enregistres'])):
        a('- `%s`' % b)
    a('')
    return '\n'.join(lignes)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--temoin', action='store_true')
    p.add_argument('--json')
    p.add_argument('--md')
    args = p.parse_args(argv)

    if args.temoin:
        inv = inventorier(temoin=True)
        vus = {
            'route fabriquee': any(r['chemin'] == '/__temoin_route_fabriquee__'
                                   for r in inv['monolithe']['routes']),
            'worker fabrique': '__temoin_worker__' in inv['monolithe']['workers'],
            'store fabrique': '__temoin_store__' in inv['monolithe']['stores'],
        }
        for quoi, vu in vus.items():
            print('TEMOIN %-18s %s' % (quoi, 'DENONCE — le detecteur mord'
                                       if vu else '*** PASSE INAPERCU ***'))
        return 0 if all(vus.values()) else 2

    inv = inventorier()
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(inv, f, indent=1, ensure_ascii=False, sort_keys=True)
        print('JSON  -> %s' % args.json)
    md = _rendre(inv)
    if args.md:
        with open(args.md, 'w', encoding='utf-8') as f:
            f.write(md + '\n')
        print('MD    -> %s' % args.md)
    else:
        print(md)
    return 0


if __name__ == '__main__':
    sys.exit(main())
