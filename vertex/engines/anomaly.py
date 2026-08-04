"""vertex/engines/anomaly.py — DÉTECTION D'ANOMALIES DE COURS (statistique, honnête).

Balaye la série de clôtures RÉELLE d'un titre et détecte ce qui sort de
l'ordinaire — sans jamais prédire, seulement CONSTATER :

  - SPIKE   : rendement journalier à |z| ≥ 2 (mouvement statistiquement anormal
              vs la distribution des rendements de la fenêtre).
  - VOL_SHIFT : la volatilité des 5 derniers jours ≥ 1,8× celle des 20 jours
              précédents — changement de régime de volatilité.
  - STREAK  : ≥ 5 clôtures consécutives dans le même sens (séquence rare).
  - EXTREME : dernière clôture = plus haut / plus bas de toute la fenêtre.

Invariants : fonction PURE ; série < 21 points → vide honnête (pas de statistique
sur rien) ; aucun point inventé, aucun lissage caché ; z-scores et ratios exacts.
Descriptif — pas une prévision, pas un conseil. Lecture seule, aucun ordre.
"""
from __future__ import annotations

import math

MIN_POINTS = 21          # 20 rendements minimum pour une distribution parlante
Z_SPIKE = 2.0
VOL_RATIO = 1.8
STREAK_MIN = 5


def _num(x):
    if isinstance(x, bool):
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if v != v or v in (float('inf'), float('-inf')):
        return None
    return v


def _std(xs):
    if len(xs) < 2:
        return None
    m = sum(xs) / len(xs)
    var = sum((x - m) ** 2 for x in xs) / len(xs)
    return math.sqrt(var)


def scan(closes):
    """Anomalies de la série de clôtures (réelle). Rend events + résumé JSON-sérialisables."""
    cl = [c for c in (closes or []) if _num(c) is not None and _num(c) > 0]
    cl = [float(c) for c in cl]
    if len(cl) < MIN_POINTS:
        return {
            'empty': True, 'points': len(cl), 'events': [], 'closes': cl,
            'n_spikes': 0, 'vol_ratio': None, 'streak': 0, 'extreme': None,
            'narrative': None, 'generator': 'deterministic',
            'reason': 'série trop courte (%d points, %d requis) — pas de statistique inventée'
                      % (len(cl), MIN_POINTS),
        }

    rets = [(cl[i] / cl[i - 1] - 1) * 100 for i in range(1, len(cl))]
    mean = sum(rets) / len(rets)
    sd = _std(rets)
    events = []

    # SPIKES : |z| ≥ 2 — l'index renvoyé est celui de la CLÔTURE concernée.
    if sd and sd > 0:
        for i, r in enumerate(rets):
            z = (r - mean) / sd
            if abs(z) >= Z_SPIKE:
                events.append({'kind': 'spike', 'i': i + 1, 'ret_pct': round(r, 2),
                               'z': round(z, 2),
                               'label': 'Mouvement anormal %+.1f %% (z=%.1f)' % (r, z)})

    # VOL SHIFT : σ(5 derniers rendements) vs σ(20 précédents).
    vol_ratio = None
    if len(rets) >= 25:
        recent, base = rets[-5:], rets[-25:-5]
        s_r, s_b = _std(recent), _std(base)
        if s_r is not None and s_b and s_b > 0:
            vol_ratio = round(s_r / s_b, 2)
            if vol_ratio >= VOL_RATIO:
                events.append({'kind': 'vol_shift', 'i': len(cl) - 1, 'ratio': vol_ratio,
                               'label': 'Régime de volatilité ×%.1f sur 5 j — le titre a changé de comportement' % vol_ratio})

    # STREAK : séquence terminale de rendements de même signe.
    streak = 0
    if rets and rets[-1] != 0:
        sign = rets[-1] > 0
        for r in reversed(rets):
            if r == 0 or (r > 0) != sign:
                break
            streak += 1
        if streak >= STREAK_MIN:
            events.append({'kind': 'streak', 'i': len(cl) - 1, 'days': streak,
                           'up': sign,
                           'label': '%d séance(s) consécutives en %s — séquence inhabituelle'
                                    % (streak, 'hausse' if sign else 'baisse')})

    # EXTREME : dernière clôture aux bornes de la fenêtre.
    extreme = None
    if cl[-1] >= max(cl):
        extreme = 'high'
        events.append({'kind': 'extreme', 'i': len(cl) - 1, 'side': 'high',
                       'label': 'Plus HAUT de la fenêtre (%d points)' % len(cl)})
    elif cl[-1] <= min(cl):
        extreme = 'low'
        events.append({'kind': 'extreme', 'i': len(cl) - 1, 'side': 'low',
                       'label': 'Plus BAS de la fenêtre (%d points)' % len(cl)})

    n_spikes = sum(1 for e in events if e['kind'] == 'spike')
    parts = []
    if n_spikes:
        last_spike = [e for e in events if e['kind'] == 'spike'][-1]
        parts.append('%d mouvement(s) statistiquement anormal(aux) détecté(s) sur la fenêtre '
                     '(dernier : %+.1f %%, z=%.1f).' % (n_spikes, last_spike['ret_pct'], last_spike['z']))
    else:
        parts.append('Aucun mouvement statistiquement anormal (|z| ≥ 2) sur la fenêtre.')
    if vol_ratio is not None and vol_ratio >= VOL_RATIO:
        parts.append('La volatilité récente est ×%.1f la normale — dimensionnement à adapter.' % vol_ratio)
    if streak >= STREAK_MIN:
        parts.append('Séquence de %d séances dans le même sens en cours.' % streak)
    if extreme:
        parts.append('Le titre clôture au plus %s de la fenêtre.' % ('haut' if extreme == 'high' else 'bas'))
    parts.append('Constat statistique descriptif — pas une prévision ; aucune recommandation d\'ordre.')

    return {
        'empty': False, 'points': len(cl), 'events': events, 'closes': cl,
        'n_spikes': n_spikes, 'vol_ratio': vol_ratio,
        'streak': (streak if streak >= STREAK_MIN else 0), 'extreme': extreme,
        'mean_ret_pct': round(mean, 3), 'sd_ret_pct': (round(sd, 3) if sd is not None else None),
        'narrative': ' '.join(parts), 'generator': 'deterministic',
    }


__all__ = ['scan']
