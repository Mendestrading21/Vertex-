"""Compatibilité descriptive des unités temporelles résultats / plan de détention."""
from __future__ import annotations


def build(options_context, earnings_context):
    options_context = options_context or {}
    earnings_context = earnings_context or {}
    best = options_context.get('best') or {}
    mandate = best.get('mandate') or {}
    bounds = mandate.get('bounds') or {}
    sessions = bounds.get('holding_plan_sessions')
    if not isinstance(sessions, (list, tuple)) or not sessions or not all(isinstance(value, (int, float)) and value >= 0 for value in sessions):
        return {'available': False, 'status': 'HOLDING_PLAN_UNAVAILABLE', 'read_only': True,
                'reason': 'plan de détention en séances non déclaré'}
    earnings_dte = earnings_context.get('days_to_earnings')
    if not earnings_context.get('available') or not isinstance(earnings_dte, (int, float)):
        return {'available': False, 'status': 'EARNINGS_DTE_UNAVAILABLE', 'read_only': True,
                'reason': 'DTE de résultats non déclaré'}
    return {
        'available': True,
        'status': 'UNITS_NOT_COMPARABLE',
        'holding_plan_sessions': list(sessions),
        'earnings_dte_calendar_days': round(float(earnings_dte), 2),
        'read_only': True,
        'note': 'le plan est en séances et les résultats en jours calendaires ; aucun recouvrement n’est inféré sans calendrier de marché déclaré',
    }


__all__ = ['build']
