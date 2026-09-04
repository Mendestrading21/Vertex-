"""Vertex Test 1.0 · #783 — CARTE DES DOMAINES DUPLIQUÉS.

Premier livrable de #783 : *« carte des modèles, imports, endpoints et
consommateurs »* pour les trois familles que `ARCHITECTURE.md` déclare en
recouvrement :

- `company` / `companies` ;
- `data` / `data_sources` ;
- `portfolio` / `positions` / `tracking`.

## Pourquoi mesurer avant de converger

`CLEANUP_POLICY.md` conditionne toute suppression à un inventaire des
consommateurs. Et l'expérience de ce dépôt est nette : **un nom qui paraît
ancien n'est pas une preuve d'obsolescence**. Deux paquets au nom voisin peuvent
être deux responsabilités distinctes correctement séparées — auquel cas les
« converger » détruirait de l'information.

L'outil ne propose donc **aucune fusion**. Il rend trois chiffres par paquet, et
c'est le rapport de force entre eux qui informe la décision :

| mesure | ce qu'elle dit |
| --- | --- |
| **consommateurs** | combien de modules importent ce paquet — sa surface réelle |
| **symboles publics** | ce qu'il expose — l'ampleur du contrat à préserver |
| **recouvrement** | les symboles portant le MÊME nom dans les deux paquets |

Le recouvrement est la seule mesure qui distingue un **doublon** d'une
**séparation légitime** : deux paquets sans un seul nom commun ne se recouvrent
pas, quoi que leurs noms suggèrent.

## Anti-vacuité

`--temoin` déclare une paire fabriquée dont on sait qu'elle n'existe pas et
exige que l'outil rende zéro consommateur — puis une paire réelle et exige
l'inverse. Un inventaire qui rend « 0 partout » parce qu'il ne sait pas lire
ressemble à un dépôt parfaitement rangé.

Usage : python tools/mesures/inventaire_domaines.py [--temoin] [--md CHEMIN]
"""
import argparse
import ast
import os
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#: Les familles déclarées en recouvrement par `ARCHITECTURE.md`. La liste est
#: recopiée du document, pas devinée — si le document change, ceci doit suivre.
FAMILLES = (
    ('entreprise', ('company', 'companies')),
    ('donnees', ('data', 'data_sources')),
    ('portefeuille', ('portfolio', 'positions', 'tracking')),
)


def _sha():
    try:
        return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=RACINE,
                              capture_output=True, text=True).stdout.strip()[:12]
    except Exception:
        return 'inconnu'


def _fichiers_python():
    out = []
    for base, dirs, noms in os.walk(RACINE):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
        for n in sorted(noms):
            if n.endswith('.py'):
                out.append(os.path.join(base, n))
    return sorted(out)


def _paquet_de(chemin):
    rel = os.path.relpath(chemin, RACINE)
    bouts = rel.split(os.sep)
    return bouts[1] if len(bouts) > 2 and bouts[0] == 'vertex' else None


def _symboles(paquet):
    """Les symboles publics d'un paquet — noms de haut niveau, hors privés."""
    rep = os.path.join(RACINE, 'vertex', paquet)
    if not os.path.isdir(rep):
        return {}
    out = {}
    for base, dirs, noms in os.walk(rep):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for n in sorted(noms):
            if not n.endswith('.py'):
                continue
            chemin = os.path.join(base, n)
            try:
                with open(chemin, encoding='utf-8') as f:
                    arbre = ast.parse(f.read())
            except (OSError, SyntaxError, UnicodeDecodeError):
                continue
            for noeud in arbre.body:
                nom = None
                if isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    nom = noeud.name
                elif isinstance(noeud, ast.Assign):
                    for c in noeud.targets:
                        if isinstance(c, ast.Name) and c.id.isupper():
                            out.setdefault(c.id, []).append(os.path.relpath(chemin, RACINE))
                    continue
                if nom and not nom.startswith('_'):
                    out.setdefault(nom, []).append(os.path.relpath(chemin, RACINE))
    return out


def _consommateurs(paquet):
    """Les modules qui IMPORTENT ce paquet — hors le paquet lui-même.

    On lit les imports à l'AST : un `grep` compterait les mentions en
    commentaire et les chaînes, ce qui gonflerait la surface d'un paquet qu'on
    envisage justement de retirer."""
    cible = 'vertex.%s' % paquet
    out = set()
    for chemin in _fichiers_python():
        if _paquet_de(chemin) == paquet:
            continue
        try:
            with open(chemin, encoding='utf-8') as f:
                arbre = ast.parse(f.read())
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        touche = False
        for noeud in ast.walk(arbre):
            if isinstance(noeud, ast.Import):
                touche |= any(a.name == cible or a.name.startswith(cible + '.')
                              for a in noeud.names)
            elif isinstance(noeud, ast.ImportFrom):
                m = noeud.module or ''
                touche |= (m == cible or m.startswith(cible + '.'))
        if touche:
            out.add(os.path.relpath(chemin, RACINE))
    return sorted(out)


_FICHIER_DONNEES = __import__('re').compile(
    r"([A-Za-z0-9_./-]+\.(?:json|jsonl|csv|db|sqlite3?))")


