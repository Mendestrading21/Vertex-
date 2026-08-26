"""vertex/data_sources/rendement_dividende.py — 0,35 % NE VAUT PAS 35 %.

## Le défaut, mesuré le 26 août 2026

`fundamentals.py` publiait `div = info.get('dividendYield')` brut, et
`engines/analysis.py` le testait ainsi :

```python
+ (2 if (_div is not None and _div >= 0.02) else (1 if _div else 0))
```

Le seuil `0.02` est écrit pour une **fraction** : « rendement ≥ 2 % ». Or
`yfinance 1.5.2`, mesuré à l'instant sur la vraie source, rend un
**pourcentage** :

```text
KO     dividendYield=2.3    trailingAnnualDividendYield=0.022611
MO     dividendYield=6.19   trailingAnnualDividendYield=0.061925
AAPL   dividendYield=0.35   trailingAnnualDividendYield=0.003383
GOOGL  dividendYield=0.25   trailingAnnualDividendYield=0.002442
```

**Les deux unités coexistent dans la même charge.** C'est ce qui rend le piège
durable : n'importe quel relecteur peut vérifier « yfinance rend une fraction »
et avoir raison — sur l'autre champ.

## Ce que ça produisait

Le seuil « ≥ 2 % » devenait « ≥ 0,02 % ». AAPL (0,35 %) et GOOGL (0,25 %)
touchaient le **bonus défensif maximal**, au même titre que MO à 6,19 %. Et la
branche de repli `else (1 if _div else 0)` — « il verse un dividende, mais
modeste » — exigeait `0 < div < 0,02`, soit un rendement réel inférieur à
**0,02 %** : aucun titre n'y tombe. **Branche morte.**

Balayage de l'espace réaliste (3 780 configurations secteur × beta × ATR ×
rendement entre 0,01 % et 1,99 %) : **900 basculent de verdict**, soit 24 %,
dans les dix secteurs. Pour AAPL et GOOGL, **13 conditions de marché sur 25**
donnent DÉFENSIF là où la règle voulait ÉQUILIBRÉ.

Ce n'est pas cosmétique : `profile` alimente `decision_stack`, qui s'en sert
pour ouvrir une décision d'option et pour `_size_hint` — la **taille de
position** affichée à l'utilisateur (`STRONG_BUY` : 5-8 % en OFFENSIF contre
4-6 % en DÉFENSIF).

## Pourquoi ce module, et pas un `/100` dans le producteur

Diviser par cent serait se rendre otage d'une version de bibliothèque : le jour
où `yfinance` repasse à la fraction, la correction devient elle-même le défaut,
en silence et dans l'autre sens. Le rendement est donc **dérivé de la charge
elle-même**, par ordre de certitude, et il **nomme sa source**.

Deux producteurs lisaient le même champ ambigu — `data_sources/fundamentals.py`
et `data/company.py`. Un seul propriétaire de l'unité, sans quoi le troisième
héritera du piège.
"""
from __future__ import annotations

import math

#: L'unité rendue. Le nom porte l'unité : c'est tout l'objet de ce module.
FRACTION = 'fraction'

#: Un rendement annuel au-delà de ce seuil, lu comme une fraction, décrirait un
#: titre qui rend la moitié de son prix en un an. Une telle valeur est donc un
#: POURCENTAGE mal étiqueté, pas un rendement.
PLAFOND_FRACTION = 0.5

#: Au-delà, même lue en pourcent, la valeur n'est plus un rendement d'action.
PLAFOND_POURCENT = 50.0


def _fini(v):
    """La valeur si elle est un nombre fini et positif ou nul, sinon `None`."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(f) or f < 0:
        return None
    return f


def rendement(info: dict) -> dict:
    """Le rendement du dividende en **fraction**, avec sa source.

    Rend toujours un dictionnaire :

    - `valeur` : fraction (`0.023` = 2,3 %), ou `None` si inconnue ;
    - `unite` : `FRACTION`, toujours — le champ existe pour que le lecteur
      n'ait pas à le déduire ;
    - `source` : le champ de la charge qui a produit la valeur ;
    - `unite_inferee` : `True` quand l'unité a dû être **déduite** faute de
      champ non ambigu ;
    - `motif` : pourquoi la valeur est absente ou l'unité inférée.

    **Zéro n'est pas l'inconnu.** Un titre qui ne verse rien rend `0.0` ; un
    titre dont on ignore le rendement rend `None`. Les confondre ferait passer
    « je ne sais pas » pour « il ne verse pas » — même distinction qu'en D-081
    pour l'open interest.
    """
    info = info if isinstance(info, dict) else {}

    #  1. Le champ NON AMBIGU. `trailingAnnualDividendYield` est une fraction
    #     dans toutes les versions observées, et se recoupe avec le pourcentage.
    t = _fini(info.get('trailingAnnualDividendYield'))
    if t is not None and t <= PLAFOND_FRACTION:
        return {'valeur': t, 'unite': FRACTION,
                'source': 'trailingAnnualDividendYield',
                'unite_inferee': False, 'motif': None}

    #  2. Reconstruire depuis le montant et le prix : deux grandeurs dont
    #     l'unite ne se discute pas.
    montant = _fini(info.get('dividendRate'))
    prix = _fini(info.get('currentPrice')) or _fini(info.get('regularMarketPrice'))
    if montant is not None and prix:
        calcule = montant / prix
        if calcule <= PLAFOND_FRACTION:
            return {'valeur': calcule, 'unite': FRACTION,
                    'source': 'dividendRate/prix',
                    'unite_inferee': False, 'motif': None}

    #  3. Le champ AMBIGU, en dernier recours. `0.35` peut vouloir dire 35 % ou
    #     0,35 % et rien dans la charge ne tranche : l'unite est INFEREE, et le
    #     dit. La lecture retenue est le pourcentage, celle des versions
    #     observees — mais elle est etiquetee, jamais presentee comme mesuree.
    brut = _fini(info.get('dividendYield'))
    if brut is None:
        return {'valeur': None, 'unite': FRACTION, 'source': None,
                'unite_inferee': False,
                'motif': 'aucun champ de rendement dans la charge'}
    if brut == 0.0:
        return {'valeur': 0.0, 'unite': FRACTION, 'source': 'dividendYield',
                'unite_inferee': False, 'motif': None}
    if brut > PLAFOND_POURCENT:
        return {'valeur': None, 'unite': FRACTION, 'source': 'dividendYield',
                'unite_inferee': False,
                'motif': ('valeur hors de tout rendement plausible (%.4g) — '
                          'refusee plutot que convertie au hasard' % brut)}
    return {'valeur': brut / 100.0, 'unite': FRACTION, 'source': 'dividendYield',
            'unite_inferee': True,
            'motif': ("unite deduite : `dividendYield` est ambigu et aucun champ "
                      "non ambigu n'accompagne la charge")}


def valeur(info: dict):
    """Le rendement seul, en fraction — pour les appelants qui n'ont pas besoin
    de la provenance. `None` si inconnu."""
    return rendement(info)['valeur']
