"""vertex.strategy.memory.migrations — migrations de schéma de la mémoire (§33)."""

CURRENT_SCHEMA_VERSION = 1


def migrate(payload: dict) -> dict:
    """Migre un blob de mémoire vers le schéma courant (idempotent)."""
    version = int(payload.get('_schema', 0))
    if version < 1:
        payload.setdefault('vxStrategyPending', [])
        payload['_schema'] = 1
    return payload
