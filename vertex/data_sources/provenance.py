"""vertex.data_sources.provenance — horodatage et fraîcheur des valeurs."""
from __future__ import annotations

import datetime as _dt

from .models import (
    ProvenancedValue, QUALITY_FRESH, QUALITY_RECENT, QUALITY_STALE,
    QUALITY_EXPIRED, QUALITY_MISSING, MODE_LIVE, MODE_DELAYED, MODE_EOD,
    SOURCE_UNAVAILABLE, utc_now_iso,
)

# Seuils de fraîcheur (secondes) par mode de source.
FRESHNESS_THRESHOLDS = {
    MODE_LIVE: {'fresh': 30, 'recent': 300, 'stale': 3600},
    MODE_DELAYED: {'fresh': 1200, 'recent': 3600, 'stale': 4 * 3600},
    MODE_EOD: {'fresh': 24 * 3600, 'recent': 3 * 24 * 3600, 'stale': 7 * 24 * 3600},
}
_DEFAULT_THRESHOLDS = FRESHNESS_THRESHOLDS[MODE_DELAYED]


def parse_iso(ts: str) -> _dt.datetime | None:
    if not ts:
        return None
    try:
        return _dt.datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except ValueError:
        return None


def age_seconds(timestamp: str, now: _dt.datetime | None = None) -> float | None:
    dt = parse_iso(timestamp)
    if dt is None:
        return None
    now = now or _dt.datetime.now(_dt.timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_dt.timezone.utc)
    return max(0.0, (now - dt).total_seconds())


def grade_quality(age: float | None, source_mode: str) -> str:
    if age is None:
        return QUALITY_MISSING
    th = FRESHNESS_THRESHOLDS.get(source_mode, _DEFAULT_THRESHOLDS)
    if age <= th['fresh']:
        return QUALITY_FRESH
    if age <= th['recent']:
        return QUALITY_RECENT
    if age <= th['stale']:
        return QUALITY_STALE
    return QUALITY_EXPIRED


def stamp(value, source: str, source_mode: str, timestamp: str = '',
          fallback_used: bool = False, now: _dt.datetime | None = None) -> ProvenancedValue:
    """Construit une ProvenancedValue complète (âge + qualité calculés)."""
    if value is None:
        return ProvenancedValue(source=source or SOURCE_UNAVAILABLE,
                                warnings=['valeur absente'])
    timestamp = timestamp or utc_now_iso()
    age = age_seconds(timestamp, now=now)
    pv = ProvenancedValue(
        value=value, source=source, source_mode=source_mode,
        timestamp=timestamp, age_seconds=age,
        quality=grade_quality(age, source_mode), fallback_used=fallback_used,
    )
    if fallback_used:
        pv.warnings.append(f'fallback utilisé ({source}/{source_mode})')
    if pv.quality in (QUALITY_STALE, QUALITY_EXPIRED):
        pv.warnings.append(f'donnée {pv.quality.lower()} (âge {int(age or 0)}s)')
    return pv


def refresh_quality(pv: ProvenancedValue, now: _dt.datetime | None = None) -> ProvenancedValue:
    """Recalcule âge/qualité d'une valeur existante (les données vieillissent)."""
    pv.age_seconds = age_seconds(pv.timestamp, now=now)
    pv.quality = grade_quality(pv.age_seconds, pv.source_mode) if pv.value is not None else QUALITY_MISSING
    return pv
