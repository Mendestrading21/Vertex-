#!/usr/bin/env python3
"""Vertex 1.0 · #783/G3 — LE MOTEUR SE NOTE-T-IL VRAIMENT ?

`RELEASE_GATES.md` G3 : *« … et la mémoire des résultats est exploitable sans
look-ahead »*. Deux questions, et la seconde n'a de sens que si la première a
une réponse :

1. la mémoire produit-elle **quoi que ce soit** ?
2. ce qu'elle produit est-il exempt de look-ahead ?

Cet outil répond à la première. Il construit un état **réaliste** — une série de
prix au format exact du produit, un registre dont les horizons sont **échus** —
et regarde ce que `track_record.evaluate()` en fait.

## Pourquoi un état fabriqué, et non le registre réel

`edge_ledger.jsonl` est gitignoré : il n'existe pas dans un dépôt frais, ni en
intégration continue. Une mesure qui en dépendrait ne dirait rien ailleurs que
sur la machine du trader. L'état fabriqué, lui, est **vérifiable** : on sait
combien d'entrées devraient se résoudre, donc l'écart se lit sans interprétation.

Le format de la série n'est pas inventé : il reproduit `vertex/engines/analysis.py`
— `dates` en ISO, `date_labels` en `%m-%d`, `close` alignés.

## Les témoins

Un détecteur qui ne trouve rien ne prouve rien.

1. **témoin positif** — une jointure qui marche DOIT résoudre les entrées dont
   l'horizon est échu ; si le compte est nul avec une série correcte, c'est
   l'instrument qui est aveugle, pas forcément le produit ;
2. **témoin négatif** — une entrée dont l'horizon n'est **pas** échu ne doit
   **jamais** être résolue : c'est la définition même de l'absence de
   look-ahead, et si elle l'était, la fiabilité affichée serait gonflée.

Usage :
    python tools/vertex_1_0/mesurer_track_record.py [--json]
Sorties : 0 = mesuré, 2 = témoin muet (mesure non fiable).
"""
from __future__ import annotations

import datetime
import json
import os
import pathlib
import sys
import tempfile
import time

RACINE = pathlib.Path(__file__).resolve().parents[2]

#: Assez long pour que +20 séances soient échues sur une entrée du début.
SEANCES = 60
#: Le seuil de bucket de `evaluate` est n >= 5 ; on en met assez pour le franchir.
ENTREES = 8


def _serie(depart: datetime.date, n: int = SEANCES):
    """Série au format EXACT du produit (`vertex/engines/analysis.py`)."""
    jours, closes = [], []
    d, p = depart, 100.0
    while len(jours) < n:
        if d.weekday() < 5:                     # jours ouvrables seulement
            jours.append(d.isoformat())
            closes.append(round(p, 2))
            p *= 1.01                           # hausse réguliere : le signe est prévisible
        d += datetime.timedelta(days=1)
    return {'dates': jours, 'close': closes,
            'date_labels': [j[5:] for j in jours]}


def _registre(chemin: str, jour_iso: str, prix: float, n: int = ENTREES):
    horodatage = time.mktime(datetime.date.fromisoformat(jour_iso).timetuple())
    with open(chemin, 'w', encoding='utf-8') as f:
        for _ in range(n):
            f.write(json.dumps({
                'ts': horodatage, 'ticker': 'AAA', 'price': prix,
                'decision': 'ACHAT', 'score': 30,
                'entry': prix, 'stop': prix * 0.95,
                'targets': {'tp1': prix * 1.03, 'tp2': prix * 1.06},
                'market_regime': 'HAUSSIER', 'sector_regime': 'RISK-ON',
                'features': {'grade': 'A', 'rs': 80, 'setup_quality': 'BON'},
                'outcome': None}) + '\n')


def _evaluer(indice_entree: int, symbole_serie: str = 'AAA') -> dict:
    """Fait tourner `evaluate()` sur un état fabriqué. Rend son résultat brut."""
    sys.path.insert(0, str(RACINE))
    from vertex.engines import track_record as tr
    from vertex.services import persist

    dossier = tempfile.mkdtemp()
    ancien = persist.cache_path
    persist.cache_path = lambda nom: os.path.join(dossier, nom)
    try:
        serie = _serie(datetime.date(2026, 5, 1))
        _registre(os.path.join(dossier, tr.LEDGER),
                  serie['dates'][indice_entree], serie['close'][indice_entree])
        etat = {'detail': {symbole_serie: {'series': serie}}}
        tr._MEMO['data'] = None                 # la mémoïsation masquerait la mesure
        return tr.evaluate(etat)
    finally:
        persist.cache_path = ancien


