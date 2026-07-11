"""vertex.options.chain_loader — entonnoir de chargement de chaîne (§14).

Ne charge JAMAIS toute la chaîne de tout l'univers :
expirations → filtrage DTE constitution → strikes plausibles → finalistes.
La partie réseau est déléguée (scheduler + ibkr_option_chain) ; ici, la
logique de sélection pure, testable sans broker.
"""
from __future__ import annotations

from .models import dte_of

MAX_EXPIRIES = 4
STRIKE_WINDOW_PCT = 0.35    # strikes retenus dans ±35 % du spot (couvre l'ultra-convexe)
MAX_STRIKES_PER_EXPIRY = 14


def pick_expiries(expirations: list[str], profile, today=None) -> list[dict]:
    """Filtre les expirations par les bornes DTE de la constitution, privilégie
    la fenêtre préférée, limite le nombre chargé."""
    d = profile.dte
    scored = []
    for exp in expirations or []:
        dte = dte_of(exp, today=today)
        if dte is None or not (d.absolute_minimum <= dte <= d.absolute_maximum):
            continue
        in_pref = d.preferred_minimum <= dte <= d.preferred_maximum
        center = (d.preferred_minimum + d.preferred_maximum) / 2
        scored.append({'expiry': exp, 'dte': dte, 'preferred': in_pref,
                       '_dist': abs(dte - center)})
    scored.sort(key=lambda e: (not e['preferred'], e['_dist']))
    picked = scored[:MAX_EXPIRIES]
    for e in picked:
        e.pop('_dist', None)
    return picked


def pick_strikes(strikes: list[float], spot: float, right: str = 'C') -> list[float]:
    """Strikes plausibles autour du spot — de l'ITM léger au très OTM (ultra-convexe)."""
    if spot <= 0:
        return []
    lo, hi = spot * (1 - STRIKE_WINDOW_PCT), spot * (1 + STRIKE_WINDOW_PCT)
    window = sorted(k for k in strikes or [] if lo <= k <= hi)
    if len(window) <= MAX_STRIKES_PER_EXPIRY:
        return window
    # échantillonnage régulier en gardant les extrêmes
    step = (len(window) - 1) / (MAX_STRIKES_PER_EXPIRY - 1)
    return [window[round(i * step)] for i in range(MAX_STRIKES_PER_EXPIRY)]


def funnel_plan(expirations: list[str], strikes_by_expiry: dict, spot: float,
                profile, right: str = 'C', today=None) -> list[dict]:
    """Plan de chargement détaillé : quelles (expiration, strikes) demander au broker."""
    plan = []
    for e in pick_expiries(expirations, profile, today=today):
        ks = pick_strikes(strikes_by_expiry.get(e['expiry'], []), spot, right)
        if ks:
            plan.append({'expiry': e['expiry'], 'dte': e['dte'],
                         'preferred': e['preferred'], 'strikes': ks, 'right': right})
    return plan
