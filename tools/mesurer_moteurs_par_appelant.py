"""tools/mesurer_moteurs_par_appelant.py — QUI APPELLE CE MOTEUR, ET SOUS QUELLE CLÉ SORT-IL ?

Cet outil remplace la méthode de `tools/mesurer_moteurs_muets.py`, qui m'a donné
**trois inventaires faux d'affilée** (lots 49, 52, 54).

## La faute, nommée précisément

L'ancienne sonde cherchait la chaîne `"nom_du_module"` dans le corps des
réponses servies. Cela ne dit la vérité que si un moteur publie sous une clé
portant son nom de fichier. Or, mesuré :

| moteur | ce qu'il publie réellement |
| --- | --- |
| `drawdown_context` | `contexts.drawdown` |
| `decision_readiness` | `decision.readiness` |
| `historical_stress` | `stress_test` |
| `walk_forward_validation` | **le corps entier** de `/api/skyler/validation` |
| `option_cohort` | **le corps entier** de `/api/tracking/options/cohort` |

Les deux derniers sont le cas décisif : **un corps de réponse ne se nomme jamais
lui-même**. Aucune recherche de nom, si maligne soit-elle, ne peut les trouver.
*Une sonde qui cherche des noms de fichiers dans du JSON mesure ma convention de
nommage, pas le produit.*

## La méthode juste : remonter la chaîne réelle

1. **L'APPELANT** — analyse AST de **tout ce qui peut appeler un moteur** :
   `vertex/app/routes/*.py`, **`terminal.py`** et `vertex/ui/**`. On repère les
   imports d'un moteur et les appels correspondants. C'est un fait de structure,
   pas une ressemblance de texte.

   Deux corrections apprises en mesurant, et toutes deux du même genre :
   *j'avais pris ma convention pour la structure.*

   - **`terminal.py` manquait.** Sans lui, l'outil annonçait « 22 moteurs sans
     appelant », dont `track_record`, `committee` et `scorecard` — tous importés
     par le monolithe qui porte encore des routes. Je n'avais pas ouvert le plus
     gros fichier du produit et j'en concluais que vingt-deux moteurs ne
     servaient à personne.
   - **Une seule forme d'import.** `from vertex.market.daily_brief import
     build_daily_brief` lie la **fonction**, pas le module : l'appel est
     `build_daily_brief(...)` et non `daily_brief.build(...)`. `daily_brief` et
     `editorial` étaient donc « sans appelant » alors que `redesign.py` les
     appelle. Les deux formes sont désormais reconnues.

   Effet mesuré : 57 → **66** moteurs appelés depuis une route, et « sans
   appelant » 22 → **10**.
2. **LA CLÉ** — on remonte de l'appel à ce qui le reçoit :
   `decision['readiness'] = _r.build(...)` → clé `readiness` ;
   `out = _w.assess(...)` puis `jsonify(out)` → **corps entier**.
3. **LA ROUTE** — le décorateur `@bp.route(...)` de la fonction englobante.
4. **L'ÉCRAN** — la clé est-elle lue dans `vertex/ui/**` ou le JS servi ?

Un moteur appelé depuis un autre moteur (et non depuis une route) est signalé
**INDIRECT** : sa sortie voyage sous la clé de son appelant, et le dire est plus
utile que de le déclarer muet.

## Deux verdicts que le premier jet rendait faux, et qu'il fallait ajouter

**1. « Peint génériquement ».** Le premier jet déclarait `drawdown_context`
MUET. Faux : il publie `contexts.drawdown`, et le bloc du lot 51 lit
`packet.contexts` **en entier**. Aucune clé individuelle n'apparaît donc dans le
code de l'interface — et c'est la QUALITÉ de ce rendu, pas un défaut : il
accueillera le vingt-deuxième contexte sans une ligne de code. Chercher chaque
clé dans les sources de l'UI reproduisait, une fois de plus, « comparer par le
texte ce qui doit l'être par la structure ». L'outil demande donc aussi : *cette
clé est-elle membre d'un conteneur que l'écran lit en bloc ?*

**1 bis. Un moteur qui sert le CORPS ENTIER n'a pas de clé — il a une ROUTE.**
Corrigé au lot 57, et c'est la septième fois de la même famille : je demandais
« la clé est-elle lue ? » à des moteurs qui n'en publient aucune, et la réponse
était non par construction. Onze moteurs étaient donc déclarés muets ; **sept**
sont en réalité peints — l'interface `fetch` leur route et affiche le corps.
`anomaly`, `evidence_lab`, `decision_stack`, `session_digest`, `skyler_journal`,
`multileg_lab` et `performance` étaient accusés à tort. La bonne question, pour
eux, est : *l'écran demande-t-il cette route ?*

**2. « Indéterminé ».** L'AST voit ce qui REÇOIT l'appel. Quand c'est une clé de
dictionnaire, c'est la clé servie ; quand c'est `jsonify(v)`, c'est le corps
entier. Mais quand c'est une variable intermédiaire (`pctx`, `ev`, `packet0`)
qui poursuit son chemin, l'outil **ne sait pas** sous quelle clé elle ressort.
Le premier jet appelait cela « muet ». Ne pas savoir n'est pas savoir que non :
ces moteurs sont désormais rangés à part, et le chiffre des muets ne les gonfle
plus.

## Anti-vacuité

Cinq moteurs sont **connus peints** (mesurés aux lots 49-54). Si l'outil n'en
retrouve pas au moins trois, c'est lui qui est cassé : il rend 2 plutôt qu'un
inventaire qui aurait l'air sérieux.

Usage : python tools/mesurer_moteurs_par_appelant.py [--base http://127.0.0.1:5002]
"""
import ast
import json
import os
import pathlib
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RACINE = pathlib.Path(__file__).resolve().parent.parent

