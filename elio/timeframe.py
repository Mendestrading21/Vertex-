"""
elio/timeframe.py — Confluence MULTI-HORIZONS (journalier × hebdomadaire).

Le réflexe pro n°1 : ne jamais juger un titre sur un seul horizon. La tendance
HEBDOMADAIRE est le « vent dominant » ; le journalier n'est que la météo du jour.
Un achat n'a de la force que si les deux vont dans le même sens — ou si un repli
journalier apparaît DANS une tendance hebdo saine (la zone d'achat des pros).

Calculé en ré-échantillonnant la série journalière réelle en bougies hebdo.
"""

import numpy as np


def _wrsi(s, n=14):
    d = s.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return (100 - 100 / (1 + up / dn.replace(0, np.nan))).fillna(100)


def analyze(close, daily_above50=False, daily_above200=False, daily_rsi=50.0):
    """close = Série pandas de clôtures journalières (index de dates).
    Renvoie l'état de confluence + une contribution bornée au score Vertex."""
    try:
        w = close.resample('W-FRI').last().dropna()
    except Exception:
        return None
    if len(w) < 32:
        return None
    we10 = w.ewm(span=10).mean()
    we30 = w.ewm(span=30).mean()
    wl = float(w.iloc[-1])
    e10 = float(we10.iloc[-1]); e30 = float(we30.iloc[-1]); e10p = float(we10.iloc[-2])
    wrsi = float(_wrsi(w).iloc[-1])
    wroc = round((wl / float(w.iloc[-14]) - 1) * 100, 1) if len(w) > 14 else None
    w_above30 = wl > e30
    w_rising = e10 > e10p
    w_stacked = wl > e10 > e30
    d_bull = bool(daily_above50)

    if w_above30 and w_rising and d_bull:
        state, col, adj = 'ALIGNÉ HAUSSIER', '#22C55E', 5
        note = ('tendances journalière ET hebdomadaire haussières — le vent porte dans '
                'le même sens : conviction maximale, on peut jouer le momentum.')
    elif w_above30 and w_rising and not d_bull:
        state, col, adj = 'REPLI DANS TENDANCE', '#38BDF8', 3
        note = ('fond hebdo haussier + repli journalier — LA zone d\'achat des pros : '
                'acheter la faiblesse passagère dans une tendance de fond intacte.')
    elif (not w_above30) and d_bull:
        state, col, adj = 'REBOND CONTRE-TENDANCE', '#FFB23F', -4
        note = ('rebond journalier DANS une tendance hebdo baissière — à contre-courant '
                'du vent dominant : garder court, méfiant, stop serré.')
    elif (not w_above30) and (not d_bull):
        state, col, adj = 'ALIGNÉ BAISSIER', '#EF4444', -5
        note = 'les deux horizons sont baissiers — le vent souffle contre, pas d\'achat.'
    else:
        state, col, adj = 'NEUTRE', '#8794ab', 0
        note = 'horizons non parfaitement alignés — signal ambigu, attendre la clarté.'

    return {
        'weekly_rsi': round(wrsi), 'weekly_roc': wroc,
        'weekly_above30': bool(w_above30), 'weekly_rising': bool(w_rising),
        'weekly_stacked': bool(w_stacked),
        'state': state, 'state_col': col, 'adj': int(adj), 'note': note,
    }
