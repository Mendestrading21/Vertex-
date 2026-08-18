"""Activation explicite du profil de release Vertex 1.0.

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


__all__ = [
    "RELEASE_PROFILES_DIR",
    "activate_release_profile",
    "list_release_versions",
    "load_release_profile",
]
