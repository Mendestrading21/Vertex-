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
    from vertex.app import payload_validation as _payload
    try:
        body = _payload.object_body(request.get_json(force=True, silent=True), max_keys=18)
        if not str(body.get('symbol') or '').strip():
            return jsonify({'error': 'symbol requis'}), 400
        sym = _payload.required_symbol(body)
        numeric = {key: _payload.optional_number(body, key)
                   for key in ('entry', 'stop', 'tp1', 'tp2', 'tp3', 'premium', 'strike',
                               'limit_price', 'account_value', 'risk_pct')}
    except _payload.PayloadError as exc:
        return jsonify({'error': str(exc)}), 400
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    plan = detail.get('plan') or {}
    is_opt = bool(body.get('is_option'))
    ticket = _ot.build_ticket(
        sym, is_option=is_opt,
        entry=numeric['entry'] if numeric['entry'] is not None else plan.get('entry'),
        stop=numeric['stop'] if numeric['stop'] is not None else plan.get('stop'),
        tp1=numeric['tp1'] if numeric['tp1'] is not None else plan.get('tp1'),
        tp2=numeric['tp2'] if numeric['tp2'] is not None else plan.get('tp2'),
        tp3=numeric['tp3'] if numeric['tp3'] is not None else plan.get('tp3'),
        rr_res=plan.get('rr_res'),
        premium=numeric['premium'],
        right=body.get('right'), strike=numeric['strike'],
        expiry=body.get('expiry'), contract_id=body.get('contract_id'),
        limit_price=numeric['limit_price'],
        account_value=numeric['account_value'],
        risk_pct=numeric['risk_pct'])
    return jsonify(ticket)


__all__ = ['bp']
