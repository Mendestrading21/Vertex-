"""vertex/app/routes/scan_api.py — L'ÉTAT DU SCAN ET SON RÉVEIL (#779, G1).

- `/scan`        — l'état partagé complet, plus ce qu'il faut pour le juger :
                   âge, source honnête, délai avant le prochain réveil possible ;
- `/api/rescan`  — réveille la boucle, au plus une fois par fenêtre globale.

⛔ Analyse seule. `/api/rescan` **recalcule**, il ne transmet rien.

## Aucune injection — et c'est le résultat d'une mesure, pas d'un pari

Le premier arbitrage classait ces deux routes parmi les plus coûteuses à
extraire. En classant chaque dépendance par son **origine** — définie dans
`terminal.py`, ou seulement importée depuis le paquet — il ne restait que la
porte anti-rafale, qui est partie dans `vertex/app/rescan_gate.py` avec elles.

Un piège s'est révélé au passage : `terminal.py` fait
`from vertex.data.universe import *`. Les six ensembles d'indices servis par
`/scan` (`_DOW30`, `_NDX100`, `_SP500_SET`, `_RUT_SET`, `_EU_SET`, `_ASIA_SET`)
venaient donc du paquet **sans qu'aucune ligne d'import ne les nomme** — une
analyse statique des symboles ne pouvait pas les voir, et les avait comptés
comme inexistants. Ils sont désormais importés explicitement.

## La source « honnête », et ce qu'elle refuse de dire

`data_source` répond « d'où viennent ces chiffres » — yfinance, stooq, démo. Elle
ne dit **pas** si IBKR est connecté : ce badge-là est piloté par l'overlay
`/quotes`, qui est la seule surface à voir les ticks. Mélanger les deux ferait
afficher « LIVE IBKR » au-dessus de cours yfinance différés de quinze minutes.
"""
from __future__ import annotations

from flask import Blueprint, jsonify

from vertex.ai import briefs as _ai
from vertex.app import rescan_gate
from vertex.app.config import IBKR_ENABLED
from vertex.app.state import scan_age, scan_state
from vertex.data.universe import (_ASIA_SET, _DOW30, _EU_SET, _NDX100, _RUT_SET,
                                  _SP500_SET, UNIVERSE)

import gzip
import hashlib
import json
import os

import flask as app_module
from flask import request

bp = Blueprint('scan_api', __name__)


#:  Cache de REPONSE de `/scan`. La charge fait ~60 Ko de JSON, et chaque page
#:  du produit la demande a l'ouverture ; huit espaces la redemandent a chaque
#:  navigation. Entre deux publications de scan, ces octets sont IDENTIQUES :
#:  les recomposer, les re-serialiser et les recompresser a chaque appel est du
#:  travail pur perdu.
#:
#:  Trois garanties, et pas une de plus :
#:    * l'ETag est le condensat des octets SERVIS — deux appels dans la meme
#:      fenetre rendent le meme, donc `If-None-Match` peut rendre 304 ;
#:    * la version gzip est produite UNE fois ; on ne recompresse jamais un
#:      corps deja compresse (le double-gzip est le defaut classique ici) ;
#:    * un client sans `Accept-Encoding: gzip` recoit le JSON nu — un repli
#:      honnete, pas une erreur.
#:
#:  `VERTEX_SCAN_CACHE=0` desactive le mecanisme : la route redevient un simple
#:  `jsonify`, sans en-tete conditionnel.
_REPONSE_CACHE: dict = {}


def _cache_actif() -> bool:
    return os.environ.get('VERTEX_SCAN_CACHE', '1') not in ('0', 'false', 'no')


def _charge_scan() -> dict:
    """Ce que `/scan` decrit. Extrait pour que le cache et le repli servent
    exactement la meme chose — deux compositions divergeraient un jour."""
    return {
        **scan_state,
        'ai_on': _ai.available(),
        'scan_age': scan_age(),
        'rescan_cooldown_remaining': rescan_gate.restant(),
        'idx_sets': {'dow': _DOW30, 'ndx': _NDX100, 'sp': _SP500_SET,
                     'rut': _RUT_SET, 'eu': _EU_SET, 'asia': _ASIA_SET},
        #  Source HONNÊTE des données du scan. Le badge « LIVE IBKR » de
        #  l'en-tête reste piloté par l'overlay /quotes — lui seul voit les ticks.
        'data_source': (scan_state.get('source')
                        or ('yfinance' if IBKR_ENABLED else 'cloud')),
    }


