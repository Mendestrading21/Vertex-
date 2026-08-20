#!/usr/bin/env python3
"""Vertex 1.0 · G2 — QUELLES SURFACES SE VIDENT, ET LE PRODUIT SAIT-IL RÉPONDRE ?

Trois défauts de suite ont eu la même forme : **une donnée existait et l'écran
restait vide**.

| chantier | ce qui était su | ce qui était montré |
| --- | --- | --- |
| hors séance | `last` sans `close` | rien (prix jeté) |
| échelle IBKR | le différé aurait répondu | rien (jamais demandé) |
| cotations | ACN à 198,0 dans le scan | `results: {}` |

Les trois ont été trouvés **un par un, après signalement**. Cet outil arrête
cette boucle : il interroge toutes les surfaces servies et classe ce qu'elles
rendent, pour que le quatrième cas se voie avant d'être vécu.

## Ce que « vide » veut dire ici

Pas « HTTP 500 » — ça se voit. **HTTP 200 avec une charge sans aucune donnée
exploitable** : `{}`, `{'results': {}}`, `{'items': []}`. C'est la panne
silencieuse, celle qui affiche une carte propre et creuse.

## Ce que l'outil NE dit PAS

Il ne dit pas « défaut ». Beaucoup de surfaces sont **légitimement** vides :
aucune alerte déclenchée, aucun trade au journal, aucune position déclarée. Un
vide honnête est un vide正. L'outil sépare donc :

- **VIDE ATTENDU** — la surface dépend du bureau de l'utilisateur, qui peut
  légitimement être vide ;
- **VIDE À EXAMINER** — la surface décrit le marché ou les moteurs, que le
  produit connaît par ailleurs. C'est là qu'ont vécu les trois défauts.

Le tri final reste humain, comme pour la preuve de non-usage du CSS.

Usage :
    python tools/vertex_1_0/mesurer_surfaces_vides.py [--json] [--base URL]
Sorties : 0 = mesuré, 2 = témoin muet.
"""
from __future__ import annotations

import json
import pathlib
import sys
import urllib.error
import urllib.request

RACINE = pathlib.Path(__file__).resolve().parents[2]
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

BASE_DEFAUT = 'http://127.0.0.1:5002'

#: Échantillons pour les routes paramétrées — un symbole que le scan connaît,
#: sinon la mesure porterait sur « symbole inconnu » et non sur la surface.
ECHANTILLONS = {'sym': 'AAPL', 'symbol': 'AAPL', 'ticker': 'AAPL',
                'decision_id': 'inexistant', 'group': 'inexistant',
                'key': 'inexistant', 'name': 'inexistant'}

#: Surfaces dont le vide vient du BUREAU de l'utilisateur : pas de trade
#: déclaré, pas d'alerte armée, pas de note. Leur vide est une vérité sur
#: l'utilisateur, pas une panne du produit.
DEPEND_DU_BUREAU = (
    '/api/desk', '/api/alerts/status', '/api/positions/alerts',
    '/api/positions/state', '/api/journal', '/api/portefeuille',
    '/api/strategie', '/api/planning/ticket', '/api/pretrade/check',
    '/api/skyler/memory', '/api/portfolio/team', '/api/portfolio/stress',
    '/api/portfolio/context', '/api/ibkr/positions',
)

#: Mots qui ne sont PAS une donnée : un statut n'est pas un contenu. Sans cette
#: liste, `{'status': 'ok'}` passerait pour une surface pleine — et l'outil ne
#: verrait plus jamais un écran creux.
MOTS_VIDES = frozenset({
    'ok', 'error', 'none', 'null', 'n/d', '—', '-', 'unknown', 'inconnu',
    'demo', 'false', 'true', 'aucune', 'aucun', 'empty', 'vide', 'not_found',
})


def compter_donnees(charge, _profondeur=0) -> int:
    """Combien de valeurs EXPLOITABLES cette charge porte-t-elle ?

    Fonction pure — c'est par elle que les témoins passent.

    Ne comptent pas : les conteneurs vides, les booléens, les mots de statut,
    et les nombres à zéro **isolés dans un compteur**… non : un `0` compte,
    parce que « zéro opportunité » est une réponse, pas un silence. Ce qui ne
    compte pas, c'est l'ABSENCE.
    """
    if _profondeur > 8:
        return 0
    if charge is None or isinstance(charge, bool):
        return 0
    if isinstance(charge, (int, float)):
        return 1
    if isinstance(charge, str):
        t = charge.strip()
        return 0 if (not t or t.lower() in MOTS_VIDES) else 1
    if isinstance(charge, dict):
        return sum(compter_donnees(v, _profondeur + 1) for v in charge.values())
    if isinstance(charge, (list, tuple)):
        return sum(compter_donnees(v, _profondeur + 1) for v in charge)
    return 0


