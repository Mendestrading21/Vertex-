"""
vertex/app/routes/feeds.py — FLUX DE DONNÉES (Blueprint, Ch. II).

Les routes de lecture pour les widgets : résumé marché, cockpit, watchlist,
board d'options, recherche, watchlist hebdo, stratégie, comité. Toutes lisent
l'état partagé (`vertex.app.state`) — aucune injection, import direct.

Lecture seule, analyse uniquement. Ces routes servent des données, jamais d'ordre.
"""

import time

from flask import Blueprint, jsonify, request

from vertex.app.config import IBKR_ENABLED
from vertex.app.state import scan_state, weekly_state
from vertex.data.universe import UNIVERSE
from vertex.engines import market_lens

bp = Blueprint('feeds', __name__)


def _scan_age():
    return round(time.time() - scan_state['scan_ts']) if scan_state.get('scan_ts') else None


@bp.route('/api/market/summary')
def api_market_summary():
    """Résumé marché pour widgets (lecture seule)."""
    mc = scan_state.get('market_ctx') or {}
    cl = market_lens.climate(mc)
    sc = cl['score'] if cl else None
    verdict = 'FAVORABLE' if (sc or 0) >= 65 else 'NEUTRE' if (sc or 0) >= 40 else 'DANGEREUX'
    return jsonify({
        'score': sc, 'verdict': verdict,
        'regime': mc.get('spy_regime'), 'roro': mc.get('roro'), 'roro_gap': mc.get('roro_gap'),
        'vix': mc.get('vix'), 'vix_band': mc.get('vix_band'), 'vix_chg': mc.get('vix_chg'),
        'breadth': mc.get('breadth'), 'market_verdict': mc.get('verdict'),
        'indices': scan_state.get('indices'), 'spy': scan_state.get('spy'),
        'best_sector': (scan_state.get('sectors') or [None])[0],
        'scanned': scan_state.get('scanned_n'), 'universe': len(UNIVERSE),
        'scan_age': _scan_age(), 'market': scan_state.get('market'),
        'source': 'ibkr' if IBKR_ENABLED else 'cloud',
    })


@bp.route('/api/cockpit')
def api_cockpit():
    """Widgets du cockpit : action du jour + top opportunités."""
    recs = scan_state.get('recommendations') or []
    cand = sorted([r for r in recs if r.get('tone') in ('buy', 'pullback')],
                  key=lambda r: ((r.get('timing') == 'BUY_NOW'), r.get('score40', 0)), reverse=True)
    top = cand[0] if cand else (recs[0] if recs else None)
    # TOP VERTEX : les meilleurs setups du jour selon le noyau quant (edge décroissant, verdict BUY/S+)
    _rows = scan_state.get('rows') or []
    _vxb = [r for r in _rows if (r.get('vx_verdict') or '') in ('VERTEX BUY', 'VERTEX S+') and r.get('vx_edge') is not None]
    vertex_top = sorted(_vxb, key=lambda r: r.get('vx_edge') or 0, reverse=True)[:5]
    return jsonify({'action': top, 'opportunities': recs[:15], 'vertex_top': vertex_top,
                    'updated': scan_state.get('updated')})


@bp.route('/api/watchlist')
def api_watchlist():
    return jsonify({'rows': scan_state.get('rows') or [], 'sectors': scan_state.get('sectors') or [],
                    'scanned': scan_state.get('scanned_n'), 'universe': len(UNIVERSE),
                    'updated': scan_state.get('updated')})


@bp.route('/api/options')
def api_options():
    return jsonify({'board': scan_state.get('options_board') or [], 'updated': scan_state.get('updated')})


@bp.route('/api/search')
def api_search():
    q = (request.args.get('q') or '').upper().strip()
    res = [{'ticker': s} for s in UNIVERSE if q in s][:20] if q else []
    return jsonify(res)


@bp.route('/api/weekly')
def api_weekly():
    return jsonify(weekly_state.get('data') or {})


@bp.route('/api/strategie')
def api_strategie():
    """Stratégie options personnalisée (1/2/3/6/9/12 mois). Lecture seule, analyse only."""
    return jsonify(scan_state.get('strategy') or {})


@bp.route('/api/comite')
def api_comite():
    """Comité d'investissement : décisions documentées (4 portes). Analyse only."""
    return jsonify(scan_state.get('committee') or {})


__all__ = ['bp']
