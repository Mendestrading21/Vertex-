#!/usr/bin/env python3
"""Vertex 1.0 · G4 — QUAND LE RÉSEAU TOMBE, LE PRODUIT LE DIT-IL ?

Le balayage QA a couvert le mode démo, l'absence d'IBKR et la panne partielle.
Il restait le cas le plus banal et le moins testé : **le réseau tombe pendant
qu'on regarde l'écran**. C'est le mode dégradé du quotidien — métro, ascenseur,
wifi qui décroche — et c'est celui où un terminal d'analyse est le plus
dangereux, parce que les chiffres restent affichés alors qu'ils ne valent plus
rien.

## Ce qui a amené cette mesure

La preuve de non-usage du CSS (#781) a classé `.vx-offline-banner` « prouvée
inatteignable » : la classe est **stylée dans `states.css` et rendue par
personne**. Plutôt que d'en conclure « CSS mort, à supprimer », la question
utile était l'inverse : *le produit a-t-il seulement une façon de dire qu'il est
hors ligne ?*

`vx-core.js` porte bien le vocabulaire (`offline: 'Hors ligne'`) dans ses puces
de fraîcheur. Reste à savoir si l'écran l'emploie quand le réseau tombe.

## Le protocole

On charge la page **en ligne** — c'est le cas réaliste, personne n'ouvre un
terminal déjà déconnecté — puis on coupe le réseau et on laisse les
rafraîchissements échouer. On relève ensuite :

1. **le produit le DIT-il ?** un texte d'aveu (« Hors ligne », « À actualiser »,
   « Erreur »…) apparaît-il quelque part ;
2. **les chiffres MENTENT-ils ?** les valeurs affichées avant la coupure
   sont-elles toujours là, sans marque de péremption ;
3. **la console crie-t-elle ?** des erreurs réseau non rattrapées.

Le point 2 est le plus important, et le moins évident : un chiffre qui reste à
l'écran sans dire qu'il est périmé est **pire** qu'un écran vide. C'est
exactement l'invariant « aucune surface ne masque une donnée périmée ».

## Les témoins

Un détecteur de « le produit avoue » doit être éprouvé dans les deux sens :
une page qui n'avoue rien doit ressortir muette, une page qui avoue doit
ressortir parlante. Sans quoi « 0 anomalie » ne distingue pas un produit
honnête d'un détecteur aveugle.

Usage :
    python tools/vertex_1_0/mesurer_hors_ligne.py [--json] [--base URL]
Sorties : 0 = mesuré, 2 = témoin muet.
"""
from __future__ import annotations

import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

from tools.vertex_1_0.mesurer_qa_espaces import _chromium, espaces  # noqa: E402

BASE_DEFAUT = 'http://127.0.0.1:5002'
LARGEUR = 1440

#: Les mots par lesquels le produit peut avouer une coupure. Recopiés depuis
#: `vx-core.js` et les états servis — ce sont les mots que l'utilisateur lit.
AVEUX = ('Hors ligne', 'hors ligne', 'À actualiser', 'A actualiser',
         'Erreur', 'erreur', 'indisponible', 'Reconnexion', 'Périmé',
         'Perime', 'non disponible', 'Impossible')

SONDE_AVEU = r"""
(aveux) => {
  const texte = document.body ? (document.body.innerText || '') : '';
  const trouves = aveux.filter(a => texte.includes(a));
  //  Une puce de fraicheur qui a bascule est l'aveu le plus fin du produit.
  const puces = [...document.querySelectorAll('.vx-fresh-chip,[data-state],.vx-freshness')]
    .map(e => ({classe: (e.className || '').toString().slice(0, 40),
                etat: e.getAttribute('data-state') || e.getAttribute('data-live') || '',
                texte: (e.textContent || '').trim().slice(0, 30)}))
    .filter(p => p.texte);
  return {aveux_trouves: trouves, puces: puces.slice(0, 12), puces_total: puces.length};
}
"""

SONDE_CHIFFRES = r"""
() => {
  //  Les VALEURS mises en avant : ce sont elles qui trompent si elles restent
  //  a l'ecran sans dire qu'elles sont perimees.
  const sel = '.vx-kpi-value, .vx-mk-idx-val, .vx-metric-value, [data-value]';
  return [...document.querySelectorAll(sel)]
    .map(e => (e.textContent || '').trim())
    .filter(t => t && t !== '—' && t !== 'n/d')
    .slice(0, 20);
}
"""

PAGE_MUETTE = ('<!doctype html><html><body><p>Cours 123,45</p>'
               '<p>Tout va bien</p></body></html>')
PAGE_PARLANTE = ('<!doctype html><html><body><p>Cours 123,45</p>'
                 '<p>Hors ligne — donnees non rafraichies</p></body></html>')


def _temoins(nav) -> list:
    e = []
    ctx = nav.new_context(viewport={'width': LARGEUR, 'height': 900},
                          service_workers='block')
    page = ctx.new_page()

    page.set_content(PAGE_MUETTE, wait_until='domcontentloaded')
    if page.evaluate(SONDE_AVEU, list(AVEUX))['aveux_trouves']:
        e.append('TEMOIN NEGATIF ROMPU : une page qui n\'avoue RIEN ressort '
                 'comme avouant — le detecteur trouverait un aveu partout')

    page.set_content(PAGE_PARLANTE, wait_until='domcontentloaded')
    if not page.evaluate(SONDE_AVEU, list(AVEUX))['aveux_trouves']:
        e.append('TEMOIN MUET : une page qui dit « Hors ligne » n\'est pas vue '
                 'comme avouant — la mesure ne mesure rien')

    if not page.evaluate(SONDE_CHIFFRES):
        e.append('TEMOIN MUET (chiffres) : aucune valeur relevee sur une page '
                 'qui en porte une — on ne saura pas si les chiffres restent')
    ctx.close()
    return e


