"""vertex.tracking — moteur de SUIVI analytique (§14-18).

« Suivre » crée un suivi HORODATÉ, HYPOTHÉTIQUE — jamais une position réelle,
jamais un gain encaissé. Vertex enregistre un prix de référence honnête (source
+ horodatage), calcule la performance depuis le suivi et contre SPY, MFE/MAE, et
conserve l'historique à l'arrêt. Lecture seule : aucun ordre. « Rendement
hypothétique depuis le suivi » est le seul vocabulaire autorisé pour un gain.
"""
from .models import (
    TRACKING_STATUSES, ENTITY_TYPES, REFERENCE_TYPES, new_tracking,
    ST_ACTIVE, ST_STOPPED, ST_EXPIRED, ST_DATA_REQUIRED,
)

__all__ = [
    'TRACKING_STATUSES', 'ENTITY_TYPES', 'REFERENCE_TYPES', 'new_tracking',
    'ST_ACTIVE', 'ST_STOPPED', 'ST_EXPIRED', 'ST_DATA_REQUIRED',
]
