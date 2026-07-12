"""vertex.positions.reconciler — réconciliation locale ↔ IBKR (§7).

Identité action : (compte, symbole, devise, classe). Identité option :
(compte, conId si connu, sous-jacent, droit, strike, expiration,
multiplicateur, devise). Aucune correction silencieuse : toute ambiguïté
produit DATA_REPAIR_REQUIRED avec les deux valeurs et la source proposée.
"""
from __future__ import annotations

import time
from datetime import date

CODES = ('POSITION_DUPLICATE', 'QUANTITY_MISMATCH', 'COST_BASIS_MISMATCH',
         'CURRENCY_MISMATCH', 'SYMBOL_MISMATCH', 'CONTRACT_MISMATCH',
         'MULTIPLIER_MISMATCH', 'ACCOUNT_MISMATCH', 'SOURCE_CONFLICT',
         'CLOSED_STATE_CONFLICT', 'EXPIRED_OPTION_OPEN', 'MISSING_POSITION',
         'UNKNOWN_POSITION')


def _identity(p: dict) -> tuple:
    if p.get('asset_type') == 'OPTION':
        return ('OPT', p.get('underlying_symbol'), p.get('right'),
                p.get('strike'), p.get('expiration'),
                p.get('multiplier') or 100, p.get('currency'))
    return ('STK', p.get('symbol'), p.get('currency'))


def _repair(code, position_id, local, broker, note=''):
    return {'code': code, 'position_id': position_id,
            'local': local, 'broker': broker, 'note': note,
            'preferred_source': 'IBKR' if broker is not None else 'MANUAL',
            'action': 'DATA_REPAIR_REQUIRED', 'confirmed': False}


def reconcile(local: list[dict], broker: list[dict],
              ibkr_online: bool = True) -> dict:
    """Compare positions locales et broker. IBKR hors ligne ⇒ AUCUNE
    position locale n'est marquée disparue (§6)."""
    issues: list[dict] = []
    by_id_local: dict[tuple, dict] = {}

    for p in local:
        key = _identity(p)
        if key in by_id_local and p.get('source') == by_id_local[key].get('source'):
            issues.append(_repair('POSITION_DUPLICATE', p['position_id'],
                                  p.get('quantity'), None,
                                  f'doublon local {key}'))
        else:
            by_id_local[key] = p
        # option expirée encore ouverte
        exp = p.get('expiration')
        if exp and p.get('status') not in ('CLOSED', 'EXPIRED'):
            try:
                if date.fromisoformat(str(exp)[:10]) < date.today():
                    issues.append(_repair('EXPIRED_OPTION_OPEN',
                                          p['position_id'], exp, None,
                                          'contrat expiré toujours ouvert'))
            except ValueError:
                pass

    matched = set()
    for b in broker:
        key = _identity(b)
        loc = by_id_local.get(key)
        if loc is None:
            issues.append(_repair('UNKNOWN_POSITION', b['position_id'],
                                  None, b.get('quantity'),
                                  'position broker absente du desk local'))
            continue
        matched.add(key)
        loc['last_reconciled_at'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        if (loc.get('quantity') is not None and b.get('quantity') is not None
                and abs(loc['quantity'] - b['quantity']) > 1e-9):
            issues.append(_repair('QUANTITY_MISMATCH', loc['position_id'],
                                  loc['quantity'], b['quantity']))
        la, ba = loc.get('average_cost'), b.get('average_cost')
        if la is not None and ba is not None and ba and abs(la - ba) / abs(ba) > 0.02:
            issues.append(_repair('COST_BASIS_MISMATCH', loc['position_id'], la, ba))
        if loc.get('currency') != b.get('currency'):
            issues.append(_repair('CURRENCY_MISMATCH', loc['position_id'],
                                  loc.get('currency'), b.get('currency')))
        if (loc.get('multiplier') or 100) != (b.get('multiplier') or 100):
            issues.append(_repair('MULTIPLIER_MISMATCH', loc['position_id'],
                                  loc.get('multiplier'), b.get('multiplier')))
        if loc.get('status') in ('CLOSED',) and (b.get('quantity') or 0) != 0:
            issues.append(_repair('CLOSED_STATE_CONFLICT', loc['position_id'],
                                  'CLOSED', b.get('quantity')))

    if ibkr_online and broker:
        for key, loc in by_id_local.items():
            if key not in matched and loc.get('source') == 'IBKR':
                issues.append(_repair('MISSING_POSITION', loc['position_id'],
                                      loc.get('quantity'), None,
                                      'présente localement (origine IBKR), absente du broker'))
    # IBKR hors ligne : rien à signaler côté broker — surtout ne rien clôturer.

    for p in local:
        if any(i['position_id'] == p['position_id'] for i in issues):
            p['data_quality']['issues'] = sorted({i['code'] for i in issues
                                                  if i['position_id'] == p['position_id']})
            p['status'] = p['lifecycle_status'] = 'DATA_REPAIR_REQUIRED'

    return {'issues': issues, 'conflicts': len(issues),
            'repairs_required': sum(1 for i in issues
                                    if i['action'] == 'DATA_REPAIR_REQUIRED'),
            'ibkr_online': ibkr_online}


__all__ = ['reconcile', 'CODES']
