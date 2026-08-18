"""
vertex/app/routes/system.py — SANTÉ SYSTÈME & PWA (Blueprint, Ch. II).

Health-check, état système institutionnel (version, LECTURE SEULE, sources,
fraîcheur des caches, moteurs), et l'enveloppe PWA (favicon, manifeste, service
worker). Lit l'état partagé ; aucune donnée sensible ; jamais d'ordre.
"""

import time
from collections import deque

from flask import Blueprint, jsonify, Response, request

from vertex.ai import briefs as ai
from vertex.app.config import IBKR_ENABLED, DEMO_MODE
from vertex.app.state import scan_state
from vertex.data.universe import UNIVERSE
from vertex.data import constants as _vconst
from vertex.data.constants import BUILD
from vertex.services import status_service as _status_svc

bp = Blueprint('system', __name__)


@bp.route('/healthz')
@bp.route('/api/healthz')
def healthz():
    """Health check (Render) — toujours 200 si le process répond. Indique l'état
    du scan sans bloquer. Aucune donnée sensible, lecture seule."""
    return jsonify({
        'status': 'ok',
        'build': BUILD,
        'data_source': scan_state.get('source'),
        'ibkr_enabled': IBKR_ENABLED,
        'universe': len(UNIVERSE),
        'scanned': scan_state.get('scanned_n'),
        'last_scan': scan_state.get('updated'),
        'scan_age': round(time.time() - scan_state['scan_ts']) if scan_state.get('scan_ts') else None,
        'scan_error': scan_state.get('error'),
        'source_health': scan_state.get('source_health') or {'scan': 'UNKNOWN'},
        'vertex_ready': sum(1 for d in (scan_state.get('detail') or {}).values() if d.get('vertex')),
        'engines': ['scoring', 'pivots', 'committee', 'strategy', 'portfolio_risk',
                    'vertex', 'vertex_ml', 'validator'],
    }), 200


# ─── TÉLÉMÉTRIE D'ERREURS CLIENT (objectif 0-erreur : observer pour corriger) ───
# Les erreurs JS des navigateurs remontent ici (window.onerror du vx_kit).
# Borné (100 max, payloads tronqués) — aucune donnée sensible, lecture locale.
_CLIENT_ERRORS = deque(maxlen=100)


@bp.route('/api/client-log', methods=['POST'])
def client_log_post():
    b = request.get_json(force=True, silent=True) or {}
    _CLIENT_ERRORS.append({
        'ts': round(time.time()),
        'page': str(b.get('page') or '')[:120],
        'msg': str(b.get('msg') or '')[:300],
        'src': str(b.get('src') or '')[:160],
        'line': b.get('line') if isinstance(b.get('line'), int) else None,
    })
    return jsonify({'ok': True})


@bp.route('/api/client-log')
def client_log_get():
    """Journal des erreurs JS remontées par les navigateurs — diagnostic 0-erreur."""
    return jsonify({'count': len(_CLIENT_ERRORS), 'errors': list(_CLIENT_ERRORS)})


@bp.route('/api/system/startup-report')
def startup_report_ep():
    """Rapport de la séquence de démarrage (§10) — honnête, jamais « OK » sans preuve."""
    from vertex.services.startup import startup_report
    return jsonify(startup_report())


@bp.route('/api/system/config')
def config_validation_ep():
    """Statuts de configuration CONFIGURED/MISSING/INVALID — aucune valeur exposée."""
    from vertex.app.config_validation import validate_config
    return jsonify(validate_config())


@bp.route('/api/system/automations')
@bp.route('/api/system/jobs')
def automations_ep():
    """Registre des jobs de fond : statut, dernière exécution, cadence, erreurs.
    Alias canonique /api/system/jobs (§41)."""
    from vertex.scheduler import registry
    return jsonify({'jobs': registry.jobs()})


@bp.route('/api/system/connections')
def connections_ep():
    """État honnête des connexions (§41) — IBKR/TradingView/Claude/stockage/
    scheduler/live. Statuts canoniques, jamais plus favorables que la réalité ;
    aucun secret exposé."""
    from vertex.services import connections
    return jsonify(connections.snapshot(scan_state, ibkr_enabled=IBKR_ENABLED,
                                        demo_mode=DEMO_MODE))


