"""vertex/app/routes/opportunities_api.py — API entonnoir d'opportunités (§11-12).

Expose l'entonnoir (Univers → … → Actionnable → Suivi → Position) et la
répartition par rôle stratégique, depuis le scan réel. Lecture seule ; aucun
ordre. Zéro actionnable est un résultat honnête (jamais de remplissage).
"""
from __future__ import annotations

from flask import Blueprint, jsonify

from vertex.app.state import scan_state
from vertex.opportunities import funnel as _funnel

bp = Blueprint('opportunities_api', __name__)


def _followed_count():
    try:
        from vertex.tracking import repository as trepo
        return trepo.summary().get('active', 0)
    except Exception:
        return 0


def _positions_count():
    try:
        from vertex.services import persist
        import json
        blob = persist.load_json('desk_data.json', {}) or {}
        raw = (blob.get('data') or {}).get('myTrades')
        trades = json.loads(raw) if isinstance(raw, str) else (raw or [])
        return len([t for t in trades if isinstance(t, dict)])
    except Exception:
        return 0


@bp.route('/api/opportunities/funnel')
def opportunities_funnel():
    try:
        return jsonify(_funnel.build_funnel(scan_state.get('rows') or [],
                                            followed=_followed_count(),
                                            positions=_positions_count()))
    except Exception as e:
        return jsonify({'stages': [], 'roles': [],
                        'error': '%s: %s' % (type(e).__name__, e)}), 500


__all__ = ['bp']
