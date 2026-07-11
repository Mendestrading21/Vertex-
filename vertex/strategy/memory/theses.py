"""vertex.strategy.memory.theses — thèses d'investissement (§33)."""
from .schemas import THESIS_FIELDS  # noqa: F401
from .store import MemoryStore


def add_thesis(store: MemoryStore, symbol: str, thesis: str, invalidation: str) -> dict:
    return store.add('vxStrategyTheses',
                     {'symbol': symbol.upper(), 'thesis': thesis,
                      'invalidation': invalidation}, status='OBSERVED')


def theses_for(store: MemoryStore, symbol: str) -> list:
    return [t for t in store.entries('vxStrategyTheses')
            if t.get('symbol') == symbol.upper() and t.get('status') != 'ARCHIVED']
