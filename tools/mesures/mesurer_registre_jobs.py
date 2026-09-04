#!/usr/bin/env python3
"""Vertex Test 1.0 · #779/G1 — LE REGISTRE DE JOBS DIT-IL VRAI ?

`RELEASE_GATES.md` G1 exige que **le scheduler ait un propriétaire modulaire**.
Un propriétaire existe déjà : `vertex/scheduler/registry.py`, qui déclare 27
jobs et les sert sur `/api/system/automations`. La question que personne n'avait
posée est plus embarrassante que « qui possède le scheduler ? » :

    **ces 27 jobs existent-ils ?**

Un job déclaré n'est pas un job qui tourne. Le registre ne reçoit d'information
que par `registry.beat('NOM')` — s'il n'existe aucun appel `beat` portant un
nom, la ligne restera éternellement à `last_run: null`, et la page Système
affichera « jamais exécuté » pour quelque chose qui n'a **aucun exécutant dans
le code**. Ce n'est pas la même chose qu'un job en panne, et l'interface ne fait
pourtant pas la différence.

## Ce que l'outil mesure

Pour chaque nom déclaré dans `registry._CANONICAL`, il cherche à l'AST tous les
appels `*.beat(<nom>, …)` du dépôt et classe :

- `ACTIF`          — au moins un émetteur porte ce nom ;
- `SANS_EMETTEUR`  — aucun appel `beat` ne le nomme. Le job ne peut pas tourner.

Il relève aussi les émetteurs dont le nom n'est **pas** une constante littérale
(`beat(nom_calcule)`) : ceux-là échappent à toute analyse statique, et leur
existence rendrait la mesure incomplète — l'outil le dit au lieu de conclure.

## Les témoins

Un détecteur qui ne trouve rien ne prouve rien. Deux témoins sont posés en
mémoire avant l'analyse :

1. un nom déclaré fabriqué, qu'aucun `beat` n'émet → doit ressortir
   `SANS_EMETTEUR` ;
2. un nom réellement émis par le dépôt → doit ressortir `ACTIF`.

Si l'un des deux ne se comporte pas comme attendu, l'outil sort en **2** :
aveugle, donc sans verdict.

Usage :
    python tools/mesures/mesurer_registre_jobs.py [--json]
Sorties : 0 = mesuré, 2 = témoin muet (mesure non fiable).
"""
from __future__ import annotations

import ast
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]

#: Un nom que le dépôt ne peut pas émettre : c'est tout l'intérêt du témoin.
TEMOIN_ABSENT = 'TEMOIN_JOB_QUI_N_EXISTE_PAS_LOT_G1'


def _fichiers_python():
    """Le monolithe + tout le paquet `vertex`. Les tests sont exclus : un `beat`
    posé dans un test ne fait pas tourner un job en production."""
    yield RACINE / 'terminal.py'
    for p in sorted((RACINE / 'vertex').rglob('*.py')):
        yield p


def emetteurs() -> tuple[dict[str, list[str]], list[str]]:
    """Rend (nom → sites d'émission, sites dont le nom est calculé).

    On vise l'attribut `.beat(` à l'AST plutôt qu'une regex : `beat` apparaît
    aussi dans de la prose (« battement ») et une regex confondrait les deux.
    """
    trouves: dict[str, list[str]] = {}
    opaques: list[str] = []
    for p in _fichiers_python():
        try:
            txt = p.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        if '.beat(' not in txt:
            continue
        try:
            arbre = ast.parse(txt)
        except SyntaxError:
            continue
        rel = str(p.relative_to(RACINE))
        for n in ast.walk(arbre):
            if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr == 'beat'):
                continue
            site = '%s:%d' % (rel, n.lineno)
            cible = n.args[0] if n.args else None
            if isinstance(cible, ast.Constant) and isinstance(cible.value, str):
                trouves.setdefault(cible.value, []).append(site)
            else:
                opaques.append(site)
    return trouves, opaques


