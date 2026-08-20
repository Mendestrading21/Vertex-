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
import json
import os
import shutil
import threading
import time
from datetime import datetime

from flask import Blueprint, jsonify, request

from vertex.data.universe import UNIVERSE
from vertex.scheduler import registry as _sched
from vertex.services import persist

BACKUP_KEEP = 7   # rotations quotidiennes conservées

#: Instantanés « avant perte » conservés (voir `_snapshot_avant_perte`). Plus
#: nombreux que les quotidiens : ils sont rares par construction — un seul est
#: pris par épisode de perte — et chacun correspond à un incident réel.
AVANT_PERTE_KEEP = 20

#: Valeurs qui ne représentent AUCUN travail. Leur disparition ne fait rien
#: perdre, donc elle n'a pas à être protégée : une liste vide reste une liste
#: vide. Tout le reste compte, y compris un JSON qu'on ne sait pas relire —
#: c'est bien la raison de ne pas l'effacer.
_VIDES = ('', '[]', '{}', 'null', '""', "''")


def _porte_du_travail(valeur) -> bool:
    """La valeur, si elle disparaissait, ferait-elle perdre quelque chose ?"""
    if valeur is None:
        return False
    if not isinstance(valeur, str):
        try:
            valeur = json.dumps(valeur, ensure_ascii=False)
        except Exception:
            return True          # illisible ≠ vide : dans le doute, on protège
    return valeur.strip() not in _VIDES


def _snapshot_avant_perte(blob) -> str | None:
    """Instantané SUPPLÉMENTAIRE, pris au moment précis d'une perte annoncée.

    Le filet quotidien (`_backup_desk`) prend son image **avant la première
    écriture du jour** : restaurer depuis lui rend l'état d'hier et perd tout le
    travail de la journée (mesuré au lot 362). Celui-ci comble exactement ce
    trou — il capture l'état *juste avant* que des clés ne soient menacées, donc
    à la seconde près plutôt qu'à la journée près."""
    try:
        horodatage = datetime.now().strftime('%Y%m%d-%H%M%S')
        nom = 'desk_avantperte_%s.json' % horodatage
        persist.save_json(nom, blob)
        vieux = sorted(glob.glob(persist.cache_path('desk_avantperte_*.json')))
        for p in vieux[:-AVANT_PERTE_KEEP]:
            os.remove(p)
        return nom
    except OSError:
        #  Un instantané impossible (disque plein, droits) ne doit pas faire
        #  échouer la sync : les clés menacées sont de toute façon CONSERVÉES
        #  par la fusion ci-dessous — l'instantané est une seconde ceinture.
        return None


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
        #  L'import est remonté en tête du module : un `beat` n'écrit que dans un
        #  dict sous verrou et ne lève pas. Le `try/except: pass` qui l'entourait
        #  ne protégeait donc que de l'import — mieux vaut qu'un import cassé
        #  éclate au démarrage qu'il ne se taise à chaque sauvegarde.
        _sched.beat('DATA_BACKUP', ok=True)
        olds = sorted(glob.glob(persist.cache_path('desk_backup_*.json')))
        for p in olds[:-BACKUP_KEEP]:
            os.remove(p)
    except Exception:
        pass

POSQ_TTL_S = 45          # fraîcheur d'une cotation de trade perso
POSQ_MAX_POSITIONS = 24  # borne dure par requête