def _fichiers_possedes(paquet):
    """Les fichiers de données que le paquet cite — SECOND AXE de duplication.

    Le recouvrement de noms de symboles ne dit pas tout : deux paquets peuvent
    exposer des noms différents et se disputer le même fichier sur disque. C'est
    la forme de doublon la plus dangereuse, parce qu'elle produit des écritures
    concurrentes plutôt qu'une simple confusion de lecture."""
    rep = os.path.join(RACINE, 'vertex', paquet)
    if not os.path.isdir(rep):
        return []
    out = set()
    for base, dirs, noms in os.walk(rep):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for n in noms:
            if not n.endswith('.py'):
                continue
            try:
                with open(os.path.join(base, n), encoding='utf-8') as f:
                    t = f.read()
            except (OSError, UnicodeDecodeError):
                continue
            out.update(_FICHIER_DONNEES.findall(t))
    return sorted(out)


def inventorier():
    familles = []
    for nom, paquets in FAMILLES:
        entrees = []
        for p in paquets:
            syms = _symboles(p)
            entrees.append({
                'paquet': p,
                'existe': os.path.isdir(os.path.join(RACINE, 'vertex', p)),
                'symboles': sorted(syms),
                'consommateurs': _consommateurs(p),
                'fichiers': _fichiers_possedes(p),
            })
        #  RECOUVREMENT : les symboles portant le MEME nom dans deux paquets.
        #  C'est la seule mesure qui distingue un doublon d'une separation
        #  legitime — deux paquets sans un seul nom commun ne se recouvrent pas.
        recouvrement = {}
        for i, a in enumerate(entrees):
            for b in entrees[i + 1:]:
                communs = sorted(set(a['symboles']) & set(b['symboles']))
                if communs:
                    recouvrement['%s ∩ %s' % (a['paquet'], b['paquet'])] = communs
        #  DISPUTE DE FICHIER : deux paquets qui citent le meme fichier de
        #  donnees. C'est la duplication qui fait perdre des ecritures.
        dispute = {}
        for i, a in enumerate(entrees):
            for b in entrees[i + 1:]:
                communs = sorted(set(a['fichiers']) & set(b['fichiers']))
                if communs:
                    dispute['%s ∩ %s' % (a['paquet'], b['paquet'])] = communs
        familles.append({'famille': nom, 'paquets': entrees,
                         'recouvrement': recouvrement, 'dispute_fichiers': dispute})
    return {'sha': _sha(), 'familles': familles}


def _rendre(inv):
    l = []
    a = l.append
    a('# Vertex Test 1.0 · #783 — Carte des domaines dupliqués')
    a('')
    a('SHA : `%s` · généré par `tools/mesures/inventaire_domaines.py`' % inv['sha'])
    a('')
    a('> Régénéré, jamais édité à la main. **Aucune fusion n\'est proposée ici** :')
    a('> un nom qui paraît ancien n\'est pas une preuve d\'obsolescence, et deux')
    a('> paquets au nom voisin peuvent être deux responsabilités correctement')
    a('> séparées. Ce sont les chiffres qui informent la décision.')
    a('')
    for fam in inv['familles']:
        a('## Famille « %s »' % fam['famille'])
        a('')
        a('| paquet | existe | symboles publics | consommateurs | fichiers possédés |')
        a('| --- | --- | --- | --- | --- |')
        for p in fam['paquets']:
            a('| `vertex/%s` | %s | %d | **%d** | %s |'
              % (p['paquet'], 'oui' if p['existe'] else 'NON',
                 len(p['symboles']), len(p['consommateurs']),
                 ', '.join('`%s`' % f for f in p['fichiers']) or '—'))
        a('')
        if fam['dispute_fichiers']:
            a('**⚠ Dispute de fichier** — deux paquets écrivent la même donnée :')
            a('')
            for paire, communs in sorted(fam['dispute_fichiers'].items()):
                a('- `%s` : %s' % (paire, ', '.join('`%s`' % c for c in communs)))
            a('')
        else:
            a('**Aucune dispute de fichier** : chaque paquet possède les siens.')
            a('')
        if fam['recouvrement']:
            a('**Recouvrement de noms** — c\'est ici que se joue la question du doublon :')
            a('')
            for paire, communs in sorted(fam['recouvrement'].items()):
                a('- `%s` : %d symbole(s) — %s'
                  % (paire, len(communs), ', '.join('`%s`' % c for c in communs[:12])))
            a('')
        else:
            a('**Aucun symbole commun.** Malgré des noms voisins, ces paquets')
            a('n\'exposent pas la même chose : les « converger » sans autre preuve')
            a('détruirait une séparation qui tient peut-être debout.')
            a('')
    return '\n'.join(l)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--temoin', action='store_true')
    p.add_argument('--md')
    args = p.parse_args(argv)

    if args.temoin:
        faux = _consommateurs('paquet_qui_nexiste_pas_temoin')
        vrai = _consommateurs('engines')
        ok_faux, ok_vrai = (faux == []), (len(vrai) > 0)
        print('TEMOIN paquet inexistant : %s'
              % ('0 consommateur — correct' if ok_faux else '*** %d trouves ***' % len(faux)))
        print('TEMOIN paquet reel       : %s'
              % ('%d consommateurs — le detecteur mord' % len(vrai) if ok_vrai
                 else '*** 0 trouve : AVEUGLE ***'))
        return 0 if (ok_faux and ok_vrai) else 2

    inv = inventorier()
    md = _rendre(inv)
    if args.md:
        with open(args.md, 'w', encoding='utf-8') as f:
            f.write(md + '\n')
        print('MD -> %s' % args.md)
    else:
        print(md)
    return 0


if __name__ == '__main__':
    sys.exit(main())
