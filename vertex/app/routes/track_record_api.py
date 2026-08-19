"""vertex/app/routes/track_record_api.py — LE MOTEUR SE NOTE (#779, G1).

`/api/track-record` : fiabilité **mesurée** des verdicts — rendements réels à
+5 et +20 séances, TP1-atteint-avant-stop — ventilée par verdict, par grade et
par régime. Analyse seule ; rien ici ne prépare ni ne transmet un ordre.

## Pourquoi un module à lui seul, et pas `tracking_api`

La question s'était posée, et le premier arbitrage l'avait laissée dans
`terminal.py` faute de bon domicile. `tracking_api` gère des suivis
**hypothétiques** — « si j'avais pris cette position » ; celui-ci note le moteur
sur ses verdicts **passés**. Les ranger ensemble aurait fait gagner un chiffre à
l'inventaire et perdu la distinction, qui est exactement celle que #783 doit
tenir entre mémoire des résultats et simulation.

## Aucune injection — mesuré, pas supposé

Ses deux dépendances vivent déjà dans le paquet :
`vertex.engines.track_record` et `vertex.app.state.scan_state`. Elle restait
dans le monolithe par habitude, pas par couplage.
"""
from __future__ import annotations

from flask import Blueprint, jsonify

from vertex.app.state import scan_state
from vertex.engines import track_record as _track

bp = Blueprint('track_record_api', __name__)


@bp.route('/api/track-record')
def api_track_record():
    """Fiabilité mesurée des verdicts par verdict/grade/régime. Analyse only."""
    return jsonify(_track.evaluate(scan_state))


__all__ = ['bp']
