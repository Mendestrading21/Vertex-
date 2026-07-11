"""
vertex/market/regime_features.py — Le « cerveau physique » de VERTEX.

Mesures issues de la physique statistique et de la théorie de l'information,
telles que les utilisent les fonds quantitatifs. TOUT est calculé à partir de
la série de prix réelle — zéro donnée inventée, zéro fausse promesse « quantique ».

  • hurst        exposant de Hurst (fractale) : > 0.5 = persistant/tendance,
                 < 0.5 = anti-persistant/retour à la moyenne, ≈ 0.5 = marche aléatoire.
  • entropy      entropie de Shannon des rendements (désordre 0→1) : bas = structuré,
                 haut = imprévisible/bruit.
  • efficiency   ratio d'efficience de Kaufman (signal/bruit) : mouvement net / chemin
                 total parcouru ∈ [0,1]. Haut = tendance propre, bas = agité.
  • half_life    demi-vie de retour à la moyenne (Ornstein-Uhlenbeck), en jours.
  • state        synthèse : TENDANCE FRACTALE / RETOUR MOYENNE / CHAOS / NEUTRE.
"""

import numpy as np


def hurst(prices, max_lag=48):
    """Exposant de Hurst par la méthode de la variance des différences décalées.
    H = pente de log(std Δ) vs log(lag). L'exposant (pente) est invariant au niveau
    de prix, donc on travaille sur les prix bruts. Validé : marche aléatoire ≈ 0.5,
    série persistante > 0.5, série de retour-moyenne < 0.5."""
    p = np.asarray(prices, dtype=float)
    p = p[np.isfinite(p)]
    if len(p) < max_lag * 2:
        return None
    lags = np.arange(2, max_lag)
    tau = []
    good = []
    for lag in lags:
        d = p[lag:] - p[:-lag]
        s = float(np.std(d))
        if s > 1e-12:
            tau.append(s)
            good.append(lag)
    if len(good) < 8:
        return None
    try:
        slope = np.polyfit(np.log(good), np.log(tau), 1)[0]
    except Exception:
        return None
    return float(np.clip(slope, 0.0, 1.0))


def entropy(rets, bins=12):
    """Entropie de Shannon des rendements, sur bins de LARGEUR ÉGALE (pas quantile —
    sinon elle vaut toujours 1). Normalisée par log(bins) → [0,1] : 1 = désordre max
    (rendements étalés uniformément), bas = concentré/structuré (mémoire, prévisibilité)."""
    r = np.asarray(rets, dtype=float)
    r = r[np.isfinite(r)]
    if len(r) < 30:
        return None
    lo, hi = float(np.min(r)), float(np.max(r))
    if hi - lo <= 1e-12:
        return 0.0
    try:
        hist, _ = np.histogram(r, bins=bins, range=(lo, hi))
        pr = hist / hist.sum()
        pr = pr[pr > 0]
        h = -np.sum(pr * np.log(pr))
        return float(np.clip(h / np.log(bins), 0.0, 1.0))
    except Exception:
        return None


def efficiency(prices, n=20):
    """Ratio d'efficience de Kaufman sur n barres : |ΔP net| / Σ|ΔP| ∈ [0,1]."""
    p = np.asarray(prices, dtype=float)
    p = p[np.isfinite(p)]
    if len(p) < n + 1:
        return None
    seg = p[-(n + 1):]
    net = abs(seg[-1] - seg[0])
    path = float(np.sum(np.abs(np.diff(seg))))
    if path <= 1e-12:
        return None
    return float(np.clip(net / path, 0.0, 1.0))


def half_life(prices, lookback=120):
    """Demi-vie de retour à la moyenne (Ornstein-Uhlenbeck) : régression
    ΔP_t = α + β·P_{t-1}. Si β < 0 → demi-vie = −ln(2)/β (jours). Sinon None."""
    p = np.asarray(prices, dtype=float)
    p = p[np.isfinite(p)]
    if len(p) < 40:
        return None
    p = p[-lookback:]
    lag = p[:-1]
    delta = np.diff(p)
    try:
        beta = np.polyfit(lag, delta, 1)[0]
    except Exception:
        return None
    if beta >= -1e-6:
        return None
    hl = -np.log(2) / beta
    if not np.isfinite(hl) or hl <= 0 or hl > 400:
        return None
    return float(round(hl, 1))


