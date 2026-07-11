"""vertex.strategy.memory.feedback — retours sur les décisions (§33)."""
from .store import MemoryStore


def record_feedback(store: MemoryStore, subject: str, note: str, outcome: str = '') -> dict:
    return store.add('vxStrategyFeedback',
                     {'subject': subject, 'note': note, 'outcome': outcome},
                     status='OBSERVED')
