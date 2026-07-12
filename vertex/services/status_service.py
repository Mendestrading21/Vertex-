"""
vertex/services/status_service.py — État système institutionnel de VERTEX.

Construit la réponse de /api/system-status : version, confirmation lecture seule,
état IBKR, sources de données, fraîcheur des caches, âge du scan / options /
fondamentaux / news, état des workers et des moteurs, erreurs et avertissements.

Aucune dépendance sur Flask : fonction pure (scan_state + contexte) → dict.
"""

from datetime import datetime, timezone


def _age_seconds(ts):
    """Âge en secondes depuis un timestamp epoch (ou None)."""
    if not ts:
        return None
    try:
        return max(0, int(datetime.now(timezone.utc).timestamp() - float(ts)))
    except Exception:
        return None


def _freshness(age, stale_after):
    """Classe une fraîcheur : fresh / stale / unknown."""
    if age is None:
        return 'unknown'
    return 'fresh' if age <= stale_after else 'stale'


def build_system_status(scan_state, *, build, readonly, ibkr_enabled, demo_mode,
                        ai_on=False, thresholds=None, engines=None):
    """Assemble le rapport d'état système complet.

    scan_state : l'état de scan partagé de l'application.
    thresholds : dict des seuils de fraîcheur (secondes).
    engines    : liste de dicts {name, status, last_success, last_error, latency_ms}.
    """
    th = thresholds or {}
    scan_age = _age_seconds(scan_state.get('scan_ts'))
    opt_age = _age_seconds(scan_state.get('options_ts'))
    fund_age = _age_seconds((scan_state.get('fundamentals') or {}).get('ts')
                            if isinstance(scan_state.get('fundamentals'), dict) else None)
    news_age = _age_seconds((scan_state.get('news') or {}).get('ts')
                            if isinstance(scan_state.get('news'), dict) else None)

    rows = scan_state.get('rows') or []
    err = scan_state.get('error')
    warnings = []
    if scan_age is not None and scan_age > th.get('scan', 900):
        warnings.append(f'scan rassis ({scan_age}s)')
    if not rows:
        warnings.append('aucun titre scanné pour l\'instant')

    status = 'ok'
    if err:
        status = 'degraded'
    elif warnings:
        status = 'warming'

    return {
        'app': status,
        'build': build,
        # Invariant de sûreté affirmé explicitement dans la réponse.
        'readonly': bool(readonly),
        'analysis_only': True,
        'order_execution': 'disabled-by-design',
        'mode': 'demo' if demo_mode else ('ibkr' if ibkr_enabled else 'cloud'),
        'data_sources': {
            # Honnêteté §2/§10 : « activé » (config) ≠ « connecté » (preuve socket).
            # On ne renvoie un état connecté que si la session live est confirmée.
            'ibkr': (('connected-live' if scan_state.get('ibkr_live')
                      else 'connected-delayed' if scan_state.get('ibkr_connected')
                      else 'enabled-idle')
                     if ibkr_enabled else 'disabled'),
            'market_data': 'demo' if demo_mode else 'yfinance/ibkr',
            'ai': 'on' if ai_on else 'off',
        },
        'freshness': {
            'scan': {'age_s': scan_age, 'state': _freshness(scan_age, th.get('scan', 900))},
            'options': {'age_s': opt_age, 'state': _freshness(opt_age, th.get('options', 1800))},
            'fundamentals': {'age_s': fund_age, 'state': _freshness(fund_age, th.get('fundamentals', 86400))},
            'news': {'age_s': news_age, 'state': _freshness(news_age, th.get('news', 3600))},
        },
        'scan': {
            'symbols': len(rows),
            'last_scan': scan_state.get('updated'),
            'error': err,
        },
        'engines': engines or [],
        'warnings': warnings,
        'ts': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }


def engine_status(name, ok=True, last_success=None, last_error=None, latency_ms=None):
    """Fabrique l'état standard d'un moteur pour le rapport système."""
    return {
        'name': name,
        'status': 'ok' if ok else 'error',
        'last_success': last_success,
        'last_error': last_error,
        'latency_ms': latency_ms,
    }


__all__ = ['build_system_status', 'engine_status']