@bp.route('/readyz')
def readyz():
    """Readiness (§41) — l'application est-elle prête à servir ? Distinct de
    /healthz (process vivant). 200 si prête, 503 sinon. Honnête : n'affirme
    READY que si les vérifications critiques passent."""
    checks = []

    def _chk(name, ok, detail=''):
        checks.append({'name': name, 'ok': bool(ok), 'detail': detail})
        return ok

    # 1. Configuration validable.
    try:
        from vertex.app.config_validation import validate_config
        cfg = validate_config()
        bad = [k for k, v in cfg.items() if isinstance(v, dict) and v.get('status') == 'INVALID']
        _chk('configuration', not bad, 'invalides: %s' % ','.join(bad) if bad else 'valide')
    except Exception:
        _chk('configuration', False, 'configuration_indisponible')

    # 2. Stratégie chargée (constitution canonique).
    try:
        from vertex.strategy import profile as _prof  # noqa: F401
        _chk('strategie', True, 'constitution disponible')
    except Exception:
        # tolérant : la stratégie peut vivre ailleurs — non bloquant.
        _chk('strategie', True, 'module stratégie optionnel')

    # 3. Stockage desk lisible.
    try:
        from vertex.services import persist
        persist.load_json('desk_data.json', {})
        _chk('stockage', True, 'desk lisible')
    except Exception:
        _chk('stockage', False, 'stockage_indisponible')

    # 4. READONLY effectif (invariant absolu).
    from vertex.app.config import READONLY
    _chk('readonly', bool(READONLY), 'lecture seule effective')

    ready = all(c['ok'] for c in checks)
    return jsonify({'ready': ready, 'readonly': True, 'checks': checks,
                    'build': BUILD}), (200 if ready else 503)


@bp.route('/api/system-status')
@bp.route('/api/system/status')
def system_status_ep():
    """État système institutionnel : version, LECTURE SEULE, sources, fraîcheur
    des caches, âge scan/options/fondamentaux/news, moteurs. Analyse uniquement."""
    detail = scan_state.get('detail') or {}
    ok = not scan_state.get('error') and bool(scan_state.get('rows'))
    last = scan_state.get('updated')
    engines = [
        _status_svc.engine_status('scanner', ok=ok, last_success=last, last_error=scan_state.get('error')),
        _status_svc.engine_status('scoring', ok=ok, last_success=last),
        _status_svc.engine_status('vertex', ok=any(d.get('vertex') for d in detail.values()), last_success=last),
        _status_svc.engine_status('physics', ok=any(d.get('physics') for d in detail.values()), last_success=last),
        _status_svc.engine_status('timeframe', ok=any(d.get('mtf') for d in detail.values()), last_success=last),
        _status_svc.engine_status('options', ok=bool(scan_state.get('options_board')), last_success=last),
        _status_svc.engine_status('committee', ok=bool(scan_state.get('committee')), last_success=last),
        _status_svc.engine_status('validator', ok=ok, last_success=last),
    ]
    thresholds = {'scan': _vconst.STALE_SCAN_SEC, 'options': _vconst.STALE_OPTIONS_SEC,
                  'fundamentals': 86400, 'news': 3600}
    return jsonify(_status_svc.build_system_status(
        scan_state, build=BUILD, readonly=True, ibkr_enabled=IBKR_ENABLED,
        demo_mode=DEMO_MODE, ai_on=ai.available(), thresholds=thresholds, engines=engines))


@bp.route('/favicon.ico')
@bp.route('/favicon.svg')
def favicon_ep():
    """Favicon Vertex : triangle cuivre sobre sur fond obsidienne, en SVG inline
    (aucune dépendance fichier → zéro 404 dans l'onglet du navigateur)."""
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
           "<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
           "<stop offset='0' stop-color='#e1a06e'/><stop offset='1' stop-color='#b96d3c'/>"
           "</linearGradient></defs>"
           "<rect width='64' height='64' rx='14' fill='#0b0e14'/>"
           "<path d='M32 15 L49 45 L15 45 Z' fill='url(#g)'/>"
           "</svg>")
    return Response(svg, mimetype='image/svg+xml',
                    headers={'Cache-Control': 'public, max-age=86400'})


@bp.route('/manifest.webmanifest')
def manifest_ep():
    """Manifeste PWA → permet « Ajouter à l'écran d'accueil » sur iPhone/Android
    et l'ouverture en plein écran comme une vraie app."""
    return jsonify({
        'name': 'Vertex — Cockpit IBKR',
        'short_name': 'Vertex',
        'description': "Cockpit d'analyse trading (analyse only).",
        'start_url': '/',
        'scope': '/',
        'display': 'standalone',
        'orientation': 'portrait-primary',
        'background_color': '#0b0e14',
        'theme_color': '#0b0e14',
        'icons': [
            {'src': '/static/icon-180.png', 'sizes': '180x180', 'type': 'image/png', 'purpose': 'any maskable'},
        ],
    })


