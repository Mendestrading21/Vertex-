"""vertex.portfolio.models — positions et instantané du Vertex Team Portfolio."""
from __future__ import annotations

from dataclasses import dataclass, field

ROLE_ATTACKER = 'ATTACKER'      # 2-3 : hypercroissance, catalyseurs, momentum (3-12 mois)
ROLE_MIDFIELDER = 'MIDFIELDER'  # 3-4 : grandes croissances de qualité (6-24 mois)
ROLE_DEFENDER = 'DEFENDER'      # ~2 : résilience, ETF, diversification
ROLE_GOALKEEPER = 'GOALKEEPER'  # cash / monétaire / réserve d'opportunité
ROLES = (ROLE_ATTACKER, ROLE_MIDFIELDER, ROLE_DEFENDER, ROLE_GOALKEEPER)

ROLE_TARGETS = {
    ROLE_ATTACKER: (2, 3),
    ROLE_MIDFIELDER: (3, 4),
    ROLE_DEFENDER: (2, 2),
    ROLE_GOALKEEPER: (1, 1),
}


@dataclass
class Position:
    symbol: str
    quantity: float
    avg_cost: float | None = None
    last_price: float | None = None
    sec_type: str = 'STK'
    sector: str = ''
    role: str = ''
    beta: float | None = None
    is_simulated: bool = False    # positions simulées EXPLICITEMENT transmises

    @property
    def market_value(self) -> float | None:
        if self.last_price is None:
            return None
        return self.quantity * self.last_price

    def to_dict(self) -> dict:
        return {'symbol': self.symbol, 'quantity': self.quantity,
                'avg_cost': self.avg_cost, 'last_price': self.last_price,
                'market_value': self.market_value, 'sec_type': self.sec_type,
                'sector': self.sector, 'role': self.role, 'beta': self.beta,
                'is_simulated': self.is_simulated}


@dataclass
class PortfolioSnapshot:
    """Instantané basé sur des positions RÉELLES (IBKR/desk) ou simulées explicites.

    provenance ∈ {'REAL', 'SIMULATED'} — jamais 'candidats du scanner'.
    """
    positions: list = field(default_factory=list)
    cash: float = 0.0
    provenance: str = 'REAL'
    as_of: str = ''
    peak_equity: float | None = None

    @property
    def equity(self) -> float | None:
        values = [p.market_value for p in self.positions]
        if any(v is None for v in values):
            return None
        return sum(values) + self.cash

    @property
    def drawdown_pct(self) -> float | None:
        eq = self.equity
        if eq is None or not self.peak_equity or self.peak_equity <= 0:
            return None
        return round((eq / self.peak_equity - 1) * 100, 2)

    def weights(self) -> dict:
        eq = self.equity
        if not eq:
            return {}
        out = {p.symbol: round((p.market_value or 0) / eq * 100, 2) for p in self.positions}
        out['_CASH'] = round(self.cash / eq * 100, 2)
        return out


def from_ibkr_positions(pv_positions, prices: dict | None = None,
                        sectors: dict | None = None, cash: float = 0.0,
                        peak_equity: float | None = None) -> PortfolioSnapshot:
    """Construit le snapshot depuis la ProvenancedValue de ibkr_positions (§6.9)."""
    prices, sectors = prices or {}, sectors or {}
    positions = []
    for raw in (pv_positions.value or []) if pv_positions else []:
        sym = raw['symbol']
        positions.append(Position(symbol=sym, quantity=raw['quantity'],
                                  avg_cost=raw.get('avg_cost'),
                                  last_price=prices.get(sym),
                                  sec_type=raw.get('sec_type', 'STK'),
                                  sector=sectors.get(sym, '')))
    return PortfolioSnapshot(positions=positions, cash=cash, provenance='REAL',
                             as_of=getattr(pv_positions, 'timestamp', ''),
                             peak_equity=peak_equity)


def simulated(positions: list[Position], cash: float = 0.0,
              peak_equity: float | None = None) -> PortfolioSnapshot:
    """Portefeuille simulé — accepté SEULEMENT par transmission explicite."""
    for p in positions:
        p.is_simulated = True
    return PortfolioSnapshot(positions=positions, cash=cash,
                             provenance='SIMULATED', peak_equity=peak_equity)
