"""vertex.data_sources.rates — taux sans risque PAR ÉCHÉANCE (§6.6).

Fini le taux global unique codé en dur : chaque demande de taux passe par
cette couche, qui expose la source, le timestamp et le caractère de repli.
Une courbe peut être fournie (points {jours: taux}) ; à défaut, un fallback
plat DOCUMENTÉ est utilisé et marqué comme tel.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .models import SOURCE_FALLBACK_EOD, MODE_EOD, utc_now_iso

# Fallback plat documenté : ordre de grandeur des T-bills US courts. Marqué
# fallback_used=True — jamais présenté comme une courbe de marché réelle.
FALLBACK_FLAT_RATE = 0.045


@dataclass
class RateQuote:
    rate: float
    tenor_days: int
    source: str
    source_mode: str
    timestamp: str
    fallback_used: bool
    notes: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {'rate': self.rate, 'tenor_days': self.tenor_days,
                'source': self.source, 'source_mode': self.source_mode,
                'timestamp': self.timestamp, 'fallback_used': self.fallback_used,
                'notes': list(self.notes)}


class RateCurve:
    """Courbe de taux zéro simple : interpolation linéaire entre points fournis.

    points = {jours: taux_annuel}, ex. {30: 0.043, 90: 0.044, 365: 0.042}.
    """

    def __init__(self, points: dict[int, float] | None = None,
                 source: str = '', timestamp: str = '') -> None:
        self.points = dict(sorted((points or {}).items()))
        self.source = source
        self.timestamp = timestamp

    def rate_for_tenor(self, tenor_days: int) -> RateQuote:
        if not self.points:
            return RateQuote(
                rate=FALLBACK_FLAT_RATE, tenor_days=tenor_days,
                source=SOURCE_FALLBACK_EOD, source_mode=MODE_EOD,
                timestamp=utc_now_iso(), fallback_used=True,
                notes=[f'aucune courbe fournie — taux plat de repli {FALLBACK_FLAT_RATE:.3f} documenté'])
        days = sorted(self.points)
        if tenor_days <= days[0]:
            r = self.points[days[0]]
        elif tenor_days >= days[-1]:
            r = self.points[days[-1]]
        else:
            for lo, hi in zip(days, days[1:]):
                if lo <= tenor_days <= hi:
                    w = (tenor_days - lo) / (hi - lo)
                    r = self.points[lo] * (1 - w) + self.points[hi] * w
                    break
        return RateQuote(rate=round(r, 6), tenor_days=tenor_days,
                         source=self.source or 'CURVE', source_mode=MODE_EOD,
                         timestamp=self.timestamp or utc_now_iso(), fallback_used=False)


def rate_sensitivity(price_fn, base_rate: float, bump: float = 0.005) -> dict:
    """Sensibilité d'un résultat au taux : réévalue price_fn(rate) à ±bump.

    Retourne les valeurs pour documenter à quel point le taux compte —
    exigence §6.6 (« sensibilité du résultat au taux »).
    """
    base = price_fn(base_rate)
    up = price_fn(base_rate + bump)
    down = price_fn(max(0.0, base_rate - bump))
    return {'base_rate': base_rate, 'bump': bump, 'value_base': base,
            'value_up': up, 'value_down': down,
            'sensitivity_per_bump': (up - down) / 2 if None not in (up, down) else None}