def _empreinte_du_scan() -> str:
    """La cle du cache : ce qui rend la charge differente.

    L'horodatage de publication du scan et son age suffisent — tout le reste
    en derive. Cle-t-on trop court, on sert du perime ; trop long, on ne sert
    jamais le cache. `updated` bouge a chaque publication, `scan_age` a chaque
    seconde ecoulee : la fenetre de validite est donc la seconde en cours, ce
    qui est exactement ce qu'un client peut revalider.
    """
    #  Le delai anti-rafale DOIT entrer dans la cle. Sans lui, une demande de
    #  rescan dans la meme seconde qu'un appel deja servi laissait le cache
    #  annoncer « 0 s » alors que la porte en appliquait 30 : la surface
    #  proposait un bouton que le serveur refusait. Une valeur perimee qui
    #  contredit le comportement reel est pire qu'une absence.
    return '%s|%s|%s|%s' % (scan_state.get('updated'),
                            scan_state.get('scan_ts_h'),
                            scan_age(),
                            rescan_gate.restant())


@bp.route('/scan')
def scan_ep():
    """L'état du scan, avec de quoi juger sa fraîcheur et sa provenance."""
    if not _cache_actif():
        return jsonify(_charge_scan())

    cle = _empreinte_du_scan()
    entree = _REPONSE_CACHE.get('e')
    if not entree or entree['cle'] != cle:
        nu = json.dumps(_charge_scan(), default=str,
                        separators=(',', ':')).encode('utf-8')
        entree = {'cle': cle, 'nu': nu,
                  'gz': gzip.compress(nu, 6),
                  'etag': '"%s"' % hashlib.blake2b(nu, digest_size=16).hexdigest()}
        _REPONSE_CACHE['e'] = entree

    #  Revalidation : le client a deja ces octets, on ne les renvoie pas.
    if request.headers.get('If-None-Match') == entree['etag']:
        r = app_module.make_response('', 304)
        r.headers['ETag'] = entree['etag']
        return r

    accepte_gzip = 'gzip' in (request.headers.get('Accept-Encoding') or '')
    corps = entree['gz'] if accepte_gzip else entree['nu']
    r = app_module.make_response(corps)
    r.headers['Content-Type'] = 'application/json'
    r.headers['ETag'] = entree['etag']
    #  L'ETag change des que le scan est republie : le client revalide, il ne
    #  garde pas une charge perimee.
    r.headers['Cache-Control'] = 'no-cache'
    if accepte_gzip:
        r.headers['Content-Encoding'] = 'gzip'
        r.headers['Vary'] = 'Accept-Encoding'
    return r


def _scan_ep_sans_cache():
    """Conserve pour lecture : la forme d'origine, sans en-tete conditionnel."""
    return jsonify({
        **scan_state,
        'ai_on': _ai.available(),
        'scan_age': scan_age(),
        'rescan_cooldown_remaining': rescan_gate.restant(),
        'idx_sets': {'dow': _DOW30, 'ndx': _NDX100, 'sp': _SP500_SET,
                     'rut': _RUT_SET, 'eu': _EU_SET, 'asia': _ASIA_SET},
        #  Source HONNÊTE des données du scan. Le badge « LIVE IBKR » de
        #  l'en-tête reste piloté par l'overlay /quotes — lui seul voit les ticks.
        'data_source': (scan_state.get('source')
                        or ('yfinance' if IBKR_ENABLED else 'cloud')),
    })


@bp.route('/api/rescan', methods=['POST', 'GET'])
def api_rescan():
    """Réveille le scan au plus une fois par fenêtre globale.

    429 avec `Retry-After` quand la porte est fermée : un refus daté, que le
    client peut respecter, plutôt qu'un échec muet ou un faux succès."""
    attente = rescan_gate.demander()
    if attente:
        reponse = jsonify({'ok': False, 'error': 'rescan_rate_limited',
                           'retry_after': attente})
        reponse.status_code = 429
        reponse.headers['Retry-After'] = str(attente)
        return reponse
    return jsonify({
        'ok': True, 'status': 'rescan_queued', 'universe': len(UNIVERSE),
        'cooldown_seconds': rescan_gate.COOLDOWN_S,
        'msg': 'Re-scan lancé — recalcul des %d titres (≈10-30 s). '
               'Recharge dans un instant.' % len(UNIVERSE),
    })


__all__ = ['bp']
