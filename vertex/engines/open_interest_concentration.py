"""Concentration d'open interest reporté pour l'horizon SWING_3_6M."""
from __future__ import annotations

import math


def _number(value, *, allow_zero=False):
    if isinstance(value, bool):
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(value) or value < 0 or (value == 0 and not allow_zero):
        return None
    return value


def build(board, *, sym=None, min_dte=90, max_dte=180):
    """Agrège l'OI tel que reporté, sans conversion ni extrapolation."""
    matching = [c for c in (board or []) if isinstance(c, dict)
                and (not sym or str(c.get('sym', '')).upper() == str(sym).upper())]
    horizon = [c for c in matching if (lambda dte: dte is not None and min_dte <= dte <= max_dte)
               (_number(c.get('dte')))]
    coverage = {'contracts_for_symbol': len(matching), 'contracts_in_horizon': len(horizon),
                'min_dte': min_dte, 'max_dte': max_dte, 'oi_reported_count': 0,
                'oi_missing_or_invalid_count': 0, 'oi_zero_reported_count': 0,
                'oi_positive_count': 0}
    by_strike = {}
    for contract in horizon:
        oi = _number(contract.get('oi'), allow_zero=True)
        if oi is None:
            coverage['oi_missing_or_invalid_count'] += 1
            continue
        coverage['oi_reported_count'] += 1
        if oi == 0:
            coverage['oi_zero_reported_count'] += 1
            continue
        strike = _number(contract.get('strike'))
        if strike is None:
            coverage['oi_missing_or_invalid_count'] += 1
            continue
        coverage['oi_positive_count'] += 1
        by_strike[strike] = by_strike.get(strike, 0.0) + oi
    if not horizon:
        return {'available': False, 'status': 'NO_CONTRACTS_IN_SWING_HORIZON', 'coverage': coverage,
                'read_only': True, 'reason': 'aucun contrat 90–180 DTE disponible'}
    if not by_strike:
        status = 'NO_POSITIVE_OI_REPORTED' if coverage['oi_reported_count'] else 'OI_UNAVAILABLE'
        return {'available': False, 'status': status, 'coverage': coverage, 'read_only': True,
                'reason': 'aucun open interest positif exploitable par strike'}
    total = sum(by_strike.values())
    top_strike, top_oi = max(by_strike.items(), key=lambda item: (item[1], -item[0]))
    return {'available': True, 'status': 'OBSERVED_OI_CONCENTRATION', 'coverage': coverage,
            'total_reported_open_interest': int(total), 'strikes_with_positive_oi': len(by_strike),
            'top_strike': top_strike, 'top_strike_open_interest': int(top_oi),
            'top_strike_share_pct': round(100.0 * top_oi / total, 2), 'read_only': True,
            'note': 'concentration d’open interest reporté sur 90–180 DTE ; sans inférence de positionnement'}


__all__ = ['build']
