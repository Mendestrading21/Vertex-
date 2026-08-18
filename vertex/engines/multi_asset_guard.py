"""Garde-fou descriptif pour les preuves multi-actifs Vertex.

Il ne contourne jamais les hard gates Skyler et ne modifie pas la décision.
Il rend visible ce qui doit être revu avant d'interpréter un contexte ETF/options.
"""
from __future__ import annotations


def build(profile, sector_coherence, options_context=None, portfolio_context=None):
    profile = profile or {}
    coherence = sector_coherence or {}
    options = options_context or {}
    portfolio = portfolio_context or {}
    issues = []
    asset_class = profile.get('asset_class')
    if asset_class == 'UNKNOWN':
        issues.append({'id': 'ASSET_TYPE_UNPROVEN', 'severity': 'REVIEW',
                       'reason': 'type d’actif non déclaré — aucune règle ETF/options spécifique applicable'})
    if asset_class == 'ETF' and profile.get('sector_proxy') and not coherence.get('available'):
        issues.append({'id': 'ETF_SECTOR_CONTEXT_MISSING', 'severity': 'REVIEW',
                       'reason': 'ETF sectoriel déclaré sans agrégat sectoriel courant'})
    if options.get('available') is True:
        if options.get('input_truncated'):
            issues.append({'id': 'OPTION_BOARD_TRUNCATED', 'severity': 'REVIEW',
                           'reason': 'board options borné à %s contrats — couverture partielle' %
                                     (options.get('input_limit') or 'une limite déclarée')})
        best = options.get('best') or {}
        mandate = best.get('mandate') or {}
        if any(value is None for key, value in mandate.items() if str(key).endswith('_ok')):
            issues.append({'id': 'OPTION_CONTRACT_EVIDENCE_PARTIAL', 'severity': 'REVIEW',
                           'reason': 'au moins une preuve de mandat options est absente'})
    mix = portfolio.get('asset_mix') or {}
    unclassified = mix.get('UNCLASSIFIED') or {}
    if unclassified.get('positions', 0):
        issues.append({'id': 'PORTFOLIO_ASSET_TYPES_PARTIAL', 'severity': 'REVIEW',
                       'reason': '%s position(s) portefeuille sans type canonique' % unclassified['positions']})
    return {
        'status': 'REVIEW_REQUIRED' if issues else 'MULTI_ASSET_COVERED',
        'read_only': True, 'does_not_change_verdict': True,
        'asset_class': asset_class,
        'issues': issues,
        'note': 'garde-fou descriptif multi-actifs ; les hard gates Skyler restent prioritaires',
    }


__all__ = ['build']
