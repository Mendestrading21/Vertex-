"""vertex/app/ibkr_state.py — LA PASSERELLE SOCKET → `scan_state` (#779, G1).

`_sync_ibkr_state` vivait dans `terminal.py`. Elle n'avait pourtant **aucune
dépendance locale au monolithe** : ses deux entrées, `_live_meta` et
`scan_state`, avaient déjà un domicile dans le paquet
(`vertex/app/caches.py`, `vertex/app/state.py`). Elle restait là par habitude,
pas par couplage — mesuré avant de la déplacer.

## Pourquoi cette fonction compte plus que sa taille

Quatre lignes, et c'est **le seul chemin** par lequel l'état réel du socket
IBKR atteint la page Système : `vertex/services/connections.py` lit
`scan_state['ibkr_connected']` et `['ibkr_live']`, que personne d'autre n'écrit.
Sans elle, la carte des connexions afficherait un état de *configuration* — « IBKR
activé » — au lieu d'un état de *session*, ce qui est précisément le mensonge que
`connections.py` existe pour éviter.

## Le garde-fou de fraîcheur, et pourquoi il n'est pas cosmétique

Un worker figé garde `connected: True` dans `_live_meta` : le socket n'a pas été
fermé, il ne répond simplement plus. Sans borne d'âge, l'écran continuerait
d'annoncer « live » sur des ticks vieux de plusieurs heures. Au-delà de
`FENETRE_S`, la session n'est plus déclarée connectée — c'est un aveu, pas une
panne.

## L'invariant qui rend le partage possible

`scan_state` est **muté en place, jamais réassigné** (règle du guide). Cette
fonction n'écrit que des clés ; c'est ce qui permet à `terminal.py`, aux
blueprints et à `connections.py` de voir le même objet.
"""
from __future__ import annotations

import time

from vertex.app.caches import _live_meta
from vertex.app.state import scan_state

#: Au-delà de cet âge, les ticks ne prouvent plus qu'une session est vivante.
#: 75 s : le worker cote la watchlist par lots avec des pauses, donc un cycle
#: complet peut dépasser la minute sans que rien n'aille mal.
FENETRE_S = 75


def sync() -> bool:
    """Reflète l'état RÉEL du socket IBKR dans `scan_state`. Rend `connected`.

    Le retour n'est pas décoratif : il permet à un appelant — et au test — de
    constater ce qui a été conclu, sans relire l'état partagé."""
    frais = (time.time() - _live_meta.get('ts', 0)) < FENETRE_S
    connecte = bool(_live_meta.get('connected')) and frais
    scan_state['ibkr_connected'] = connecte
    scan_state['ibkr_live'] = connecte and bool(_live_meta.get('rt'))
    return connecte


def frais() -> bool:
    """Les cotations en mémoire sont-elles assez récentes pour être servies ?

    Même fenêtre que `sync()`, et c'est le point : deux tables de seuils
    divergeraient au premier ajustement, et `/quotes` servirait des cours que
    la page Système déclare périmés."""
    return (time.time() - _live_meta.get('ts', 0)) < FENETRE_S


__all__ = ['sync', 'frais', 'FENETRE_S']
