"""
vertex/app/routes/desk.py — DESK PERSO (Blueprint, Ch. II).

Les routes du poste de travail personnel : synchronisation du desk entre
appareils (/api/desk), export TradingView de l'univers (/api/watchlist-tv)
et cotation en direct des trades perso (/api/pos-quotes).

(/api/ticker/<sym> vit dans terminal.py : sa version enrichie — profil
d'entreprise + comparaison aux pairs — a remplacé la version simple.)

Les dépendances lourdes du monolithe (pack options réseau, file de jobs IBKR)
sont INJECTÉES à la construction — le Blueprint reste testable sans réseau.

⛔ Lecture seule : ces routes lisent et cotent, ne passent JAMAIS d'ordre.
"""

import glob
import os
import shutil
import threading
import time
from datetime import datetime

from flask import Blueprint, jsonify, request

from vertex.data.universe import UNIVERSE
from vertex.services import persist

BACKUP_KEEP = 7   # rotations quotidiennes conservées


def _backup_desk():
    """Snapshot QUOTIDIEN de desk_data.json avant écrasement (1er write du jour).
    Filet de sécurité contre le last-writer-wins : positions/journal/alertes
    restaurables sur 7 jours. Silencieux — ne bloque jamais la sync."""
    try:
        src = persist.cache_path('desk_data.json')
        if not os.path.exists(src) or os.path.getsize(src) < 20:
            return
        day = datetime.now().strftime('%Y%m%d')
        dst = persist.cache_path('desk_backup_%s.json' % day)
        if os.path.exists(dst):
            return                                   # déjà sauvegardé aujourd'hui
        shutil.copyfile(src, dst)
        try:
            from vertex.scheduler import registry as _sched
            _sched.beat('DATA_BACKUP', ok=True)
        except Exception:
            pass
        olds = sorted(glob.glob(persist.cache_path('desk_backup_*.json')))
        for p in olds[:-BACKUP_KEEP]:
            os.remove(p)
    except Exception:
        pass

POSQ_TTL_S = 45          # fraîcheur d'une cotation de trade perso
POSQ_MAX_POSITIONS = 24  # borne dure par requête


def _scan_fallback_quote(p):
    """Marque DIFFÉRÉE d'une position quand IBKR ne cote pas (TWS fermé).

    Actions : prix du scan (yfinance différé). Options : mid du contrat
    correspondant du board (sym + droit + strike, échéance par préfixe —
    le desk stocke 'YYYY-MM', le board 'YYYY-MM-DD'). Étiquetée delayed:True
    pour que l'UI l'affiche « différé » — un titre absent du scan reste sans
    marque (aucun chiffre inventé).
    """
    from vertex.app.state import scan_state
    sym = (p.get('sym') or '').upper()
    if not sym:
        return None
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    spot = detail.get('price')
    right = (p.get('right') or '').upper()
    is_opt = bool(right or p.get('strike') is not None)
    q = {}
    if isinstance(spot, (int, float)) and spot > 0:
        q['spot'] = spot
    if is_opt:
        want_type = 'PUT' if right.startswith('P') else 'CALL'
        want_exp = str(p.get('exp') or '')
        try:
            want_strike = float(p.get('strike'))
        except (TypeError, ValueError):
            want_strike = None
        for c in (scan_state.get('options_board') or []):
            if (str(c.get('sym', '')).upper() == sym
                    and c.get('type') == want_type
                    and c.get('mid') is not None
                    and want_strike is not None
                    and abs(float(c.get('strike') or 0) - want_strike) < 0.01
                    and (not want_exp or str(c.get('exp', '')).startswith(want_exp))):
                q['mark'] = c.get('mid')
                break
        if 'mark' not in q and want_strike is not None:
            # Le board n'a que les « meilleurs » strikes — cote le contrat EXACT
            # détenu via la chaîne (cache TTL 15 min dans on_demand).
            try:
                from vertex.options import on_demand as _od
                mk = _od.contract_mark(sym, want_exp, want_strike,
                                       'P' if right.startswith('P') else 'C')
                if mk is not None:
                    q['mark'] = mk
            except Exception:
                pass
    if not q:
        return None
    q['delayed'] = True
    q['src'] = 'scan'
    return q


