"""vertex.strategy.memory.schemas — schémas de la mémoire stratégique (§33)."""
from __future__ import annotations

# Clés de stockage NEUTRES (aucun nom personnel, synchronisées via le desk)
STORAGE_KEYS = ('vxStrategyProfile', 'vxStrategyRules', 'vxStrategyTheses',
                'vxStrategyFeedback', 'vxStrategyLearnings', 'vxStrategyPending',
                'vxStrategyVersions')

STATUSES = ('OBSERVED', 'PROPOSED', 'CONFIRMED', 'REJECTED', 'ARCHIVED')

# Seul un statut CONFIRMED rend un objet actif — testé.
ACTIVE_STATUS = 'CONFIRMED'

RULE_FIELDS = ('id', 'title', 'body', 'status', 'created_at', 'confirmed_at', 'source')
THESIS_FIELDS = ('id', 'symbol', 'thesis', 'invalidation', 'status', 'created_at')
FEEDBACK_FIELDS = ('id', 'subject', 'note', 'outcome', 'created_at')


def validate_status(status: str) -> str:
    if status not in STATUSES:
        raise ValueError(f'statut inconnu: {status} (attendus: {STATUSES})')
    return status
