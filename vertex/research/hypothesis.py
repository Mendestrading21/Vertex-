"""vertex.research.hypothesis — définition d'hypothèse (§29). Voir factory.py."""
from .factory import REQUIRED_DEFINITION, LifecycleError


def validate_definition(definition: dict) -> list[str]:
    """Champs obligatoires d'une hypothèse de recherche — liste des manquants."""
    return [k for k in REQUIRED_DEFINITION if not (definition or {}).get(k)]
