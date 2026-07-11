"""vertex.portfolio.team_engine — Vertex Team Portfolio, 8-10 composantes (§25).

Rôles : Attaquants (2-3), Milieux (3-4), Défenseurs (~2), Gardien (cash/monétaire).
Toute nouvelle action doit répondre aux 7 questions ; aucune 11e position
automatique — au-delà du maximum, un REMPLACEMENT est obligatoire.
"""
from __future__ import annotations

from .models import (PortfolioSnapshot, ROLE_ATTACKER, ROLE_DEFENDER,
                     ROLE_GOALKEEPER, ROLE_MIDFIELDER, ROLE_TARGETS, ROLES)

DEFENSIVE_SECTORS = {'Santé', 'Conso de base', 'Utilities', 'HEALTHCARE',
                     'STAPLES', 'UTILITIES'}
CASH_LIKE = {'CASH', 'BIL', 'SGOV', 'SHV', 'MMF'}

FIT_QUESTIONS = (
    'quelle_place',            # Quelle place occupe-t-elle ?
    'remplace_qui',            # Quelle position remplace-t-elle ?
    'renforce_qualite',        # Améliore-t-elle la qualité ?
    'renforce_asymetrie',      # Améliore-t-elle l'asymétrie ?
    'augmente_correlation',    # Augmente-t-elle la corrélation ?
    'risque_sectoriel',        # Ajoute-t-elle un risque sectoriel ?
    'risque_evenementiel',     # Ajoute-t-elle un risque événementiel ?
)


def classify_role(position, profile_hint: dict | None = None) -> str:
    """Classe une position dans un rôle d'équipe (heuristique honnête + hint)."""
    hint = (profile_hint or {}).get(position.symbol)
    if hint in ROLES:
        return hint
    if position.symbol.upper() in CASH_LIKE or position.sec_type in ('CASH', 'MMF'):
        return ROLE_GOALKEEPER
    if position.sec_type == 'ETF' or position.sector in DEFENSIVE_SECTORS \
            or (position.beta is not None and position.beta < 0.8):
        return ROLE_DEFENDER
    if position.beta is not None and position.beta >= 1.4:
        return ROLE_ATTACKER
    return ROLE_MIDFIELDER


def team_view(snapshot: PortfolioSnapshot, profile, role_hints: dict | None = None) -> dict:
    """Vue d'équipe : composition par rôle, places libres, conformité 8-10."""
    by_role: dict[str, list] = {r: [] for r in ROLES}
    for p in snapshot.positions:
        role = p.role or classify_role(p, role_hints)
        p.role = role
        by_role[role].append(p.to_dict())
    if snapshot.cash > 0 and not by_role[ROLE_GOALKEEPER]:
        by_role[ROLE_GOALKEEPER].append({'symbol': '_CASH', 'role': ROLE_GOALKEEPER,
                                         'market_value': snapshot.cash})
    stock_count = sum(len(v) for r, v in by_role.items() if r != ROLE_GOALKEEPER)
    free_slots = max(0, profile.portfolio_max_positions - stock_count)
    issues = []
    for role, (lo, hi) in ROLE_TARGETS.items():
        n = len(by_role[role])
        if role == ROLE_GOALKEEPER:
            if n < lo:
                issues.append('pas de gardien (cash/monétaire) — réserve d’opportunité absente')
            continue
        if n < lo:
            issues.append(f'{role}: {n} < cible [{lo},{hi}]')
        elif n > hi:
            issues.append(f'{role}: {n} > cible [{lo},{hi}]')
    if stock_count < profile.portfolio_min_positions:
        issues.append(f'{stock_count} composantes < minimum {profile.portfolio_min_positions}')
    if stock_count > profile.portfolio_max_positions:
        issues.append(f'{stock_count} composantes > maximum {profile.portfolio_max_positions}')
    return {'by_role': by_role, 'stock_count': stock_count, 'free_slots': free_slots,
            'targets': {r: list(v) for r, v in ROLE_TARGETS.items()},
            'issues': issues, 'provenance': snapshot.provenance,
            'weights': snapshot.weights()}


def candidate_fit(snapshot: PortfolioSnapshot, profile, candidate: dict) -> dict:
    """Réponses aux 7 questions pour un candidat.

    candidate : {'symbol','role','sector','correlation_to_portfolio',
    'quality_improvement','asymmetry_improvement','event_risk','replaces'}.
    """
    team = team_view(snapshot, profile)
    answers = {}
    role = candidate.get('role', ROLE_MIDFIELDER)
    answers['quelle_place'] = role
    replaces = candidate.get('replaces')
    answers['remplace_qui'] = replaces or None
    answers['renforce_qualite'] = bool(candidate.get('quality_improvement'))
    answers['renforce_asymetrie'] = bool(candidate.get('asymmetry_improvement'))
    corr = candidate.get('correlation_to_portfolio')
    answers['augmente_correlation'] = bool(corr is not None and corr >= 0.75)
    sector = candidate.get('sector', '')
    sector_count = sum(1 for p in snapshot.positions if p.sector and p.sector == sector)
    answers['risque_sectoriel'] = sector_count >= 3
    answers['risque_evenementiel'] = bool(candidate.get('event_risk'))

    blocked, reasons = False, []
    if team['free_slots'] == 0 and not replaces:
        blocked = True
        reasons.append(f"portefeuille plein ({team['stock_count']}/"
                       f'{profile.portfolio_max_positions}) — une nouvelle position '
                       'EXIGE un remplacement explicite (aucune 11e position automatique)')
    lo, hi = ROLE_TARGETS.get(role, (0, 99))
    if len(team['by_role'].get(role, [])) >= hi and not replaces:
        reasons.append(f'rôle {role} déjà au complet — remplacement requis')
        blocked = True
    if answers['augmente_correlation'] and not answers['renforce_qualite']:
        reasons.append('corrélation en hausse sans gain de qualité — apport douteux')
    return {'answers': answers, 'blocked': blocked, 'reasons': reasons,
            'questions': list(FIT_QUESTIONS), 'team': {'stock_count': team['stock_count'],
                                                       'free_slots': team['free_slots']}}
