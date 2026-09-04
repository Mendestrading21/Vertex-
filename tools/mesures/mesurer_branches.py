#!/usr/bin/env python3
"""Vertex Test 1.0 · #782 — 697 BRANCHES : LESQUELLES PEUT-ON PERDRE SANS RIEN PERDRE ?

`CLEANUP_POLICY.md` interdit toute suppression sans **preuve de non-usage**.
Cet outil produit cette preuve, branche par branche, et **ne supprime rien**.

## Les quatre classes, et ce que chacune prouve

| classe | critère mesuré | ce qu'on peut en conclure |
| --- | --- | --- |
| `FUSIONNEE` | tous ses commits sont des ancêtres de `main` | suppression **prouvée sans perte** |
| `CONTENU_IDENTIQUE` | commits inédits, mais `git diff main..branche` est **vide** | le travail est dans `main`, l'historique seul diffère |
| `UNIQUE` | commits inédits **et** un diff non vide | contient du travail que `main` n'a pas |
| `INACCESSIBLE` | la référence ne se résout pas | anomalie à signaler, jamais à supprimer en silence |

La distinction qui compte est celle entre les deux premières et la troisième :
**« pas fusionnée » ne veut pas dire « contient du travail »**. Une branche
rebasée, cherry-pickée ou refaite garde des commits inédits alors que son
contenu est déjà dans `main` — la supprimer ne perd rien, et la garder par
prudence entretient un dépôt que plus personne ne sait lire.

## Ce que l'outil NE dit pas

Il ne dit pas si une branche `UNIQUE` **mérite** d'être gardée : un travail
inédit peut être abandonné, remplacé par mieux, ou faux. Cette lecture-là
demande un humain, et c'est exactement le partage que `CLEANUP_POLICY.md`
prévoit.

Il ne dit rien non plus des branches locales : seules les références distantes
sont mesurées, parce que ce sont elles qui persistent.

## Les témoins

1. **positif** — `main` comparée à elle-même doit ressortir `FUSIONNEE` et sans
   diff : si ce n'est pas le cas, la comparaison ne compare rien ;
2. **négatif** — une référence fabriquée doit ressortir `INACCESSIBLE`, jamais
   fusionnée par défaut. Une classification qui range l'inconnu du côté
   rassurant est plus dangereuse que pas de classification du tout.

Usage :
    python tools/mesures/mesurer_branches.py [--json] [--base origin/main]
Sorties : 0 = mesuré, 2 = témoin muet.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]

BASE_DEFAUT = 'origin/main'
TEMOIN_ABSENT = 'origin/branche-temoin-qui-n-existe-pas-vertex-1-0'


def _git(*args, defaut=None):
    r = subprocess.run(['git', *args], cwd=RACINE, capture_output=True, text=True)
    if r.returncode != 0:
        return defaut
    return r.stdout.strip()


def _distantes():
    sortie = _git('for-each-ref', '--format=%(refname:short)', 'refs/remotes/origin',
                  defaut='') or ''
    return [b for b in sortie.splitlines()
            if b and not b.endswith('/HEAD') and b != 'origin/HEAD']


def _fusionnees(base):
    """Les branches dont TOUS les commits sont des ancêtres de la base.

    Une seule commande git pour les 697 : le faire branche par branche coûterait
    une minute et donnerait le même résultat."""
    sortie = _git('branch', '-r', '--merged', base, '--format=%(refname:short)',
                  defaut='') or ''
    return {b.strip() for b in sortie.splitlines() if b.strip()}


def classer(branche: str, base: str, deja_fusionnees: set) -> dict:
    if _git('rev-parse', '--verify', '--quiet', branche + '^{commit}') is None:
        return {'branche': branche, 'classe': 'INACCESSIBLE',
                'commits_inedits': None, 'diff_vide': None}
    if branche in deja_fusionnees:
        return {'branche': branche, 'classe': 'FUSIONNEE',
                'commits_inedits': 0, 'diff_vide': True}
    inedits = _git('rev-list', '--count', '%s..%s' % (base, branche), defaut='0')
    #  Diff de CONTENU entre la base et la branche : vide ⇒ le travail est déjà
    #  dans `main`, seule l'histoire diffère.
    vide = subprocess.run(['git', 'diff', '--quiet', base, branche],
                          cwd=RACINE, capture_output=True).returncode == 0
    return {'branche': branche,
            'classe': 'CONTENU_IDENTIQUE' if vide else 'UNIQUE',
            'commits_inedits': int(inedits or 0), 'diff_vide': vide}


def _contenues_ailleurs(branches):
    """Les branches dont la pointe est un ancêtre d'une AUTRE branche.

    Sans cette mesure, le chiffre « 665 uniques » est vrai et inutile : la série
    Skyler V2 est une **chaîne linéaire** — `lot-120` contient `lot-119`, qui
    contient `lot-118`, et ainsi de suite. Chaque maillon a des commits inédits
    par rapport à `main`, donc chacun ressort « UNIQUE », alors qu'un seul —
    la pointe — porte réellement l'ensemble du travail.

    Supprimer un maillon intermédiaire ne perd rien **tant que sa descendante
    existe**. C'est ce que cette classe dit, et rien de plus : elle ne juge pas
    si le travail vaut d'être gardé.
    """
    contenues = {}
    for b in branches:
        sortie = _git('branch', '-r', '--contains', b, '--format=%(refname:short)',
                      defaut='') or ''
        autres = {x.strip() for x in sortie.splitlines()
                  if x.strip() and x.strip() != b and not x.endswith('/HEAD')}
        if autres:
            contenues[b] = sorted(autres)[:3]
    return contenues


def _jumelles(branches):
    """Groupes de branches dont l'ARBRE est identique au bit près.

    Deux histoires différentes peuvent porter exactement le même contenu — une
    branche recréée, un rebase, une intégration. Dans ce cas, toutes sauf une
    sont redondantes quel que soit leur historique.

    Un seul `git cat-file --batch-check` pour les 697 : demander l'arbre branche
    par branche coûterait autant que tout le reste de la mesure.
    """
    demandes = '\n'.join('%s^{tree}' % b for b in branches)
    r = subprocess.run(['git', 'cat-file', '--batch-check=%(objectname)'],
                       cwd=RACINE, input=demandes, capture_output=True, text=True)
    arbres = r.stdout.split()
    if len(arbres) != len(branches):
        return {}
    par_arbre = {}
    for b, a in zip(branches, arbres):
        par_arbre.setdefault(a, []).append(b)
    return {a: sorted(v) for a, v in par_arbre.items() if len(v) > 1}


def mesurer(base: str = BASE_DEFAUT, *, confinement: bool = True) -> dict:
    """`confinement=False` saute la recherche des maillons de chaîne.

    Cette passe coûte un `git branch --contains` par branche non fusionnée —
    614 appels, ~70 s. C'est acceptable pour un rapport lancé à la main, pas
    pour un gardien qui tourne à chaque suite : un test lent finit par être
    désactivé, et un gardien désactivé ne garde rien.
    """
    branches = _distantes()
    fusionnees = _fusionnees(base)
    lignes = [classer(b, base, fusionnees) for b in branches]
    #  Une branche « UNIQUE » entierement contenue dans une autre est un maillon
    #  de chaine, pas un travail distinct.
    uniques = [l['branche'] for l in lignes if l['classe'] == 'UNIQUE']
    contenues = _contenues_ailleurs(uniques) if confinement else {}
    for l in lignes:
        if l['classe'] == 'UNIQUE' and l['branche'] in contenues:
            l['classe'] = 'CONTENUE_AILLEURS'
            l['contenue_dans'] = contenues[l['branche']]
    jumelles = _jumelles(branches)
    par_classe = {}
    for l in lignes:
        par_classe.setdefault(l['classe'], []).append(l['branche'])
    return {
        'base': base,
        'arbres_distincts': len(branches) - sum(len(v) - 1 for v in jumelles.values()),
        'groupes_jumeaux': [v for v in jumelles.values()],
        'total': len(lignes),
        'par_classe': {k: len(v) for k, v in sorted(par_classe.items())},
        'supprimables_sans_perte': sorted(
            par_classe.get('FUSIONNEE', []) + par_classe.get('CONTENU_IDENTIQUE', [])),
        'contenues_ailleurs': len(par_classe.get('CONTENUE_AILLEURS', [])),
        'pointes': sorted(par_classe.get('UNIQUE', [])),
        'uniques': sorted(par_classe.get('UNIQUE', [])),
        'inaccessibles': sorted(par_classe.get('INACCESSIBLE', [])),
        'branches': lignes,
    }


def _temoins(r: dict) -> list:
    echecs = []
    base = r['base']
    #  Témoin positif : la base comparée à elle-même.
    soi = classer(base, base, _fusionnees(base))
    if soi['classe'] != 'FUSIONNEE':
        echecs.append(
            'TEMOIN POSITIF MUET : « %s » comparee a elle-meme ressort « %s » — '
            'la comparaison ne compare rien' % (base, soi['classe']))
    #  Témoin négatif : une référence fabriquée ne doit JAMAIS passer pour
    #  fusionnée. Ranger l'inconnu du cote rassurant serait pire que rien.
    fantome = classer(TEMOIN_ABSENT, base, _fusionnees(base))
    if fantome['classe'] != 'INACCESSIBLE':
        echecs.append(
            'TEMOIN NEGATIF ROMPU : une reference inexistante est classee '
            '« %s » — l\'inconnu est range du cote rassurant' % fantome['classe'])
    if not r['total']:
        echecs.append('aucune branche distante trouvee : la mesure porte sur rien')
    return echecs


def rendre_texte(r: dict) -> str:
    out = ['BRANCHES DISTANTES — CE QU\'ON PEUT PERDRE SANS RIEN PERDRE',
           '=' * 64,
           'base    : %s' % r['base'],
           'total   : %d branches distantes' % r['total'],
           '']
    etiquettes = {
        'FUSIONNEE': 'tous les commits sont dans la base — perte NULLE prouvee',
        'CONTENU_IDENTIQUE': 'commits inedits mais diff VIDE — le travail est dans la base',
        'CONTENUE_AILLEURS': 'maillon de chaine : une AUTRE branche la contient entierement',
        'UNIQUE': 'contient du travail que la base n\'a pas',
        'INACCESSIBLE': 'reference non resolue — a signaler, jamais a supprimer',
    }
    for classe, n in r['par_classe'].items():
        out.append('%-18s %4d   %s' % (classe, n, etiquettes.get(classe, '')))
    out.append('')
    out.append('SUPPRIMABLES SANS PERTE      : %d' % len(r['supprimables_sans_perte']))
    out.append('MAILLONS (contenus ailleurs) : %d' % r['contenues_ailleurs'])
    out.append('POINTES A EXAMINER           : %d' % len(r['uniques']))
    out.append('')
    for b in r['uniques'][:40]:
        d = next(x for x in r['branches'] if x['branche'] == b)
        out.append('   %-58s %4d commits inedits' % (b, d['commits_inedits']))
    if len(r['uniques']) > 40:
        out.append('   … et %d autres' % (len(r['uniques']) - 40))
    out.append('')
    out.append('ARBRES DISTINCTS : %d sur %d branches' % (r['arbres_distincts'], r['total']))
    if r['groupes_jumeaux']:
        out.append('   groupes au contenu IDENTIQUE au bit pres :')
        for g in r['groupes_jumeaux']:
            out.append('     %s' % ' = '.join(g))
    out.append('')
    out.append('RAPPEL : cet outil NE SUPPRIME RIEN. « UNIQUE » ne veut pas dire')
    out.append('« a garder » — un travail inedit peut etre abandonne ou faux.')
    out.append('Cette lecture-la demande un humain (CLEANUP_POLICY.md).')
    return '\n'.join(out)


def main() -> int:
    base = BASE_DEFAUT
    if '--base' in sys.argv:
        base = sys.argv[sys.argv.index('--base') + 1]
    r = mesurer(base)
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
