"""vertex.portfolio.team_roles — définition des rôles de l'équipe (§25)."""
from __future__ import annotations

from .models import (ROLE_ATTACKER, ROLE_DEFENDER, ROLE_GOALKEEPER,
                     ROLE_MIDFIELDER, ROLE_TARGETS, ROLES)

ROLE_DESCRIPTIONS = {
    ROLE_ATTACKER: {'count': [2, 3], 'horizon_months': [3, 12],
                    'profile': 'hypercroissance, catalyseurs, momentum, fort potentiel'},
    ROLE_MIDFIELDER: {'count': [3, 4], 'horizon_months': [6, 24],
                      'profile': 'grandes sociétés de croissance, qualité, cash-flow, leadership'},
    ROLE_DEFENDER: {'count': [2, 2], 'horizon_months': None,
                    'profile': 'résilience, ETF, diversification, réduction de volatilité'},
    ROLE_GOALKEEPER: {'count': [1, 1], 'horizon_months': None,
                      'profile': 'cash, ETF monétaire, actif défensif, réserve d’opportunité'},
}

__all__ = ['ROLES', 'ROLE_TARGETS', 'ROLE_DESCRIPTIONS', 'ROLE_ATTACKER',
           'ROLE_MIDFIELDER', 'ROLE_DEFENDER', 'ROLE_GOALKEEPER']