def completer_par_repli(todo, out, repli):
    """Comble les positions ACTION encore sans cotation, depuis une source déjà
    en mémoire. Fonction PURE — c'est par elle que les témoins passent.

    Le défaut qu'elle corrige, reproduit localement : sans IBKR (ou si le worker
    ne rend rien), `/api/pos-quotes` renvoyait `results: {}`. Le client en
    déduisait `ok = false` et n'affichait AUCUN P&L — alors que le produit avait
    le prix en mémoire (scan yfinance). Une valeur connue restait invisible
    parce qu'un seul fournisseur était consulté.

    Les OPTIONS ne sont pas comblées : le scan ne cote pas de contrats, et
    fabriquer un prix d'option à partir du sous-jacent serait exactement la
    donnée inventée que le produit interdit. Elles restent absentes, donc
    honnêtement `—`.

    Chaque valeur de repli porte `source` : sans étiquette, un cours de scan se
    ferait passer pour une cotation broker.
    """
    if not repli:
        return 0
    combles = 0
    for p in todo:
        if not isinstance(p, dict):
            continue
        cle = p.get('key')
        if not cle or cle in out:
            continue
        if (p.get('right') or '').upper() in ('C', 'P'):
            continue                                   # option : jamais comblée
        sym = (p.get('sym') or '').upper()
        try:
            v = repli(sym)
        except Exception:                              # noqa: BLE001
            v = None
        #  LA PRIORITE N'EST PAS DECIDEE ICI. Elle vient de
        #  `source_router.PRIORITY`, seule table de priorite du produit, via
        #  `cotation_unifiee`. Un `if broker sinon scan` ecrit ici serait la
        #  troisieme regle de priorite du depot — et les deux precedentes
        #  (ordres de ports, escalades de type de donnees) ont diverge.
        from vertex.data_sources.cotation_unifiee import (
            en_charge_client, resoudre_cotation,
        )
        charge = en_charge_client(resoudre_cotation(broker=None, secondaire=v))
        if charge is None:
            continue
        out[cle] = charge
        combles += 1
    return combles


