"""vertex.strategy.memory.versions — versions de la mémoire stratégique (§33)."""
from .store import MemoryStore


def snapshot_version(store: MemoryStore, label: str) -> dict:
    counts = {k: len(store.entries(k)) for k in
              ('vxStrategyRules', 'vxStrategyTheses', 'vxStrategyFeedback',
               'vxStrategyLearnings')}
    return store.add('vxStrategyVersions', {'label': label, 'counts': counts},
                     status='OBSERVED')
