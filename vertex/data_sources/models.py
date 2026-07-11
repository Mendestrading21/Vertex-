"""vertex.data_sources.models — types de base porteurs de provenance."""
from __future__ import annotations

import time
from dataclasses import dataclass, field, asdict
from typing import Any

# Sources reconnues (ordre = priorité décroissante par défaut)
SOURCE_IBKR = 'IBKR'
SOURCE_SECONDARY = 'SECONDARY'      # fournisseur secondaire validé (ex: yfinance)
SOURCE_FALLBACK_EOD = 'FALLBACK_EOD'
SOURCE_UNAVAILABLE = 'UNAVAILABLE'

# Modes d'une source
MODE_LIVE = 'LIVE'
MODE_DELAYED = 'DELAYED'
MODE_FROZEN = 'FROZEN'
MODE_EOD = 'EOD'
MODE_NONE = 'NONE'

# Qualité d'une donnée
QUALITY_FRESH = 'FRESH'
QUALITY_RECENT = 'RECENT'
QUALITY_STALE = 'STALE'
QUALITY_EXPIRED = 'EXPIRED'
QUALITY_MISSING = 'MISSING'

# Provenance des Greeks (défaut 6.8 : ne jamais présenter un modèle comme vérité broker)
GREEKS_BROKER = 'BROKER_GREEKS'
GREEKS_MODEL = 'MODEL_ESTIMATE'
GREEKS_FALLBACK = 'FALLBACK_ESTIMATE'


@dataclass
class ProvenancedValue:
    """Une valeur + d'où elle vient + quand + à quel point on peut s'y fier."""
    value: Any = None
    source: str = SOURCE_UNAVAILABLE
    source_mode: str = MODE_NONE
    timestamp: str = ''          # ISO 8601 UTC
    age_seconds: float | None = None
    quality: str = QUALITY_MISSING
    fallback_used: bool = False
    warnings: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def usable(self) -> bool:
        return self.value is not None and self.quality not in (QUALITY_EXPIRED, QUALITY_MISSING)


def missing(warning: str = '') -> ProvenancedValue:
    pv = ProvenancedValue()
    if warning:
        pv.warnings.append(warning)
    return pv


def utc_now_iso() -> str:
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


@dataclass
class AnalyticsPacket:
    """Paquet analytique par symbole : toutes les sources, un seul as_of.

    Interdit de mélanger silencieusement spot live et chaîne d'une autre
    séance : le paquet expose la qualité globale et ses avertissements, et la
    réconciliation (reconciliation.py) peut le dégrader.
    """
    symbol: str
    as_of: str = field(default_factory=utc_now_iso)
    sources: dict = field(default_factory=lambda: {
        'spot': {}, 'history': {}, 'fundamentals': {}, 'catalysts': {}, 'options': {},
    })
    quality: dict = field(default_factory=lambda: {'overall': QUALITY_MISSING, 'warnings': []})

    def set_source(self, kind: str, pv: ProvenancedValue) -> None:
        self.sources[kind] = pv.to_dict()

    def to_dict(self) -> dict:
        return {'symbol': self.symbol, 'as_of': self.as_of,
                'sources': self.sources, 'quality': self.quality}
