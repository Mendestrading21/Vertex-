"""vertex/app/routes/live_state_api.py — LES SONDES D'ÉTAT (#779, G1).

Trois routes que le client interroge pour savoir **ce que le serveur sait, et à
quel point c'est frais** :

- `/quotes`            — cours en direct du flux IBKR, avec leur fraîcheur ;
- `/ibkr`              — instantané du compte (lecture seule) ;
- `/api/alerts/status` — alertes déclenchées côté serveur.

⛔ Lecture seule. Aucune de ces routes ne prépare ni ne transmet un ordre.

## Ce que `/quotes` refuse de faire, et c'est le point

Servir des cours périmés en les présentant comme du direct. Au-delà de
`ibkr_state.FENETRE_S`, la route rend **`quotes: {}`** plutôt qu'une table
ancienne : une absence honnête, jamais une valeur qui a l'air vivante. Le drapeau
`fresh` accompagne la réponse pour que l'appelant n'ait pas à le redéduire — et
le seuil est **emprunté**, jamais recopié : deux tables divergeraient au premier
ajustement, et `/quotes` servirait des cours que la page Système déclare périmés.

Elle appelle aussi `ibkr_state.sync()` au passage. Ce n'est pas un effet de bord
gratuit : c'est le seul moment où l'état du socket est confronté à l'âge réel des
ticks avant d'être servi.

## Les deux injections, et pourquoi elles restent

- `ibkr_snapshot` — interroge le compte via un worker `ib_async` que le
  monolithe tient (thread, timeout, cache) ;
- `alerts_fired` — le dictionnaire persisté que la boucle d'alertes **mute en
  place** dans `terminal.py`.

Les importer d'ici inverserait la dépendance sans la réduire : le blueprint
importerait le monolithe. Elles sont donc passées à la fabrique, et le jour où
leur état déménage, la signature le dira.
"""
from __future__ import annotations

import time
from typing import Any, Callable, Dict

from flask import Blueprint, jsonify

from vertex.app import ibkr_state
from vertex.app.caches import _live_meta, _live_quotes


def make_blueprint(*, ibkr_snapshot: Callable[[], Dict[str, Any]],
                   alerts_fired: Dict[str, Any]) -> Blueprint:
    """Construit le blueprint des sondes d'état.

    `alerts_fired` est passé **par référence** : la boucle d'alertes le mute en
    place, et c'est ce partage qui fait que la route sert l'état courant plutôt
    qu'une copie figée au démarrage. Le réassigner côté monolithe romprait le
    lien en silence."""
    bp = Blueprint('live_state_api', __name__)

    @bp.route('/quotes')
    def quotes_ep():
        frais = ibkr_state.frais()
        ibkr_state.sync()          # l'état honnête, avant de servir
        return jsonify({'quotes': _live_quotes if frais else {},
                        'meta': _live_meta, 'fresh': frais})

    @bp.route('/ibkr')
    def ibkr_ep():
        return jsonify(ibkr_snapshot())

    @bp.route('/api/alerts/status')
    def api_alerts_status():
        """Alertes déclenchées côté serveur (évaluées toutes les 60 s)."""
        return jsonify({'fired': alerts_fired, 'ts': int(time.time())})

    return bp


__all__ = ['make_blueprint']
