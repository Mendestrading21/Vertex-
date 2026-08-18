"""Validation bornée des entrées HTTP analytiques Vertex."""
from __future__ import annotations

import re

_SYMBOL = re.compile(r'^[A-Z0-9][A-Z0-9.\-]{0,11}$')


def symbol(value):
    """Retourne le symbole canonique ou ``None`` ; aucune troncature implicite."""
    candidate = str(value or '').strip().upper()
    return candidate if _SYMBOL.fullmatch(candidate) else None


__all__ = ['symbol']
