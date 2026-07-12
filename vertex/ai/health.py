"""vertex.ai.health — état de santé du runtime Claude (§10).

Aucun appel réseau spontané : la santé se déduit de la configuration et du
dernier appel réel (audit). Statuts canoniques : CONFIGURED / MISSING /
CONNECTED / DEGRADED / OFFLINE — jamais « connecté » sans preuve.
"""
from __future__ import annotations

import os
import time

_LAST = {'ok_ts': None, 'err_ts': None, 'error': None}


def record_success() -> None:
    _LAST['ok_ts'] = time.time()
    _LAST['error'] = None


def record_failure(err: str) -> None:
    _LAST['err_ts'] = time.time()
    _LAST['error'] = str(err)[:200]


def configured() -> bool:
    return bool(os.environ.get('ANTHROPIC_API_KEY', '').strip())


def model() -> str:
    return os.environ.get('ANTHROPIC_MODEL', '').strip() or 'claude-sonnet-5'


def health() -> dict:
    """Résumé honnête : configuration + dernier appel réel observé."""
    if not configured():
        return {'status': 'MISSING', 'configured': False, 'model': None,
                'fallback': 'déterministe (moteurs)',
                'note': 'ANTHROPIC_API_KEY absente — synthèse déterministe servie.'}
    st = 'CONFIGURED'
    if _LAST['ok_ts'] and (not _LAST['err_ts'] or _LAST['ok_ts'] >= _LAST['err_ts']):
        st = 'CONNECTED'
    elif _LAST['err_ts']:
        st = 'DEGRADED'
    return {'status': st, 'configured': True, 'model': model(),
            'last_success': _LAST['ok_ts'], 'last_error': _LAST['error'],
            'fallback': 'déterministe (moteurs)'}