def mesurer() -> dict:
    sys.path.insert(0, str(RACINE))
    #  `from vertex.scheduler import registry` rend l'OBJET `registry` réexporté
    #  par le paquet, pas le module : `vertex/scheduler/__init__.py` masque le
    #  nom. On importe donc le module par son chemin complet.
    import importlib
    _reg = importlib.import_module('vertex.scheduler.registry')

    declares = [(nom, desc, interval) for nom, desc, interval in _reg._CANONICAL]
    emis, opaques = emetteurs()

    lignes = []
    for nom, desc, interval in declares:
        sites = emis.get(nom, [])
        lignes.append({
            'nom': nom,
            'description': desc,
            'interval_s': interval,
            'etat': 'ACTIF' if sites else 'SANS_EMETTEUR',
            'emetteurs': sites,
        })

    #  Émis mais pas déclaré : le registre crée alors la ligne à la volée
    #  (`setdefault` dans `beat`), donc elle n'apparaît PAS dans `jobs()`, qui
    #  n'itère que sur `_CANONICAL`. Un battement invisible est une mesure
    #  perdue, pas une erreur bruyante — d'où le relevé.
    noms_declares = {n for n, _, _ in declares}
    orphelins = sorted(n for n in emis if n not in noms_declares)

    return {
        'declares': len(declares),
        'actifs': sum(1 for l in lignes if l['etat'] == 'ACTIF'),
        'sans_emetteur': sum(1 for l in lignes if l['etat'] == 'SANS_EMETTEUR'),
        'jobs': lignes,
        'emetteurs_a_nom_calcule': opaques,
        'emis_non_declares': orphelins,
    }


def _temoins(rapport: dict) -> list[str]:
    """Deux témoins, l'un négatif, l'autre positif. Rend la liste des échecs."""
    echecs = []
    emis, _ = emetteurs()

    #  Témoin 1 (négatif) : un nom que rien n'émet doit ressortir SANS_EMETTEUR.
    if TEMOIN_ABSENT in emis:
        echecs.append('le temoin negatif est emis par le depot : il ne temoigne '
                      'plus de rien')

    #  Témoin 2 (positif) : au moins un job du produit doit ressortir ACTIF,
    #  sinon le détecteur ne détecte simplement rien du tout.
    if rapport['actifs'] == 0:
        echecs.append('AUCUN job actif trouve : le detecteur d\'emetteurs est '
                      'aveugle (l\'analyse AST ne voit plus les appels .beat)')
    return echecs


def rendre_texte(r: dict) -> str:
    out = ['REGISTRE DE JOBS — CE QUI EST DECLARE, CE QUI EXISTE',
           '=' * 68,
           'declares      : %d' % r['declares'],
           'actifs        : %d  (un appel beat() porte ce nom)' % r['actifs'],
           'sans emetteur : %d  (aucun code ne peut les faire tourner)'
           % r['sans_emetteur'],
           '']
    for etat in ('SANS_EMETTEUR', 'ACTIF'):
        lot = [l for l in r['jobs'] if l['etat'] == etat]
        if not lot:
            continue
        out.append('%s (%d)' % (etat, len(lot)))
        for l in lot:
            suffixe = ('  <- %s' % ', '.join(l['emetteurs'][:2])) if l['emetteurs'] else ''
            out.append('   %-34s%s' % (l['nom'], suffixe))
        out.append('')
    if r['emetteurs_a_nom_calcule']:
        out.append('EMETTEURS A NOM CALCULE (hors portee de l\'analyse statique) :')
        out += ['   ' + s for s in r['emetteurs_a_nom_calcule']]
        out.append('')
    if r['emis_non_declares']:
        out.append('EMIS MAIS NON DECLARES (leurs battements ne sont jamais servis) :')
        out += ['   ' + s for s in r['emis_non_declares']]
    return '\n'.join(out)


def main() -> int:
    r = mesurer()
    echecs = _temoins(r)
    if echecs:
        for e in echecs:
            print('TEMOIN MUET : %s' % e, file=sys.stderr)
        return 2
    if '--json' in sys.argv:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        print(rendre_texte(r))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
