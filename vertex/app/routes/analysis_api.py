"""
vertex/app/routes/analysis_api.py — ENDPOINTS D'ANALYSE (Blueprint, Ch. II).

Trois lectures analytiques du scan : le deep-dive VERTEX d'un titre, le
validateur hors-échantillon (walk-forward / DSR / PSR / PBO) et le Risk Manager
de portefeuille. Lisent l'état partagé (`vertex.app.state.scan_state`) — plus
d'injection : le Blueprint importe directement le même objet.

Analyse uniquement, indicatif. Ces routes lisent, ne commandent jamais.
"""

from flask import Blueprint, jsonify

from vertex.engines import quant_engine as vertex
from vertex.validation import out_of_sample as validator
from vertex.portfolio import risk_engine as portfolio_risk
from vertex.app.state import scan_state

bp = Blueprint('analysis_api', __name__)


@bp.route('/api/vertex/<sym>')
def api_vertex(sym):
    """Deep-dive VERTEX d'un titre : bloc quant complet + décomposition explicable."""
    d = (scan_state.get('detail') or {}).get(sym.upper())
    if not d:
        return jsonify({'ok': False, 'note': 'titre non scanné'})
    v = d.get('vertex')
    if not v:
        return jsonify({'ok': False, 'note': 'vertex indisponible'})
    return jsonify({'ok': True, 'symbol': sym.upper(), 'price': d.get('price'),
                    'grade': d.get('grade'), 'score': d.get('score'),
                    'vertex': v, 'explain': vertex.explain(v, d)})


@bp.route('/api/validator')
def api_validator():
    """VERTEX — validateur hors échantillon (walk-forward, DSR, PSR, PBO). Indicatif."""
    pf = scan_state.get('portfolio') or {}
    eq = pf.get('equity')
    if not eq:
        return jsonify({'ok': False, 'note': 'backtest indisponible (univers/historique insuffisant)'})
    return jsonify(validator.build(eq))


@bp.route('/api/risk')
def api_risk():
    """VERTEX v4 — Risk Manager portefeuille (corrélation, concentration, secteurs).
    Panier = top convictions du scan. Lecture seule, indicatif, aucun ordre."""
    rows = scan_state.get('rows') or []
    detail = scan_state.get('detail') or {}
    syms = [r['symbol'] for r in rows[:10]]
    return jsonify(portfolio_risk.build(syms, detail))


__all__ = ['bp']
