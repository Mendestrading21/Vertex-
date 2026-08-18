"""Structure temporelle IV observée, sans interpolation de surface."""
from __future__ import annotations


def _num(value):
    try:
        value = float(value)
        return value if value > 0 else None
    except (TypeError, ValueError):
        return None


def _median(values):
    values = sorted(values)
    if not values:
        return None
    midpoint = len(values) // 2
    return values[midpoint] if len(values) % 2 else round((values[midpoint - 1] + values[midpoint]) / 2.0, 4)


def build(board, *, sym=None, short_max_dte=60, long_min_dte=90):
    contracts = [contract for contract in (board or []) if isinstance(contract, dict)
                 and (not sym or str(contract.get('sym', '')).upper() == str(sym).upper())]
    short_ivs, long_ivs = [], []
    for contract in contracts:
        dte, iv = _num(contract.get('dte')), _num(contract.get('iv'))
        if dte is None or iv is None:
            continue
        if dte <= short_max_dte:
            short_ivs.append(iv)
        elif dte >= long_min_dte:
            long_ivs.append(iv)
    short_median, long_median = _median(short_ivs), _median(long_ivs)
    coverage = {'contracts_considered': len(contracts), 'short_iv_count': len(short_ivs),
                'long_iv_count': len(long_ivs), 'short_max_dte': short_max_dte, 'long_min_dte': long_min_dte}
    if short_median is None or long_median is None:
        return {'available': False, 'status': 'INSUFFICIENT_SHORT_LONG_IV', 'coverage': coverage,
                'read_only': True, 'reason': 'IV observée requise sur horizons court et long'}
    return {'available': True, 'status': 'OBSERVED_IV_TERM_STRUCTURE', 'coverage': coverage,
            'short_median_iv': short_median, 'long_median_iv': long_median,
            'long_minus_short_iv_points': round(long_median - short_median, 4), 'read_only': True,
            'note': 'médianes IV observées par horizons ; sans interpolation ni prévision'}


__all__ = ['build']
