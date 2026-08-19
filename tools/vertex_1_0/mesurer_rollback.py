#!/usr/bin/env python3
"""Vertex 1.0 · G6 — REVENIR EN ARRIÈRE EST-IL POSSIBLE SANS RIEN PERDRE ?

Le rapport d'exploitation annonçait « rollback applicatif non testé : revenir à
un SHA antérieur et démarrer demanderait un second arbre de travail ». C'était
une renonciation, pas un constat : `git worktree` fait exactement cela, et la
place disque ne manque pas. Cet outil lève donc le résidu.

## La question n'est pas « est-ce que ça redémarre »

Un rollback qui démarre mais qui perd le bureau de l'utilisateur n'est pas un
rollback — c'est une panne différente. Deux choses sont donc mesurées, et la
seconde est la vraie :

1. **la version antérieure démarre-t-elle ?** (`/healthz`, puis une page servie
   pour de bon, pas seulement une sonde de vie) ;
2. **lit-elle les données écrites par la version récente, à l'identique ?**
   Le format du bureau a-t-il divergé au point qu'un retour arrière rende un
   bureau vide, tronqué, ou pire : partiellement lu, donc faux.

Le point 2 se moque des tests unitaires : il ne se voit qu'en faisant tourner
DEUX versions sur les MÊMES octets.

## Comment la fidélité est obtenue

`persist.cache_path` ancre les fichiers à la racine du dépôt. Un `worktree` a sa
propre racine, alors qu'un vrai rollback (`git checkout <sha>` sur place) garde
la même. On recopie donc `desk_data.json` dans l'arbre antérieur : sans cela on
mesurerait un démarrage à vide, ce qui répondrait « oui » à une question qu'on
n'a pas posée.

## Le témoin

Un comparateur qui trouve tout identique ne prouve rien tant qu'une différence
fabriquée ne le fait pas parler. `comparer_bureaux` est pur et éprouvé dans les
deux sens.

Usage :
    python tools/vertex_1_0/mesurer_rollback.py [--sha SHA] [--json]
Sorties : 0 = mesuré, 2 = témoin muet, 3 = rollback en échec.
"""
from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

RACINE = pathlib.Path(__file__).resolve().parents[2]
PORT_ANCIEN = 5103
FICHIER_BUREAU = 'desk_data.json'


