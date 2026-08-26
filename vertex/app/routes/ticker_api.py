"""vertex/app/routes/ticker_api.py — LA FICHE D'UN TITRE (#779, G1).

- `/options/<sym>`    — le paquet options seul ;
- `/api/ticker/<sym>` — la fiche complète : détail du scan, entreprise, pairs,
  médianes sectorielles, carte des risques, et le paquet options.

⛔ **Analyse seule.** Ces deux routes lisent et comparent ; elles ne préparent
ni ne transmettent aucun ordre.

## La comparaison aux pairs ne fabrique rien

Chaque pair est cherché **dans le cache seul** (`allow_fetch=False`) : ouvrir
une fiche déclencherait sinon quatre appels réseau supplémentaires, et un
throttle sur le titre principal. Un pair absent du cache sort avec ses champs à
`None` — une case vide, jamais une valeur devinée depuis le secteur.

## Chaque bloc a son propre `try`, et c'est délibéré

Le paquet options, la fiche entreprise, les médianes et la carte des risques
échouent **indépendamment**. Un `try` global ferait disparaître la fiche entière
parce que yfinance n'a pas répondu sur une chaîne d'options — alors que le
détail du scan, lui, était disponible. Chaque zone dit son absence sans
emporter les autres.
"""
from __future__ import annotations

from flask import Blueprint, jsonify

from vertex.app import snapshot as _instantane
from vertex.app.config import DEMO_MODE
from vertex.app.state import scan_state
from vertex.data import company as _company
from vertex.data.universe import UNIVERSE
from vertex.options.pack import options_pack

bp = Blueprint('ticker_api', __name__)

#: Le magasin d'instantanés de la fiche. Il VIT dans `vertex/app/caches.py`,
#: avec les autres propriétaires de caches et sa politique écrite : en créer un
#: second ici donnerait deux magasins pour une même route, et le registre
#: décrirait un objet que personne n'utilise.
from vertex.app.caches import _TICKER_SNAPSHOTS as MAGASIN    # noqa: E402

#: Fenêtre de fraîcheur. Alignée sur le `ttl:60000` que la page Analyse
#: applique déjà côté client : une fenêtre serveur plus courte ferait
#: reconstruire une valeur que le navigateur ne redemandera pas.
FRAICHEUR_S = 60.0

#: Pairs comparés sur la fiche. Au-delà, la table devient illisible et chaque
#: ligne coûte une lecture de cache.
MAX_PAIRS = 4


@bp.route('/options/<sym>')
def opt_ep(sym):
    return jsonify(options_pack(sym.upper()))


