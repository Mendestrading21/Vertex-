"""vertex/options/entrees_mesurees.py — LE SIMULATEUR CESSE DE TOURNER SUR DES CONSTANTES.

## Ce qui était constant, et ce que ça coûtait

`scenario_pricer` prend un taux et un rendement de dividende. Les deux sites de
production — `options_intel_api.options_simulate` et
`redesign.options_simulate` — ne lui passaient **ni l'un ni l'autre** :

- `rate_curve` était omis, donc `RateCurve()` sans points, donc le taux plat de
  repli **4,5 %** ;
- `UnderlyingSetup.dividend_yield` était omis, donc **0,0**.

Or les deux données sont **déjà collectées et déjà en mémoire** : la courbe
dans `scan_state['macro']` (que la page Marchés dessine), le rendement dans
`scan_state['fundamentals']`.

Mesuré le 26 août 2026, DTE 180 — la cible du mandat — ATM, IV 30 % :

| entrée ignorée | effet sur un call |
|---|---|
| taux réel 3,738 % au lieu de 4,5 % (76 pb) | **−1,94 %** |
| dividende KO-like 2,26 % au lieu de 0 | **−6,8 %** |
| les deux | **−8,6 %** |

Les deux erreurs poussent dans le **même sens** pour un call. Vertex est un
produit d'achat de calls longs à risque borné : le simulateur surévaluait
systématiquement ce que l'utilisateur achète, et d'autant plus que l'échéance
est lointaine — donc au maximum sur l'horizon visé (DTE préféré 120–240).

## Un seul propriétaire

Les deux routes faisaient déjà la même chose ; leur faire faire la même lecture
deux fois serait créer le troisième endroit qui divergera. Ce module lit
`scan_state` et rend les entrées **avec leur provenance**, pour qu'une surface
puisse dire d'où vient un prix.

## Lire, pas collecter

Aucun appel réseau : une requête de page ne collecte pas (D-072, P0.1). Quand
une entrée manque, elle **manque** — la courbe retombe sur le repli plat
documenté, déjà marqué `fallback_used=True`, et le rendement reste `0.0`. Le
comportement dégradé est donc exactement celui d'avant ce lot, et il se dit.
"""
from __future__ import annotations

from vertex.data_sources import courbe_taux as _ct


def courbe(scan_state) -> object:
    """La courbe de taux bâtie sur le scan, ou le repli plat documenté."""
    return _ct.depuis_macro((scan_state or {}).get('macro'))


def taux(scan_state, echeance_jours) -> float:
    """Le taux annuel continu pour cette échéance, en **fraction**.

    Les moteurs `multileg_lab` et `double_prob` prennent un `r` scalaire, pas
    une courbe : ils reçoivent donc le point interpolé de leur propre échéance,
    et non un taux global — c'était tout l'objet de la couche par échéance
    (§6.6), restée inerte jusqu'à D-098.

    Quand aucune courbe n'est disponible, rend le taux plat documenté : la
    valeur exacte que ces moteurs employaient déjà par défaut. Le chemin
    dégradé est donc identique à celui d'avant.
    """
    try:
        jours = int(echeance_jours or 0)
    except (TypeError, ValueError):
        jours = 0
    return float(courbe(scan_state).rate_for_tenor(max(jours, 1)).rate)


#: Une IV d'action hors de cet intervalle n'est pas une IV : c'est une cotation
#: corrompue, un champ mal lu, ou une unite qui n'est pas celle qu'on croit.
#: Le point est ECARTE et non converti au hasard.
IV_MIN, IV_MAX_PLAUSIBLE = 0.02, 3.00


def iv_cotee(board, symbole: str) -> dict:
    """L'IV **reellement cotee** du titre, avec la base sur laquelle elle repose.

    Rend `{'valeur', 'n_contrats', 'source'}` — `valeur` a `None` si aucune
    cotation exploitable.

    ## Pourquoi une seule cotation suffit a l'emporter sur le proxy

    On pourrait exiger trois contrats : une mediane sur un seul n'est pas une
    surface de volatilite, et D-078 refuse justement les medianes trop minces.
    Mesure du 26 aout 2026 : le seuil a trois ne couvrirait que **145 des 211
    titres** du board (69 %), et les 66 autres retomberaient sur le proxy ATR —
    dont l'ecart mesure est de **+40 % de mediane, sur 30 titres tous
    surevalues**.

    Preferer un proxy systematiquement faux a une cotation reelle, au motif
    qu'elle est unique, serait choisir l'erreur connue. La cotation l'emporte
    donc des un contrat — et `n_contrats` dit sur quoi elle repose, pour qu'un
    lecteur puisse en juger.

    ## Unite

    Le board exprime l'IV en **POURCENT** (`44.7` = 44,7 %) : meme piege qu'en
    D-095, et la meme reponse — la conversion est faite ici, une fois, par le
    proprietaire des entrees.
    """
    sym = str(symbole or '').upper()
    vus = []
    for c in (board or []):
        if not isinstance(c, dict) or str(c.get('sym', '')).upper() != sym:
            continue
        brut = c.get('iv')
        if not isinstance(brut, (int, float)) or isinstance(brut, bool):
            continue
        v = float(brut) / 100.0
        if IV_MIN <= v <= IV_MAX_PLAUSIBLE:
            vus.append(v)
    if not vus:
        return {'valeur': None, 'n_contrats': 0, 'source': None}
    vus.sort()
    milieu = len(vus) // 2
    valeur = (vus[milieu] if len(vus) % 2
              else (vus[milieu - 1] + vus[milieu]) / 2.0)
    return {'valeur': valeur, 'n_contrats': len(vus),
            'source': 'options_board (mediane des contrats cotes)'}


def rendement_dividende(scan_state, symbole: str):
    """Le rendement du dividende du titre, en **fraction**, ou `None`.

    Lu dans les fondamentaux du scan, où `div` est déjà normalisé en fraction
    par `data_sources/rendement_dividende` (D-096). Ne rend jamais `0.0` pour
    un rendement **inconnu** : c'est la distinction de D-081, et la confondre
    ferait passer « je ne sais pas » pour « ce titre ne verse rien ».
    """
    fond = (scan_state or {}).get('fundamentals') or {}
    par_sym = fond.get('by_sym') if isinstance(fond, dict) else None
    dossier = (par_sym or {}).get(str(symbole or '').upper()) or {}
    valeur = dossier.get('div')
    try:
        return float(valeur) if valeur is not None else None
    except (TypeError, ValueError):
        return None


def provenance(scan_state, symbole: str) -> dict:
    """D'où viennent les entrées de CETTE simulation.

    Sans ce bloc, un prix corrigé serait aussi opaque qu'un prix faux : le
    lecteur ne saurait pas si le dividende a été appliqué, ni sur quelle courbe.
    """
    fond = (scan_state or {}).get('fundamentals') or {}
    par_sym = fond.get('by_sym') if isinstance(fond, dict) else None
    dossier = (par_sym or {}).get(str(symbole or '').upper()) or {}
    q = rendement_dividende(scan_state, symbole)
    return {
        'taux': _ct.couverture((scan_state or {}).get('macro')),
        'dividende': {
            'rendement': q,
            'applique': q is not None and q > 0,
            'source': dossier.get('div_source'),
            'unite_inferee': bool(dossier.get('div_unite_inferee')),
            'recu_a': dossier.get('recu_a'),
            'motif': (None if q is not None else
                      'rendement du dividende inconnu pour ce titre — non applique'),
        },
        'read_only': True,
    }
