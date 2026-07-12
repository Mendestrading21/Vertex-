"""vertex.positions.detector — détection au démarrage + rapport (§6).

Compare l'état courant au dernier inventaire connu (fichier de snapshots)
et produit le Startup Position Report. IBKR hors ligne ⇒ AUCUNE position
locale n'est clôturée (test_ibkr_offline_does_not_close_positions).
"""
from __future__ import annotations

import time

from vertex.positions.repository import load_positions
from vertex.positions.reconciler import reconcile
from vertex.services import persist

_INVENTORY_FILE = 'position_inventory.json'


def _identity_set(positions: list[dict]) -> dict:
    return {p['position_id']: {'quantity': p.get('quantity'),
                               'average_cost': p.get('average_cost'),
                               'symbol': p.get('symbol')}
            for p in positions}


def startup_position_report(desk_blob: dict | None,
                            ibkr_positions: list | None,
                            ibkr_online: bool) -> dict:
    positions = load_positions(desk_blob, ibkr_positions)
    open_pos = [p for p in positions if p.get('status') != 'CLOSED']
    prev = persist.load_json(_INVENTORY_FILE, {}) or {}
    prev_ids = prev.get('ids') or {}
    cur_ids = _identity_set(open_pos)

    new = [pid for pid in cur_ids if pid not in prev_ids]
    missing = [pid for pid in prev_ids if pid not in cur_ids]
    modified = [pid for pid in cur_ids
                if pid in prev_ids and (
                    cur_ids[pid]['quantity'] != prev_ids[pid].get('quantity')
                    or cur_ids[pid]['average_cost'] != prev_ids[pid].get('average_cost'))]

    rec = reconcile([p for p in open_pos if p['source'] != 'IBKR'],
                    [p for p in open_pos if p['source'] == 'IBKR'],
                    ibkr_online=ibkr_online)
    report = {
        'positions_detected': len(open_pos),
        'new_positions': len(new),
        'modified_positions': len(modified),
        'missing_positions': len(missing) if ibkr_online else 0,
        'closed_positions_detected': len(missing) if ibkr_online else 0,
        'duplicates': sum(1 for i in rec['issues'] if i['code'] == 'POSITION_DUPLICATE'),
        'conflicts': rec['conflicts'],
        'repairs_required': rec['repairs_required'],
        'errors': [],
        'ibkr_online': ibkr_online,
        'note': (None if ibkr_online else
                 'IBKR hors ligne — positions locales conservées, aucune clôture automatique'),
        'generated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    }
    try:
        persist.save_json(_INVENTORY_FILE, {'ids': cur_ids, 'ts': time.time()})
    except Exception as e:                       # jamais bloquant
        report['errors'].append(f'inventaire non persisté: {e}')
    return report


__all__ = ['startup_position_report']
