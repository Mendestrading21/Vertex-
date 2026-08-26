"""vertex/data_sources/courbe_taux.py — LA COURBE ÉTAIT COLLECTÉE, AFFICHÉE, ET IGNORÉE.

## Le défaut, mesuré le 26 août 2026

`vertex/data_sources/rates.py` expose une couche de taux **par échéance**,
honnête : elle marque `fallback_used=True` quand elle sert son taux plat
documenté de 4,5 %. Elle ne ment donc pas.

Mais elle n'a jamais rien d'autre à servir. Recensement : `RateCurve(` est
construite **une seule fois dans tout le dépôt**, sans points —
`scenario_pricer.py:109`. Toute la couche par échéance rend donc, à chaque
simulation, la constante de repli.

Or le produit **collecte déjà la vraie courbe** et **l'affiche** : le scan
remplit `scan_state['macro']` avec `^IRX`, `^FVX`, `^TNX`, `^TYX`, et la page
Marchés en dessine l'échelle des maturités. La donnée était là, sous la main,
et le simulateur tournait à côté sur une constante.

Mesure du jour :

```text
^IRX   3M    3.705 %
^FVX   5A    4.351 %
^TNX  10A    4.639 %
^TYX  30A    5.174 %

repli employe        4.500 %
taux reel a 180 j    3.738 %   (interpole 3M -> 5A)
ecart                  76 points de base
```

À DTE 180 — la cible du mandat — ATM, IV 30 % : le call est **surévalué de
1,94 %**, le put sous-évalué de 2,56 %. Cumulé avec le dividende ignoré
(D-097), un call KO-like ressort **8,6 % trop cher**.

Les deux erreurs poussent dans le **même sens** pour un call. Et Vertex est un
produit d'achat de calls longs à risque borné : le simulateur surévaluait
systématiquement ce que l'utilisateur achète.

## Ce que ce module fait, et ce qu'il ne fait pas

Il **lit** ce que le scan a déjà collecté. Il n'appelle pas le réseau : une
requête de page ne collecte pas (D-072, P0.1), et une couche de taux qui
irait chercher une courbe au moment de pricer rouvrirait exactement le défaut
qu'on vient de fermer.

Quand la courbe est absente ou trop pauvre, il rend une `RateCurve` **vide** —
c'est-à-dire le repli plat documenté, déjà marqué `fallback_used=True`. Le
comportement dégradé reste donc celui d'aujourd'hui, et il se dit.
"""
from __future__ import annotations

import math

from .rates import RateCurve

#: Échéance, en jours, de chaque indice de taux. `^IRX` est le bon du Trésor à
#: 13 semaines ; les trois autres sont des rendements constants-maturité.
ECHEANCES_JOURS = {
    '^IRX': 91,
    '^FVX': 1825,
    '^TNX': 3652,
    '^TYX': 10957,
}

#: Un rendement du Trésor US hors de cet intervalle n'est pas un rendement :
#: c'est une erreur d'unité, un mauvais champ, ou une cotation corrompue. Le
#: point est écarté et nommé, jamais converti au hasard.
TAUX_MIN_PCT = 0.0
TAUX_MAX_PCT = 25.0

#: Il faut au moins deux points pour qu'« interpoler » veuille dire quelque
#: chose. Avec un seul, on servirait une constante en la présentant comme une
#: courbe — ce qui serait pire que le repli, qui, lui, se déclare.
POINTS_MINIMUM = 2

SOURCE = 'scan.macro (yfinance ^IRX/^FVX/^TNX/^TYX)'


def _pourcent_vers_fraction(v):
    """`3.705` (pourcent) → `0.03705`. `None` si la valeur n'est pas un taux."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(f) or not (TAUX_MIN_PCT <= f <= TAUX_MAX_PCT):
        return None
    return f / 100.0


def points_depuis_macro(macro) -> dict:
    """Les points de courbe exploitables : `{jours: taux_fraction}`.

    Les items `macro` du scan portent leur valeur en **pourcent** (`unit: '%'`)
    et `terminal.py` a déjà corrigé les cotations ×10 de certains indices.
    """
    points = {}
    for item in (macro or []):
        if not isinstance(item, dict):
            continue
        jours = ECHEANCES_JOURS.get(str(item.get('id')))
        if jours is None:
            continue
        taux = _pourcent_vers_fraction(item.get('value'))
        if taux is None:
            continue
        points[jours] = taux
    return points


def _horodatage(macro) -> str:
    """La date de clôture la plus récente parmi les points retenus."""
    dates = [str(i.get('date') or '') for i in (macro or [])
             if isinstance(i, dict) and str(i.get('id')) in ECHEANCES_JOURS]
    return max([d for d in dates if d] or [''])


def depuis_macro(macro) -> RateCurve:
    """Une `RateCurve` bâtie sur ce que le scan a **déjà** collecté.

    Rend une courbe **vide** — donc le repli plat documenté, marqué
    `fallback_used=True` — quand moins de `POINTS_MINIMUM` points sont
    exploitables. Le comportement dégradé reste celui d'avant, et il se dit.
    """
    points = points_depuis_macro(macro)
    if len(points) < POINTS_MINIMUM:
        return RateCurve()
    return RateCurve(points=points, source=SOURCE, timestamp=_horodatage(macro))


def couverture(macro) -> dict:
    """De quoi la courbe est faite, pour qu'une surface puisse le dire.

    `interpolation_large` signale le trou réel de cette courbe : entre 3 mois et
    5 ans il n'y a **aucun point**, et l'échéance visée par le produit — 120 à
    240 jours — tombe en plein dedans. Interpoler linéairement sur un intervalle
    de près de cinq ans est bien meilleur qu'une constante à 4,5 %, et reste une
    **approximation** : le dire est la condition pour s'en servir.
    """
    points = points_depuis_macro(macro)
    return {
        'points': len(points),
        'echeances_jours': sorted(points),
        'source': SOURCE if len(points) >= POINTS_MINIMUM else None,
        'horodatage': _horodatage(macro) or None,
        'repli': len(points) < POINTS_MINIMUM,
        'interpolation_large': (91 in points and 1825 in points
                                and not any(91 < j < 1825 for j in points)),
        'note': ("aucun point entre 3 mois et 5 ans : l'echeance visee par le "
                 "produit (120-240 j) est interpolee sur un intervalle large"),
        'read_only': True,
    }
