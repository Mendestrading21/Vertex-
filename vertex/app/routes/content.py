"""
vertex/app/routes/content.py — FILS DE CONTENU (Blueprint, Ch. II).

Actualités, calendrier de catalyseurs, watchlist hebdo — lectures des états
partagés (`vertex.app.state`). Le flag `ai_on` signale si la couche IA
(résumés/traductions) est disponible. Lecture seule, analyse uniquement.
"""

from flask import Blueprint, jsonify, request

from elio import ai
from vertex.app.state import news_state, cal_state, weekly_state

bp = Blueprint('content', __name__)


@bp.route('/news-feed')
def news_feed_ep():
    """Fil de news. Recherche serveur : ?sym=NVDA (ticker) · ?q=fed (mot-clé)."""
    items = news_state.get('items') or []
    sym = (request.args.get('sym') or '').upper().strip()
    q = (request.args.get('q') or '').lower().strip()
    if sym:
        items = [n for n in items if (n.get('sym') or '').upper() == sym]
    if q:
        items = [n for n in items
                 if q in (str(n.get('title') or '') + ' ' + str(n.get('fr') or '')
                          + ' ' + str(n.get('publisher') or '')).lower()]
    return jsonify({**news_state, 'items': items, 'filtered': bool(sym or q),
                    'ai_on': ai.available()})


@bp.route('/cal-feed')
def cal_feed_ep():
    return jsonify(cal_state)


@bp.route('/weekly-feed')
def weekly_feed_ep():
    return jsonify({**weekly_state, 'ai_on': ai.available()})


__all__ = ['bp']
