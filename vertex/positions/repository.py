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
                   ibkr_positions: list | None = None,
                   include_closed: bool = False) -> list[dict]:
    """Toutes les positions, toutes sources — chaque entrée étiquetée."""
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

    for raw in (ibkr_positions or []):
        if not isinstance(raw, dict):
            continue
        qty = raw.get('qty') or raw.get('position')
        trade = {'id': f"IBKR:{raw.get('conId') or raw.get('sym')}",
                 'sym': raw.get('sym') or raw.get('symbol'),
                 'type': ('CALL' if raw.get('right') == 'C' else
                          'PUT' if raw.get('right') == 'P' else 'STK'),
                 'right': raw.get('right'), 'strike': raw.get('strike'),
                 'exp': raw.get('exp'), 'qty': qty,
                 'cost': (raw.get('avgCost') or 0) * (qty or 0)
                         if raw.get('avgCost') is not None and qty else None,
                 'currency': raw.get('currency') or 'USD',
                 'account_id': raw.get('account'),
                 'conid': raw.get('conId')}
        p = _to_position(trade, 'IBKR')
        p['source_reference'] = f"ibkr:{raw.get('account') or ''}"
        out.append(p)
    return out


__all__ = ['load_positions']
