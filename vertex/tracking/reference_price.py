"""vertex.tracking.reference_price — choix honnête du prix de référence (§14).

Actions : mid valide → last récent → close (marché fermé) → fallback identifié.
Options : mid valide → mark broker → last (avec avertissement) → DATA_REQUIRED.
On n'utilise JAMAIS l'ask comme prix d'achat simulé sans le signaler. Une
référence absente rend `None` + statut DATA_REQUIRED, jamais un zéro.
"""
from __future__ import annotations

from .models import (REF_MID, REF_LAST, REF_CLOSE, REF_MARK, REF_FALLBACK,
                     ST_DATA_REQUIRED, ST_ACTIVE)


def _pos(x):
    try:
        x = float(x)
        return x if x > 0 else None
    except (TypeError, ValueError):
        return None


def _mid(quote):
    bid, ask = _pos(quote.get('bid')), _pos(quote.get('ask'))
    if bid and ask and ask >= bid:
        return round((bid + ask) / 2, 4)
    return _pos(quote.get('mid'))


def pick_stock_reference(quote, *, market_open=True):
    """Rend (price, type, source, status, warnings) pour une action/ETF."""
    quote = quote or {}
    warnings = []
    src = quote.get('source') or ''
    mid = _mid(quote)
    if mid is not None:
        return mid, REF_MID, src, ST_ACTIVE, warnings
    last = _pos(quote.get('last')) or _pos(quote.get('price'))
    if last is not None and market_open:
        return last, REF_LAST, src, ST_ACTIVE, warnings
    close = _pos(quote.get('close'))
    if close is not None and not market_open:
        return close, REF_CLOSE, src, ST_ACTIVE, warnings
    # Repli identifié (dernier prix connu, marché fermé sans close officiel…).
    fb = last if last is not None else close
    if fb is not None:
        warnings.append('référence de repli (ni mid ni close officiel)')
        return fb, REF_FALLBACK, src, ST_ACTIVE, warnings
    return None, '', src, ST_DATA_REQUIRED, ['aucune référence de prix valide']


def pick_option_reference(quote):
    """Rend (price, type, source, status, warnings) pour une option.

    mid → mark → last (avertissement) → DATA_REQUIRED. Jamais l'ask seul."""
    quote = quote or {}
    warnings = []
    src = quote.get('source') or ''
    mid = _mid(quote)
    if mid is not None:
        return mid, REF_MID, src, ST_ACTIVE, warnings
    mark = _pos(quote.get('mark'))
    if mark is not None:
        return mark, REF_MARK, src, ST_ACTIVE, warnings
    last = _pos(quote.get('last'))
    if last is not None:
        warnings.append('référence = dernier échange (last) — pas un mid/mark fiable')
        return last, REF_LAST, src, ST_ACTIVE, warnings
    return None, '', src, ST_DATA_REQUIRED, ['aucune référence (mid/mark/last) — suivi impossible']


__all__ = ['pick_stock_reference', 'pick_option_reference']