def mesurer() -> dict:
    #  Entrée à la 10ᵉ séance sur 60 : +1, +5 et +20 sont tous ÉCHUS.
    echu = _evaluer(10)
    #  Entrée à la DERNIÈRE séance : aucun horizon, pas même +1, n'est échu.
    #
    #  ⚠ Première version : `SEANCES - 2`. À cet indice, +1 séance EST échue —
    #  la borne était fausse, pas le produit. Le témoin l'a signalé dès que la
    #  jointure a été réparée. Avant la réparation, il « passait » : rien ne se
    #  résolvait, donc rien ne pouvait se résoudre à tort. Un témoin négatif
    #  vert sur un détecteur aveugle ne prouve rien — c'est exactement le piège
    #  qu'il est censé fermer, et il ne le ferme qu'une fois la mesure vivante.
    trop_recent = _evaluer(SEANCES - 1)
    #  Un symbole que le scan ne connaît plus (titre sorti de l'univers).
    disparu = _evaluer(10, symbole_serie='BBB')

    return {
        'horizons_echus': {
            'entrees': echu.get('entries'), 'resolus': echu.get('resolved'),
            'verdicts': sorted(echu.get('by_verdict') or {}),
            'attendu': ENTREES,
        },
        'horizons_non_echus': {
            'entrees': trop_recent.get('entries'),
            'resolus': trop_recent.get('resolved'),
            'attendu': 0,
        },
        'symbole_hors_univers': {
            'entrees': disparu.get('entries'), 'resolus': disparu.get('resolved'),
        },
        'note_servie': echu.get('note'),
    }


def _temoins(r: dict) -> list:
    echecs = []
    if r['horizons_non_echus']['resolus'] != 0:
        echecs.append(
            'TEMOIN NEGATIF ROMPU : %d entrees dont AUCUN horizon n\'est echu '
            'ont ete resolues — la fiabilite affichee serait gonflee par du '
            'look-ahead' % r['horizons_non_echus']['resolus'])
    e = r['horizons_echus']
    if e['resolus'] == 0 and e['entrees']:
        echecs.append(
            'TEMOIN POSITIF MUET : aucune entree resolue alors que +1, +5 et '
            '+20 sont tous echus. Soit la jointure est cassee, soit '
            'l\'instrument ne construit plus une serie au format du produit.')
    if r['horizons_echus']['entrees'] != ENTREES:
        echecs.append('le registre fabrique n\'est pas lu : %s entrees vues sur %d'
                      % (r['horizons_echus']['entrees'], ENTREES))
    return echecs


def rendre_texte(r: dict) -> str:
    e, t, d = r['horizons_echus'], r['horizons_non_echus'], r['symbole_hors_univers']
    verdict = ('LE MOTEUR SE NOTE' if e['resolus'] == e['attendu']
               else 'LE MOTEUR NE SE NOTE PAS')
    return '\n'.join([
        'MEMOIRE DES RESULTATS — CE QUE `evaluate()` PRODUIT VRAIMENT',
        '=' * 66,
        '',
        'horizons ECHUS        : %d entrees -> %d resolues (attendu %d)  %s'
        % (e['entrees'], e['resolus'], e['attendu'],
           'OK' if e['resolus'] == e['attendu'] else '<-- ECART'),
        '   buckets par verdict : %s' % (e['verdicts'] or '(aucun)'),
        '',
        'horizons NON echus    : %d entrees -> %d resolues (attendu 0)  %s'
        % (t['entrees'], t['resolus'],
           'OK — pas de look-ahead' if t['resolus'] == 0 else '<-- LOOK-AHEAD'),
        '',
        'symbole hors univers  : %d entrees -> %d resolues'
        % (d['entrees'], d['resolus']),
        '   (un verdict sur un titre qui a quitte l\'univers n\'est jamais note :',
        '    la fiabilite ne porte que sur les SURVIVANTS)',
        '',
        'VERDICT : %s' % verdict,
    ])


def main() -> int:
    r = mesurer()
    echecs = _temoins(r)
    if echecs:
        for e in echecs:
            print(e, file=sys.stderr)
        return 2
    print(json.dumps(r, indent=2, ensure_ascii=False) if '--json' in sys.argv
          else rendre_texte(r))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
