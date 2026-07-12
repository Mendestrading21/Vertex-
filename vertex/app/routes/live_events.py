"""vertex/app/routes/live_events.py — Server-Sent Events (§26).

GET /api/live/events : flux SSE (reconnexion via Last-Event-ID, battement
de cœur toutes les 25 s). GET /api/live/events/stats : état du diffuseur.
Lecture seule — le flux ne transporte que des DESCRIPTIONS d'état.
"""
from __future__ import annotations

import queue

from flask import Blueprint, Response, request, jsonify

from vertex.services.live_stream import BROKER, sse_format

bp = Blueprint('live_events', __name__)


@bp.route('/api/live/events')
def live_events():
    last_id = 0
    hdr = request.headers.get('Last-Event-ID') or request.args.get('lastEventId')
    try:
        last_id = int(hdr or 0)
    except (TypeError, ValueError):
        last_id = 0

    def stream():
        q = BROKER.subscribe()
        try:
            yield 'retry: 4000\n\n'
            for ev in BROKER.replay_since(last_id):
                yield sse_format(ev)
            while True:
                try:
                    ev = q.get(timeout=25)
                    yield sse_format(ev)
                except queue.Empty:
                    yield ': heartbeat\n\n'
        finally:
            BROKER.unsubscribe(q)

    return Response(stream(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache',
                             'X-Accel-Buffering': 'no',
                             'Connection': 'keep-alive'})


@bp.route('/api/live/events/stats')
def live_events_stats():
    return jsonify(BROKER.stats())


__all__ = ['bp']
