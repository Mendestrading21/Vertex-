"""vertex/options/iv_units.py — FRONTIÈRE DE NORMALISATION de la volatilité implicite.

Contrat OPTIONS_CORRECTNESS (Skyler V2) : plus JAMAIS d'heuristique silencieuse
« si IV > 1,5, diviser par 100 » dans le cœur métier. Toute IV entre ici avec une
unité EXPLICITE et ressort en DÉCIMAL (0.404 = 40,4 %).

Deux portes :

- `normalize_iv(value, unit)`   — unité déclarée par l'appelant (PERCENT/DECIMAL).
- `from_legacy_board(value)`    — UNIQUE frontière tolérée pour le board historique
  dont le contrat d'unité est mixte (producteurs réels en pourcentage, fixtures en
  décimal). La détection y est EXPLICITE, ÉTIQUETÉE (unité détectée + avertissement)
  et testée — jamais muette. À terme (normalisation du producteur), cette porte
  disparaît.

Aucun ordre, lecture seule.
"""
from __future__ import annotations

import math

PERCENT = 'PERCENT'
DECIMAL = 'DECIMAL'

# Seuil de détection legacy : une vol décimale > 1.5 (150 %) est rarissime ; une vol
# en pourcentage < 1.5 (« 1,4 % ») l'est tout autant. Documenté, testé, borné à
# `from_legacy_board` — le cœur métier n'a pas le droit de deviner.
_LEGACY_THRESHOLD = 1.5


def _finite(value):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    return v


def normalize_iv(value, unit):
    """IV → décimal, unité EXPLICITE. Renvoie None pour toute valeur inutilisable
    (absente, NaN/inf, ≤ 0). Lève ValueError pour une unité inconnue : une unité
    devinée est un bug, pas une donnée."""
    if unit not in (PERCENT, DECIMAL):
        raise ValueError('unité IV inconnue : %r (attendu PERCENT ou DECIMAL)' % (unit,))
    v = _finite(value)
    if v is None or v <= 0:
        return None
    return v / 100.0 if unit == PERCENT else v


def from_legacy_board(value):
    """Frontière legacy du board options (contrat d'unité historiquement mixte).

    Renvoie (iv_decimal|None, unité_détectée|None, avertissement|None). L'appelant
    DOIT propager l'unité détectée et l'avertissement — la détection n'est jamais
    silencieuse."""
    v = _finite(value)
    if v is None or v <= 0:
        return None, None, None
    if v > _LEGACY_THRESHOLD:
        return (v / 100.0, PERCENT,
                'IV du board détectée en POURCENTAGE (%.4g) — convertie en décimal à la '
                'frontière legacy (iv_units.from_legacy_board).' % v)
    return v, DECIMAL, None


__all__ = ['PERCENT', 'DECIMAL', 'normalize_iv', 'from_legacy_board']
