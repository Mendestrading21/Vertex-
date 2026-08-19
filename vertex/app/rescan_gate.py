"""vertex/app/rescan_gate.py — LA PORTE ANTI-RAFALE DU RE-SCAN (#779, G1).

`/api/rescan` réveille la boucle de scan. Sans borne, un client qui rafraîchit
en boucle — ou huit onglets ouverts — relancerait un scan d'univers complet
toutes les secondes. La porte n'est donc pas un confort : c'est ce qui empêche
le produit de se saturer lui-même, et de saturer yfinance avec lui.

## Ce que la porte ne fait PAS, et c'est délibéré

Elle ne trace **aucune identité de demandeur** : pas d'IP, pas de session, pas de
compteur par client. La fenêtre est **globale**. Un quota par utilisateur
supposerait de savoir qui demande, donc de le retenir ; sur un terminal
personnel, ça n'apporterait rien qu'une donnée de plus à conserver.

## Pourquoi `time.monotonic()` et pas `time.time()`

Une horloge murale peut reculer — NTP, changement d'heure, veille de la machine.
Un recul rendrait le délai restant **négatif**, donc la porte ouverte, au moment
précis où l'on veut qu'elle tienne. `monotonic()` ne recule jamais.

## L'événement est PARTAGÉ, jamais recréé

`EVENEMENT` est passé à `vertex/services/live_engine.py::configure` et attendu par la
boucle de scan. Le réassigner — au lieu de le muter par `set()` — laisserait la
boucle attendre un objet que plus personne ne réveille : le re-scan cesserait de
fonctionner **sans qu'aucune erreur ne soit levée**. Même famille de piège que
`scan_state` (« muter en place, jamais réassigner »).
"""
from __future__ import annotations

import math
import os
import threading
import time

#: Réveille la boucle de scan pour un passage immédiat. **Partagé** : la boucle
#: attend cet objet précis.
EVENEMENT = threading.Event()


def fenetre_depuis_env(brut: str | None) -> int:
    """Traduit `VERTEX_RESCAN_COOLDOWN_SEC` en une fenêtre utilisable.

    Bornée à 1 s au minimum : `0` — ou une valeur négative — ouvrirait la porte
    en grand, ce qui est exactement ce qu'elle existe pour empêcher. Une valeur
    illisible retombe sur le défaut plutôt que de faire échouer le démarrage :
    une variable mal saisie ne doit pas empêcher le terminal de se lancer, mais
    elle ne doit pas non plus désactiver la garde en silence.

    Fonction séparée pour être testable **sans recharger le module** : un
    `importlib.reload` recréerait `EVENEMENT`, et la boucle de scan attendrait
    alors un objet que plus personne ne réveille."""
    try:
        valeur = int(brut) if brut is not None else 30
    except (TypeError, ValueError):
        valeur = 30
    return max(1, valeur)


#: Fenêtre globale minimale entre deux réveils.
COOLDOWN_S = fenetre_depuis_env(os.getenv('VERTEX_RESCAN_COOLDOWN_SEC'))

_VERROU = threading.Lock()
_DERNIER = 0.0


def restant(maintenant: float | None = None) -> int:
    """Secondes restantes avant le prochain réveil autorisé (0 si ouvert)."""
    courant = time.monotonic() if maintenant is None else float(maintenant)
    ecoule = max(0.0, courant - _DERNIER)
    return max(0, int(math.ceil(COOLDOWN_S - ecoule)))


def demander() -> int:
    """Demande un re-scan. Rend **0** s'il est lancé, sinon les secondes à attendre.

    La lecture du délai et l'écriture de l'horodatage se font sous **le même**
    verrou : deux demandes simultanées verraient sinon toutes deux la porte
    ouverte, et deux scans partiraient — exactement ce que la porte existe pour
    empêcher."""
    with _VERROU:
        attente = restant()
        if attente:
            return attente
        global _DERNIER
        _DERNIER = time.monotonic()
        EVENEMENT.set()
        return 0


def reinitialiser() -> None:
    """Rouvre la porte. **Réservé aux tests** — aucun chemin de production n'a
    de raison de contourner la fenêtre."""
    global _DERNIER
    with _VERROU:
        _DERNIER = 0.0
        EVENEMENT.clear()


__all__ = ['EVENEMENT', 'COOLDOWN_S', 'fenetre_depuis_env', 'restant',
           'demander', 'reinitialiser']
