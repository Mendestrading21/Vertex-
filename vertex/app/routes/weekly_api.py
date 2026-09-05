"""vertex/app/routes/weekly_api.py — RÉGÉNÉRATION DE LA SÉLECTION HEBDO (#779, G1).

`/weekly-regen` force le recalcul du snapshot hebdomadaire — nouveau lundi
manuel, ou changement de marché assez net pour que la sélection figée ne tienne
plus. **Analyse seule** : elle recalcule un instantané, elle ne transmet rien.

## Elle refuse de travailler sur un scan absent

Sans `rows` **et** `detail`, la route rend `ok: false` et le dit. Bâtir une
sélection sur un univers vide produirait un snapshot *plausible* — une liste de
six titres, une semaine, des métadonnées — qui ne reposerait sur rien, et qui
serait relu toute la semaine comme s'il était mesuré.

## `force=True`, et ce que cela remplace

Le chemin normal (`get_or_build` sans `force`) réutilise le snapshot du lundi.
Ici on écrase délibérément, et `weekly_state['regenerated']` passe à `True` :
l'interface peut ainsi distinguer une sélection figée d'une sélection refaite à
la main, ce qui n'est pas la même chose à lire.
"""
from __future__ import annotations

from datetime import datetime

from flask import Blueprint, jsonify

from vertex.app.state import scan_state, weekly_state
from vertex.app.weekly_selection import CHEMIN, carte_resultats
from vertex.scanner import weekly

bp = Blueprint('weekly_api', __name__)


@bp.route('/weekly-regen', methods=['POST', 'GET'])
def weekly_regen_ep():
    """Force la régénération de la sélection hebdo. ANALYSE ONLY."""
    if not (scan_state.get('rows') and scan_state.get('detail')):
        return jsonify({'ok': False, 'error': 'scan pas encore prêt'})
    try:
        snap, _ = weekly.get_or_build(CHEMIN, scan_state['rows'], scan_state['detail'],
                                      earnings=carte_resultats(), n=6,
                                      with_options=True, force=True)
        weekly_state.update({'data': snap, 'regenerated': True,
                             'updated': datetime.now().strftime('%H:%M:%S')})
        return jsonify({'ok': True, 'week': snap.get('week'),
                        'n': snap.get('meta', {}).get('n')})
    except Exception:                                         # noqa: BLE001
        #  Code stable, jamais le texte de l'exception : `type(e).__name__` et
        #  son message livraient un détail interne au client.
        return jsonify({'ok': False, 'error': 'weekly_rebuild_unavailable',
                        'note': 'la sélection hebdomadaire n’a pas pu être '
                                'reconstruite — l’instantané précédent est '
                                'conservé'})


__all__ = ['bp']
