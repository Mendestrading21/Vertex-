"""
vertex/app/routes/options_lab_api.py — API du centre de recherche options.

Une seule route : /api/options-lab — le payload complet des 12 chapitres,
consolidé côté serveur (le client ne télécharge plus le /scan géant).

Analyse uniquement, lecture seule. Aucun ordre.
"""

from flask import Blueprint, jsonify

from vertex.app.config import DEMO_MODE
from vertex.app.state import cal_state, scan_state
from vertex.engines import options_lab

bp = Blueprint('options_lab_api', __name__)


@bp.route('/api/options-lab')
def api_options_lab():
    """OPTIONS RESEARCH CENTER — cockpit, fiche, analyse, plan, viz, stratégies,
    tops, comparateur, comité, risques, timeline. Lecture seule."""
    try:
        return jsonify(options_lab.build(scan_state, demo=DEMO_MODE,
                                         cal_items=cal_state.get('items')))
    except Exception as e:
        return jsonify({'empty': True, 'error': f'{type(e).__name__}: {e}'}), 500


__all__ = ['bp']