#: Surfaces alimentees par un CACHE que le reseau remplit (noms d'entreprises,
#: fiches analystes). Leur vide dit « le cache n'est pas encore rempli », pas
#: « le produit est casse » — et dans un environnement sans reseau il ne peut
#: pas l'etre. Les confondre ferait accuser le produit d'une contrainte
#: d'environnement.
DEPEND_DU_RESEAU = ('/api/names', '/api/analyst/', '/api/weekly',
                    '/api/live/report', '/api/search')


def classer(chemin: str, statut: int, charge) -> str:
    """PLEINE / VIDE_ATTENDU / VIDE_A_EXAMINER / ATTENDU_404 / ERREUR.

    `ATTENDU_404` n'est pas une indulgence : les routes parametrees sont
    interrogees avec des echantillons DELIBEREMENT inexistants
    (`decision_id=inexistant`). Un 404 y est la BONNE reponse, et le compter
    comme une panne noierait les vraies sous du bruit que l'instrument
    fabrique lui-meme.
    """
    if statut == 404 and any(v in chemin for v in ECHANTILLONS.values()
                             if v.startswith('inexistant')):
        return 'ATTENDU_404'
    if statut != 200:
        return 'ERREUR'
    if compter_donnees(charge) > 0:
        return 'PLEINE'
    if any(chemin.startswith(p) for p in DEPEND_DU_BUREAU):
        return 'VIDE_ATTENDU'
    if any(chemin.startswith(p) for p in DEPEND_DU_RESEAU):
        return 'VIDE_CACHE_RESEAU'
    return 'VIDE_A_EXAMINER'


#: Routes GET qui DECLENCHENT un travail (rescan, rafraichissement, balayage).
#: Un instrument qui les appelle ne mesure plus : il agit — il relance un scan,
#: consomme du quota chez un fournisseur, et fausse la mesure suivante. Le
#: premier essai de cet outil a expire pour cette raison exacte.
#: Ce n'est PAS une liste d'exceptions qui affaiblit la mesure : ces routes ne
#: servent pas une donnee, elles en produisent une.
#: Flux permanents (SSE). Ils NE REPONDENT JAMAIS « fini » : c'est leur nature,
#: pas une panne. Le premier essai de cet outil a expire dessus et les a
#: classes « en erreur » — accusant un endpoint qui fonctionne exactement comme
#: prevu. Un instrument qui ne distingue pas une requete d'un flux mesure le
#: mauvais objet.
FLUX_PERMANENTS = ('/api/live/events',)

ROUTES_A_EFFET = (
    '/api/rescan', '/api/live/refresh', '/api/skyler/sweep',
    '/api/ai/refresh', '/api/options/scanner', '/api/options/simulate',
    '/api/weekly-regen', '/api/copilot/ask',
)


def surfaces_servies() -> list:
    """Corpus dérivé de la TABLE DE ROUTAGE, jamais d'une liste écrite à la
    main : une liste recopiée diverge au premier ajout de route, et la mesure
    porte alors sur un produit qui n'existe plus."""
    import terminal                                          # noqa: F401
    vues = []
    for regle in terminal.app.url_map.iter_rules():
        if 'GET' not in (regle.methods or set()):
            continue
        chemin = str(regle)
        if not chemin.startswith('/api/'):
            continue
        for cle, val in ECHANTILLONS.items():
            chemin = chemin.replace('<%s>' % cle, val)
            chemin = chemin.replace('<string:%s>' % cle, val)
            chemin = chemin.replace('<path:%s>' % cle, val)
        if '<' in chemin:                                    # paramètre inconnu
            continue
        if any(chemin.startswith(x) for x in ROUTES_A_EFFET):
            continue
        if chemin in FLUX_PERMANENTS:
            continue
        vues.append(chemin)
    return sorted(set(vues))


def _appeler(base: str, chemin: str, delai: float = 8.0):
    url = base.rstrip('/') + chemin
    try:
        with urllib.request.urlopen(url, timeout=delai) as r:
            brut = r.read()
            statut = r.status
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:                                   # noqa: BLE001
        return 0, {'_erreur': str(e)[:120]}
    try:
        return statut, json.loads(brut)
    except ValueError:
        return statut, {'_texte': len(brut)}


