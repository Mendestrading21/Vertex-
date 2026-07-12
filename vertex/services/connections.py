"""vertex.services.connections — état honnête des connexions (§9/§41).

Consolide l'état des intégrations (IBKR, TradingView, Claude, stockage,
scheduler, flux live) en statuts CANONIQUES, jamais plus favorables que la
réalité. Configuré ≠ connecté ; clé présente ≠ testée. Aucune valeur de secret
n'est exposée. Lecture seule.
"""
from __future__ import annotations

import os

# Vocabulaire canonique (§2).
NOT_IMPLEMENTED = 'NOT_IMPLEMENTED'
CONFIGURATION_MISSING = 'CONFIGURATION_MISSING'
BLOCKED = 'BLOCKED'
OFFLINE = 'OFFLINE'
DEGRADED = 'DEGRADED'
STALE = 'STALE'
DELAYED = 'DELAYED'
FALLBACK = 'FALLBACK'
DEMO = 'DEMO'
LOADING = 'LOADING'
READY = 'READY'
LIVE = 'LIVE'
ERROR = 'ERROR'

CANONICAL_STATUSES = (NOT_IMPLEMENTED, CONFIGURATION_MISSING, BLOCKED, OFFLINE,
                      DEGRADED, STALE, DELAYED, FALLBACK, DEMO, LOADING, READY,
                      LIVE, ERROR)


def _conn(name, status, *, configured, detail, impact='', action=''):
    return {'name': name, 'status': status, 'configured': bool(configured),
            'detail': detail, 'impact': impact, 'action': action}


def _env(name):
    return bool(os.environ.get(name, '').strip())


def snapshot(scan_state, *, ibkr_enabled=False, demo_mode=False):
    """État consolidé des connexions — chaque statut reflète la réalité observée."""
    conns = []

    # IBKR : configuré ≠ connecté ; on ne déclare jamais LIVE sans preuve live.
    if not ibkr_enabled:
        conns.append(_conn('IBKR', OFFLINE, configured=False,
                           detail='IBKR non activé (aucune session TWS/Gateway détectée).',
                           impact='P&L/Greeks broker indisponibles ; cotations en secours ou démo.',
                           action='Lancer TWS/Gateway en lecture seule et définir IBKR_PORT.'))
    else:
        # Activé ≠ connecté : on ne déclare LIVE/DELAYED que sur preuve d'une
        # session ; sinon OFFLINE honnête (§2/§10 — jamais plus favorable).
        live = bool(scan_state.get('ibkr_live'))
        connected = bool(scan_state.get('ibkr_connected'))
        if live:
            st, det = LIVE, 'Session IBKR active, données temps réel (lecture seule).'
        elif connected:
            st, det = DELAYED, 'Session IBKR active, données différées (lecture seule).'
        else:
            st, det = OFFLINE, 'IBKR configuré mais aucune session active confirmée (jamais présenté comme connecté sans preuve).'
        conns.append(_conn('IBKR', st, configured=True, detail=det,
                           impact='Lecture seule stricte (readonly=True).' if (live or connected)
                           else 'P&L/Greeks broker indisponibles tant que la session n\'est pas confirmée.',
                           action='' if (live or connected) else 'Vérifier TWS/Gateway et le port IBKR.'))

    # TradingView : dépend du secret webhook.
    tv_ok = _env('TRADINGVIEW_WEBHOOK_SECRET') or _env('TRADINGVIEW_SECRET')
    conns.append(_conn('TradingView', READY if tv_ok else CONFIGURATION_MISSING,
                       configured=tv_ok,
                       detail=('Webhook signé activé (/api/tradingview/webhook).' if tv_ok
                               else 'Webhook désactivé — 503 honnête, aucun signal inventé.'),
                       impact='' if tv_ok else 'Les alertes TradingView ne sont pas reçues.',
                       action='' if tv_ok else 'Définir TRADINGVIEW_WEBHOOK_SECRET.'))

    # Claude : clé présente → runtime dispo ; sinon fallback déterministe.
    try:
        from vertex.ai import briefs as _ai
        ai_on = bool(_ai.available())
    except Exception:
        ai_on = False
    conns.append(_conn('Claude', READY if ai_on else FALLBACK, configured=ai_on,
                       detail=('Runtime IA disponible (explications enrichies).' if ai_on
                               else 'Aucune clé — synthèse déterministe des moteurs (fallback).'),
                       impact='' if ai_on else 'Explications servies par les moteurs, pas par l\'IA.',
                       action='' if ai_on else 'Définir ANTHROPIC_API_KEY pour activer l\'IA.'))

    # Stockage desk : lisible = READY.
    try:
        from vertex.services import persist
        persist.load_json('desk_data.json', {})
        storage_ok = True
    except Exception:
        storage_ok = False
    conns.append(_conn('Stockage', READY if storage_ok else ERROR, configured=True,
                       detail=('Desk lisible (desk_data.json + backups).' if storage_ok
                               else 'Stockage desk inaccessible.'),
                       impact='' if storage_ok else 'Synchronisation des données utilisateur compromise.',
                       action='' if storage_ok else 'Vérifier VERTEX_DATA_DIR et les permissions.'))

    # Scheduler : jobs enregistrés + au moins un battement.
    try:
        from vertex.scheduler import registry
        jobs = registry.jobs()
        ran = sum(1 for j in jobs if j.get('runs'))
        sched_status = READY if jobs and ran else (DEGRADED if jobs else OFFLINE)
        conns.append(_conn('Scheduler', sched_status, configured=True,
                           detail='%d jobs enregistrés, %d avec au moins une exécution.' % (len(jobs), ran),
                           impact='' if ran else 'Aucun job n\'a encore tourné.',
                           action=''))
    except Exception:
        conns.append(_conn('Scheduler', ERROR, configured=True,
                           detail='Registre des jobs indisponible.', impact='Automatisations non observables.'))

    # Flux live (SSE) : présence du service.
    try:
        from vertex.services import live_stream  # noqa: F401
        conns.append(_conn('Live Stream', READY, configured=True,
                           detail='SSE disponible (/api/live/events).',
                           impact='', action=''))
    except Exception:
        conns.append(_conn('Live Stream', FALLBACK, configured=True,
                           detail='SSE indisponible — repli polling.', impact='Mises à jour moins réactives.'))

    if demo_mode:
        for c in conns:
            c['demo'] = True
    return {'connections': conns, 'demo': bool(demo_mode),
            'readonly': True}


__all__ = ['snapshot', 'CANONICAL_STATUSES']
