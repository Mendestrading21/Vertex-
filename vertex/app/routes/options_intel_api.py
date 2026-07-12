"""vertex/app/routes/options_intel_api.py — API Options Intelligence (§18).

Expose la synthèse de l'espace /options : vue d'ensemble, volatilité par
sous-jacent, risque d'événement, et l'interprétation canonique des graphiques.
⛔ LECTURE SEULE : aucune route ne passe/modifie/clôture d'ordre. Les données
proviennent du scan (options_board) et des mesures pures — champ absent → None,
jamais de chiffre inventé.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request

from vertex.app.config import DEMO_MODE
from vertex.app.state import scan_state
from vertex.options import overview as _ov
from vertex.options import interpretation as _oi

bp = Blueprint('options_intel_api', __name__)


def _board():
    return scan_state.get('options_board') or []


def _as_of():
    return scan_state.get('scan_ts_h') or scan_state.get('updated')


def _detail_by_sym():
    return scan_state.get('detail') or {}


@bp.route('/api/options/overview')
def options_overview():
    """Vue d'ensemble : compteurs, radar, environnement, pulses, interprétation."""
    try:
        return jsonify(_ov.summarize(_board(), as_of=_as_of(),
                                     demo=bool(DEMO_MODE), source='SCAN',
                                     detail_by_sym=_detail_by_sym()))
    except Exception as e:
        return jsonify({'empty': True, 'error': '%s: %s' % (type(e).__name__, e)}), 500


@bp.route('/api/options/environment')
def options_environment():
    """Score LONG OPTION ENVIRONMENT (§14) — dimensions + verdict canonique."""
    from vertex.options.environment import score_environment
    try:
        return jsonify(score_environment(_board(), detail_by_sym=_detail_by_sym(),
                                         as_of=_as_of(), source='SCAN'))
    except Exception as e:
        return jsonify({'score': None, 'label': 'INCONNU',
                        'error': '%s: %s' % (type(e).__name__, e)}), 500


