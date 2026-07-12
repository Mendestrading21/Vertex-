"""vertex.ai.tool_registry — outils Claude AUTORISÉS (lecture) et INTERDITS (§28).

Claude lit, analyse, explique, propose. Il ne calcule pas les indicateurs
(les moteurs déterministes s'en chargent) et ne peut JAMAIS toucher un ordre :
tout outil interdit est rejeté à l'enregistrement, et les tests de sécurité
inspectent ce registre.
"""
from __future__ import annotations

from typing import Callable

ALLOWED_TOOLS = (
    'get_strategy', 'get_market_regime', 'get_market_breadth', 'get_portfolio',
    'get_positions', 'get_stock_packet', 'get_fundamentals', 'get_catalysts',
    'get_technicals', 'get_sentiment', 'get_anomalies', 'get_institutional_context',
    'get_tradingview_signals', 'get_option_chain', 'get_vol_surface',
    'simulate_option', 'get_thesis', 'get_track_record', 'get_validation_results',
    'save_analysis_note', 'propose_alert', 'propose_rule',
)

FORBIDDEN_TOOLS = (
    'place_order', 'modify_order', 'cancel_order', 'exercise_option',
    'transfer_cash', 'change_constitution', 'activate_rule', 'delete_history',
    'submit_order', 'transmit_order', 'withdraw_cash', 'rebalance_automatically',
    'auto_execute',

    'auto_close_position', 'auto_rebalance', 'one_click_trade',
)

# Outils d'écriture tolérés : ils créent des PROPOSITIONS (statut PROPOSED),
# jamais des actions actives — la confirmation humaine reste obligatoire.
PROPOSAL_TOOLS = ('save_analysis_note', 'propose_alert', 'propose_rule')


class ForbiddenToolError(ValueError):
    """Tentative d'enregistrer un outil d'exécution — refusée par conception."""


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Callable] = {}

    def register(self, name: str, fn: Callable, description: str = '') -> None:
        if name in FORBIDDEN_TOOLS:
            raise ForbiddenToolError(f'outil interdit: {name}')
        if name not in ALLOWED_TOOLS:
            raise ForbiddenToolError(f'outil hors liste blanche: {name}')
        self._tools[name] = fn

    def names(self) -> list[str]:
        return sorted(self._tools)

    def call(self, name: str, **kwargs):
        if name not in self._tools:
            raise KeyError(f'outil non enregistré: {name}')
        return self._tools[name](**kwargs)

    def specs(self) -> list[dict]:
        return [{'name': n, 'read_only': n not in PROPOSAL_TOOLS} for n in self.names()]
