"""Vérifie que le balisage RÉELLEMENT SERVI est correctement imbriqué.

Pourquoi cet outil existe : le dossier `/analysis/<sym>` était cassé depuis
longtemps parce qu'une `<section>` était fermée par un `</div>` orphelin. Le
navigateur ignore une fermante qui ne correspond à rien : la section restait
ouverte et TOUT le dossier s'imbriquait dans une carte collante — cartes
empilées, colonnes réduites à un mot par ligne.

Aucun contrôle existant ne pouvait l'attraper :
  · 0 débordement horizontal — le contenu débordait verticalement ;
  · 0 erreur console — un balisage mal fermé n'est pas une erreur JavaScript ;
  · 0 bloc vide — les blocs contenaient du texte, simplement illisible ;
  · la suite de tests était verte — aucun test ne rend la page.

**On lit le HTML SERVI, pas le DOM.** Un navigateur répare toujours : son
`outerHTML` est bien formé par construction, même quand la source ne l'est pas.
Interroger le DOM reviendrait donc à demander au correcteur s'il a corrigé
quelque chose. On analyse ce que le serveur écrit.

Usage :
    python tools/vertex_2_0_balisage.py --base http://127.0.0.1:8099
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request

ROUTES = ('/', '/calendar', '/markets', '/opportunities', '/analysis',
          '/analysis/AAPL', '/options', '/options/dossier/AAPL', '/simulator',
          '/portfolio', '/follow-up', '/performance', '/intelligence',
          '/system', '/design-system')

#: Balises sans contenu : les fermer n'a pas de sens.
VIDES = {'br', 'hr', 'img', 'input', 'meta', 'link', 'source', 'path', 'circle',
         'rect', 'line', 'use', 'stop', 'col', 'area', 'base', 'embed', 'track',
         'wbr', 'polyline', 'polygon', 'ellipse', 'animate', 'feoffset',
         'fegaussianblur', 'femerge', 'femergenode', 'feflood', 'fecomposite'}

#: Balises dont la fermeture est facultative en HTML : une ouverture non fermée
#: n'y est pas une faute. On ne les empile pas.
OPTIONNELLES = {'li', 'p', 'td', 'th', 'tr', 'option', 'dt', 'dd',
                'thead', 'tbody', 'tfoot', 'colgroup'}

_BALISE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>')


def _contenu_principal(html: str) -> str:
    """Le contenu de `<main>`, sans sa propre balise ouvrante ni fermante.

    La coque est identique sur toutes les pages : ce qu'on veut mesurer, c'est
    ce que la PAGE écrit. Inclure `<main>` lui-même le ferait apparaître comme
    « jamais fermée » sur chaque route — un faux positif uniforme, donc inutile.
    """
    m = re.search(r'<main\b[^>]*>', html)
    if not m:
        return ''
    fin = html.find('</main>', m.end())
    return html[m.end():fin if fin != -1 else len(html)]


def _sans_bruit(fragment: str) -> str:
    """Retire commentaires, `<script>` et `<style>` : du texte, pas du balisage.

    Sans cela, une chaîne JavaScript contenant `'</div>'` — il y en a beaucoup,
    ces pages construisent leur HTML côté client — compterait comme une balise.
    """
    fragment = re.sub(r'<!--.*?-->', '', fragment, flags=re.S)
    fragment = re.sub(r'<script\b[^>]*>.*?</script>', '', fragment, flags=re.S | re.I)
    fragment = re.sub(r'<style\b[^>]*>.*?</style>', '', fragment, flags=re.S | re.I)
    return fragment


def analyser(html: str) -> dict:
    corps = _sans_bruit(_contenu_principal(html))
    pile, orphelines = [], []
    for m in _BALISE.finditer(corps):
        fermante, tag, auto = m.group(1) == '/', m.group(2).lower(), m.group(3) == '/'
        if tag in VIDES or auto or tag in OPTIONNELLES:
            continue
        if not fermante:
            pile.append(tag)
            continue
        if pile and pile[-1] == tag:
            pile.pop()
            continue
        trouve = next((k for k in range(len(pile) - 1, -1, -1) if pile[k] == tag), None)
        if trouve is None:
            orphelines.append({'tag': tag, 'attendait': pile[-1] if pile else None})
        else:
            del pile[trouve:]
    return {'orphelines': orphelines, 'non_fermees': pile}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--routes', nargs='*', default=list(ROUTES))
    ap.add_argument('--json', default='')
    args = ap.parse_args()

    rapport, defauts = {}, 0
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    for route in args.routes:
        try:
            with opener.open(args.base + route, timeout=30) as r:
                html = r.read().decode('utf-8', 'replace')
        except Exception as exc:  # noqa: BLE001
            print(f'{route:<18} INJOIGNABLE — {exc}')
            defauts += 1
            continue
        r = analyser(html)
        rapport[route] = r
        n = len(r['orphelines']) + len(r['non_fermees'])
        defauts += n
        if n:
            print(f'{route:<18} {n} anomalie(s)')
            for o in r['orphelines'][:5]:
                print(f'      fermante orpheline </{o["tag"]}> '
                      f'(la pile attendait </{o["attendait"]}>)')
            for t in r['non_fermees'][:5]:
                print(f'      jamais fermée <{t}>')
        else:
            print(f'{route:<18} OK')

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
    print(f'\nTOTAL : {defauts} anomalie(s) de balisage')
    return 1 if defauts else 0


if __name__ == '__main__':
    sys.exit(main())
