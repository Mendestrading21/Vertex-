"""vertex/app/routes/positions_api.py — API Position Intelligence.

Expose l'état analytique des positions (calculs, cycle de vie, thèse,
verdict, priorité), le rapport de démarrage, l'audit et les alertes.
⛔ LECTURE SEULE : aucune route ne peut passer, modifier ou clôturer un
ordre. Le desk (myTrades) reste la source déclarative ; ces routes le
LISENT et l'analysent.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request

from vertex.services import persist


def make_blueprint(scan_state: dict, *, opt_job=None, ibkr_enabled=False) -> Blueprint:
    bp = Blueprint('positions_api', __name__)

    def _desk_blob():
        return persist.load_json('desk_data.json', {}) or {}

    def _ibkr_positions():
        if not ibkr_enabled or opt_job is None:
            return None
        try:
            return opt_job('positions', (), timeout=20)
        except Exception:
            return None

    def _quotes(positions):
        """Cote via le worker IBKR (posq) quand disponible — sinon None."""
        if not ibkr_enabled or opt_job is None:
            return {}
        todo = []
        for p in positions:
            if p['asset_type'] == 'OPTION':
                todo.append({'sym': p['symbol'], 'exp': p.get('expiration'),
                             'strike': p.get('strike'),
                             'right': 'P' if p.get('right') == 'PUT' else 'C',
                             'key': '%s|%s|%s|%s' % (p['symbol'], p.get('expiration') or '',
                                                     p.get('strike') if p.get('strike') is not None else '',
                                                     'P' if p.get('right') == 'PUT' else 'C')})
            else:
                todo.append({'sym': p['symbol'], 'exp': '', 'strike': '', 'right': '',
                             'key': '%s||%s|' % (p['symbol'], '')})
        try:
            return opt_job('posq', (todo,), timeout=45) or {}
        except Exception:
            return {}

    @bp.route('/api/positions/state')
    def positions_state():
        """État complet recalculé de toutes les positions ouvertes."""
        from vertex.positions.recalculator import recalculate_all
        from vertex.positions.repository import load_positions
        blob = _desk_blob()
        ibkr = _ibkr_positions()
        base = load_positions(blob, ibkr)
        quotes = _quotes([p for p in base if p.get('status') != 'CLOSED'])
        state = recalculate_all(scan_state, blob, quotes, ibkr)
        state['live'] = bool(ibkr_enabled)
        return jsonify(state)

    @bp.route('/api/positions/report')
    def positions_report():
        """Startup Position Report (§6) — détection/réconciliation."""
        from vertex.positions.detector import startup_position_report
        return jsonify(startup_position_report(_desk_blob(), _ibkr_positions(),
                                               ibkr_online=bool(ibkr_enabled)))

    @bp.route('/api/positions/audit')
    def positions_audit():
        """Audit d'intégrité (§41) — HEALTHY/DEGRADED/CRITICAL."""
        from vertex.positions.audit import audit_positions
        from vertex.positions.repository import load_positions
        return jsonify(audit_positions(load_positions(_desk_blob(), _ibkr_positions())))

    @bp.route('/api/positions/reconcile')
    def positions_reconcile():
        """Réconciliation locale ↔ IBKR (§7) — DATA_REPAIR_REQUIRED explicite."""
        from vertex.positions.repository import load_positions
        from vertex.positions.reconciler import reconcile
        pos = load_positions(_desk_blob(), _ibkr_positions())
        local = [p for p in pos if p['source'] != 'IBKR']
        broker = [p for p in pos if p['source'] == 'IBKR']
        return jsonify(reconcile(local, broker, ibkr_online=bool(ibkr_enabled)))

    @bp.route('/api/portfolio/stress')
    def portfolio_stress():
        """STRESS-SCÉNARIOS du book : ±X % appliqués aux positions actions déclarées,
        valorisées au prix RÉEL du scan. Options exclues honnêtement (IBKR requis).
        Descriptif — pas une prévision, aucun ordre."""
        import json as _json
        from vertex.engines import portfolio_stress as _stress
        blob = _desk_blob()
        data = (blob or {}).get('data') or {}
        raw = data.get('myTrades')
        try:
            positions = _json.loads(raw) if isinstance(raw, str) else (raw or [])
            if not isinstance(positions, list):
                positions = []
        except Exception:
            positions = []
        detail = scan_state.get('detail') or {}
        prices = {s: (d or {}).get('price') for s, d in detail.items()}
        return jsonify(_stress.build(positions, prices))

    @bp.route('/api/positions/alerts')
    def positions_alerts():
        """Alertes consolidées de positions (§29) — lecture seule."""
        from vertex.positions.recalculator import recalculate_all
        from vertex.positions.alerts import ALERTS
        from vertex.positions.repository import load_positions
        blob = _desk_blob()
        ibkr = _ibkr_positions()
        base = [p for p in load_positions(blob, ibkr) if p.get('status') != 'CLOSED']
        state = recalculate_all(scan_state, blob, _quotes(base), ibkr)
        fresh = ALERTS.evaluate(state['positions'])
        return jsonify({'new': fresh, 'active': ALERTS.active(),
                        'gamma': _gamma_events(state['positions'])})

    def _gamma_events(positions):
        """SURVEILLANCE GAMMA (descriptive, lecture seule) : pour chaque titre en
        position, signale depuis le profil GEX réel du board (a) un support de
        positionnement cassé (spot < mur put) et (b) un régime accélérateur
        (spot sous la bascule zero-gamma). Aucun état, aucun ordre — la liste
        DÉCRIT le positionnement courant ; board vide → liste vide honnête."""
        from vertex.options import gex as _gex
        board = scan_state.get('options_board') or []
        out, seen = [], set()
        for p in positions or []:
            sym = str(p.get('symbol') or '').upper()
            if not sym or sym in seen:
                continue
            seen.add(sym)
            contracts = [c for c in board if str(c.get('sym', '')).upper() == sym]
            if not contracts:
                continue
            detail = (scan_state.get('detail') or {}).get(sym) or {}
            prof = _gex.compute(contracts, spot=detail.get('price'), symbol=sym)
            if prof.get('empty') or prof.get('spot') is None:
                continue
            spot = prof['spot']
            pw, zg = prof.get('put_wall'), prof.get('zero_gamma')
            if pw is not None and spot < pw:
                out.append({'type': 'GAMMA_SUPPORT_BREAK', 'symbol': sym,
                            'spot': spot, 'put_wall': pw,
                            'detail': 'Spot sous le mur put (%s < %s) — le support de '
                                      'positionnement a cédé.' % (spot, pw)})
            if zg is not None and spot < zg:
                out.append({'type': 'GAMMA_REGIME_ACCELERATING', 'symbol': sym,
                            'spot': spot, 'zero_gamma': zg,
                            'detail': 'Spot sous la bascule zero-gamma (%s < %s) — les '
                                      'dealers amplifient les mouvements.' % (spot, zg)})
        return out

    @bp.route('/api/positions/<position_id>/changes')
    def position_changes(position_id):
        """« Ce qui a changé » (§27) pour une position — depuis le dernier snapshot."""
        from vertex.positions.recalculator import recalculate_all
        from vertex.positions.change_detector import diff
        blob = _desk_blob()
        ibkr = _ibkr_positions()
        from vertex.positions.repository import load_positions
        base = [p for p in load_positions(blob, ibkr) if p.get('status') != 'CLOSED']
        state = recalculate_all(scan_state, blob, _quotes(base), ibkr)
        cur = next((p for p in state['positions'] if p['position_id'] == position_id), None)
        if not cur:
            return jsonify({'error': 'position introuvable', 'changed': False}), 200
        prev = persist.load_json('position_snap_%s.json' %
                                 position_id.replace('|', '_').replace(':', '_'), None)
        d = diff(prev, cur)
        try:
            persist.save_json('position_snap_%s.json' %
                              position_id.replace('|', '_').replace(':', '_'), cur)
        except Exception:
            pass
        return jsonify(d)

    return bp


__all__ = ['make_blueprint']
