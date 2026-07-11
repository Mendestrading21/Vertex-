"""vertex.anomalies.models — format standard d'une anomalie (§15)."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict

SEV_INFO = 1
SEV_WARN = 2
SEV_BLOCK = 3


@dataclass
class Anomaly:
    code: str
    severity: int = SEV_WARN          # 1 info · 2 avertissement · 3 majeur
    confidence: float = 0.5           # 0..1
    source: str = ''
    observed: dict = field(default_factory=dict)
    expected: dict = field(default_factory=dict)
    impact: str = ''
    blocking: bool = False            # True → ACTIONABLE interdit

    def to_dict(self) -> dict:
        return asdict(self)


def blocking_codes(anomalies: list) -> list[str]:
    return [a.code for a in anomalies if getattr(a, 'blocking', False)]


def any_blocking(anomalies: list) -> bool:
    return any(getattr(a, 'blocking', False) for a in anomalies)
