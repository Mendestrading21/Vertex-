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
        return jsonify({'empty': True, 'error': 'options_overview_unavailable'}), 500


@bp.route('/api/options/environment')
def options_environment():
    """Score LONG OPTION ENVIRONMENT (§14) — dimensions + verdict canonique."""
    from vertex.options.environment import score_environment
    try:
        return jsonify(score_environment(_board(), detail_by_sym=_detail_by_sym(),
                                         as_of=_as_of(), source='SCAN'))
    except Exception as e:
        return jsonify({'score': None, 'label': 'INCONNU',
                        'error': 'options_environment_unavailable'}), 500


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
    # Série CANONIQUE du scan (LOT 4) — les formes legacy 'closes'/'history'
    # n'avaient aucun producteur et ne sont plus admises.
    from vertex.data import series as _series
    closes, _closes_src = _series.closes(detail)
    closes = closes or None
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
    try:
        dte_raw = float(c.get('dte'))
        dte = int(dte_raw) if dte_raw >= 0 and dte_raw.is_integer() else None
    except (TypeError, ValueError):
        dte = None
    if dte is None:
        return jsonify({'symbol': sym, 'empty': True,
                        'reason': 'dte indisponible ou invalide — simulation refusée (aucune échéance inventée)',
                        'input_coverage': {'dte_available': False,
                                           'status': 'DTE_UNAVAILABLE',
                                           'read_only': True}}), 200
    iv = c.get('iv')
    contract = {'symbol': sym, 'right': 'P' if c.get('type') == 'PUT' else 'C',
                'strike': _num(c.get('strike')), 'dte': dte,
                'mid': ((_num(c.get('cost')) or 0) / 100.0 if _num(c.get('cost')) else None),
                'iv': (iv / 100.0 if isinstance(iv, (int, float)) and iv > 3 else iv),
                'expiry': c.get('exp') or ''}
    setup = UnderlyingSetup(symbol=sym, spot=spot, invalidation=plan.get('stop'),
                            tp1=plan.get('tp1'), tp2=plan.get('tp2'), tp3=plan.get('tp3'))
    try:
        sim = scenario_pricer.simulate(contract, setup)
    except Exception as e:
        return jsonify({'symbol': sym, 'empty': True,
                        'reason': 'simulation_indisponible'}), 200
    return jsonify({'symbol': sym, 'empty': False, 'contract': {
        'type': c.get('type'), 'strike': c.get('strike'), 'dte': c.get('dte'),
        'exp': c.get('exp'), 'iv': iv, 'cost': c.get('cost'), 'spot': spot,
    }, 'sim': sim, 'as_of': _as_of()})


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


@bp.route('/api/options/gex-radar')
def options_gex_radar():
    """RADAR de positionnement : GEX de tous les sous-jacents du board, classés
    par |net GEX|. « Où les dealers poussent-ils le plus fort ? » Lecture seule."""
    from vertex.options import gex_scan as _gs
    try:
        d = _gs.scan(_board(), _detail_by_sym(), top=30)
        d['as_of'] = _as_of()
        d['demo'] = bool(DEMO_MODE)
        return jsonify(d)
    except Exception as e:
        return jsonify({'empty': True, 'rows': [],
                        'error': 'options_gex_radar_unavailable'}), 500


@bp.route('/api/options/gex/<sym>')
def options_gex(sym):
    """Positionnement dealer d'un sous-jacent : profil GEX + flux notable + thèse.
    Données réelles du board (OI/gamma/volume) — jamais inventées. Vue FENÊTRÉE :
    le board ne retient que les strikes du scan (±35 % du spot), pas la chaîne
    entière — signalé honnêtement au client. Lecture seule, aucun ordre."""
    from vertex.options import gex as _gex, flow as _flow, dealer_synthesis as _ds
    sym = (sym or '').upper()[:12]
    board = _board()
    contracts = [c for c in board if str(c.get('sym', '')).upper() == sym]
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    spot = None
    for c in contracts:
        spot = _num(c.get('spot'))
        if spot:
            break
    if not spot:
        spot = _num(detail.get('price'))
    # Move attendu du cycle : médiane des em_pct RÉELS des contrats (jamais inventé).
    ems = sorted(_num(c.get('em_pct')) for c in contracts
                 if _num(c.get('em_pct')) is not None)
    em_pct = ems[len(ems) // 2] if ems else None
    try:
        profile = _gex.compute(contracts, spot=spot, symbol=sym)
        flow = _flow.analyze(contracts, symbol=sym)
        synth = _ds.build(profile, flow,
                          earnings_in_days=detail.get('earnings_in_days'),
                          symbol=sym, em_pct=em_pct)
    except Exception as e:
        return jsonify({'symbol': sym, 'empty': True,
                        'error': 'options_gex_unavailable'}), 500
    # Journal quotidien du GEX (best-effort, réel seulement) → série « Daily GEX ».
    history = []
    history_availability = {
        'available': False,
        'status': 'GEX_HISTORY_UNAVAILABLE',
        'points_loaded': 0,
        'read_only': True,
        'reason': 'historique GEX indisponible ; une série vide ne signifie pas absence d’observation historique',
    }
    try:
        from vertex.options import gex_history as _gh
        _gh.record(profile)
        history = _gh.series(sym)
        history_availability = {
            'available': True,
            'status': 'GEX_HISTORY_AVAILABLE',
            'points_loaded': len(history) if isinstance(history, list) else 0,
            'read_only': True,
        }
    except Exception:
        pass
    return jsonify({
        'symbol': sym, 'as_of': _as_of(), 'demo': bool(DEMO_MODE),
        'contracts_available': len(contracts),
        'coverage': 'fenêtre du scan (strikes ±35 % du spot) — pas la chaîne complète',
        'gex': profile, 'flow': flow, 'synthesis': synth, 'history': history,
        'history_availability': history_availability,
    })


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
                        'error': 'options_vol_charts_unavailable'}), 500


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


@bp.route('/api/options/scanner/<universe>')
def api_options_scanner(universe):
    """SCANNERS PAR UNIVERS (SKYLER LOT 6) : TACTICAL / SWING / LEAPS strictement
    séparés, mandat LEAPS V2 étiqueté par candidat, probabilité de doublement
    (modèle documenté, ESTIMATED) sur les 5 meilleurs. Lecture seule."""
    from flask import request
    from vertex.options import double_prob as _dp, horizon_scanners as _hs
    sym = (request.args.get('sym') or '').upper().strip() or None
    res = _hs.scan(scan_state.get('options_board') or [], universe, sym=sym)
    if res.get('available'):
        for c in res['candidates'][:5]:
            prem = (c.get('cost') / 100.0) if isinstance(c.get('cost'), (int, float)) else None
            c['double_prob'] = _dp.double_probability(
                spot=c.get('spot'), strike=c.get('strike'), premium=prem,
                dte=c.get('dte'), iv=c.get('iv'), right=c.get('type') or 'CALL')
    res['as_of'] = _as_of()
    from vertex.app.config import DEMO_MODE as _demo
    res['demo'] = _demo
    return jsonify(res)


__all__ = ['bp']
