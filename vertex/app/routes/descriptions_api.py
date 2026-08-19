"""vertex/app/routes/descriptions_api.py — LA FICHE D'ACTIVITÉ (#779, G1).

`/desc/<sym>` : que fait cette entreprise ? Une phrase, un secteur, un pays, un
effectif. Servi **à la demande**, jamais en masse — c'est ce qui évite le
throttle yfinance, qui limite les appels `info` bien plus vite que les cotations.

⛔ Aucune donnée de marché ici : pas de prix, pas de Greek. Rien de ce que cette
route sert ne périme en séance.

## Ce qui est mis en cache, et ce qui ne l'est pas

**Seuls les appels réussis** sont écrits sur disque. Un `info` vide — throttle,
ticker inconnu, réseau coupé — n'est pas mémorisé : le cacher figerait un écran
vide pour toujours, alors qu'un simple réessai plus tard aurait réussi. La
distinction « rien trouvé » / « pas encore demandé » est ici la différence entre
une fiche qui se remplit un jour et une fiche définitivement muette.

Le cache mémoire, lui, retient aussi les réponses issues de la table française :
elles ne coûtent rien à reconstruire, mais servir deux fois le même travail
n'apporte rien.

## `lang`, et pourquoi il n'est pas décoratif

`fr` si le résumé a réellement été traduit, `en` si le texte anglais est servi
tel quel. Sans ce drapeau, l'interface annoncerait du français au-dessus d'un
paragraphe anglais — le genre de petite affirmation fausse que le produit
s'interdit ailleurs.
"""
from __future__ import annotations

import json
import threading

import yfinance as yf
from flask import Blueprint, jsonify

from vertex.ai import briefs as _ai
from vertex.app.config import DEMO_MODE
from vertex.data.descriptions_fr import DESCRIPTIONS
from vertex.services import persist

bp = Blueprint('descriptions_api', __name__)

#: Cache disque des descriptions déjà obtenues. Le chemin passe par
#: `persist.cache_path` : le calculer avec `os.path.dirname(__file__)` le ferait
#: pointer dans `vertex/app/routes/`, et l'ancien cache ne serait plus jamais
#: relu — sans la moindre erreur.
CHEMIN = persist.cache_path('desc_cache.json')

try:
    with open(CHEMIN, 'r', encoding='utf-8') as _fh:
        _cache = json.load(_fh)
except Exception:
    _cache = {}

_verrou = threading.Lock()

#: Résumé tronqué avant traduction : au-delà, on paie une traduction pour du
#: texte que personne ne lit.
LIMITE_RESUME = 900


@bp.route('/desc/<sym>')
def desc_ep(sym):
    sym = (sym or '').upper()
    if sym in _cache:
        return jsonify(_cache[sym])
    out = {'sym': sym, 'summary': '', 'industry': '', 'employees': None,
           'country': '', 'lang': 'fr'}
    if DEMO_MODE or sym in DESCRIPTIONS:     # vitrine / secours : description FR intégrée
        fd = DESCRIPTIONS.get(sym)
        if fd:
            out['summary'], out['industry'], out['country'] = fd[0], fd[1], fd[2]
            _cache[sym] = out
            return jsonify(out)
    try:
        info = yf.Ticker(sym).info
        _en = (info.get('longBusinessSummary') or '')[:LIMITE_RESUME]
        out['summary'] = _ai.fr_desc(sym, _en) if _en else ''
        out['lang'] = 'fr' if (out['summary'] and out['summary'] != _en) else 'en'
        out['industry'] = info.get('industry') or ''
        out['employees'] = info.get('fullTimeEmployees')
        out['country'] = info.get('country') or ''
    except Exception:
        pass
    if out['summary']:
        #  ON NE CACHE QUE LES FETCH RÉUSSIS. Mémoriser un échec figerait une
        #  fiche vide pour toujours, alors qu'un réessai plus tard aboutirait.
        with _verrou:
            _cache[sym] = out
            try:
                with open(CHEMIN, 'w', encoding='utf-8') as _fh:
                    json.dump(_cache, _fh)
            except Exception:
                pass
    return jsonify(out)


__all__ = ['bp', 'CHEMIN', 'LIMITE_RESUME']
