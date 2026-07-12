"""vertex.options.expected_move — mouvement attendu par échéance (§18/§19).

Le mouvement attendu (« expected move ») est l'amplitude d'un écart-type
implicite jusqu'à l'échéance : spot × IV × sqrt(dte/365). Pur, testable,
None si donnée manquante.
"""
from __future__ import annotations

import math

DAYS_YEAR = 365.0


def expected_move(spot, atm_iv, dte):
    """Écart-type implicite en valeur absolue ($) jusqu'à l'échéance.

    spot : cours ; atm_iv : IV ATM (fraction, 0.30 = 30 %) ; dte : jours
    calendaires. None si l'un manque ou est invalide."""
    if spot is None or atm_iv is None or dte is None:
        return None
    try:
        spot, atm_iv, dte = float(spot), float(atm_iv), float(dte)
    except (TypeError, ValueError):
        return None
    if spot <= 0 or atm_iv <= 0 or dte < 0:
        return None
    return round(spot * atm_iv * math.sqrt(dte / DAYS_YEAR), 4)


def expected_move_pct(atm_iv, dte):
    """Mouvement attendu en % du spot (indépendant du niveau du spot)."""
    if atm_iv is None or dte is None:
        return None
    try:
        atm_iv, dte = float(atm_iv), float(dte)
    except (TypeError, ValueError):
        return None
    if atm_iv <= 0 or dte < 0:
        return None
    return round(atm_iv * math.sqrt(dte / DAYS_YEAR) * 100.0, 2)


def expected_range(spot, atm_iv, dte, sigmas=1.0):
    """Fourchette (bas, haut) à `sigmas` écarts-types. None si em None."""
    em = expected_move(spot, atm_iv, dte)
    if em is None:
        return None
    try:
        spot = float(spot)
        k = float(sigmas)
    except (TypeError, ValueError):
        return None
    return (round(spot - k * em, 4), round(spot + k * em, 4))


def move_covers_target(spot, atm_iv, dte, target):
    """Le mouvement attendu (1σ) couvre-t-il la distance jusqu'à `target` ?

    Rend un ratio distance_cible / expected_move (None si indéterminé). <1 =
    la cible est à l'intérieur d'1σ (atteignable), >1 = au-delà d'1σ."""
    em = expected_move(spot, atm_iv, dte)
    if em is None or em <= 0 or target is None:
        return None
    try:
        dist = abs(float(target) - float(spot))
    except (TypeError, ValueError):
        return None
    return round(dist / em, 3)


__all__ = ['expected_move', 'expected_move_pct', 'expected_range',
           'move_covers_target', 'DAYS_YEAR']
