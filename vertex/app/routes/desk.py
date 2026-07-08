"""
vertex/app/routes/desk.py — DESK PERSO (Blueprint, Ch. II).

Les routes du poste de travail personnel : synchronisation du desk entre
appareils (/api/desk), export TradingView de l'univers (/api/watchlist-tv),
fiche express d'un titre (/api/ticker/<sym>) et cotation en direct des trades
perso (/api/pos-quotes).

Les dépendances lourdes du monolithe (pack options réseau, file de jobs IBKR)
sont INJECTÉES à la construction — le Blueprint reste testable sans réseau.

⛔ Lecture seule : ces routes lisent et cotent, ne passent JAMAIS d'ordre.
"""

import threading
import time

from flask import Blueprint, jsonify, request

from vertex.app.state import scan_state
from vertex.data.universe import UNIVERSE
from vertex.services import persist

POSQ_TTL_S = 45          # fraîcheur d'une cotation de trade perso
POSQ_MAX_POSITIONS = 24  # borne dure par requête


def make_blueprint(*, options_pack, opt_job, ibkr_enabled):
    """Construit le Blueprint du desk.

    options_pack(sym) -> dict   : pack options/GEX/earnings à la demande (réseau).
    opt_job(kind, args, timeout): job IBKR sérialisé (None si indisponible).
    ibkr_enabled                : cotations live possibles (sinon cache seul).
    """
    bp = Blueprint('desk', __name__)
    desk_lock = threading.Lock()
    posq_cache = {}      # cotations des trades perso : {key: (ts, data)} — TTL 45 s

    @bp.route('/api/desk', methods=['GET', 'POST'])
    def api_desk():
        """Synchronisation du desk perso (trades, journal, favoris, capital, simulateur) entre appareils.
        Stockage local dans desk_data.json — dernier écrivain gagne (blob complet + timestamp)."""
        if request.method == 'POST':
            body = request.get_json(force=True, silent=True) or {}
            if not isinstance(body.get('data'), dict) or not body.get('ts'):
                return jsonify({'ok': False, 'err': 'payload invalide'}), 400
            with desk_lock:
                persist.save_json('desk_data.json', {'ts': body['ts'], 'data': body['data']})
            return jsonify({'ok': True, 'ts': body['ts']})
        with desk_lock:
            d = persist.load_json('desk_data.json', {}) or {}
        return jsonify(d)

    @bp.route('/api/watchlist-tv')
    def api_watchlist_tv():
        """Univers du desk au format TradingView (à coller dans une watchlist TV pour rester synchronisé)."""
        syms = list(UNIVERSE)
        return jsonify({'count': len(syms), 'symbols': syms, 'tv': ','.join(syms)})

    @bp.route('/api/ticker/<sym>')
    def api_ticker(sym):
        sym = sym.upper()
        return jsonify({'symbol': sym, 'in_universe': sym in UNIVERSE,
                        'detail': (scan_state.get('detail') or {}).get(sym), 'pack': options_pack(sym)})

    @bp.route('/api/pos-quotes', methods=['POST'])
    def api_pos_quotes():
        """Cote en direct les TRADES PERSO saisis sur la page Ma Stratégie (actions + options).
        Body : {positions:[{sym, exp?, strike?, right?}]} — exp 'YYYY-MM' acceptée (résolue au vrai jour).
        ⛔ Lecture seule : cote les contrats, ne passe JAMAIS d'ordre."""
        body = request.get_json(force=True, silent=True) or {}
        poss = (body.get('positions') or [])[:POSQ_MAX_POSITIONS]
        now = time.time()
        todo, out = [], {}
        for p in poss:
            if not isinstance(p, dict):
                continue
            key = '%s|%s|%s|%s' % ((p.get('sym') or '').upper(), p.get('exp') or '',
                                   p.get('strike') if p.get('strike') is not None else '',
                                   (p.get('right') or '').upper())
            p['key'] = key
            c = posq_cache.get(key)
            if c and now - c[0] < POSQ_TTL_S:
                out[key] = c[1]
            else:
                todo.append(p)
        if todo and ibkr_enabled:
            res = opt_job('posq', (todo,), timeout=45) or {}
            for k, v in res.items():
                if v is not None:
                    posq_cache[k] = (now, v)
                    out[k] = v
        return jsonify({'results': out, 'live': bool(ibkr_enabled), 'ts': int(now)})

    return bp


__all__ = ['make_blueprint', 'POSQ_TTL_S', 'POSQ_MAX_POSITIONS']
