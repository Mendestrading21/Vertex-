"""
vertex/app/routes/live_api.py — API du Vertex Live Engine.

GET  /api/live/status   — mode global + état/source/fraîcheur par domaine
POST /api/live/refresh  — déclenche la mise à jour (tout ou ?domains=a,b)
GET  /api/live/report   — dernier rapport de synchronisation

Lecture seule, analyse uniquement — jamais d'ordre.
"""

from flask import Blueprint, jsonify, request

from vertex.services import live_engine

bp = Blueprint('live_api', __name__)


@bp.route('/api/live/status')
def live_status():
    return jsonify(live_engine.status())


@bp.route('/api/live/refresh', methods=['POST', 'GET'])
def live_refresh():
    raw = (request.args.get('domains') or '').strip()
    domains = [d.strip() for d in raw.split(',') if d.strip()] or None
    return jsonify(live_engine.refresh(domains))


@bp.route('/api/live/report')
def live_report():
    return jsonify(live_engine.report())


__all__ = ['bp']