@bp.route('/api/options/volatility/<sym>')
def options_volatility(sym):
    """Interprétation de la volatilité d'un sous-jacent (depuis le board/detail)."""
    sym = (sym or '').upper()[:12]
    board = _board()
    contracts = [c for c in board if str(c.get('sym', '')).upper() == sym]
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    # IV courante = médiane des IV du board pour ce titre (en fraction)
    ivs = sorted(c.get('iv') / 100.0 for c in contracts
                 if isinstance(c.get('iv'), (int, float)))
    cur_iv = ivs[len(ivs) // 2] if ivs else None
    iv_low = min(ivs) if ivs else None
    iv_high = max(ivs) if ivs else None
    closes = detail.get('closes') or detail.get('history') or None
    d = _oi.interpret_volatility(sym, current_iv=cur_iv, iv_low=iv_low,
                                 iv_high=iv_high, closes=closes,
                                 source='SCAN', as_of=_as_of())
    return jsonify({'symbol': sym, 'contracts': len(contracts),
                    'current_iv': cur_iv, 'interpretation': d})


@bp.route('/api/options/scenarios/<sym>')
def options_scenarios(sym):
    """Scénarios multi-facteurs (§19) du meilleur contrat d'un titre : spot ×
    temps × IV via scenario_pricer. ESTIMATION Black-Scholes clairement étiquetée."""
    from vertex.options import scenario_pricer
    from vertex.options.models import UnderlyingSetup
    sym = (sym or '').upper()[:12]
    contracts = sorted([c for c in _board()
                        if str(c.get('sym', '')).upper() == sym and c.get('quality') is not None],
                       key=lambda c: c.get('quality', 0), reverse=True)
    if not contracts:
        return jsonify({'symbol': sym, 'empty': True,
                        'reason': 'aucun contrat pour ce titre dans le tableau'}), 200
    c = contracts[0]
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    plan = detail.get('plan') or {}
    spot = _num(c.get('spot')) or _num(detail.get('price'))
    if not spot or spot <= 0:
        return jsonify({'symbol': sym, 'empty': True,
                        'reason': 'spot indisponible — simulation refusée (aucune donnée inventée)'}), 200
    iv = c.get('iv')
    contract = {'symbol': sym, 'right': 'P' if c.get('type') == 'PUT' else 'C',
                'strike': _num(c.get('strike')), 'dte': int(c.get('dte') or 0),
                'mid': ((_num(c.get('cost')) or 0) / 100.0 if _num(c.get('cost')) else None),
                'iv': (iv / 100.0 if isinstance(iv, (int, float)) and iv > 3 else iv),
                'expiry': c.get('exp') or ''}
    setup = UnderlyingSetup(symbol=sym, spot=spot, invalidation=plan.get('stop'),
                            tp1=plan.get('tp1'), tp2=plan.get('tp2'), tp3=plan.get('tp3'))
    try:
        sim = scenario_pricer.simulate(contract, setup)
    except Exception as e:
        return jsonify({'symbol': sym, 'empty': True,
                        'reason': 'simulation impossible: %s' % e}), 200
    return jsonify({'symbol': sym, 'empty': False, 'contract': {
        'type': c.get('type'), 'strike': c.get('strike'), 'dte': c.get('dte'),
        'exp': c.get('exp'), 'iv': iv, 'cost': c.get('cost'), 'spot': spot,
    }, 'sim': sim, 'as_of': _as_of()})


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


@bp.route('/api/options/vol-charts/<sym>')
def options_vol_charts(sym):
    """Jeux de données pour les graphiques de volatilité d'un titre (§15)."""
    from vertex.options import vol_charts
    sym = (sym or '').upper()[:12]
    expiry = request.args.get('dte')
    try:
        expiry = int(expiry) if expiry else None
    except (TypeError, ValueError):
        expiry = None
    try:
        return jsonify(vol_charts.build(_board(), sym, as_of=_as_of(),
                                        source='SCAN', expiry=expiry))
    except Exception as e:
        return jsonify({'symbol': sym, 'empty': True,
                        'error': '%s: %s' % (type(e).__name__, e)}), 500


@bp.route('/api/options/event-risk/<sym>')
def options_event_risk(sym):
    """Risque d'événement pour le meilleur contrat d'un titre."""
    sym = (sym or '').upper()[:12]
    board = _board()
    contracts = sorted([c for c in board if str(c.get('sym', '')).upper() == sym
                        and c.get('quality') is not None],
                       key=lambda c: c.get('quality', 0), reverse=True)
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    top = contracts[0] if contracts else {}
    d = _oi.interpret_event_risk(
        sym, earnings_in_days=detail.get('earnings_in_days'),
        ex_dividend_days=detail.get('ex_dividend_days'),
        right=top.get('type'), dte=top.get('dte'),
        source='SCAN', as_of=_as_of())
    return jsonify({'symbol': sym, 'interpretation': d})


@bp.route('/api/charts/<path:chart_id>/interpretation')
def chart_interpretation(chart_id):
    """Interprétation canonique d'un graphique identifié. Route de contrat :
    délègue aux moteurs selon chart_id (options.overview_mix, options.volatility…)."""
    sym = (request.args.get('sym') or '').upper()[:12]
    cid = str(chart_id)
    if cid in ('options.overview_mix', 'options.overview'):
        s = _ov.summarize(_board(), as_of=_as_of(), demo=bool(DEMO_MODE), source='SCAN')
        return jsonify(s['interpretation'])
    if cid == 'options.volatility' and sym:
        return jsonify(options_volatility(sym).get_json()['interpretation'])
    if cid == 'options.event_risk' and sym:
        return jsonify(options_event_risk(sym).get_json()['interpretation'])
    from vertex.visualization.schemas import unknown
    return jsonify(unknown(cid, 'Graphique non reconnu',
                           reason='chart_id inconnu ou paramètre sym manquant',
                           source='SCAN'))


__all__ = ['bp']
