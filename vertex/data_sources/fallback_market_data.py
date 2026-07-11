"""vertex.data_sources.fallback_market_data — repli EOD honnête.

Dernier échelon de la priorité §12 : données de fin de journée (téléchargement
différé type yfinance/Stooq déjà présent dans l'app), TOUJOURS marquées
fallback_used=True et source_mode=EOD. Aucune donnée inventée : indisponible
reste indisponible.
"""
from __future__ import annotations

from .models import SOURCE_SECONDARY, SOURCE_FALLBACK_EOD, MODE_EOD, MODE_DELAYED, ProvenancedValue
from .provenance import stamp


def eod_close_to_provenanced(symbol: str, close: float | None,
                             session_date: str = '') -> ProvenancedValue:
    """Convertit une clôture EOD en valeur tracée (fallback explicite)."""
    if close is None:
        pv = ProvenancedValue(source=SOURCE_FALLBACK_EOD)
        pv.warnings.append(f'{symbol}: clôture EOD indisponible')
        return pv
    ts = f'{session_date}T21:00:00Z' if session_date else ''
    pv = stamp(value={'price': float(close), 'symbol': symbol.upper()},
               source=SOURCE_FALLBACK_EOD, source_mode=MODE_EOD,
               timestamp=ts, fallback_used=True)
    return pv


def secondary_quote_to_provenanced(symbol: str, price: float | None,
                                   timestamp: str = '') -> ProvenancedValue:
    """Fournisseur secondaire validé (différé ~15 min) — jamais confondu avec du live."""
    if price is None:
        pv = ProvenancedValue(source=SOURCE_SECONDARY)
        pv.warnings.append(f'{symbol}: cotation secondaire indisponible')
        return pv
    return stamp(value={'price': float(price), 'symbol': symbol.upper()},
                 source=SOURCE_SECONDARY, source_mode=MODE_DELAYED,
                 timestamp=timestamp, fallback_used=True)