#  Les paquets où vivent les moteurs. Mesuré, pas supposé : `historical_stress`
#  est dans `portfolio/` et `option_cohort` dans `tracking/` — les chercher tous
#  dans `engines/` était l'une des erreurs du lot 52.
PAQUETS = ('vertex/engines', 'vertex/market', 'vertex/portfolio', 'vertex/tracking')

#  Mesurés peints aux lots 49-54 : ils servent de témoin.
TEMOINS = ('regime_break', 'instrument_profile', 'sector_coherence',
           'opportunity_reliability', 'opportunity_attribution', 'decision_readiness')


def moteurs():
    """Tout module de moteur, avec son chemin — relevé sur le disque."""
    trouves = {}
    for paquet in PAQUETS:
        for f in sorted((RACINE / paquet).glob('*.py')):
            if f.stem.startswith('_'):
                continue
            trouves[f.stem] = '%s/%s.py' % (paquet, f.name)
    return trouves


def _routes_du_fichier(arbre):
    """Chemin de route de chaque fonction décorée `@bp.route('/x')`."""
    par_fonction = {}
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for deco in noeud.decorator_list:
            if (isinstance(deco, ast.Call) and deco.args
                    and isinstance(deco.args[0], ast.Constant)
                    and isinstance(deco.args[0].value, str)
                    and deco.args[0].value.startswith('/')):
                par_fonction[noeud.name] = deco.args[0].value
    return par_fonction


def _fonction_englobante(arbre, ligne):
    """La fonction qui contient cette ligne — pour rattacher un appel à sa route."""
    choix, meilleure = None, -1
    for noeud in ast.walk(arbre):
        if isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fin = max((getattr(n, 'lineno', noeud.lineno) for n in ast.walk(noeud)),
                      default=noeud.lineno)
            if noeud.lineno <= ligne <= fin and noeud.lineno > meilleure:
                choix, meilleure = noeud.name, noeud.lineno
    return choix


def _alias_des_moteurs(arbre, connus):
    """Les deux façons d'atteindre un moteur, et j'en connaissais UNE.

    - `from vertex.engines import decision_readiness as _r` → `_r` est le MODULE ;
      les appels sont des attributs (`_r.build(...)`).
    - `from vertex.market.daily_brief import build_daily_brief` → le nom lié est
      la **fonction**, et l'appel est un simple `build_daily_brief(...)`.

    Le premier jet ne voyait que la première forme. Résultat : `daily_brief` et
    `editorial`, appelés depuis `vertex/app/routes/redesign.py`, étaient rangés
    « sans appelant ». Encore une convention prise pour une structure.

    Rend deux tables : les alias de MODULE et les noms de FONCTION importés.
    """
    modules, fonctions = {}, {}
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.ImportFrom):
            chemin = noeud.module or ''
            if not chemin.startswith('vertex'):
                continue
            dernier = chemin.rsplit('.', 1)[-1]
            for nom in noeud.names:
                if nom.name in connus:
                    modules[nom.asname or nom.name] = nom.name
                elif dernier in connus:
                    #  Import profond d'un symbole : le nom lié appartient au
                    #  module `dernier`.
                    fonctions[nom.asname or nom.name] = dernier
        elif isinstance(noeud, ast.Import):
            for nom in noeud.names:
                court = nom.name.rsplit('.', 1)[-1]
                if court in connus:
                    modules[nom.asname or court] = court
    return modules, fonctions


