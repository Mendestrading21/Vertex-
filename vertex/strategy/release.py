"""Activation explicite du profil de release Vertex Test 1.0.

Les profils V1–V3 restent dans ``strategy/profiles`` pour la compatibilité et
le rollback. Le runtime canonique active ``strategy/release_profiles`` avant
l'import du monolithe historique; un lancement direct de ``terminal.py`` reste
donc volontairement un mode legacy.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from . import constitution

RELEASE_PROFILES_DIR = Path(__file__).resolve().parent / "release_profiles"
_ACTIVATED = False
_ORIGINAL_LOAD_PROFILE: Callable = constitution.load_profile
_ORIGINAL_LIST_VERSIONS: Callable = constitution.list_versions
_ORIGINAL_PROPOSE_NEW_VERSION: Callable = constitution.propose_new_version


def load_release_profile(version: int | None = None):
    """Charge un profil de release sans modifier l'état global du processus."""
    return _ORIGINAL_LOAD_PROFILE(version=version, profiles_dir=RELEASE_PROFILES_DIR)


def list_release_versions() -> list[int]:
    """Retourne l'historique disponible dans le corpus de release."""
    return _ORIGINAL_LIST_VERSIONS(profiles_dir=RELEASE_PROFILES_DIR)


def activate_release_profile() -> None:
    """Fait de V4 la constitution par défaut du processus canonique.

    L'opération est idempotente et intervient avant l'import de ``terminal``.
    Les appels qui fournissent explicitement ``profiles_dir`` restent respectés.
    """
    global _ACTIVATED
    if _ACTIVATED:
        return

    def load_profile(version: int | None = None, profiles_dir: Path | None = None):
        target = RELEASE_PROFILES_DIR if profiles_dir is None else Path(profiles_dir)
        return _ORIGINAL_LOAD_PROFILE(version=version, profiles_dir=target)

    def list_versions(profiles_dir: Path | None = None) -> list[int]:
        target = RELEASE_PROFILES_DIR if profiles_dir is None else Path(profiles_dir)
        return _ORIGINAL_LIST_VERSIONS(profiles_dir=target)

    def propose_new_version(changes: dict, confirm: bool = False,
                            profiles_dir: Path | None = None) -> dict:
        target = RELEASE_PROFILES_DIR if profiles_dir is None else Path(profiles_dir)
        return _ORIGINAL_PROPOSE_NEW_VERSION(
            changes, confirm=confirm, profiles_dir=target)

    constitution.PROFILES_DIR = RELEASE_PROFILES_DIR
    constitution.load_profile = load_profile
    constitution.list_versions = list_versions
    constitution.propose_new_version = propose_new_version
    _ACTIVATED = True


def etat_actif() -> dict:
    """QUELLE constitution s'applique dans CE processus, et d'ou elle vient.

    ## Pourquoi ce temoin existe

    Le repertoire lu depend de la facon dont Vertex a ete lance, et rien ne le
    disait. Recensement du 26 aout 2026 :

    | lanceur | commande | constitution |
    |---|---|---|
    | `Lancer_VERTEX.bat` | `python -m vertex` | **V4** |
    | `Lancer_VERTEX_DEMO.bat` | `python -m vertex` | **V4** |
    | `render.yaml` | `gunicorn vertex.runtime:app` | **V4** |
    | `Installer_Demarrage_Auto.bat` | `pythonw terminal.py` | **V3** |

    Le dernier est celui du **demarrage automatique de Windows** : celui qui
    fait tourner Vertex a chaque ouverture de session. Il court-circuitait
    `vertex.runtime`, donc l'activation, donc V4.

    Les deux constitutions different sur **29 points**. V3 n'a ni
    `equity_profile` — les horizons 3/6/12 mois des actions — ni
    `holding_period_weeks` — les revues a 2/4/6 semaines ; son DTE prefere est
    `[90, 180]` cible 135 au lieu de `[120, 240]` cible 180, et son time-stop
    tombe a 5-8 seances au lieu de 30-45. Ce n'est pas un detail de version :
    c'est un autre mandat.

    `CLAUDE.md` exige que « la constitution strategique ne change qu'au moyen
    d'une nouvelle version explicite et revue humainement ». Elle changeait
    selon la commande de lancement, sans que rien ne l'affiche.
    """
    etat = {
        'release_active': bool(_ACTIVATED),
        'repertoire': constitution.PROFILES_DIR.name,
        'version': None,
        'strategy_id': None,
        'dte_prefere': None,
        'dte_cible': None,
        'erreur': None,
        'read_only': True,
    }
    try:
        profil = constitution.load_profile()
    except Exception as exc:                                   # noqa: BLE001
        etat['erreur'] = ('%s: %s' % (type(exc).__name__, exc))[:160]
        return etat
    swing = (profil.options_profile or {}).get('swing_3_6m') or {}
    etat.update({
        'version': profil.version,
        'strategy_id': getattr(profil, 'strategy_id', None),
        'dte_prefere': swing.get('preferred_dte'),
        'dte_cible': swing.get('target_dte'),
    })
    return etat


__all__ = [
    "RELEASE_PROFILES_DIR",
    "activate_release_profile",
    "etat_actif",
    "list_release_versions",
    "load_release_profile",
]
