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


# Modèle par défaut : profondeur maximale pour l'analyste privé (cf .env.example
# et le runbook). VERTEX_AI_MODEL prime, ANTHROPIC_MODEL en repli — les deux ids
# sont valides ; l'utilisateur choisit (claude-opus-4-8 · claude-sonnet-5).
DEFAULT_MODEL = 'claude-opus-4-8'


def resolve_model() -> str:
    """Résolution unique du modèle IA (partagée provider + santé) — jamais deux
    sources de vérité divergentes entre /api/ai/status et l'appel réel."""
    return (os.environ.get('VERTEX_AI_MODEL', '').strip()
            or os.environ.get('ANTHROPIC_MODEL', '').strip()
            or DEFAULT_MODEL)


def model() -> str:
    return resolve_model()


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
