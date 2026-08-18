"""Recouvrement descriptif entre résultats déclarés et expiration options."""
from __future__ import annotations


def build(options_context, earnings_context):
    options_context = options_context or {}
    earnings_context = earnings_context or {}
    best = options_context.get('best') or {}
    option_dte = best.get('dte')
    if not isinstance(option_dte, (int, float)) or option_dte < 0:
        return {'available': False, 'status': 'OPTION_DTE_UNAVAILABLE', 'read_only': True,
                'reason': 'DTE du contrat options non fourni — recouvrement non calculé'}
    days_to_earnings = earnings_context.get('days_to_earnings')
    if not earnings_context.get('available') or not isinstance(days_to_earnings, (int, float)):
        return {'available': False, 'status': 'EARNINGS_DTE_UNAVAILABLE', 'read_only': True,
                'reason': 'DTE de résultats non déclaré — recouvrement non calculé'}
    before_expiry = float(days_to_earnings) <= float(option_dte)
    return {
        'available': True,
        'status': 'EARNINGS_BEFORE_EXPIRY' if before_expiry else 'EARNINGS_AFTER_EXPIRY',
        'option_dte': round(float(option_dte), 2), 'days_to_earnings': round(float(days_to_earnings), 2),
        'earnings_before_option_expiry': before_expiry,
        'days_between_earnings_and_expiry': round(float(option_dte) - float(days_to_earnings), 2),
        'read_only': True,
        'note': 'constat sur DTE déclarés ; ni stratégie, ni estimation, ni signal d’ordre',
    }


__all__ = ['build']
