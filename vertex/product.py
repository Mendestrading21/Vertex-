"""Contrat produit canonique de Vertex 1.0.

Ce module contient uniquement des constantes stables et testables. Les moteurs,
l'interface, les documents et les agents IA doivent s'aligner sur ces valeurs.
"""

from types import MappingProxyType

ANALYSIS_ONLY = True
ORDER_EXECUTION = "disabled-by-design"

CANONICAL_SPACES = (
    "today",
    "markets",
    "opportunities",
    "analysis",
    "portfolio",
    "options",
    "journal",
    "system",
)

OPTIONS_MANDATE = MappingProxyType({
    "holding_weeks": (2, 4, 6),
    "review_sessions": (10, 20, 30),
    "preferred_dte": (120, 240),
    "target_dte": 180,
    "absolute_dte": (60, 540),
    "max_simultaneous_positions": 3,
    "primary_direction": "LONG_CALL",
    "automatic_execution": False,
})

EQUITY_MANDATE = MappingProxyType({
    "decision_horizons_months": (3, 6, 12),
    "maximum_weight_pct": 15,
    "thesis_required": True,
    "invalidation_required": True,
})

DAILY_INTELLIGENCE_MANDATE = MappingProxyType({
    "source_name": "WMB Brief",
    "cadence": "daily",
    "role": "macro_context",
    "requires_provenance": True,
    "may_override_hard_gates": False,
    "may_supply_market_prices": False,
})

INTEGRATION_CONTRACT = MappingProxyType({
    "ibkr": "read-only market, options and portfolio data",
    "tradingview": "authenticated signals that trigger reevaluation only",
    "wmb_brief": "daily macro context with provenance",
    "claude": "explanation and synthesis only; never the canonical calculator",
    "yfinance": "delayed fallback data, explicitly labelled",
})

__all__ = [
    "ANALYSIS_ONLY",
    "ORDER_EXECUTION",
    "CANONICAL_SPACES",
    "OPTIONS_MANDATE",
    "EQUITY_MANDATE",
    "DAILY_INTELLIGENCE_MANDATE",
    "INTEGRATION_CONTRACT",
]