def _git(*a: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.run(('git',) + a, cwd=str(cwd or RACINE), text=True,
                          capture_output=True, check=True).stdout.strip()


def sha_anterieur() -> str:
    """Par défaut : la base commune avec `main` — le point de retour réel,
    celui vers lequel un incident ferait revenir."""
    return _git('merge-base', 'HEAD', 'origin/main')


def comparer_bureaux(neuf: dict, apres_retour: dict) -> dict:
    """Compare deux blobs de bureau. Fonction PURE : les témoins passent par
    elle, sinon ils éprouveraient une copie.

    Les trois façons de perdre, nommées séparément parce qu'elles ne se
    réparent pas de la même manière :

    - ``absentes``  : la clé a disparu — perte franche, visible ;
    - ``differentes``: la clé est là, son contenu a changé — perte SILENCIEUSE,
      la plus dangereuse : l'écran affiche quelque chose, donc rien n'alerte ;
    - ``ajoutees``  : la version antérieure invente une clé que la neuve
      n'avait pas. Bénin le plus souvent, mais c'est ainsi qu'un défaut de
      format se signale d'abord.
    """
    a = (neuf or {}).get('data') or {}
    b = (apres_retour or {}).get('data') or {}
    absentes = sorted(set(a) - set(b))
    ajoutees = sorted(set(b) - set(a))
    differentes = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    return {'absentes': absentes, 'ajoutees': ajoutees,
            'differentes': differentes, 'cles_neuf': len(a),
            'cles_apres': len(b),
            'identique': not (absentes or ajoutees or differentes)}


def _temoins() -> list:
    e = []
    base = {'data': {'myTrades': '[1]', 'myFavs': '["AAPL"]'}}
    if not comparer_bureaux(base, base)['identique']:
        e.append('TEMOIN NEGATIF ROMPU : deux bureaux identiques ressortent '
                 'differents — la mesure crierait au loup partout')
    perdu = {'data': {'myTrades': '[1]'}}
    r = comparer_bureaux(base, perdu)
    if r['identique'] or r['absentes'] != ['myFavs']:
        e.append('TEMOIN MUET (perte franche) : une cle disparue n\'est pas vue')
    altere = {'data': {'myTrades': '[]', 'myFavs': '["AAPL"]'}}
    r = comparer_bureaux(base, altere)
    if r['identique'] or r['differentes'] != ['myTrades']:
        e.append('TEMOIN MUET (perte silencieuse) : un contenu change n\'est '
                 'pas vu — c\'est pourtant la perte la plus dangereuse, celle '
                 'qui laisse un ecran plausible')
    return e


def _http(url: str, timeout: float = 10.0):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.status, r.read()


def _attendre(url: str, secondes: int = 45) -> bool:
    for _ in range(secondes * 2):
        try:
            if _http(url, timeout=3)[0] == 200:
                return True
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(0.5)
    return False


def mesurer(sha: str | None = None, *, temoins: bool = True) -> dict:
    echecs = _temoins() if temoins else []
    sha = sha or sha_anterieur()
    arbre = pathlib.Path('/tmp/vertex-rollback-%s' % sha[:8])
    r: dict = {'sha_anterieur': sha, 'sha_courant': _git('rev-parse', 'HEAD'),
               'echecs_temoins': echecs, 'arbre': str(arbre)}

    #  Le bureau tel que la version RECENTE l'a ecrit. C'est lui qu'on emporte.
    source = RACINE / FICHIER_BUREAU
    r['bureau_present'] = source.exists()
    neuf = json.loads(source.read_text(encoding='utf-8')) if source.exists() else {}

    if arbre.exists():
        subprocess.run(('git', 'worktree', 'remove', '--force', str(arbre)),
                       cwd=str(RACINE), capture_output=True)
    _git('worktree', 'add', '--detach', str(arbre), sha)
    proc = None
    try:
        if source.exists():
            shutil.copy2(source, arbre / FICHIER_BUREAU)

        #  `PORT` et pas autre chose : c'est la variable que le produit lit
        #  (`os.environ.get('PORT', 5002)`), des deux cotes du rollback. Le
        #  premier essai passait `VERTEX_PORT`, que RIEN ne lit — la version
        #  anterieure s'est donc liee au 5002 deja pris et n'a pas demarre.
        #  L'instrument accusait le produit d'un defaut qui etait le sien.
        env = dict(os.environ, DEMO='1', NO_IBKR='1', PORT=str(PORT_ANCIEN))
        env.pop('VERTEX_CODE', None)
        journal = open('/tmp/vertex-rollback-%s.log' % sha[:8], 'w')
        proc = subprocess.Popen((sys.executable, '-m', 'vertex'), cwd=str(arbre),
                                env=env, stdout=journal, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, start_new_session=True)
        base = 'http://127.0.0.1:%d' % PORT_ANCIEN
        r['demarre'] = _attendre(base + '/healthz')

        #  Une sonde de vie ne prouve pas qu'une PAGE est servie : on demande
        #  l'accueil, c'est-a-dire tout le chemin de rendu.
        r['accueil'] = None
        r['octets_accueil'] = 0
        if r['demarre']:
            try:
                code, corps = _http(base + '/', timeout=30)
                r['accueil'] = code
                r['octets_accueil'] = len(corps)
            except Exception as e:                       # noqa: BLE001
                r['accueil_erreur'] = str(e)[:160]

        r['bureau'] = None
        if r['demarre']:
            try:
                _, corps = _http(base + '/api/desk', timeout=20)
                r['bureau'] = comparer_bureaux(neuf, json.loads(corps))
            except Exception as e:                       # noqa: BLE001
                r['bureau_erreur'] = str(e)[:160]
    finally:
        if proc is not None:
            try:
                os.killpg(os.getpgid(proc.pid), 15)
            except Exception:                            # noqa: BLE001
                proc.kill()
            proc.wait(timeout=20)
        subprocess.run(('git', 'worktree', 'remove', '--force', str(arbre)),
                       cwd=str(RACINE), capture_output=True)
    return r


def rendre_texte(r: dict) -> str:
    b = r.get('bureau') or {}
    o = ['REVENIR EN ARRIERE EST-IL POSSIBLE SANS RIEN PERDRE ?', '=' * 62,
         'version courante  : %s' % r['sha_courant'][:12],
         'retour vers       : %s' % r['sha_anterieur'][:12], '',
         '1. la version anterieure DEMARRE      : %s'
         % ('oui' if r.get('demarre') else 'NON'),
         '2. elle SERT la page d\'accueil        : %s (%d octets)'
         % (r.get('accueil') or '—', r.get('octets_accueil') or 0),
         '3. elle relit le bureau ECRIT PAR LA VERSION RECENTE :']
    if not r.get('bureau_present'):
        o.append('     aucun bureau sur disque — RIEN N\'A ETE EPROUVE ici')
    elif not b:
        o.append('     non mesure (%s)' % r.get('bureau_erreur', 'serveur muet'))
    else:
        o.append('     %d cles ecrites -> %d cles relues'
                 % (b['cles_neuf'], b['cles_apres']))
        o.append('     identique : %s' % ('OUI' if b['identique'] else 'NON'))
        for nom, cles in (('DISPARUES', b['absentes']),
                          ('MODIFIEES (perte silencieuse)', b['differentes']),
                          ('inventees', b['ajoutees'])):
            if cles:
                o.append('     %s : %s' % (nom, ', '.join(cles)))
    o.append('')
    o.append('LECTURE : un rollback qui demarre mais rend un bureau vide n\'est')
    o.append('pas un rollback. C\'est le point 3 qui repond, pas le point 1.')
    return '\n'.join(o)


def main() -> int:
    sha = None
    if '--sha' in sys.argv:
        sha = sys.argv[sys.argv.index('--sha') + 1]
    r = mesurer(sha)
    if r['echecs_temoins']:
        for x in r['echecs_temoins']:
            print(x, file=sys.stderr)
        return 2
    print(json.dumps(r, indent=2, ensure_ascii=False) if '--json' in sys.argv
          else rendre_texte(r))
    b = r.get('bureau') or {}
    if not r.get('demarre') or r.get('accueil') != 200:
        return 3
    if r.get('bureau_present') and not b.get('identique'):
        return 3
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