def make_blueprint(*, opt_job, ibkr_enabled, cotation_repli=None):
    """Construit le Blueprint du desk.

    opt_job(kind, args, timeout): job IBKR sérialisé (None si indisponible).
    ibkr_enabled                : cotations live possibles (sinon cache seul).
    cotation_repli(symbole)     : dernier recours pour une ACTION, rendant
                                  {'spot':…, 'spot_chg':…} ou None. Injecté —
                                  le blueprint ne doit pas savoir d'où vient
                                  cette valeur, et l'injection le rend
                                  éprouvable sans serveur.
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
                #  ── UN PUSH NE PEUT PLUS EFFACER CE QU'IL N'ENVOIE PAS ──────
                #  Mesuré au lot 362 : le last-writer-wins était TOTAL, donc un
                #  push partiel — ou `data: {}` — remplaçait le blob entier et
                #  les clés absentes disparaissaient. Le scénario n'est pas
                #  théorique : le client omet toute clé absente de localStorage
                #  (`if (v != null)` dans vx-entities.js), et un navigateur dont
                #  l'écriture localStorage échoue en silence (navigation privée,
                #  quota) hydrate sans rien persister, puis pousse `{}`.
                #
                #  UNE CLÉ ABSENTE NE VEUT JAMAIS DIRE « SUPPRIMÉE » : aucun
                #  chemin du produit n'appelle `removeItem` sur une clé de desk
                #  (vérifié) — vider une liste écrit `'[]'`, qui est bien envoyé.
                #  Une absence est donc toujours un défaut de lecture, jamais une
                #  intention. On la traite comme telle : on conserve.
                ancien = persist.load_json('desk_data.json', {}) or {}
                ancien_data = ancien.get('data')
                if not isinstance(ancien_data, dict):
                    ancien_data = {}
                fusion = dict(body['data'])
                conservees = sorted(k for k, v in ancien_data.items()
                                    if k not in fusion and _porte_du_travail(v))
                instantane = None
                if conservees:
                    #  Instantané À LA SECONDE, en plus du filet quotidien qui,
                    #  lui, remonte à avant la première sync du jour.
                    instantane = _snapshot_avant_perte(ancien)
                    for k in conservees:
                        fusion[k] = ancien_data[k]
                _backup_desk()                       # snapshot quotidien AVANT écrasement
                persist.save_json('desk_data.json', {'ts': body['ts'], 'data': fusion})
            #  La conservation est DITE, pas silencieuse : un client qui perd
            #  son localStorage doit pouvoir s'en apercevoir.
            return jsonify({'ok': True, 'ts': body['ts'],
                            'conservees': conservees,
                            'instantane': instantane})
        with desk_lock:
            d = persist.load_json('desk_data.json', {}) or {}
        return jsonify(d)

    @bp.route('/api/desk/backups')
    def api_desk_backups():
        """Liste les instantanés du desk (restaurables), les deux familles.

        `quotidien` remonte à avant la première sync du jour ; `avant-perte` est
        pris à la seconde, au moment où un push allait faire disparaître des
        clés. Les lister ensemble n'est pas cosmétique : un instantané qu'aucune
        sortie ne nomme n'est pas un filet, c'est un fichier."""
        out = []
        for p in sorted(glob.glob(persist.cache_path('desk_backup_*.json')), reverse=True):
            nom = os.path.basename(p)
            out.append({'name': nom, 'date': nom[12:20], 'type': 'quotidien',
                        'size': os.path.getsize(p)})
        for p in sorted(glob.glob(persist.cache_path('desk_avantperte_*.json')),
                        reverse=True):
            nom = os.path.basename(p)
            out.append({'name': nom, 'date': nom[16:24], 'heure': nom[25:31],
                        'type': 'avant-perte', 'size': os.path.getsize(p)})
        return jsonify({'backups': out, 'keep': BACKUP_KEEP,
                        'keep_avant_perte': AVANT_PERTE_KEEP})

    @bp.route('/api/desk/restore', methods=['POST'])
    def api_desk_restore():
        """Restaure un snapshot quotidien → desk_data.json (ts=maintenant, donc
        tous les appareils re-tireront cette version). Nom STRICTEMENT validé."""
        name = str((request.get_json(force=True, silent=True) or {}).get('name') or '')
        import re
        #  Deux familles, une seule grammaire de chaque — le nom reste
        #  STRICTEMENT validé (aucun séparateur de chemin possible).
        if not (re.fullmatch(r'desk_backup_\d{8}\.json', name)
                or re.fullmatch(r'desk_avantperte_\d{8}-\d{6}\.json', name)):
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

    @bp.route('/api/journal/postmortem')
    def api_journal_postmortem():
        """POST-MORTEM du journal : stats réelles + drapeaux de discipline depuis les
        trades clôturés du desk (myTradesClosed + vxJournal). Descriptif, pas un
        conseil. Lecture seule — aucun ordre."""
        import json as _json
        from vertex.engines import postmortem as _pm
        blob = persist.load_json('desk_data.json', {}) or {}
        data = blob.get('data') or {}

        def _parse(key):
            raw = data.get(key)
            try:
                v = _json.loads(raw) if isinstance(raw, str) else (raw or [])
                return v if isinstance(v, list) else []
            except Exception:
                return []
        return jsonify(_pm.build(_parse('myTradesClosed'), _parse('vxJournal')))

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
        #  DERNIER RECOURS pour les actions. Sans lui, `results` revenait VIDE
        #  des que IBKR etait absent ou muet — et le client, qui exige une
        #  cotation par ligne, n'affichait aucun P&L alors que le prix etait
        #  deja en memoire. Verifie en local : POST {sym: ACN} rendait `{}`
        #  pendant que le scan portait ACN a 198,0.
        #  Le repli n'est PAS mis en cache : le cache sert les cotations
        #  broker, et y ranger un cours de scan le ferait servir a la place
        #  d'une vraie cotation pendant tout le TTL.
        combles = completer_par_repli(todo, out, cotation_repli)
        #  #779/G1 — POSITION_REFRESH était déclaré au registre des jobs mais
        #  n'avait AUCUN émetteur : la page Système l'affichait « jamais
        #  exécuté » alors qu'il tourne à chaque cotation du portefeuille. Il
        #  est à la demande, pas périodique — d'où `interval_s: None` côté
        #  registre : annoncer « prochaine dans ~45 s » aurait été une seconde
        #  invention.
        _sched.beat('POSITION_REFRESH', ok=True,
                    duration_ms=(time.time() - now) * 1000.0)
        return jsonify({'results': out, 'live': bool(ibkr_enabled),
                        'fallback_used': bool(combles), 'ts': int(now)})

    return bp


__all__ = ['make_blueprint', 'completer_par_repli', 'POSQ_TTL_S',
           'POSQ_MAX_POSITIONS']
