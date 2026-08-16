"""vertex/app/routes/tracking_api.py — API du moteur de SUIVI (§33).

Crée/lit/arrête des suivis HYPOTHÉTIQUES et calcule leur performance depuis le
scan (prix réels, source + horodatage). ⛔ LECTURE SEULE : aucune route ne passe
d'ordre. Les identifiants et horodatages sont générés serveur à partir de
l'horloge de requête (le repository reste, lui, déterministe).
"""
from __future__ import annotations

import uuid
import datetime as _dt

from flask import Blueprint, jsonify, request

from vertex.app.state import scan_state
from vertex.tracking import repository as repo
from vertex.tracking import performance as perf
from vertex.tracking import reference_price as ref_price
from vertex.options import quote_resolver as option_quotes

bp = Blueprint('tracking_api', __name__)


def _now_iso():
    return _dt.datetime.now(_dt.timezone.utc).astimezone().isoformat(timespec='seconds')


def _new_id():
    return 'trk_%s' % uuid.uuid4().hex[:12]


def _stock_quote(sym):
    d = (scan_state.get('detail') or {}).get(sym.upper()) or {}
    price = d.get('price')
    if price is None:
        return None
    return {'last': price, 'price': price, 'source': scan_state.get('source') or 'scan'}


def _spy_quote():
    for it in (scan_state.get('indices') or []):
        nm = (it.get('name') or '').upper()
        if 'SPY' in nm or 'S&P' in nm or 'SP500' in nm:
            p = it.get('price') or it.get('last')
            if p is not None:
                return {'last': p, 'price': p, 'source': scan_state.get('source') or 'scan'}
    return None


def _market_open():
    mc = scan_state.get('market_ctx') or {}
    return bool(mc.get('open')) if 'open' in mc else True


def _option_quote_from_body(body):
    q = {}
    for k in ('bid', 'ask', 'mid', 'mark', 'last', 'iv', 'source'):
        if body.get(k) is not None:
            q[k] = body[k]
    return q


def _option_quote_from_board(contract_id, symbol):
    """Quote canonique : identité exacte dans le board courant, jamais au symbole seul."""
    return option_quotes.resolve(
        scan_state.get('options_board') or [], contract_id_value=contract_id,
        symbol=symbol, as_of=scan_state.get('options_as_of'),
        source=scan_state.get('options_source') or 'options_board')


@bp.route('/api/tracking', methods=['GET'])
def list_tracking():
    status = request.args.get('status')
    items = repo.list_all(status=status)
    return jsonify({'trackings': items, 'summary': repo.summary()})


@bp.route('/api/tracking/summary')
def tracking_summary():
    return jsonify(repo.summary())


@bp.route('/api/tracking/options/cohort')
def tracking_option_cohort():
    """Cohorte de contrats options hypothétiques, construite sur les snapshots
    observés seulement. Ne produit aucune métrique sous le seuil d’échantillon."""
    from vertex.tracking import option_cohort
    return jsonify(option_cohort.build(repo.list_all()))


@bp.route('/api/tracking', methods=['POST'])
def create_tracking():
    """Crée un suivi hypothétique. body: {entity_type, symbol, contract_id?,
    decision?, score?, quote?} — pour une action la marque vient du scan ;
    pour une option, la quote (bid/ask/mark) est fournie dans le body."""
    body = request.get_json(force=True, silent=True) or {}
    et = (body.get('entity_type') or 'STOCK').upper()
    sym = (body.get('symbol') or '').upper()
    if not sym:
        return jsonify({'error': 'symbol requis'}), 400
    quote_evidence = None
    if et == 'OPTION':
        quote_evidence = _option_quote_from_board(body.get('contract_id'), sym)
        quote = quote_evidence.get('quote') or {}
        if not quote_evidence.get('available'):
            # Compatibilité avec les clients historiques : un prix transmis peut
            # encore être suivi, mais son origine est explicitement déclarée.
            quote = _option_quote_from_body(body)
            if quote:
                quote['source'] = quote.get('source') or 'client_input_unverified'
    else:
        quote = _stock_quote(sym)
        if quote is None:
            # référence indisponible → suivi DATA_REQUIRED honnête (pas de prix inventé)
            quote = {}
    t = repo.create(tracking_id=_new_id(), entity_type=et, symbol=sym, quote=quote,
                    started_at=_now_iso(), market_open=_market_open(),
                    benchmark_quote=_spy_quote(), decision=body.get('decision', ''),
                    score=body.get('score'), contract_id=body.get('contract_id'),
                    data_quality=({'option_quote_resolution': quote_evidence}
                                  if quote_evidence is not None else None))
    return jsonify(t), 201


