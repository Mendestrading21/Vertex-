"""vertex.positions.repository — chargement des positions par source (§5).

Sources : desk (myTrades → MANUAL, myTradesClosed → CLOSED), simulateur
legacy (simTrades → SIMULATED), IBKR (fetcher injecté, lecture seule).
IBKR hors ligne ⇒ les positions locales sont CONSERVÉES telles quelles —
jamais clôturées automatiquement (§6).
"""
from __future__ import annotations

import json

from vertex.positions.models import stock_position, option_position


def _parse_key(blob: dict, key: str):
    raw = (blob.get('data') or {}).get(key)
    try:
        v = json.loads(raw) if isinstance(raw, str) else (raw or [])
        return v if isinstance(v, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def _to_position(trade: dict, source: str) -> dict:
    ttype = str(trade.get('type') or 'STK').upper()
    if ttype in ('CALL', 'PUT') or trade.get('right') in ('C', 'P'):
        return option_position(trade, source)
    return stock_position(trade, source)


def load_positions(desk_blob: dict | None = None,
                   include_closed: bool = False) -> list[dict]:
    """Positions DÉCLARÉES (manuelles + simulées explicites), étiquetées.

    Lot 25 : le paramètre `ibkr_positions` et sa branche sont retirés — le
    portefeuille est déclaré par l'utilisateur, jamais lu chez le courtier
    (invariant market-data-only). Tous les appelants passaient déjà None."""
    out: list[dict] = []
    blob = desk_blob or {}

    for t in _parse_key(blob, 'myTrades'):
        if isinstance(t, dict):
            out.append(_to_position(t, 'MANUAL'))
    for t in _parse_key(blob, 'simTrades'):
        if isinstance(t, dict):
            p = _to_position(t, 'SIMULATED')
            p['is_real'] = False
            out.append(p)
    if include_closed:
        for t in _parse_key(blob, 'myTradesClosed'):
            if isinstance(t, dict):
                p = _to_position(t, 'MANUAL')
                p['status'] = p['lifecycle_status'] = 'CLOSED'
                out.append(p)

    return out


__all__ = ['load_positions']
