"""vertex/app/routes/ai_api.py — API du « cerveau Claude » (§28).

Expose l'enrichissement Claude+web : instantané daté, santé honnête, et un
rafraîchissement à la demande (« Mettre à jour avec Claude »). Lecture seule ;
aucun ordre. Sans clé ANTHROPIC_API_KEY → statut MISSING, aucune donnée estimée
(l'app le dit franchement plutôt que d'inventer).
"""
from __future__ import annotations

import threading

from flask import Blueprint, jsonify

from vertex.app.state import scan_state
from vertex.ai import enrichment as _enrich
from vertex.ai import health as _health

bp = Blueprint('ai_api', __name__)

_refresh_lock = threading.Lock()
_refreshing = {'on': False}


def enrich_symbols(limit=None):
    """Titres à enrichir : scan (rows) + positions déclarées, dédupliqués."""
    syms: list[str] = []
    seen = set()

    def _add(s):
        s = str(s or '').upper().strip()
        if s and '.' not in s and s not in seen:
            seen.add(s)
            syms.append(s)

    for r in (scan_state.get('rows') or []):
        _add(r.get('symbol'))
    try:                                     # positions déclarées (localStorage synchronisé)
        import json
        from vertex.services import persist
        blob = persist.load_json('desk_data.json', {}) or {}
        raw = (blob.get('data') or {}).get('myTrades')
        for t in (json.loads(raw) if isinstance(raw, str) else (raw or [])):
            if isinstance(t, dict):
                _add(t.get('symbol') or t.get('ticker'))
    except Exception:
        pass
    return syms[:(limit or _enrich.MAX_SYMBOLS)]


def _run_refresh():
    try:
        _enrich.run(enrich_symbols())
    finally:
        with _refresh_lock:
            _refreshing['on'] = False


def start_background_enrichment():
    """Lance un enrichissement en tâche de fond (idempotent). Non bloquant."""
    with _refresh_lock:
        if _refreshing['on']:
            return False
        _refreshing['on'] = True
    threading.Thread(target=_run_refresh, daemon=True).start()
    return True


@bp.route('/api/ai/enrichment')
def ai_enrichment():
    """Instantané complet Claude+web (cotations/actualités étiquetées provenance)."""
    return jsonify(_enrich.load_snapshot())


@bp.route('/api/ai/status')
def ai_status():
    """Santé du cerveau Claude : configuration + dernier enrichissement observé."""
    st = _enrich.status()
    st['health'] = _health.health()
    st['refreshing'] = _refreshing['on']
    return jsonify(st)


@bp.route('/api/ai/refresh', methods=['POST'])
def ai_refresh():
    """Déclenche « Mettre à jour avec Claude » (tâche de fond). 202 = accepté."""
    started = start_background_enrichment()
    return jsonify({'accepted': started, 'refreshing': True,
                    'note': ('Enrichissement Claude+web lancé.' if started
                             else 'Un enrichissement est déjà en cours.')}), 202


__all__ = ['bp', 'enrich_symbols', 'start_background_enrichment']