def temoins() -> list:
    """Un classeur qui range tout dans « pleine » ne verrait plus jamais un
    écran creux ; un classeur qui range tout dans « vide » crierait partout."""
    e = []
    if compter_donnees({'results': {}}) != 0:
        e.append('TEMOIN ROMPU : un conteneur vide passe pour une donnee')
    if compter_donnees({'items': [], 'meta': {'ok': True}}) != 0:
        e.append('TEMOIN ROMPU : un statut passe pour un contenu — c\'est '
                 'exactement ce qui rend une carte creuse invisible')
    if compter_donnees({'quotes': {'ACN': {'last': 198.0}}}) != 1:
        e.append('TEMOIN MUET : une vraie valeur n\'est pas comptee')
    if compter_donnees({'n': 0}) != 1:
        e.append('TEMOIN ROMPU : un zero MESURE est traite comme une absence — '
                 '« zero opportunite » est une reponse, pas un silence')
    if compter_donnees({'etat': 'n/d', 'source': 'demo'}) != 0:
        e.append('TEMOIN ROMPU : un aveu d\'absence compte comme une donnee')
    if classer('/api/desk', 200, {}) != 'VIDE_ATTENDU':
        e.append('TEMOIN ROMPU : un vide qui vient du bureau est signale comme '
                 'suspect — l\'outil crierait sur un utilisateur sans trades')
    corpus = surfaces_servies()
    if any(x in FLUX_PERMANENTS for x in corpus):
        e.append('TEMOIN ROMPU : un FLUX permanent est dans le corpus — '
                 'l\'instrument attendrait une fin qui ne vient jamais et '
                 'accuserait un endpoint qui fonctionne')
    if any(x.startswith('/api/rescan') for x in corpus):
        e.append('TEMOIN ROMPU : une route A EFFET est dans le corpus — '
                 'l\'instrument declencherait un rescan au lieu de mesurer')
    if classer('/api/market/summary', 200, {}) != 'VIDE_A_EXAMINER':
        e.append('TEMOIN MUET : une surface MARCHE vide n\'est pas signalee — '
                 'c\'est precisement la ou les trois defauts ont vecu')
    if classer('/api/skyler/memory/inexistant', 404, None) != 'ATTENDU_404':
        e.append('TEMOIN ROMPU : un 404 sur un echantillon DELIBEREMENT '
                 'inexistant est compte comme une panne — l\'instrument noie '
                 'les vraies sous son propre bruit')
    if classer('/api/decision/reelle', 404, None) != 'ERREUR':
        e.append('TEMOIN ROMPU : un VRAI 404 est excuse — l\'indulgence du 404 '
                 'd\'echantillon s\'est etendue a tout')
    if classer('/api/names', 200, {}) != 'VIDE_CACHE_RESEAU':
        e.append('TEMOIN ROMPU : un cache reseau vide est confondu avec un '
                 'defaut produit')
    return e


def mesurer(base: str = BASE_DEFAUT) -> dict:
    echecs = temoins()
    releves = []
    for chemin in surfaces_servies():
        statut, charge = _appeler(base, chemin)
        releves.append({
            'chemin': chemin, 'statut': statut,
            'donnees': compter_donnees(charge),
            'classe': classer(chemin, statut, charge),
        })
    par_classe = {}
    for r in releves:
        par_classe.setdefault(r['classe'], []).append(r['chemin'])
    return {'base': base, 'echecs_temoins': echecs, 'releves': releves,
            'par_classe': par_classe, 'total': len(releves)}


def rendre_texte(r: dict) -> str:
    o = ['QUELLES SURFACES SE VIDENT ?', '=' * 60,
         'base : %s   surfaces servies : %d' % (r['base'], r['total']), '']
    for classe in ('ERREUR', 'VIDE_A_EXAMINER', 'VIDE_CACHE_RESEAU',
                   'VIDE_ATTENDU', 'ATTENDU_404', 'PLEINE'):
        liste = r['par_classe'].get(classe) or []
        o.append('%-18s %3d' % (classe, len(liste)))
    o.append('')
    for classe, titre in (('ERREUR', 'EN ERREUR'),
                          ('VIDE_A_EXAMINER', 'VIDES — A EXAMINER')):
        liste = r['par_classe'].get(classe) or []
        if liste:
            o.append('%s :' % titre)
            for c in liste:
                o.append('   %s' % c)
            o.append('')
    o.append('LECTURE : un vide n\'est pas un defaut. Une surface qui depend du')
    o.append('RESEAU (caches de noms, fiches analystes) est vide tant que le')
    o.append('cache n\'est pas rempli — dans un environnement sans reseau, elle')
    o.append('NE PEUT PAS l\'etre. Lancer cet outil SUR LA MACHINE DE PRODUCTION')
    o.append('est donc la seule mesure qui discrimine vraiment.')
    o.append('BUREAU peut etre vide en verite. Celles qui decrivent le MARCHE ou')
    o.append('les MOTEURS, non : le produit connait ces donnees par ailleurs.')
    o.append('Cet outil ne corrige rien — il montre ou regarder.')
    return '\n'.join(o)


def main() -> int:
    base = BASE_DEFAUT
    if '--base' in sys.argv:
        base = sys.argv[sys.argv.index('--base') + 1]
    r = mesurer(base)
    if r['echecs_temoins']:
        for x in r['echecs_temoins']:
            print(x, file=sys.stderr)
        return 2
    print(json.dumps(r, indent=2, ensure_ascii=False) if '--json' in sys.argv
          else rendre_texte(r))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
