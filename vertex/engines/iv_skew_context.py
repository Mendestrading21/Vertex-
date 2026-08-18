"""Skew IV put/call observé sur contrats OTM, sans interpolation ni prévision."""
from __future__ import annotations

from vertex.options import gex


def build(board, *, sym=None, spot=None):
    try:
        spot = float(spot)
    except (TypeError, ValueError):
        spot = None
    if spot is None or spot <= 0:
        return {'available': False, 'status': 'SPOT_UNAVAILABLE', 'read_only': True,
                'reason': 'spot canonique absent — skew IV non calculé'}
    contracts = [contract for contract in (board or []) if isinstance(contract, dict)
                 and (not sym or str(contract.get('sym', '')).upper() == str(sym).upper())]
    put_otm_with_iv, call_otm_with_iv = 0, 0
    for contract in contracts:
        strike = gex._num(contract.get('strike'))
        iv = gex._iv_frac(contract.get('iv'))
        if strike is None or iv is None:
            continue
        if str(contract.get('type', '')).upper() == 'PUT' and strike < spot:
            put_otm_with_iv += 1
        elif str(contract.get('type', '')).upper() == 'CALL' and strike > spot:
            call_otm_with_iv += 1
    skew = gex.iv_skew(contracts, spot)
    coverage = {'contracts_considered': len(contracts), 'put_otm_with_iv': put_otm_with_iv,
                'call_otm_with_iv': call_otm_with_iv}
    if skew is None:
        return {'available': False, 'status': 'INSUFFICIENT_OTM_CALL_PUT_IV', 'coverage': coverage,
                'read_only': True,
                'reason': 'IV OTM exploitable requise des deux côtés call et put'}
    return {'available': True, 'status': 'OBSERVED_OTM_IV_SKEW', 'skew_iv_points': skew,
            'coverage': coverage, 'read_only': True,
            'note': 'médianes IV PUT OTM moins CALL OTM ; constat descriptif sans interpolation ni prévision'}


__all__ = ['build']
