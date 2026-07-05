"""
vertex/engines/swing.py — PROJECTION SWING D'OPTIONS (Ch. II).

Estime le rendement d'un CALL si le titre fait un mouvement réaliste ~1σ sur
~3 semaines (delta + convexité gamma, érosion thêta faible sur échéance
lointaine), et annote un board de contrats. Logique VERTEX : acheter loin
(>=90j) pour le coussin temporel, revendre en 1-4 semaines sur un gain rapide.

Extrait verbatim du monolithe. Analyse uniquement, aucune exécution.
"""

import math


def _swing_project(spot, iv, delta, cost, theta_burn, dte, days=21):
    """Projection SWING SÉCURISÉ : rendement estimé si le titre fait un mouvement
    réaliste ~1σ sur ~3 semaines, en tenant compte du delta (levier) et de l'érosion
    théta (faible sur les échéances lointaines). Renvoie (swing_ret%, swing_ok).

    Logique VERTEX : on achète loin (≥ 90j) pour le coussin temporel / la faible érosion,
    mais l'objectif est de REVENDRE en 1-4 semaines sur un gain rapide (≥ +25 %)."""
    try:
        spot = float(spot or 0); iv = float(iv or 0) / (100.0 if (iv or 0) > 3 else 1.0)
        delta = abs(float(delta or 0)); cost = float(cost or 0)
        if spot <= 0 or cost <= 0 or iv <= 0:
            return None, False
        sigma = spot * iv * math.sqrt(days / 252.0)          # 1σ sur la fenêtre (~3 sem)
        move = 1.25 * sigma                                  # SWING de CONVICTION (setup A+ sélectif, pas du bruit)
        T = max((dte or 30) / 365.0, 0.02)
        gamma = 0.399 / (spot * iv * math.sqrt(T))           # convexité (approx ATM) : le delta monte avec le titre
        eff_delta = min(0.95, delta + 0.5 * gamma * move)    # delta moyen effectif sur la hausse (gamma)
        gain = eff_delta * move * 100.0                      # gain option (delta effectif × ΔS × 100)
        theta_cost = cost * (float(theta_burn or 0) / 100.0) * days  # érosion faible sur échéance lointaine
        net = gain - theta_cost
        swing_ret = round(net / cost * 100.0)
        swing_ok = bool((dte or 0) >= 90 and swing_ret >= 25)   # ≥ 90j (sécurité) + ≥ +25 % (objectif 1-4 sem)
        return swing_ret, swing_ok
    except Exception:
        return None, False


def _annotate_swing(board, detail):
    """Ajoute swing_ret / swing_ok à chaque contrat du board (démo et réel)."""
    for c in board or []:
        if not isinstance(c, dict):
            continue
        spot = c.get('spot') or ((detail or {}).get(c.get('sym')) or {}).get('price')
        sr, ok = _swing_project(spot, c.get('iv'), c.get('delta'),
                                c.get('cost'), c.get('theta_burn'), c.get('dte'))
        c['swing_ret'] = sr
        c['swing_ok'] = ok
    return board


__all__ = ['project', 'annotate']


# Alias publics (API du module) vers les fonctions extraites verbatim.
project = _swing_project
annotate = _annotate_swing
