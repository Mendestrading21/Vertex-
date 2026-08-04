"""vertex/options/double_prob.py — PROBABILITÉ DE DOUBLEMENT (SKYLER LOT 6).

Ce n'est PAS une PoP : la condition est P(valeur_option ≥ 2 × coût), bien plus
exigeante que « finir en profit ».

Modèle : `lognormal_terminal_intrinsic` — valeur TERMINALE intrinsèque sous
distribution lognormale risque-neutre (drift r − q). Pour un call long :
doubler ⇒ S_T ≥ K + 2×prime ; pour un put long : S_T ≤ K − 2×prime (seuil ≤ 0
→ probabilité 0, jamais inventée).

Hypothèses AFFICHÉES (contrat OPTIONS_CORRECTNESS) : tenue jusqu'à l'échéance
(pas de sortie anticipée), pas de trajectoire d'IV (vega ignoré avant terme),
spread/slippage exclus, mesure risque-neutre (pas une fréquence historique).
Modèle NON CALIBRÉ → statut ESTIMATED, confiance RÉDUITE (calibration : lot 9).

Fonction pure, entrées invalides refusées structurellement. Aucun ordre.
"""
from __future__ import annotations

import math

R_DEFAULT = 0.045
Q_DEFAULT = 0.0


def _fin(x):
    if isinstance(x, bool):
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    return v


def _ncdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def double_probability(spot, strike, premium, dte, iv, right='CALL',
                       r=R_DEFAULT, q=Q_DEFAULT):
    """P(valeur terminale ≥ 2 × prime), prime PAR ACTION, IV DÉCIMALE."""
    refusals = []

    def bad(field, value, why):
        refusals.append({'field': field, 'value': None if value is None else str(value),
                         'why': why})

    s, k, p = _fin(spot), _fin(strike), _fin(premium)
    d, v = _fin(dte), _fin(iv)
    if s is None or s <= 0:
        bad('spot', spot, 'cours absent, non fini ou <= 0')
    if k is None or k <= 0:
        bad('strike', strike, 'strike absent, non fini ou <= 0')
    if p is None or p <= 0:
        bad('premium', premium, 'prime absente, non finie ou <= 0 (par action)')
    if d is None or d <= 0:
        bad('dte', dte, 'DTE absent, non fini ou <= 0')
    if v is None or v <= 0:
        bad('iv', iv, 'IV absente, non finie ou <= 0 (décimale attendue)')
    elif v > 3.0:
        bad('iv', iv, 'IV > 300 % — probablement un POURCENTAGE non converti (iv_units)')
    right = (right or 'CALL').upper()
    if right not in ('CALL', 'PUT'):
        bad('right', right, 'type de jambe inconnu')
    if refusals:
        return {'available': False, 'refusals': refusals,
                'reason': 'entrée invalide — ' + ' ; '.join(x['why'] for x in refusals)}

    T = d / 365.0
    threshold = (k + 2.0 * p) if right == 'CALL' else (k - 2.0 * p)
    model = {
        'type': 'lognormal_terminal_intrinsic', 'calibrated': False,
        'measure': 'risque-neutre', 'r': r, 'q': q, 'iv_unit': 'DECIMAL',
        'assumptions': [
            'tenue jusqu’à l’échéance (pas de sortie anticipée)',
            'valeur terminale intrinsèque (pas de trajectoire d’IV avant terme)',
            'spread/slippage exclus du coût',
            'mesure risque-neutre — pas une fréquence historique',
        ],
        'limits': 'modèle non calibré (calibration : lot 9) — estimation, pas une promesse',
    }

    if right == 'PUT' and threshold <= 0:
        prob = 0.0
        note = 'seuil de doublement ≤ 0 $ — impossible pour ce put (aucune invention)'
    else:
        sq = v * math.sqrt(T)
        dnum = (math.log(s / threshold) + (r - q - v * v / 2.0) * T) / sq
        prob = _ncdf(dnum) if right == 'CALL' else _ncdf(-dnum)
        note = None

    return {
        'available': True, 'probability': round(prob, 4),
        'threshold_price': round(threshold, 4), 'right': right,
        'status': 'ESTIMATED', 'confidence': 'REDUITE',
        'model': model, 'note': note,
    }


__all__ = ['double_probability']
