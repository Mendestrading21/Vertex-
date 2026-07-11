"""vertex.ai.strategy_context — contexte stratégique injecté dans chaque analyse."""
from __future__ import annotations

from vertex.strategy import constitution as _constitution


def build_strategy_context() -> dict:
    p = _constitution.load_profile()
    return {
        'strategy_id': p.strategy_id,
        'display_name': p.display_name,
        'style': p.style,
        'benchmark': p.benchmark,
        'portfolio_positions': [p.portfolio_min_positions, p.portfolio_max_positions],
        'max_simultaneous_options': p.max_simultaneous_options,
        'allowed_final_decisions': list(p.allowed_final_decisions),
        'analysis_order': list(p.analysis_order),
        'dte_preferred': [p.dte.preferred_minimum, p.dte.preferred_maximum],
        'reminders': [
            'lecture seule absolue: aucun ordre, jamais',
            'la décision finale appartient au moteur exécutif déterministe',
            'aucune promesse de performance, aucun langage de certitude',
            'donnée absente = dire absente, jamais inventer',
        ],
    }
