"""
vertex/app/routes/auth.py — VERROU D'ACCÈS (Blueprint, Ch. II · Ch. XV).

Le code d'entrée optionnel de VERTEX, sorti du monolithe : page /login,
/logout, et la garde globale (`before_app_request`) qui protège toute l'app
quand VERTEX_CODE est défini. Anti-force-brute par IP (verrou progressif),
session signée 30 jours, comparaison en temps constant (hmac.compare_digest).

Le code d'entrée est INJECTÉ à la construction (`make_blueprint(code=...)`) —
aucune lecture d'environnement ici, la source unique reste vertex/app/config.
Chaque instance porte son propre compteur d'échecs (testable en isolation).

Lecture seule, analyse uniquement — ce module ne protège que des pages
d'analyse ; il n'existe aucun ordre à protéger.
"""

import hmac
import time
from html import escape

from flask import Blueprint, jsonify, redirect, request, session

# Chemins publics même verrou actif : le verrou lui-même, la santé, la PWA.
# Le webhook TradingView est public par NÉCESSITÉ : les serveurs TV n'ont pas
# de session — il porte sa PROPRE authentification par secret (hmac.compare_digest,
# anti-replay, dédup). Sans cette exemption, le verrou VERTEX_CODE rendrait le
# webhook injoignable (401) et la fonctionnalité serait morte dès le verrou actif.
PUBLIC_PATHS = {'/login', '/logout', '/healthz', '/api/healthz',
                '/favicon.ico', '/favicon.svg', '/manifest.webmanifest', '/sw.js',
                '/api/tradingview/webhook'}

# Flux de données hors /api/ : répondent 401 JSON (le JS le gère) au lieu
# d'une redirection HTML vers le verrou.
DATA_PATHS = ('/scan', '/quotes', '/cal-feed', '/news-feed', '/weekly-feed')


def _safe_next(raw):
    """Cible de redirection sûre : chemin local uniquement.

    Refuse les URLs absolues et les schémas relatifs au protocole ('//evil.com')
    — sinon /login?next=//evil.com devient une redirection ouverte.
    """
    nxt = (raw or '/').strip()
    if not nxt.startswith('/') or nxt.startswith('//'):
        return '/'
    return nxt