def make_blueprint(*, opt_job, ibkr_enabled):
    """Construit le Blueprint du desk.

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
                _backup_desk()                       # snapshot quotidien AVANT écrasement
                persist.save_json('desk_data.json', {'ts': body['ts'], 'data': body['data']})
            return jsonify({'ok': True, 'ts': body['ts']})
        with desk_lock:
            d = persist.load_json('desk_data.json', {}) or {}
        return jsonify(d)

    @bp.route('/api/desk/backups')
    def api_desk_backups():
        """Liste les snapshots quotidiens du desk (restaurables)."""
        out = []
        for p in sorted(glob.glob(persist.cache_path('desk_backup_*.json')), reverse=True):
            name = os.path.basename(p)
            out.append({'name': name, 'date': name[12:20], 'size': os.path.getsize(p)})
        return jsonify({'backups': out, 'keep': BACKUP_KEEP})

    @bp.route('/api/desk/restore', methods=['POST'])
    def api_desk_restore():
        """Restaure un snapshot quotidien → desk_data.json (ts=maintenant, donc
        tous les appareils re-tireront cette version). Nom STRICTEMENT validé."""
        name = str((request.get_json(force=True, silent=True) or {}).get('name') or '')
        import re
        if not re.fullmatch(r'desk_backup_\d{8}\.json', name):
            return jsonify({'ok': False, 'err': 'nom invalide'}), 400
        src = persist.cache_path(name)
        if not os.path.exists(src):
            return jsonify({'ok': False, 'err': 'backup introuvable'}), 404
        with desk_lock:
            snap = persist.load_json(name, None)
            if not snap or not isinstance(snap.get('data'), dict):
                return jsonify({'ok': False, 'err': 'backup illisible'}), 500
            persist.save_json('desk_data.json', {'ts': int(time.time() * 1000), 'data': snap['data']})
        return jsonify({'ok': True, 'restored': name})

    @bp.route('/api/watchlist-tv')
    def api_watchlist_tv():
        """Univers du desk au format TradingView (à coller dans une watchlist TV pour rester synchronisé)."""
        syms = list(UNIVERSE)
        return jsonify({'count': len(syms), 'symbols': syms, 'tv': ','.join(syms)})

    @bp.route('/api/ibkr/positions')
    def api_ibkr_positions():
        """Portefeuille TWS en LECTURE SEULE — pour l'import dans le Desk.
        Hors connexion : erreur claire, jamais de données inventées."""
        # ok:false en 200 : broker hors ligne = état attendu (pas une panne du
        # serveur Vertex) — un 503 pollue la console à chaque visite Portefeuille.
        if not ibkr_enabled:
            return jsonify({'ok': False, 'positions': [],
                            'err': 'IBKR non connecté (mode cloud/démo) — ouvre TWS ou Gateway puis réessaie.'}), 200
        res = opt_job('positions', (), timeout=20)
        if res is None:
            return jsonify({'ok': False, 'positions': [],
                            'err': 'TWS injoignable — vérifie que TWS/Gateway est ouvert et l\'API activée.'}), 200
        return jsonify({'ok': True, 'positions': res, 'count': len(res)})

    @bp.route('/api/pos-quotes', methods=['POST'])
    def api_pos_quotes():
        """Cote en direct les TRADES PERSO saisis sur la page Ma Stratégie (actions + options).
        Body : {positions:[{sym, exp?, strike?, right?}]} — exp 'YYYY-MM' acceptée (résolue au vrai jour).
        ⛔ Lecture seule : cote les contrats, ne passe JAMAIS d'ordre."""
        body = request.get_json(force=True, silent=True) or {}
        poss = (body.get('positions') or [])[:POSQ_MAX_POSITIONS]
        now = time.time()
        # purge des cotations périmées : le cache reste borné (pas de fuite mémoire
        # au fil des contrats cotés sur des semaines d'usage)
        for k in [k for k, (ts, _) in posq_cache.items() if now - ts > 20 * POSQ_TTL_S]:
            posq_cache.pop(k, None)
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
        # REPLI DIFFÉRÉ : TWS fermé (ou contrat non coté) → marque du scan/board,
        # étiquetée delayed — le portefeuille garde un P&L honnête au lieu de
        # « marques indisponibles ». Position hors scan : toujours rien d'inventé.
        for p in todo:
            k = p.get('key')
            if k and k not in out:
                fb = _scan_fallback_quote(p)
                if fb:
                    posq_cache[k] = (now, fb)
                    out[k] = fb
        return jsonify({'results': out, 'live': bool(ibkr_enabled), 'ts': int(now)})

    return bp


__all__ = ['make_blueprint', 'POSQ_TTL_S', 'POSQ_MAX_POSITIONS']
