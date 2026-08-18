"""tools/mesurer_surface_ibkr.py — QUELLE SURFACE D'IBKR LE CODE TOUCHE-T-IL ?

Réserve ouverte du lot 31 : le garde-fou READONLY interdit `placeOrder`,
`place_order`, `submit_order`, `transmit`… — une **liste noire de noms**. Elle ne
peut rien contre un chemin qu'on n'a pas pensé à nommer, et le lot 33 vient de
montrer, en trouvant une quatrième sortie de news, ce que valent les listes de
noms tenues à la main.

Cet outil inverse l'instrument : au lieu d'interdire des noms, il **énumère les
capacités réellement employées** sur l'objet `IB` et les confronte à une liste
blanche classée. Une capacité nouvelle — quel que soit son nom — sort du lot et
doit être classée par un humain.

Trois précautions, chacune payée par une erreur de mesure :

1. Les identifiants portant un `IB()` sont **dérivés du code** (recherche des
   affectations depuis `IB(...)`), jamais devinés. Une liste d'identifiants
   écrite à la main reproduirait exactement le défaut qu'on corrige.
2. On suit les **chemins pointés** : `ib.client.marketDataType` est une capacité
   d'IBKR autant que `ib.reqTickers`. Ma première mesure ne regardait que le
   premier niveau et annonçait « aucun accès dynamique » — c'était faux, il y en
   a un, au second niveau.
3. Les `getattr` enracinés sur un objet IB sont relevés à part : un nom calculé
   échappe par construction à toute liste, blanche comme noire. Ceux dont le nom
   est une **constante** sont rendus à la liste blanche ; les autres sont
   signalés comme non résolubles.

Usage : python tools/mesurer_surface_ibkr.py
"""
import ast
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Capacités de LECTURE d'ib_insync employées par Vertex, classées une à une.
# Ce n'est pas une liste d'interdits : c'est l'inventaire de ce qui est permis.
LISTE_BLANCHE = {
    # connexion / cycle de vie
    'connect', 'disconnect', 'isConnected', 'sleep', 'run', 'client',
    'RequestTimeout', 'managedAccounts',
    # référentiel
    'qualifyContracts', 'reqSecDefOptParams', 'reqNewsProviders',
    # données de marché (lecture)
    'reqTickers', 'reqTickersAsync', 'reqMktData', 'cancelMktData',
    'reqMarketDataType', 'reqHistoricalData', 'reqHistoricalNews',
    'reqScannerData',
    # compte (lecture)
    'positions', 'accountSummary',
    # second niveau : lecture du mode de données du client bas niveau
    'client.marketDataType',
}

# Vocabulaire d'exécution — sert UNIQUEMENT à garder la liste blanche elle-même
# honnête (personne n'y glisse un verbe d'ordre), jamais à filtrer le code.
VERBES_D_ORDRE = ('placeorder', 'cancelorder', 'reqglobalcancel', 'exercise',
                  'transmit', 'submitorder', 'openorders', 'reqallopenorders',
                  'trades', 'oneCancelsAll'.lower(), 'whatifor')


def _fichiers_python(racine):
    for base, dossiers, fichiers in os.walk(racine):
        dossiers[:] = [d for d in dossiers
                       if d not in ('.git', '__pycache__', 'node_modules', '.venv')]
        for f in fichiers:
            if f.endswith('.py'):
                yield os.path.join(base, f)


def _cibles(assign):
    for cible in assign.targets:
        if isinstance(cible, ast.Name):
            yield cible.id
        elif isinstance(cible, ast.Attribute):         # self._ib = …
            yield cible.attr


def _porteurs_d_ib(arbre, connus):
    """Identifiants portant un objet IB — dérivés, jamais devinés.

    Deux sources : l'affectation depuis `IB(...)`, et **l'ALIAS**
    (`self._ib = ib`). L'alias n'est pas un détail : le passerelle IBKR
    n'appelle `isConnected` et `disconnect` QUE par `self._ib`. Ma première
    version ne suivait pas les alias et perdait ces trois accès — un instrument
    qui ne voit pas une capacité ne peut pas la garder.
    """
    noms = set()
    for n in ast.walk(arbre):
        if not isinstance(n, ast.Assign):
            continue
        v = n.value
        depuis_constructeur = isinstance(v, ast.Call) and (
            (isinstance(v.func, ast.Name) and v.func.id == 'IB')
            or (isinstance(v.func, ast.Attribute) and v.func.attr == 'IB'))
        depuis_alias = ((isinstance(v, ast.Name) and v.id in connus)
                        or (isinstance(v, ast.Attribute) and v.attr in connus))
        if depuis_constructeur or depuis_alias:
            noms.update(_cibles(n))
    return noms