def _annexes(sym):
    """La partie COÛTEUSE de la fiche — jamais sur le chemin de la requête.

    Mesuré le 25 août 2026 : `options_pack` seul coûte 46,6 s sur un titre
    neuf, contre 3,4 s pour tout le reste du dossier. Sous charge, la fiche
    entière montait à 28–48 s, et cinq demandes simultanées du même titre
    faisaient cinq collectes — dont une à 136,9 s.

    Le `pack` est CONSERVÉ dans la charge : `/options/<sym>` le sert aussi, et
    retirer une clé casserait le contrat. Mesuré par ailleurs : la page Analyse
    lit `detail`, `company`, `peers_data`, `sector_median`, `risk_map` et
    `in_universe` — et `pack` **zéro fois**. Le coût était donc payé par
    quelqu'un qui ne s'en servait pas.
    """
    try:
        pack = options_pack(sym)
    except Exception as e:                                    # noqa: BLE001
        #  L'aveu reste STRUCTURÉ. Avant ce lot, une coupure réseau faisait
        #  sortir `IndexError: single positional indexer is out-of-bounds` dans
        #  la charge servie — une exception Python présentée comme un état.
        pack = {'sym': sym, 'error': '%s: %s' % (type(e).__name__, e),
                'contracts': []}
    try:
        comp = _company.get(sym, demo=DEMO_MODE, brief=True)
    except Exception:                                         # noqa: BLE001
        comp = None
    det_all = scan_state.get('detail') or {}
    peers_data = []
    for p in ((comp or {}).get('peers') or [])[:MAX_PAIRS]:
        pd = det_all.get(p) or {}
        try:
            pc = _company.get(p, demo=DEMO_MODE, allow_fetch=False)   # cache seul
        except Exception:                                     # noqa: BLE001
            pc = {}
        pf = (pc or {}).get('fundamentals') or {}
        peers_data.append({'symbol': p, 'name': (pc or {}).get('name'),
                           'score': pd.get('score'), 'verdict': pd.get('verdict'),
                           'perf_q': pd.get('perf_q'), 'rev_growth': pf.get('rev_growth'),
                           'margin': pf.get('margin'), 'pe': pf.get('pe'),
                           'roe': pf.get('roe')})
    try:
        sec_med = _company.sector_medians().get((comp or {}).get('sector')) or {}
    except Exception:                                         # noqa: BLE001
        sec_med = {}
    try:
        from vertex.company import risk_map as _risk_map
        _det = det_all.get(sym) or {}
        risque = _risk_map.build(comp, sector_median=sec_med,
                                 earnings_in_days=_det.get('earnings_dte'))
    except Exception:                                         # noqa: BLE001
        risque = None
    valeur = {'company': comp, 'peers_data': peers_data, 'pack': pack,
              'sector_median': sec_med, 'risk_map': risque}
    etat = _instantane.DEMO if DEMO_MODE else _instantane.DELAYED
    #  La RAISON de la dégradation remonte dans `meta`, nommée. Avant ce lot,
    #  elle n'existait que sous la forme d'un texte d'exception enfoui dans
    #  `pack.error` — mesuré sous coupure réseau : « IndexError: single
    #  positional indexer is out-of-bounds ». Un consommateur ne peut pas agir
    #  sur une phrase pareille ; il peut agir sur « paquet options
    #  indisponible ». Le texte brut RESTE dans `pack.error` : il aide au
    #  diagnostic, il ne sert simplement plus d'état.
    manques = []
    if (pack or {}).get('error'):
        manques.append('paquet options indisponible')
    if comp is None:
        manques.append('fiche entreprise indisponible')
    return valeur, {'source': 'demo' if DEMO_MODE else 'yfinance+ibkr',
                    'etat': etat,
                    'erreur': ' ; '.join(manques) or None,
                    'qualite': 'PARTIELLE' if manques else 'COMPLETE'}


@bp.route('/api/ticker/<sym>')
def api_ticker(sym):
    """La fiche d'un titre, servie SANS collecte sur le chemin synchrone.

    Le noyau — symbole, appartenance à l'univers, détail du scan — vit déjà en
    mémoire et part immédiatement. Les annexes coûteuses viennent du magasin
    d'instantanés : présentes si elles existent (fraîches ou datées), absentes
    et AVOUÉES sinon, avec une collecte lancée en fond et coalescée.

    Le contrat de sortie garde toutes ses clés ; `meta` s'y ajoute.
    """
    sym = sym.upper()
    det_all = scan_state.get('detail') or {}
    annexes, meta = MAGASIN.servir(sym, lambda: _annexes(sym),
                                   fraicheur_s=FRAICHEUR_S, attendre=False)
    annexes = annexes or {}
    return jsonify({
        'symbol': sym,
        'in_universe': sym in UNIVERSE,
        'detail': det_all.get(sym),
        #  Aucune clé ne DISPARAIT : un consommateur qui lisait `pack` continue
        #  de le trouver. Il vaut `None` tant que la collecte n'a pas abouti —
        #  une absence dite, jamais un objet vide qui ressemble à une réponse.
        'company': annexes.get('company'),
        'peers_data': annexes.get('peers_data') or [],
        'pack': annexes.get('pack'),
        'sector_median': annexes.get('sector_median') or {},
        'risk_map': annexes.get('risk_map'),
        'meta': meta.vers_dict(),
    })


__all__ = ['bp', 'MAX_PAIRS']
