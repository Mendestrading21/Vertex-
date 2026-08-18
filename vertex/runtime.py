"""Point d'entrée WSGI et local canonique de Vertex 1.0.

``terminal.py`` reste temporairement le noyau de composition historique. Ce
module active d'abord le profil de release V4, puis charge l'adaptateur legacy.
Les consommateurs ne doivent plus importer ``terminal`` directement.
"""

from importlib import import_module
from types import ModuleType

from vertex.strategy.release import activate_release_profile


def _legacy_runtime() -> ModuleType:
    activate_release_profile()
    return import_module("terminal")


def create_app():
    """Retourne l'application Flask canonique sans démarrer le serveur local."""
    return _legacy_runtime().app


app = create_app()


def main() -> None:
    """Lance Vertex localement avec les workers et protections existants."""
    runtime = _legacy_runtime()
    runtime._start_app()


__all__ = ["app", "create_app", "main"]
