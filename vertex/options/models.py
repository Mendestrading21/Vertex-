"""vertex.options.models — modèles du desk Vertex Dynamic Options."""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field

CATEGORY_BALANCED = 'BALANCED'
CATEGORY_DYNAMIC = 'DYNAMIC'          # catégorie principale
CATEGORY_ULTRA_CONVEX = 'ULTRA_CONVEX'
CATEGORY_BEARISH_TACTICAL = 'BEARISH_TACTICAL'

CALL_CATEGORIES = (CATEGORY_BALANCED, CATEGORY_DYNAMIC, CATEGORY_ULTRA_CONVEX)

# Provenance des Greeks / du pricing (§6.8)
GREEKS_BROKER = 'BROKER_GREEKS'
GREEKS_MODEL = 'MODEL_ESTIMATE'
GREEKS_FALLBACK = 'FALLBACK_ESTIMATE'


def dte_of(expiry: str, today: _dt.date | None = None) -> int | None:
    try:
        exp = _dt.date.fromisoformat(str(expiry)[:10])
    except ValueError:
        return None
    today = today or _dt.date.today()
    return (exp - today).days


@dataclass
class UnderlyingSetup:
    """Ce que le scanner/décisionnel sait du sous-jacent au moment de choisir un contrat."""
    symbol: str
    spot: float
    invalidation: float | None = None      # stop du SOUS-JACENT (le stop option en dérive)
    tp1: float | None = None
    tp2: float | None = None
    tp3: float | None = None
    expected_move_pct: float | None = None
    setup_quality: str = 'STANDARD'        # STANDARD | STRONG | EXCEPTIONAL
    direction: str = 'LONG'                # LONG (calls) | SHORT (puts tactiques)
    dividend_yield: float = 0.0
    ex_dividend_days: int | None = None
    earnings_in_days: int | None = None
    catalyst: str = ''


@dataclass
class ScoredContract:
    contract: dict
    category: str
    score: float
    reasons: list = field(default_factory=list)
    penalties: list = field(default_factory=list)
    anomalies: list = field(default_factory=list)
    scenarios: dict = field(default_factory=dict)
    liquidity: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {'contract': self.contract, 'category': self.category,
                'score': round(self.score, 2), 'reasons': self.reasons,
                'penalties': self.penalties,
                'anomalies': [a.to_dict() if hasattr(a, 'to_dict') else a
                              for a in self.anomalies],
                'scenarios': self.scenarios, 'liquidity': self.liquidity}