@bp.route('/api/tracking/<tracking_id>', methods=['GET'])
def get_tracking(tracking_id):
    t = repo.get(tracking_id)
    if not t:
        return jsonify({'error': 'suivi introuvable'}), 404
    return jsonify(t)


@bp.route('/api/tracking/<tracking_id>', methods=['PATCH'])
def patch_tracking(tracking_id):
    body = request.get_json(force=True, silent=True) or {}
    t = repo.patch(tracking_id, **body)
    if not t:
        return jsonify({'error': 'suivi introuvable'}), 404
    return jsonify(t)


@bp.route('/api/tracking/<tracking_id>/performance')
def tracking_performance(tracking_id):
    t = repo.get(tracking_id)
    if not t:
        return jsonify({'error': 'suivi introuvable'}), 404
    cur = None
    if t['entity_type'] != 'OPTION':
        q = _stock_quote(t['symbol'])
        cur = q['last'] if q else None
    else:
        resolution = _option_quote_from_board(t.get('contract_id'), t['symbol'])
        cur, _, _, _, _ = ref_price.pick_option_reference(resolution.get('quote') or {})
    spy = _spy_quote()
    bench_cur = spy['last'] if spy else None
    out = perf.compute(t, cur, bench_current=bench_cur,
                       current_decision=None, current_score=None)
    if t['entity_type'] == 'OPTION':
        out['option_quote_resolution'] = resolution
    return jsonify(out)


@bp.route('/api/tracking/<tracking_id>/stop', methods=['POST'])
def stop_tracking(tracking_id):
    body = request.get_json(force=True, silent=True) or {}
    t = repo.get(tracking_id)
    if not t:
        return jsonify({'error': 'suivi introuvable'}), 404
    fp = body.get('final_price')
    if fp is None and t['entity_type'] != 'OPTION':
        q = _stock_quote(t['symbol'])
        fp = q['last'] if q else None
    t = repo.stop(tracking_id, at=_now_iso(), final_price=fp,
                  final_decision=body.get('final_decision'),
                  reason=body.get('reason', ''))
    return jsonify(t)


@bp.route('/api/tracking/<tracking_id>/restart', methods=['POST'])
def restart_tracking(tracking_id):
    body = request.get_json(force=True, silent=True) or {}
    old = repo.get(tracking_id)
    if not old:
        return jsonify({'error': 'suivi introuvable'}), 404
    if old['entity_type'] == 'OPTION':
        quote = _option_quote_from_body(body)
    else:
        quote = _stock_quote(old['symbol']) or {}
    t = repo.restart(tracking_id, new_tracking_id=_new_id(), quote=quote,
                     started_at=_now_iso(), market_open=_market_open(),
                     benchmark_quote=_spy_quote(), decision=body.get('decision', ''),
                     score=body.get('score'))
    return jsonify(t), 201


@bp.route('/api/tracking/<tracking_id>/history')
def tracking_history(tracking_id):
    t = repo.get(tracking_id)
    if not t:
        return jsonify({'error': 'suivi introuvable'}), 404
    return jsonify({'tracking_id': tracking_id, 'snapshots': t.get('snapshots', []),
                    'final': t.get('final'), 'started_at': t.get('started_at'),
                    'stopped_at': t.get('stopped_at')})


__all__ = ['bp']
