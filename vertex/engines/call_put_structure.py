"""Structure call-put observée sur un board options, sans interprétation prédictive."""
from __future__ import annotations

from vertex.options import pulse


def build(board, *, sym=None):
    contracts = [contract for contract in (board or []) if isinstance(contract, dict)
                 and (not sym or str(contract.get('sym', '')).upper() == str(sym).upper())]
    snapshot = pulse.option_pulse(contracts)
    calls, puts = snapshot['calls'], snapshot['puts']
    coverage = {'contracts_considered': len(contracts), 'calls': calls, 'puts': puts}
    if not contracts:
        return {'available': False, 'status': 'OPTION_BOARD_UNAVAILABLE', 'coverage': coverage,
                'read_only': True, 'reason': 'aucun contrat options disponible pour le symbole'}
    if not calls or not puts:
        return {'available': False, 'status': 'ONE_SIDED_CONTRACT_SET', 'coverage': coverage,
                'read_only': True, 'reason': 'contrats call et put requis pour le ratio observé'}
    return {'available': True, 'status': 'OBSERVED_CALL_PUT_STRUCTURE', 'coverage': coverage,
            'call_put_ratio': snapshot['call_put_ratio'], 'read_only': True,
            'note': 'comptage de contrats observés ; ni flux net, ni prévision, ni recommandation'}


__all__ = ['build']
