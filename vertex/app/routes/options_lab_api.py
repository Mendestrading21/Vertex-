"""
vertex/app/routes/options_lab_api.py — API du centre de recherche options.

Une seule route : /api/options-lab — le payload complet des 12 chapitres,
consolidé côté serveur (le client ne télécharge plus le /scan géant).

Analyse uniquement, lecture seule. Aucun ordre.
"""

from flask import Blueprint, jsonify

from vertex.app.config import DEMO_MODE
from vertex.app.state import cal_state, scan_state
from vertex.engines import multileg_lab, options_lab

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


@bp.route('/api/options/strategies/<sym>')
def api_options_strategies(sym):
    """Stratégies options MULTI-JAMBES construites depuis le board RÉEL : payoff à
    l'échéance, breakevens, gain/perte max, probabilité de profit, greeks agrégés.
    Analyse pure, lecture seule — aucun ordre. Donnée absente => available:false honnête."""
    sym = sym.upper()
    try:
        board = scan_state.get('options_board') or []
        detail = (scan_state.get('detail') or {}).get(sym) or {}
        spot = detail.get('price')
        if not spot:
            spot = next((c.get('spot') for c in board
                         if c.get('sym') == sym and c.get('spot')), None)
        # Biais directionnel RÉEL du titre (verdict/score du scan) → recommandation adaptée.
        verdict = (detail.get('verdict') or '').upper()
        score = detail.get('score')
        if verdict in ('ACHETER', 'RENFORCER', 'BUY') or (score is not None and score >= 60):
            bias = 'bullish'
        elif verdict in ('ÉVITER', 'EVITER', 'ALLÉGER', 'ALLEGER', 'AVOID') or (score is not None and score < 40):
            bias = 'bearish'
        else:
            bias = 'neutral'
        res = multileg_lab.strategies_for_symbol(board, sym, spot, bias=bias)
        res['as_of'] = scan_state.get('scan_ts_h') or scan_state.get('updated')
        res['demo'] = DEMO_MODE
        return jsonify(res)
    except Exception as e:
        return jsonify({'available': False, 'reason': f'{type(e).__name__}: {e}'}), 200


__all__ = ['bp']
