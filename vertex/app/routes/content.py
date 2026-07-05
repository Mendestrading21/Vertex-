"""
vertex/app/routes/content.py — FILS DE CONTENU (Blueprint, Ch. II).

Actualités, calendrier de catalyseurs, watchlist hebdo — lectures des états
partagés (`vertex.app.state`). Le flag `ai_on` signale si la couche IA
(résumés/traductions) est disponible. Lecture seule, analyse uniquement.
"""

from flask import Blueprint, jsonify

from elio import ai
from vertex.app.state import news_state, cal_state, weekly_state

bp = Blueprint('content', __name__)


@bp.route('/news-feed')
def news_feed_ep():
    return jsonify({**news_state, 'ai_on': ai.available()})


@bp.route('/cal-feed')
def cal_feed_ep():
    return jsonify(cal_state)


@bp.route('/weekly-feed')
def weekly_feed_ep():
    return jsonify({**weekly_state, 'ai_on': ai.available()})


__all__ = ['bp']
