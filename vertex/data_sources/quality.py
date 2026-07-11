"""vertex.data_sources.quality — qualité agrégée d'un paquet analytique.

La qualité globale d'un paquet est celle de sa PIRE composante critique :
un spot frais ne rachète pas une chaîne d'options d'une autre séance.
"""
from __future__ import annotations

from .models import (
    AnalyticsPacket, QUALITY_FRESH, QUALITY_RECENT, QUALITY_STALE,
    QUALITY_EXPIRED, QUALITY_MISSING,
)

_ORDER = [QUALITY_FRESH, QUALITY_RECENT, QUALITY_STALE, QUALITY_EXPIRED, QUALITY_MISSING]

# Composantes dont la fraîcheur conditionne une décision ACTIONABLE.
CRITICAL_KINDS = ('spot', 'options')
# Composantes lentes par nature (un fondamental d'hier n'est pas un défaut).
SLOW_KINDS = ('fundamentals', 'catalysts', 'history')


def worst(*qualities: str) -> str:
    known = [q for q in qualities if q in _ORDER]
    if not known:
        return QUALITY_MISSING
    return _ORDER[max(_ORDER.index(q) for q in known)]


def grade_packet(packet: AnalyticsPacket) -> dict:
    """Met à jour packet.quality et retourne {'overall', 'warnings', 'actionable_allowed'}."""
    warnings: list[str] = []
    critical = []
    for kind in CRITICAL_KINDS:
        src = packet.sources.get(kind) or {}
        q = src.get('quality', QUALITY_MISSING)
        critical.append(q)
        if q in (QUALITY_STALE, QUALITY_EXPIRED):
            warnings.append(f'{kind}: donnée {q.lower()}')
        warnings.extend(src.get('warnings') or [])
    for kind in SLOW_KINDS:
        src = packet.sources.get(kind) or {}
        if src.get('fallback_used'):
            warnings.append(f'{kind}: fallback utilisé ({src.get("source", "?")})')
    overall = worst(*critical)
    actionable_allowed = overall in (QUALITY_FRESH, QUALITY_RECENT)
    packet.quality = {
        'overall': overall,
        'warnings': warnings,
        'actionable_allowed': actionable_allowed,
    }
    return packet.quality