def _cle_recevante(arbre, appel):
    """Ce qui reçoit le résultat de l'appel : clé de dict, variable, ou rien.

    C'est ICI que se joue la correction du lot 54. Un `jsonify(variable)` dans la
    même fonction signifie que le moteur remplit le **corps entier** — cas que
    l'ancienne méthode ne pouvait structurellement pas voir."""
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Assign):
            continue
        if noeud.value is not appel:
            continue
        cible = noeud.targets[0]
        if (isinstance(cible, ast.Subscript) and isinstance(cible.slice, ast.Constant)
                and isinstance(cible.slice.value, str)):
            porteur = getattr(cible.value, 'id', '')
            return ('cle', '%s.%s' % (porteur, cible.slice.value) if porteur
                    else cible.slice.value, cible.slice.value)
        if isinstance(cible, ast.Name):
            return ('variable', cible.id, cible.id)
        if isinstance(cible, ast.Tuple):
            noms = [getattr(e, 'id', '?') for e in cible.elts]
            return ('variables', ', '.join(noms), noms[0] if noms else '')
    return (None, '', '')


def _sert_le_corps(arbre, fonction, variable):
    """La fonction rend-elle `jsonify(<variable>)` — donc le corps entier ?"""
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if noeud.name != fonction:
            continue
        for n in ast.walk(noeud):
            if (isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'jsonify'
                    and n.args and getattr(n.args[0], 'id', None) == variable):
                return True
    return False


def fichiers_appelants():
    """OÙ CHERCHER LES APPELANTS — et `terminal.py` en fait partie.

    Premier jet : seulement `vertex/app/routes/*.py`. Il rendait alors
    « 22 moteurs sans appelant », dont `track_record`, `committee` et
    `scorecard` — tous importés par **`terminal.py`**, le monolithe qui porte
    encore des routes. Je n'avais pas ouvert le plus gros fichier du produit et
    j'en concluais que vingt-deux moteurs ne servaient à personne.

    Les pages de `vertex/ui/**` appellent elles aussi des moteurs au rendu.
    """
    fs = sorted((RACINE / 'vertex' / 'app' / 'routes').glob('*.py'))
    fs.append(RACINE / 'terminal.py')
    fs += sorted((RACINE / 'vertex' / 'ui').rglob('*.py'))
    return [f for f in fs if f.exists()]


def relever():
    connus = moteurs()
    trace = {n: [] for n in connus}
    for f in fichiers_appelants():
        src = f.read_text(encoding='utf-8')
        try:
            arbre = ast.parse(src)
        except SyntaxError:                          # pragma: no cover - diagnostic
            continue
        modules, fonctions = _alias_des_moteurs(arbre, connus)
        if not modules and not fonctions:
            continue
        routes = _routes_du_fichier(arbre)
        for noeud in ast.walk(arbre):
            if not isinstance(noeud, ast.Call):
                continue
            #  Deux formes d'appel, une par forme d'import (cf. _alias_des_moteurs).
            porteur = getattr(noeud.func, 'value', None)
            nom_module = getattr(porteur, 'id', None)
            nom_fonction = getattr(noeud.func, 'id', None)
            if nom_module in modules:
                moteur = modules[nom_module]
            elif nom_fonction in fonctions:
                moteur = fonctions[nom_fonction]
            else:
                continue
            fonction = _fonction_englobante(arbre, noeud.lineno)
            genre, etiquette, variable = _cle_recevante(arbre, noeud)
            corps_entier = (genre == 'variable'
                            and _sert_le_corps(arbre, fonction, variable))
            trace[moteur].append({
                'fichier': f.name, 'fonction': fonction,
                'route': routes.get(fonction), 'genre': genre,
                'etiquette': etiquette, 'corps_entier': corps_entier,
            })
    return connus, trace


