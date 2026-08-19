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

bp = Blueprint('scan_api', __name__)


@bp.route('/scan')
def scan_ep():
    """L'état du scan, avec de quoi juger sa fraîcheur et sa provenance."""
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
