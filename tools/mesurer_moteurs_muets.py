"""tools/mesurer_moteurs_muets.py — QUELS MOTEURS SORTENT, ET PAR OÙ ?

La fusion de `main` a apporté 34 moteurs neufs. Deux questions les séparent en
trois familles, et **c'est la seule chose qui décide de leur valeur** :

| famille | définition | ce qu'il faut faire |
| --- | --- | --- |
| **PEINT** | sa clé sort d'une route ET l'interface la lit | rien |
| **MUET** | sa clé sort d'une route, personne ne la lit | la peindre |
| **ENFERMÉ** | sa clé ne sort d'aucune route servie | l'exposer, puis la peindre |

## Pourquoi cet outil existe

J'ai répondu deux fois à la main, et **deux fois faux**. Le premier sondage
déclarait 23 moteurs muets ; il interrogeait une seule route. Le deuxième en
déclarait 20 enfermés ; il utilisait un titre au dossier pauvre — clôtures
parfaitement plates, aucune date, aucun secteur — et trois moteurs qui sortent
très bien ont été comptés absents. **Je mesurais la pauvreté de mon jeu d'essai,
pas le produit.**

D'où les deux règles de montage :

1. **Un dossier RICHE** — deux cents clôtures bruitées, dates, secteur, volume.
   Un moteur qui exige un historique daté ne peut pas être jugé sur un titre
   qui n'en a pas.
2. **TOUTES les routes GET servies**, pas celle que je soupçonne. C'est
   l'énumération du lot 33, réutilisée telle quelle.

## Anti-vacuité

Trois moteurs sont **connus sortants** (mesurés aux lots 49 et 50). Si le
balayage n'en retrouve aucun, c'est la sonde qui est morte, pas le produit :
l'outil rend 2 plutôt qu'un inventaire trompeur.

Usage : python tools/mesurer_moteurs_muets.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SYM = 'MUET1'

#  Les 34 modules apportés par la fusion, lus dans le dépôt et non recopiés :
#  une liste écrite à la main diverge dès le premier ajout.
def moteurs_neufs():
    import subprocess
    out = subprocess.run(
        ['git', 'diff', '--name-only', '--diff-filter=A', '8d82297..HEAD',
         '--', 'vertex/'],
        capture_output=True, text=True, cwd=os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))).stdout
    return sorted({os.path.basename(f)[:-3] for f in out.split()
                   if f.endswith('.py')})


#  Mesurés sortants aux lots 49 et 50 — ils servent de témoin au balayage.
TEMOINS = ('regime_break', 'opportunity_reliability', 'instrument_profile')


def dossier_riche():
    """Un titre que les moteurs peuvent réellement juger."""
    import random
    random.seed(11)
    closes = [100.0]
    for _ in range(240):
        closes.append(round(closes[-1] * (1 + random.gauss(0.0005, 0.014)), 4))
    dates = ['2026-%02d-%02d' % (1 + i // 28, 1 + i % 28) for i in range(len(closes))]
    return {
        'price': closes[-1], 'closes': closes, 'dates': dates,
        'series': {'closes': closes, 'dates': dates},
        'sector': 'Technology', 'volume': 1_500_000, 'avg_volume': 1_000_000,
        'rsi': 54.0, 'ma20': closes[-1] * 0.99, 'ma200': closes[-1] * 0.92,
        'atr_pct': 2.1, 'change': 0.8,
    }


def main(argv=None):
    os.environ.setdefault('NO_IBKR', '1')
    os.environ.setdefault('DEMO', '1')
    os.environ.setdefault('START_ON_IMPORT', '0')
    import tempfile

    from tools.mesurer_sorties_news import armer_l_alarme, chemins_get, interroger

    from vertex.services import persist
    persist._BASE_DIR = tempfile.mkdtemp(prefix='vx-muets-')
    import terminal
    from vertex.app.state import scan_state
    scan_state.setdefault('detail', {})[SYM] = dossier_riche()
    armer_l_alarme()

    noms = moteurs_neufs()
    if not noms:
        print('AVEUGLE — aucun module neuf releve : la borne de comparaison '
              'git a bouge, refus de conclure.')
        return 2
    print('moteurs neufs : %d · titre d\'essai : %s (dossier riche)' % (len(noms), SYM))

    client = terminal.app.test_client()
    chemins = [c for c in chemins_get(terminal.app) if 'TSTQ' not in c]
    chemins += ['/api/skyler/%s' % SYM, '/api/decision/%s' % SYM,
                '/api/evidence/%s' % SYM, '/api/anomalies/%s' % SYM,
                '/api/vertex/%s' % SYM, '/analysis/%s' % SYM]
    chemins = sorted(set(chemins))
    print('routes interrogees : %d' % len(chemins))

    sort_par = {}
    for chemin in chemins:
        corps = interroger(client, chemin, secondes=6)
        if not corps:
            continue
        for n in noms:
            if '"%s"' % n in corps or "'%s'" % n in corps:
                sort_par.setdefault(n, []).append(chemin)

    vus_temoins = [t for t in TEMOINS if t in sort_par]
    if not vus_temoins:
        print('\nAVEUGLE — aucun des trois moteurs connus sortants n\'a ete '
              'retrouve. C\'est la sonde qui est morte, pas le produit.')
        return 2
    print('temoin : %d/%d moteurs connus sortants retrouves' % (len(vus_temoins),
                                                                len(TEMOINS)))

    #  Lu par l'interface ? On cherche la clé dans ce qui PEINT.
    import pathlib
    ui = ''
    for p in list(pathlib.Path('vertex/ui').rglob('*.py')) + \
            list(pathlib.Path('vertex/static/vertex/js').rglob('*.js')):
        ui += p.read_text(encoding='utf-8', errors='replace')

    peints, muets, enfermes = [], [], []
    for n in noms:
        routes = sort_par.get(n)
        if not routes:
            enfermes.append(n)
        elif re.search(r'\b%s\b' % re.escape(n), ui):
            peints.append((n, routes))
        else:
            muets.append((n, routes))

    print('\nPEINTS   — sortent ET sont lus : %d' % len(peints))
    for n, r in peints:
        print('  %-32s %s' % (n, r[0]))
    print('\nMUETS    — sortent, personne ne les lit : %d' % len(muets))
    for n, r in muets:
        print('  %-32s %s%s' % (n, r[0], ' (+%d)' % (len(r) - 1) if len(r) > 1 else ''))
    print('\nENFERMES — ne sortent d\'aucune route servie : %d' % len(enfermes))
    for n in enfermes:
        print('  %s' % n)
    print('\n%d peints · %d a peindre · %d a exposer' %
          (len(peints), len(muets), len(enfermes)))
    return 0


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