def _indirects(connus):
    """Moteurs appelés par d'AUTRES moteurs : leur sortie voyage sous la clé de
    l'appelant. Les déclarer muets serait faux."""
    par = {}
    for paquet in PAQUETS:
        for f in sorted((RACINE / paquet).glob('*.py')):
            src = f.read_text(encoding='utf-8')
            try:
                arbre = ast.parse(src)
            except SyntaxError:                      # pragma: no cover
                continue
            mods, fns = _alias_des_moteurs(arbre, connus)
            for cible in list(mods.values()) + list(fns.values()):
                if cible != f.stem:
                    par.setdefault(cible, set()).add(f.stem)
    return par


_CACHE_ECRAN = {}


def _source_ecran():
    """Tout ce qui peint : les pages Python et le JS servi."""
    if 'texte' not in _CACHE_ECRAN:
        texte = ''
        for p in list((RACINE / 'vertex' / 'ui').rglob('*.py')) + \
                list((RACINE / 'vertex' / 'static' / 'vertex' / 'js').rglob('*.js')):
            texte += p.read_text(encoding='utf-8', errors='replace')
        _CACHE_ECRAN['texte'] = texte
    return _CACHE_ECRAN['texte']


def _lu_par_l_ecran(cles):
    texte = _source_ecran()
    return {c for c in cles if c and c in texte}


