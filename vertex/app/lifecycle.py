"""vertex/app/lifecycle.py — DÉMARRAGE DES BOUCLES : UNE SEULE FOIS (#779, G1).

`RELEASE_GATES.md` G1 exige un propriétaire modulaire pour le lifecycle **et**
« sans double démarrage ». Ce module tient la seconde moitié, qui n'était tenue
par rien.

## Le défaut, mesuré et non supposé

`terminal.py` appelle `_start_workers()` à **deux** endroits :

```python
if os.environ.get('START_ON_IMPORT') == '1':
    _start_workers()          # (1) à l'import

def _start_app():
    _start_workers()          # (2) au lancement
```

`_start_workers()` n'avait **aucune garde d'idempotence** : il démarrait ses
threads à chaque appel. Mesure directe, en `DEMO=1 NO_IBKR=1` :

```text
START_ON_IMPORT absent  : import → 1 fil,  puis _start_workers() → 4  (+3)
START_ON_IMPORT=1       : import → 4 fils, puis _start_workers() → 7  (+3)
```

Autrement dit, dans le second cas **`_loop`, `_alerts_loop` et `_cal_loop`
tournent en double** : deux boucles de scan qui mutent `scan_state` en même
temps. Rien ne plante, rien ne s'affiche — les deux écrivent, et la dernière
gagne, au hasard de l'ordonnancement.

## Où le défaut mord, et où il ne mord pas

**La production n'est pas touchée.** `render.yaml` lance
`gunicorn vertex.runtime:app --workers 1` : l'import démarre les boucles une
fois, et `_start_app()` n'est jamais appelé.

**Le lancement local l'est** — `python -m vertex` et `python terminal.py`
passent tous deux par `_start_app()`. Or `START_ON_IMPORT=1` est précisément la
variable des commandes documentées et des outils de mesure du dépôt
(`tools/profile_hot_routes.py`, `tools/rc_short_audit.js`). Toute mesure prise
dans ce mode l'a donc été avec deux boucles concurrentes.

## Le choix : ignorer le second appel, et le dire

Lever une exception casserait un démarrage qui « marche » aujourd'hui. Ne rien
faire du tout laisserait le doute. Le second appel est donc **ignoré et
compté** : `statut()` expose `appels` et `ignores`, pour qu'un diagnostic
puisse constater qu'une seconde tentative a eu lieu plutôt que de la deviner.
"""
from __future__ import annotations

import threading
from typing import Any, Callable, Dict

_VERROU = threading.Lock()
_ETAT: Dict[str, Any] = {'demarre': False, 'appels': 0, 'ignores': 0, 'nom': None}


def demarrer_une_seule_fois(demarreur: Callable[[], None], nom: str = 'workers') -> bool:
    """Exécute `demarreur` au premier appel seulement. Rend True s'il a tourné.

    Le verrou couvre la lecture ET l'écriture du drapeau : deux appels
    concurrents (import et lancement peuvent se croiser sous un serveur à
    threads) verraient sinon tous deux `demarre == False`, et la garde ne
    garderait rien."""
    with _VERROU:
        _ETAT['appels'] += 1
        if _ETAT['demarre']:
            _ETAT['ignores'] += 1
            return False
        _ETAT['demarre'] = True
        _ETAT['nom'] = nom
    #  L'appel se fait HORS du verrou : `demarreur` lance des threads et peut
    #  durer ; le tenir sous verrou bloquerait un second appelant au lieu de le
    #  laisser repartir immédiatement avec `False`.
    demarreur()
    return True


def statut() -> Dict[str, Any]:
    """État observable du cycle de vie — `appels` et `ignores` compris.

    `ignores > 0` n'est pas une erreur : c'est la trace qu'une seconde
    tentative a eu lieu et a été neutralisée. Sans ce compteur, la garde
    travaillerait en silence et personne ne saurait que le double appel existe
    encore dans le code."""
    with _VERROU:
        return dict(_ETAT)


def reinitialiser() -> None:
    """Remet le cycle de vie à zéro. **Réservé aux tests.**

    Aucun chemin de production n'a de raison de redémarrer les boucles : c'est
    exactement ce que la garde interdit."""
    with _VERROU:
        _ETAT.update({'demarre': False, 'appels': 0, 'ignores': 0, 'nom': None})


__all__ = ['demarrer_une_seule_fois', 'statut', 'reinitialiser']
