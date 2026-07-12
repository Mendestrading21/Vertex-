"""vertex.services.startup — séquence de démarrage ordonnée + rapport (§10).

Ordre : configuration → Claude → IBKR → TradingView → stockage → moteurs
déterministes → scheduler → flux live. Chaque étape produit un statut
honnête (CONNECTED/CONFIGURED/DEGRADED/OFFLINE/MISSING) — jamais « OK »
sans preuve. Le rapport est conservé en mémoire et exposé par
GET /api/system/startup-report.
"""
from __future__ import annotations

import os
import time

_REPORT: dict = {'ran': False}


def _step(name, fn):
    t0 = time.time()
    try:
        status, detail = fn()
    except Exception as e:  # jamais bloquant : le démarrage continue
        status, detail = 'ERROR', str(e)[:200]
    return {'step': name, 'status': status, 'detail': detail,
            'ms': round((time.time() - t0) * 1000)}


def run_startup_sequence(scan_state: dict) -> dict:
    """Exécute les vérifications — aucune ne bloque le lancement."""
    from vertex.app.config_validation import validate_config
    from vertex.app.config import IBKR_ENABLED, DEMO_MODE, READONLY
    from vertex.ai import health as ai_health

    steps = []

    def cfg():
        v = validate_config()
        s = v['_summary']
        st = 'CONFIGURED' if not s['invalid'] else 'DEGRADED'
        return st, f"{s['configured']} configurées · {s['missing']} absentes · {s['invalid']} invalides"
    steps.append(_step('configuration', cfg))

    steps.append(_step('claude', lambda: (
        ai_health.health()['status'],
        ai_health.health().get('note') or ai_health.health().get('model') or '')))

    def ibkr():
        if not IBKR_ENABLED:
            return 'OFFLINE', 'NO_IBKR=1 — marques desk/EOD, Greeks MODEL_ESTIMATE'
        return 'CONFIGURED', 'passerelle readonly=True — connexion au premier usage'
    steps.append(_step('ibkr', ibkr))

    def tv():
        secret = os.environ.get('TRADINGVIEW_WEBHOOK_SECRET',
                                os.environ.get('TRADINGVIEW_SECRET', ''))
        return ('CONFIGURED', 'webhook signé actif') if secret \
            else ('MISSING', 'secret absent — webhook 503 honnête')
    steps.append(_step('tradingview', tv))

    def storage():
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        ok = os.access(base, os.W_OK)
        return ('CONNECTED', 'desk_data.json + backups quotidiens') if ok \
            else ('DEGRADED', 'répertoire non inscriptible')
    steps.append(_step('storage', storage))

    def engines():
        from vertex.strategy import constitution
        p = constitution.load_profile()
        return 'READY', f'constitution {p.version} chargée · moteurs déterministes importés'
    steps.append(_step('engines', engines))

    def scheduler():
        try:
            from vertex.scheduler import registry
            return 'READY', f'{len(registry.jobs())} jobs enregistrés'
        except Exception:
            return 'DEGRADED', 'registre de jobs indisponible'
    steps.append(_step('scheduler', scheduler))

    def live():
        try:
            from vertex.services.live_stream import BROKER
            return 'READY', 'flux SSE prêt (repli polling côté client)'
        except Exception:
            return 'DEGRADED', 'SSE indisponible — polling seul'
    steps.append(_step('live_stream', live))

    _REPORT.clear()
    _REPORT.update({
        'ran': True, 'ts': time.time(),
        'readonly': READONLY, 'demo_mode': DEMO_MODE,
        'order_execution': 'disabled-by-design',
        'steps': steps,
        'ok': all(s['status'] not in ('ERROR',) for s in steps),
    })
    return dict(_REPORT)


def startup_report() -> dict:
    return dict(_REPORT)


__all__ = ['run_startup_sequence', 'startup_report']
