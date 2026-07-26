"""
vertex/engines/session_snapshot.py — MANIFEST DE SESSION D'ANALYSE (CONTINUITY LOT 5).

Identifie de façon STABLE la session d'analyse courante (le cycle de scan publié) et
expose son manifest d'intégrité : `session_id`, statut, fraîcheur, couverture (sociétés
scannées / univers), qualité (couverture des détails moteur), présence d'erreur.

Rôle : permettre au client une BASCULE ATOMIQUE — tant que le `session_id` ne change
pas, toutes les pages lisent le même instantané ; quand un nouveau scan se publie, le
`session_id` change et le client bascule d'un coup (notification « Analyse mise à jour »).

Invariants : AUCUN calcul financier, AUCUN verdict recalculé — lecture/agrégation de
l'état DÉJÀ produit par le scan de fond. Lecture seule, aucun ordre. Fonction pure.

Le `session_id` est dérivé de `scan_ts` (horodatage de publication du scan) : il est
donc identique pour tous les lecteurs d'un même cycle, et change exactement quand le
scan republie — c'est le point de bascule atomique côté client.
"""
from __future__ import annotations

import time


def session_id_for(scan_ts):
    """Identifiant stable d'un cycle de scan (None si aucun scan publié / horodatage
    non numérique — jamais de crash sur un état inattendu)."""
    if not isinstance(scan_ts, (int, float)) or isinstance(scan_ts, bool):
        return None
    return 'S%d' % int(scan_ts)


def build(scan_state):
    """Manifest de la session d'analyse courante, depuis l'état déjà calculé."""
    scan_state = scan_state or {}
    ts = scan_state.get('scan_ts')
    rows = scan_state.get('rows') or []
    detail = scan_state.get('detail') or {}
    err = scan_state.get('error')
    scanned = scan_state.get('scanned_n')
    universe = scan_state.get('universe_n')

    has_data = bool(rows)
    if err and not has_data:
        status = 'error'
    elif has_data:
        status = 'ready'
    else:
        status = 'analyzing'         # démarrage à froid : scan pas encore publié

    coverage = (min(100, round(100 * scanned / universe))     # jamais > 100 % (univers périmé)
                if isinstance(scanned, (int, float)) and universe else None)
    covered = sum(1 for r in rows if isinstance(r, dict) and r.get('symbol') in detail) if rows else 0
    quality = round(100 * covered / len(rows)) if rows else None

    return {
        'session_id': session_id_for(ts),
        'status': status,
        'as_of': scan_state.get('scan_ts_h') or scan_state.get('updated'),
        'age_s': (round(time.time() - ts) if isinstance(ts, (int, float)) and not isinstance(ts, bool) else None),
        'universe': universe,
        'scanned': scanned,
        'coverage_pct': coverage,
        'quality_pct': quality,
        'error': bool(err),
        'source': scan_state.get('source'),
        'generator': 'deterministic',
    }


__all__ = ['build', 'session_id_for']