def mesurer(base: str = BASE_DEFAUT, *, temoins: bool = True,
            attente_s: int = 12) -> dict:
    from playwright.sync_api import sync_playwright
    releves, echecs = [], []
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=_chromium(), args=['--no-sandbox'])
        if temoins:
            echecs = _temoins(nav)
        for ident, href in espaces():
            ctx = nav.new_context(viewport={'width': LARGEUR, 'height': 900},
                                  service_workers='block')
            page = ctx.new_page()
            erreurs = []
            page.on('pageerror', lambda x: erreurs.append(str(x)[:150]))
            page.on('console', lambda m: erreurs.append(m.text[:150])
                    if m.type == 'error' else None)
            page.goto(base.rstrip('/') + href, wait_until='domcontentloaded',
                      timeout=25000)
            page.wait_for_timeout(2000)
            avant_aveu = page.evaluate(SONDE_AVEU, list(AVEUX))
            avant_chiffres = page.evaluate(SONDE_CHIFFRES)

            #  LE RESEAU TOMBE. On laisse les rafraichissements echouer.
            ctx.set_offline(True)
            page.wait_for_timeout(attente_s * 1000)
            apres_aveu = page.evaluate(SONDE_AVEU, list(AVEUX))
            apres_chiffres = page.evaluate(SONDE_CHIFFRES)
            ctx.close()

            restes = [c for c in apres_chiffres if c in avant_chiffres]
            releves.append({
                'espace': ident,
                'avoue_avant': avant_aveu['aveux_trouves'],
                'avoue_apres': apres_aveu['aveux_trouves'],
                'nouvel_aveu': sorted(set(apres_aveu['aveux_trouves'])
                                      - set(avant_aveu['aveux_trouves'])),
                'chiffres_avant': len(avant_chiffres),
                'chiffres_apres': len(apres_chiffres),
                'chiffres_restes': len(restes),
                'puces': apres_aveu['puces'][:6],
                'erreurs': erreurs[:6],
                'erreurs_total': len(erreurs),
            })
        nav.close()

    muets = [r['espace'] for r in releves if not r['avoue_apres']]
    return {
        'base': base, 'attente_s': attente_s,
        'echecs_temoins': echecs, 'releves': releves,
        'espaces_muets': muets,
        'espaces_avec_nouvel_aveu': [r['espace'] for r in releves if r['nouvel_aveu']],
        'chiffres_restes_total': sum(r['chiffres_restes'] for r in releves),
        'erreurs_total': sum(r['erreurs_total'] for r in releves),
    }


def rendre_texte(r: dict) -> str:
    o = ['QUAND LE RESEAU TOMBE, LE PRODUIT LE DIT-IL ?',
         '=' * 68,
         'base : %s   coupure maintenue %d s' % (r['base'], r['attente_s']), '']
    entete = '%-14s %-10s %-10s %-9s %s' % ('espace', 'chiffres', 'restes',
                                            'erreurs', 'aveu apres coupure')
    o.append(entete)
    o.append('-' * len(entete))
    for x in r['releves']:
        o.append('%-14s %-10d %-10d %-9d %s'
                 % (x['espace'], x['chiffres_apres'], x['chiffres_restes'],
                    x['erreurs_total'],
                    ', '.join(x['avoue_apres'][:3]) or '— AUCUN —'))
    o.append('')
    o.append('ESPACES MUETS (aucun aveu apres coupure) : %d/%d  %s'
             % (len(r['espaces_muets']), len(r['releves']),
                ', '.join(r['espaces_muets']) or ''))
    o.append('ESPACES AVEC UN NOUVEL AVEU               : %d/%d  %s'
             % (len(r['espaces_avec_nouvel_aveu']), len(r['releves']),
                ', '.join(r['espaces_avec_nouvel_aveu']) or ''))
    o.append('CHIFFRES ENCORE AFFICHES apres coupure    : %d'
             % r['chiffres_restes_total'])
    o.append('')
    o.append('LECTURE : un chiffre qui reste sans dire qu\'il est perime est PIRE')
    o.append('qu\'un ecran vide. Ce que la mesure verifie, c\'est que l\'ecran')
    o.append('l\'AVOUE — pas qu\'il se vide.')
    for x in r['releves']:
        if x['puces']:
            o.append('')
            o.append('   %s — puces de fraicheur apres coupure :' % x['espace'])
            for p in x['puces'][:4]:
                o.append('      [%s] %s' % (p['etat'] or '—', p['texte']))
            break
    return '\n'.join(o)


def main() -> int:
    base = BASE_DEFAUT
    if '--base' in sys.argv:
        base = sys.argv[sys.argv.index('--base') + 1]
    r = mesurer(base)
    if r['echecs_temoins']:
        for x in r['echecs_temoins']:
            print('TEMOIN MUET : %s' % x, file=sys.stderr)
        return 2
    print(json.dumps(r, indent=2, ensure_ascii=False) if '--json' in sys.argv
          else rendre_texte(r))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
