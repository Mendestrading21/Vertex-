"""vertex/app/routes/planning_api.py — préparation d'ordre (READONLY, §11/§32).

Dimensionne une position et compose un ticket à COPIER manuellement dans IBKR.
⛔ N'exécute, ne transmet et n'appelle JAMAIS un courtier. Le plan (entrée/stop/
objectifs) vient du scan ; l'utilisateur fournit compte + budget de risque.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request

from vertex.app.state import scan_state
from vertex.planning import order_ticket as _ot

bp = Blueprint('planning_api', __name__)


@bp.route('/api/planning/ticket', methods=['POST'])
def planning_ticket():
    body = request.get_json(force=True, silent=True) or {}
    sym = (body.get('symbol') or '').upper()[:12]
    if not sym:
        return jsonify({'error': 'symbol requis'}), 400
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    plan = detail.get('plan') or {}
    is_opt = bool(body.get('is_option'))
    ticket = _ot.build_ticket(
        sym, is_option=is_opt,
        entry=body.get('entry', plan.get('entry')),
        stop=body.get('stop', plan.get('stop')),
        tp1=body.get('tp1', plan.get('tp1')),
        tp2=body.get('tp2', plan.get('tp2')),
        tp3=body.get('tp3', plan.get('tp3')),
        rr_res=plan.get('rr_res'),
        premium=body.get('premium'),
        right=body.get('right'), strike=body.get('strike'),
        expiry=body.get('expiry'), contract_id=body.get('contract_id'),
        limit_price=body.get('limit_price'),
        account_value=body.get('account_value'),
        risk_pct=body.get('risk_pct'))
    return jsonify(ticket)


__all__ = ['bp']
