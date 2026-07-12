"""vertex.options.event_risk — risque d'événement sur une option (§17/§18).

Un achat d'option porté à travers un earnings ou un ex-dividende subit un
risque spécifique : crush d'IV post-earnings, saut de gap, décote de dividende.
Ce module classe ce risque en clair — sans jamais inventer de date.
"""
from __future__ import annotations

RISK_NONE = 'AUCUN'
RISK_LOW = 'FAIBLE'
RISK_MODERATE = 'MODERE'
RISK_HIGH = 'ELEVE'
RISK_UNKNOWN = 'INCONNU'


def earnings_risk(earnings_in_days, dte):
    """Risque earnings : l'échéance traverse-t-elle une publication ?

    earnings_in_days : jours avant publication (None = inconnu) ; dte : jours
    avant expiration. Rend (niveau, note)."""
    if earnings_in_days is None:
        return RISK_UNKNOWN, "Date d'earnings inconnue — vérifier avant d'exposer du theta."
    try:
        e = int(earnings_in_days)
    except (TypeError, ValueError):
        return RISK_UNKNOWN, "Date d'earnings illisible."
    if e < 0:
        return RISK_NONE, "Earnings déjà passé sur la fenêtre analysée."
    if dte is not None:
        try:
            if int(dte) < e:
                return RISK_NONE, "L'échéance précède la publication — pas de crush porté."
        except (TypeError, ValueError):
            pass
    if e <= 3:
        return RISK_HIGH, "Earnings imminent (≤3 j) : crush d'IV probable après la publication."
    if e <= 10:
        return RISK_MODERATE, "Earnings sous 10 j : IV possiblement gonflée, crush à anticiper."
    return RISK_LOW, "Earnings éloigné : impact indirect via l'IV."


def dividend_risk(ex_dividend_days, right, dte):
    """Risque ex-dividende (surtout CALLS : décote du spot, exercice anticipé)."""
    if ex_dividend_days is None:
        return RISK_NONE, ''
    try:
        d = int(ex_dividend_days)
    except (TypeError, ValueError):
        return RISK_UNKNOWN, "Date ex-dividende illisible."
    if d < 0:
        return RISK_NONE, ''
    if dte is not None:
        try:
            if int(dte) < d:
                return RISK_NONE, "L'échéance précède l'ex-dividende."
        except (TypeError, ValueError):
            pass
    r = str(right or '').upper()[:1]
    if r == 'C' and d <= 5:
        return RISK_MODERATE, "Ex-dividende proche sur un CALL : décote du spot et risque d'exercice anticipé."
    if d <= 5:
        return RISK_LOW, "Ex-dividende proche : léger impact sur le sous-jacent."
    return RISK_LOW, "Ex-dividende dans la fenêtre : impact modéré."


_ORDER = {RISK_NONE: 0, RISK_LOW: 1, RISK_MODERATE: 2, RISK_HIGH: 3,
          RISK_UNKNOWN: 1}


def combined(earnings_in_days, ex_dividend_days, right, dte):
    """Synthèse du risque d'événement : niveau max + notes cumulées."""
    e_lvl, e_note = earnings_risk(earnings_in_days, dte)
    d_lvl, d_note = dividend_risk(ex_dividend_days, right, dte)
    worst = e_lvl if _ORDER[e_lvl] >= _ORDER[d_lvl] else d_lvl
    notes = [n for n in (e_note, d_note) if n]
    return {'level': worst, 'earnings': e_lvl, 'dividend': d_lvl, 'notes': notes}


__all__ = ['earnings_risk', 'dividend_risk', 'combined',
           'RISK_NONE', 'RISK_LOW', 'RISK_MODERATE', 'RISK_HIGH', 'RISK_UNKNOWN']
