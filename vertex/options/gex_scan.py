"""vertex/options/gex_scan.py — RADAR DE POSITIONNEMENT (GEX multi-titres).

Balaye le board d'options ENTIER et classe chaque sous-jacent par positionnement
dealer : net GEX, régime (stabilisant/accélérateur), biais, murs, bascule. Répond
à « où les dealers poussent-ils le plus fort ? » — l'écran de chasse, avant le
détail par titre (gex.compute).

Invariants : fonction pure ; réutilise gex.compute (aucune formule dupliquée) ;
un titre sans OI/gamma exploitables est ignoré (jamais estimé) ; board vide →
radar vide honnête. Lecture seule, aucun ordre.
"""
from __future__ import annotations

from vertex.options import gex as _gex


def scan(board, detail_by_sym=None, *, top=None):
    """Radar : profils GEX de tous les sous-jacents du board, classés par |net GEX|.

    board         : options_board complet (tous titres confondus).
    detail_by_sym : scan_state['detail'] — source de spot de secours (prix réel).
    top           : bornage optionnel du nombre de lignes retournées.
    """
    detail_by_sym = detail_by_sym or {}
    by_sym = {}
    for c in (board or []):
        if not isinstance(c, dict):
            continue
        sym = str(c.get('sym') or '').upper()
        if sym:
            by_sym.setdefault(sym, []).append(c)

    rows = []
    for sym, contracts in by_sym.items():
        spot = (detail_by_sym.get(sym) or {}).get('price')
        prof = _gex.compute(contracts, spot=spot, symbol=sym)
        if prof.get('empty'):
            continue                                   # rien d'exploitable → pas de ligne inventée
        rows.append({
            'symbol': sym,
            'spot': prof['spot'],
            'net_gex': prof['net_gex_total'],
            'net_vanna': prof.get('net_vanna_total'),
            'regime': prof['regime'],
            'bias': prof['bias'],
            'zero_gamma': prof['zero_gamma'],
            'call_wall': prof['call_wall'],
            'put_wall': prof['put_wall'],
            'contracts_used': prof['contracts_used'],
        })

    rows.sort(key=lambda r: abs(r['net_gex'] or 0), reverse=True)
    if top:
        rows = rows[:max(1, int(top))]

    n_stab = sum(1 for r in rows if r['regime'] == 'stabilisant')
    n_acc = sum(1 for r in rows if r['regime'] == 'accelerateur')
    n_bull = sum(1 for r in rows if r['bias'] == 'haussier')
    n_bear = sum(1 for r in rows if r['bias'] == 'baissier')
    if not rows:
        climate = None
    elif n_stab >= n_acc * 2:
        climate = 'marché majoritairement épinglé (dealers longs gamma)'
    elif n_acc >= n_stab * 2:
        climate = 'marché majoritairement accélérateur (dealers courts gamma) — mouvements amplifiés'
    else:
        climate = 'régimes mixtes selon les titres'

    return {
        'empty': not rows,
        'rows': rows,
        'symbols_scanned': len(by_sym),
        'symbols_usable': len(rows),
        'counts': {'stabilisant': n_stab, 'accelerateur': n_acc,
                   'haussier': n_bull, 'baissier': n_bear},
        'climate': climate,
        'generator': 'deterministic',
        'reason': (None if rows else
                   'aucun sous-jacent avec OI + gamma exploitables dans le board'),
    }


__all__ = ['scan']
