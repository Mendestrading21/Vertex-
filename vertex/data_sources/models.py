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
    """Une valeur + d'où elle vient + quand + à quel point on peut s'y fier.

    Lot 5 — portée au contrat canonique du skill (enveloppe
    `connection-and-resilience-matrix.md`). Les champs historiques ne changent
    ni de nom ni de défaut ; les nouveaux ont tous un défaut None/''/[] :
    aucune fixture ne casse, et surtout AUCUN défaut n'invente une valeur —
    une unité ou une devise par défaut serait une invention.
    """
    value: Any = None
    source: str = SOURCE_UNAVAILABLE
    source_mode: str = MODE_NONE
    timestamp: str = ''          # ISO 8601 UTC
    age_seconds: float | None = None
    quality: str = QUALITY_MISSING
    fallback_used: bool = False
    warnings: list = field(default_factory=list)

    #  ── Contrat canonique (lot 5) ────────────────────────────────────────
    #  `unit` : unité du champ (USD, %, contrats, actions…) — None = non
    #  déclarée, jamais devinée. `currency` : devise si monétaire.
    unit: str | None = None
    currency: str | None = None
    #  Identité d'instrument (symbole qualifié, conId…) — pas le symbole nu.
    instrument_id: str | None = None
    #  Séparer l'heure d'OBSERVATION chez la source de l'heure de RÉCEPTION
    #  ici : l'écart entre les deux est la latence, et la confondre avec
    #  l'âge rend une donnée lente « fraîche » à tort.
    observed_at: str = ''
    received_at: str = ''
    #  Droit d'accès à la donnée (souscription temps réel, différé…).
    entitlement: str | None = None
    #  Version du schéma de l'enveloppe — pour détecter la dérive.
    schema_version: str = '1.1'
    #  Chaîne de production : chaque étape s'ajoute, aucune ne s'efface.
    lineage: list = field(default_factory=list)
    #  Erreur portée par la valeur (et non levée) : la panne est une donnée.
    error: str | None = None

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