def make_blueprint(*, code):
    """Construit le Blueprint du verrou. `code` vide/None → verrou inactif."""
    bp = Blueprint('auth', __name__)
    auth_on = bool(code)
    login_fails = {}    # ip -> [nb_essais, bloqué_jusquà_ts]

    def _client_ip():
        # ⚠️ Sécurité anti-bypass du lockout : X-Forwarded-For est fourni par le CLIENT
        # (sa valeur la plus à gauche est librement usurpable → essais illimités).
        # Derrière UN proxy de confiance (Render), la seule valeur fiable est la plus
        # à DROITE (ajoutée par le proxy). En local, remote_addr suffit.
        xf = [p.strip() for p in (request.headers.get('X-Forwarded-For') or '').split(',') if p.strip()]
        return (xf[-1] if xf else '') or request.remote_addr or '?'

    @bp.before_app_request
    def _auth_gate():
        if not auth_on:
            return None
        p = request.path
        if p in PUBLIC_PATHS or p.startswith('/static'):
            return None
        if session.get('vx_ok'):
            return None
        # Non authentifié : les appels de données répondent 401 (le JS le gère),
        # les pages redirigent vers le verrou.
        if p.startswith('/api/') or p in DATA_PATHS:
            return jsonify({'error': 'auth', 'login': '/login'}), 401
        return redirect('/login?next=' + p)

    def _login_page(msg='', locked=False):
        err = ('<div class="err">' + msg + '</div>') if msg else ''
        nxt = escape(_safe_next(request.args.get('next')), quote=True)
        return ('<!doctype html><html lang="fr"><head><meta charset="utf-8">'
          '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
          '<meta name="theme-color" content="#0a0b0d"><title>VERTEX · Accès</title>'
          '<style>'
          '*{box-sizing:border-box}html,body{margin:0;height:100%}'
          'body{background:radial-gradient(130% 60% at 50% -10%,rgba(222,227,237,.06),transparent 60%),linear-gradient(180deg,#0e0f12,#070809);'
          'color:#f3f5f8;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;display:flex;align-items:center;justify-content:center;padding:20px}'
          '.card{width:100%;max-width:360px;background:linear-gradient(180deg,rgba(30,33,38,.72),rgba(17,19,23,.72));'
          '-webkit-backdrop-filter:blur(16px) saturate(1.05);backdrop-filter:blur(16px) saturate(1.05);border:1px solid rgba(222,227,237,.14);'
          'border-radius:20px;padding:32px 24px;box-shadow:0 40px 90px -30px rgba(0,0,0,.9),inset 0 1px 0 rgba(255,255,255,.06);text-align:center}'
          '.mark{width:56px;height:56px;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;font-size:24px;'
          'background:linear-gradient(135deg,rgba(222,227,237,.12),rgba(222,227,237,.03));border:1px solid rgba(222,227,237,.22);'
          'border-radius:16px;color:#e6e9ee;box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}'
          '.t{font-size:20px;font-weight:900;letter-spacing:2px}.t b{color:#c9cdd4}'
          '.s{font-size:12px;color:#828892;margin:6px 0 20px}'
          'input{width:100%;background:rgba(255,255,255,.03);border:1px solid rgba(222,227,237,.12);color:#f3f5f8;border-radius:12px;'
          'padding:14px 16px;font-size:20px;text-align:center;letter-spacing:5px;font-weight:700;outline:none}'
          'input:focus{border-color:rgba(201,205,212,.5);box-shadow:0 0 0 3px rgba(201,205,212,.14)}'
          'button{width:100%;margin-top:12px;background:linear-gradient(135deg,#3a3f47,#23262c);color:#eef0f3;border:1px solid rgba(222,227,237,.18);'
          'border-radius:12px;padding:14px;font-weight:800;font-size:15px;letter-spacing:.5px;cursor:pointer;box-shadow:0 8px 24px -10px rgba(0,0,0,.6)}'
          'button:hover{filter:brightness(1.12)}button:disabled{opacity:.5;cursor:not-allowed}'
          '.err{background:rgba(237,101,92,.1);border:1px solid rgba(237,101,92,.4);color:#f0b0b0;font-size:13px;'
          'border-radius:12px;padding:10px 12px;margin-bottom:16px}'
          '.foot{font-size:10px;color:#5c626b;margin-top:16px;letter-spacing:1px}'
          '</style></head><body>'
          '<form class="card" method="POST" action="/login?next=' + nxt + '">'
          '<div class="mark">▲</div><div class="t">VERTEX<b>.</b></div>'
          '<div class="s">🔒 Accès protégé — entre ton code</div>'
          + err +
          '<input name="code" type="password" inputmode="numeric" autocomplete="current-password" '
          'placeholder="• • • •" autofocus ' + ('disabled' if locked else '') + '>'
          '<button type="submit"' + (' disabled' if locked else '') + '>Entrer →</button>'
          '<div class="foot">VERTEX TRADING DESK · ANALYSE ONLY</div>'
          '</form></body></html>')

    @bp.route('/login', methods=['GET', 'POST'])
    def login_page():
        if not auth_on:
            return redirect('/')
        ip = _client_ip()
        now = time.time()
        st = login_fails.get(ip, [0, 0])
        nxt = _safe_next(request.args.get('next'))
        if request.method == 'POST':
            if st[1] > now:
                return _login_page("Trop d'essais. Réessaie dans %ds." % int(st[1] - now), locked=True)
            attempt = (request.form.get('code') or '').strip()
            if code and hmac.compare_digest(attempt, code):
                session.permanent = True
                session['vx_ok'] = True
                login_fails.pop(ip, None)
                return redirect(nxt)
            st[0] += 1
            lock = min(300, 15 * (st[0] - 4)) if st[0] >= 5 else 0   # verrou progressif après 5 essais
            st[1] = now + lock
            login_fails[ip] = st
            return _login_page('Code incorrect.' + (' Bloqué %ds.' % lock if lock else ''), locked=lock > 0)
        if session.get('vx_ok'):
            return redirect(nxt)
        return _login_page()

    @bp.route('/logout')
    def logout_page():
        session.clear()
        return redirect('/login')

    return bp


__all__ = ['make_blueprint', 'PUBLIC_PATHS', 'DATA_PATHS']