def score_adjust(phy, ext_atr=0.0, rsi=50.0):
    """Rétroaction : combien la PHYSIQUE modifie le score Vertex (borné [-10, +8]).
    Une structure fractale fiable renforce la conviction ; le chaos et le retour-
    moyenne sur titre sur-étendu la réduisent. C'est ici que la physique DÉCIDE."""
    if not phy:
        return 0, ''
    st = phy.get('state')
    H = phy.get('hurst')
    E = phy.get('efficiency') or 0.0
    S = phy.get('entropy')
    adj = 0
    why = []
    if st == 'TENDANCE FRACTALE':
        adj += 4
        why.append('structure fractale persistante (+4)')
        if E >= 0.45:
            adj += 3
            why.append('tendance propre, efficience haute (+3)')
    elif st == 'CHAOS':
        adj -= 7
        why.append('chaos : mouvement imprévisible, conviction réduite (−7)')
    elif st == 'RETOUR MOYENNE':
        adj -= 3
        why.append('anti-persistant : la poursuite de tendance est risquée (−3)')
        if ext_atr and ext_atr >= 3:
            adj -= 3
            why.append('déjà sur-étendu → risque de rappel vers la moyenne (−3)')
    if S is not None and S >= 0.92:
        adj -= 2
        why.append('entropie extrême, forte incertitude (−2)')
    adj = int(max(-10, min(8, adj)))
    return adj, ' · '.join(why)


def analyze(close):
    """Renvoie le bilan physique complet d'une série de clôtures + une synthèse FR."""
    p = np.asarray(close, dtype=float)
    p = p[np.isfinite(p)]
    if len(p) < 80:
        return None
    rets = np.diff(p) / p[:-1]
    H = hurst(p)
    S = entropy(rets)
    E = efficiency(p)
    HL = half_life(p)

    # ─ Synthèse d'état : ce que la physique dit de la structure du titre ─
    state, col, note = 'NEUTRE', '#8794ab', 'structure indécise (proche d\'une marche aléatoire)'
    if H is not None and E is not None:
        if H >= 0.56 and E >= 0.38:
            state, col = 'TENDANCE FRACTALE', '#22C55E'
            note = ('mémoire longue persistante (Hurst %.2f) et mouvement propre '
                    '(efficience %.0f%%) — la tendance a de l\'inertie, elle se prolonge.' % (H, E * 100))
        elif H <= 0.44 and HL is not None:
            state, col = 'RETOUR MOYENNE', '#38BDF8'
            note = ('anti-persistant (Hurst %.2f) — le titre revient vers sa moyenne, '
                    'demi-vie ≈ %s j : acheter les excès bas, vendre les excès hauts.' % (H, HL))
        elif (S is not None and S >= 0.90) and E <= 0.24:
            state, col = 'CHAOS', '#EF4444'
            note = ('désordre élevé (entropie %.0f%%) et faible efficience — mouvement '
                    'bruité, peu prévisible : réduire la taille, éviter le levier.' % (S * 100))
        elif H >= 0.53:
            state, col = 'TENDANCE FRACTALE', '#22C55E'
            note = 'mémoire persistante (Hurst %.2f) — biais de continuation de tendance.' % H
        elif H <= 0.47:
            state, col = 'RETOUR MOYENNE', '#38BDF8'
            note = 'anti-persistant (Hurst %.2f) — biais de retour à la moyenne.' % H

    return {
        'hurst': (round(H, 3) if H is not None else None),
        'entropy': (round(S, 3) if S is not None else None),
        'efficiency': (round(E, 3) if E is not None else None),
        'half_life': HL,
        'state': state, 'state_col': col, 'note': note,
    }