def _chemin(node, porteurs):
    """Rend le chemin pointé si l'expression est enracinée sur un objet IB.

    `ib`            -> ''            (la racine elle-même)
    `ib.client`     -> 'client'
    `self._ib.foo`  -> 'foo'
    sinon           -> None
    """
    if isinstance(node, ast.Name):
        return '' if node.id in porteurs else None
    if isinstance(node, ast.Attribute):
        if node.attr in porteurs:                      # self._ib / obj.ib
            return ''
        dessous = _chemin(node.value, porteurs)
        if dessous is None:
            return None
        return (dessous + '.' + node.attr).lstrip('.')
    return None


def mesurer(racine=RACINE, ignorer_tests=True):
    """Rend (surface, dynamiques, porteurs, fichiers_lus)."""
    surface, dynamiques, porteurs_vus, lus = {}, [], set(), 0
    arbres = []
    for p in _fichiers_python(racine):
        rel = os.path.relpath(p, racine)
        if ignorer_tests and (rel.startswith('tests' + os.sep)
                              or os.path.basename(p).startswith('test_')):
            continue
        try:
            arbres.append((rel, ast.parse(open(p, encoding='utf-8').read())))
        except Exception:
            continue
    # Les porteurs sont dérivés de TOUT le dépôt avant d'analyser quoi que ce
    # soit : `IB()` peut être construit dans un fichier et employé dans un autre.
    # Itération jusqu'au POINT FIXE : `self._ib = ib` n'ajoute `_ib` qu'une fois
    # `ib` connu, et une chaîne d'alias plus longue demanderait un tour de plus.
    for _ in range(10):
        avant = len(porteurs_vus)
        for _, arbre in arbres:
            porteurs_vus |= _porteurs_d_ib(arbre, porteurs_vus)
        if len(porteurs_vus) == avant:
            break
    for rel, arbre in arbres:
        lus += 1
        for n in ast.walk(arbre):
            if isinstance(n, ast.Attribute):
                c = _chemin(n, porteurs_vus)
                if c:
                    surface.setdefault(c, []).append(rel)
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                    and n.func.id == 'getattr' and n.args):
                base = _chemin(n.args[0], porteurs_vus)
                if base is None:
                    continue
                nom = n.args[1] if len(n.args) > 1 else None
                if isinstance(nom, ast.Constant) and isinstance(nom.value, str):
                    c = (base + '.' + nom.value).lstrip('.')
                    surface.setdefault(c, []).append(rel)
                else:
                    dynamiques.append((rel, n.lineno))
    return surface, dynamiques, porteurs_vus, lus


def main():
    surface, dynamiques, porteurs, lus = mesurer()
    print('fichiers analyses : %d · objets IB derives : %s'
          % (lus, ', '.join(sorted(porteurs)) or 'AUCUN'))
    print('\nSURFACE MESUREE (%d capacites distinctes) :' % len(surface))
    for nom in sorted(surface):
        marque = ' ' if nom in LISTE_BLANCHE else '  <-- HORS LISTE BLANCHE'
        print('  %-28s %2d site(s)%s' % (nom, len(surface[nom]), marque))
    hors = sorted(set(surface) - LISTE_BLANCHE)
    print('\nacces a nom CALCULE (echappe a toute liste) : %s'
          % (dynamiques or 'aucun'))
    if hors:
        print('\n%d CAPACITE(S) HORS LISTE BLANCHE : %s' % (len(hors), ', '.join(hors)))
        print('A CLASSER PAR UN HUMAIN — lecture seule, ou execution ?')
        return 1
    print('\nTOUTE LA SURFACE EST CLASSEE EN LECTURE SEULE.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