def _corps(base, chemin):
    try:
        with urllib.request.urlopen(base + chemin, timeout=40) as r:
            return r.read().decode('utf-8', 'replace')
    except Exception:
        return ''


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    base = 'http://127.0.0.1:5002'
    if '--base' in argv:
        base = argv[argv.index('--base') + 1]

    connus, trace = relever()
    indirects = _indirects(connus)
    directs = {n for n, v in trace.items() if v}
    print('moteurs releves sur le disque : %d (%s)'
          % (len(connus), ', '.join(p.split('/')[-1] for p in PAQUETS)))
    print('appeles depuis une route : %d · appeles par un autre moteur : %d'
          % (len(directs), len(indirects)))

    vus = [t for t in TEMOINS if t in directs or t in indirects]
    if len(vus) < 3:
        print('\nAVEUGLE — seuls %d des %d moteurs connus peints ont ete '
              'retrouves. C\'est la sonde qui est cassee, pas le produit.'
              % (len(vus), len(TEMOINS)))
        return 2
    print('temoin : %d/%d moteurs connus peints retrouves' % (len(vus), len(TEMOINS)))

    #  CE QUE L'ÉCRAN LIT NOMMÉMENT — interrogé au moment du classement, et non
    #  pré-calculé. Ma première version bâtissait cet ensemble AVANT la
    #  résolution contre le produit vivant : une clé découverte à la résolution
    #  ne pouvait donc jamais y figurer, et `instrument_profile` — peint depuis
    #  le lot 49, confirmé au navigateur — ressortait MUET. Un défaut d'ordre
    #  dans ma propre sonde, pas dans le produit.
    ecran = _source_ecran()
    lues = lambda cle: bool(cle) and cle in ecran  # noqa: E731 - lisibilité locale

    #  … et ce que l'écran lit EN BLOC. Mesuré sur le produit vivant : les clés
    #  réellement publiées dans `packet.contexts`, que le bloc du lot 51 rend
    #  génériquement. Une clé membre de ce conteneur est peinte sans être nommée.
    generiques, dans_decision = set(), set()
    conteneur_lu = 'packet.contexts' in _source_ecran()
    corps = _corps(base, '/api/skyler/ACN')
    if corps:
        try:
            rep = json.loads(corps)
            generiques = set(((rep.get('packet') or {}).get('contexts') or {}))
            dans_decision = set(rep.get('decision') or {})
        except ValueError:
            pass
    if not generiques:
        print('\nAVEUGLE — `/api/skyler/ACN` n\'a pas rendu de contextes : sans '
              'le produit vivant, impossible de distinguer « peint en bloc » de '
              '« muet ». Demarrer le serveur de demonstration.')
        return 2
    if not conteneur_lu:
        print('note : l\'ecran ne lit plus `packet.contexts` — le rendu '
              'generique du lot 51 a disparu, plus rien n\'est peint « en bloc ».')

    peints, par_bloc, muets, flous = [], [], [], []
    indirect_only, jamais = [], []
    for nom in sorted(connus):
        usages = trace.get(nom) or []
        if not usages:
            (indirect_only if nom in indirects else jamais).append(nom)
            continue
        u = next((x for x in usages if x['route']), usages[0])
        route = u['route'] or ('via %s' % u['fonction'])
        if u['corps_entier']:
            #  PAS DE CLÉ, DONC UNE ROUTE. Demander « la cle est-elle lue ? » a
            #  un moteur qui n'en publie aucune, c'est obtenir « non » par
            #  construction — sept moteurs etaient ainsi accuses a tort.
            #  On demande donc : l'ecran demande-t-il cette route ? Le prefixe
            #  stable est ce qui precede le premier parametre.
            prefixe = (u['route'] or '').split('<')[0].rstrip('/')
            demandee = bool(prefixe) and prefixe in ecran
            ligne = (nom, route, 'corps entier · route %s' %
                     ('demandee par l\'ecran' if demandee else 'JAMAIS demandee'))
            (peints if demandee else muets).append(ligne)
            continue
        if u['genre'] != 'cle':
            #  L'AST ne sait pas sous quelle clé cette variable ressort. Plutôt
            #  que de deviner OU de renoncer, on RÉSOUT contre le produit vivant :
            #  la structure propose des candidats, le serveur tranche. Les
            #  candidats sont le nom de la variable qui reçoit et le nom du
            #  module débarrassé de son suffixe `_context` — deux conventions
            #  observées, jamais supposées.
            candidats = [c for c in (u['etiquette'], nom,
                                     nom[:-8] if nom.endswith('_context') else '')
                         if c and ',' not in c and c != '—']
            trouve = next((c for c in candidats
                           if c in generiques or c in dans_decision), None)
            if trouve is None:
                flous.append((nom, route, u['etiquette'] or '—'))
                continue
            cle = trouve
            u = dict(u, etiquette=('packet.contexts.%s' % trouve
                                   if trouve in generiques else 'decision.%s' % trouve))
        else:
            cle = u['etiquette'].split('.')[-1]
        ligne = (nom, route, u['etiquette'])
        if lues(cle):
            peints.append(ligne)
        elif cle in generiques:
            par_bloc.append(ligne)
        else:
            muets.append(ligne)

    print('\nPEINTS NOMMEMENT — la cle est lue telle quelle : %d' % len(peints))
    for n, r, c in peints:
        print('  %-30s %-34s %s' % (n, r, c))
    print('\nPEINTS EN BLOC — membres de `packet.contexts`, rendus par le bloc '
          'generique du lot 51 : %d' % len(par_bloc))
    for n, r, c in par_bloc:
        print('  %-30s %-34s %s' % (n, r, c))
    print('\nMUETS — la sortie atteint une route et rien ne la lit : %d' % len(muets))
    for n, r, c in muets:
        print('  %-30s %-34s %s' % (n, r, c))
    print('\nINDETERMINES — la variable qui recoit poursuit son chemin ; l\'AST '
          'ne suit pas jusqu\'a la cle servie : %d' % len(flous))
    for n, r, c in flous:
        print('  %-30s %-34s recoit -> %s' % (n, r, c))
    print('\nINDIRECTS — appeles par un autre moteur, sortent sous SA cle : %d'
          % len(indirect_only))
    for n in indirect_only:
        print('  %-30s appele par %s' % (n, ', '.join(sorted(indirects[n]))))
    print('\nSANS APPELANT — ni route ni moteur ne les appelle : %d' % len(jamais))
    for n in jamais:
        print('  %s' % n)

    #  CONTRÔLE SUR LE PRODUIT VIVANT : pour les moteurs qui remplissent une clé
    #  sous une route interrogeable sans paramètre, on vérifie que la clé est
    #  bien là. La structure dit ce qui DEVRAIT sortir ; seul le serveur dit ce
    #  qui sort.
    verif, ok = [], 0
    for nom, usages in sorted(trace.items()):
        for u in usages:
            if not u['route'] or '<' in u['route'] or u['genre'] != 'cle':
                continue
            cle = u['etiquette'].split('.')[-1]
            corps = _corps(base, u['route'])
            if not corps:
                continue
            verif.append((nom, u['route'], cle, ('"%s"' % cle) in corps))
            break
    for nom, route, cle, present in verif:
        ok += 1 if present else 0
    if verif:
        print('\ncontrole sur le serveur : %d/%d cles attendues reellement '
              'presentes' % (ok, len(verif)))
        for nom, route, cle, present in verif:
            if not present:
                print('  ABSENTE  %-26s %s -> "%s"' % (nom, route, cle))
    return 0


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
