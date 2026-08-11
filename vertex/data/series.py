"""vertex/data/series.py — SÉRIE DE CLÔTURES CANONIQUE (SKYLER LOT 4).

Une seule source de vérité pour les chemins décisionnels : la série produite par
le scan dans `detail['series']['close']` (clôtures RÉELLES, None filtrés par le
producteur). Les formes historiques `detail['closes']` / `detail['history']`
n'avaient AUCUN producteur dans le code — les accepter ouvrait la porte à des
séries ambiguës ; elles ne sont plus admises.

Invariants : aucun point inventé, aucun lissage ; points non numériques ou ≤ 0
écartés (jamais transformés) ; provenance explicite retournée à l'appelant.
"""
from __future__ import annotations

import math

CANONICAL_SOURCE = 'scan.series.close'


def closes(detail):
    """→ (clôtures_valides, source) — ([], None) honnête si la série canonique
    est absente. Seule `detail['series']['close']` est admise."""
    raw = (((detail or {}).get('series') or {}).get('close'))
    if not isinstance(raw, (list, tuple)) or not raw:
        return [], None
    out = []
    for x in raw:
        if isinstance(x, bool):
            continue
        try:
            v = float(x)
        except (TypeError, ValueError):
            continue
        if math.isnan(v) or math.isinf(v) or v <= 0:
            continue
        out.append(v)
    return out, (CANONICAL_SOURCE if out else None)


__all__ = ['closes', 'CANONICAL_SOURCE']