_SW_JS = r"""
const CACHE='td-shell-v245';  // v245 SIGNAL OS · UNE PORTEE N'EST PAS UNE SORTIE. Reserve du lot 63 : « opts.freshness n'est passe par aucun appelant de VXCharts.card ». Je l'avais lue au grep — ce n'est pas une mesure. tools/mesurer_contrat_chart_shell.py compare les DEUX cotes du contrat du Chart Shell : passee-mais-jamais-lue (une page CROIT dire quelque chose et le composant l'ignore — la direction grave) et lue-mais-jamais-passee (du code mort). Deux temoins, un par direction, sur copie en memoire. RESULTAT RASSURANT sur la premiere : AUCUNE. Aucune page ne croit nommer une source, une conclusion ou une limite que le shell jetterait en silence. Sur la seconde, la conclusion du lot 581 est RENVERSEE : il concluait de freshnessBadge « un seul site d'appel, mais dans C.card — chaque carte-graphique du produit rend donc ce badge ». C'est l'inverse, mesure des deux cotes : opts.freshness n'etait passe par personne et la fonction rend '' sans valeur ; au navigateur, 4 cartes-graphiques peintes et 0 badge de fraicheur. Le lot 581 avait justement corrige « un compte d'appels n'est pas une surface d'ecran » et a commis aussitot son symetrique : une portee n'est pas une sortie. RETIRE plutot que cable, parce que l'age a DEJA un domicile sur la carte — la provenance en pied, peinte sur les 4 cartes mesurees ; cabler l'en-tete aurait cree un second domicile, le defaut meme corrige au lot 63 sur Opportunites. Le retrait est a rendu IDENTIQUE (mesure avant/apres : 4 cartes, 4 provenances, 0 badge) et supprime une des deux grammaires de fraicheur divergentes que le 581 relevait. TROIS ARTEFACTS DE MON PROPRE DECOUPAGE ARRETES AVANT PUBLICATION : `false` et `true` pris pour des options (valeurs par defaut d'une destructuration), `height` declaree ignoree (lue via chartHeightStyle(opts), un saut non suivi), et `coup` pris pour une cle — venu de « se lit d'un coup d'oeil », un COMMENTAIRE dont les apostrophes ASCII desynchronisaient le suivi des chaines. Puis une quatrieme, revelee par mutation : je masquais l'interieur des gabarits, or ${…} contient du CODE reel et c'est la que C.card compose tout son en-tete. Huit mutations, huit detectees.
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['/manifest.webmanifest','/static/icon-180.png','/static/vertex/css/fonts.css','/static/vertex/fonts/inter-var.woff2','/static/vertex/fonts/jetbrains-mono-var.woff2']).catch(()=>{})));});
self.addEventListener('activate',e=>{e.waitUntil((async()=>{const ks=await caches.keys();await Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim();})());});
self.addEventListener('fetch',e=>{
  const req=e.request; if(req.method!=='GET')return;
  const url=new URL(req.url); if(url.origin!==location.origin)return;
  const cacheable=(req.mode==='navigate'||url.pathname.startsWith('/static')||url.pathname==='/manifest.webmanifest');
  e.respondWith((async()=>{
    const cache=await caches.open(CACHE);
    try{
      // network-first : on prefere TOUJOURS le frais ; repli cache si reseau lent (cold start) ou hors-ligne
      const net=await Promise.race([fetch(req),new Promise((_,rej)=>setTimeout(()=>rej(new Error('to')),4500))]);
      if(net&&net.ok&&cacheable)cache.put(req,net.clone());
      return net;
    }catch(err){
      const c=(await cache.match(req))||(req.mode==='navigate'?await cache.match('/'):null);
      return c||fetch(req);
    }
  })());
});
"""


@bp.route('/sw.js')
def service_worker():
    """Service worker PWA (network-first + repli cache) — masque les cold starts
    Render. ⛔ Aucune donnee perso ici (favoris/notes restent en localStorage)."""
    return Response(_SW_JS, mimetype='application/javascript',
                    headers={'Service-Worker-Allowed': '/', 'Cache-Control': 'no-cache'})


__all__ = ['bp']
