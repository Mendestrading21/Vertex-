"""vertex.strategy.memory.learnings — leçons apprises et règles proposées (§33).

Une règle apprise naît PROPOSED ; elle ne devient jamais active sans
confirmation humaine (store.set_status(..., confirmed_by_human=True)).
"""
from .store import MemoryStore


def propose_rule(store: MemoryStore, title: str, body: str, source: str = 'engine') -> dict:
    return store.add('vxStrategyRules',
                     {'title': title, 'body': body, 'source': source},
                     status='PROPOSED')


def active_rules(store: MemoryStore) -> list:
    return store.active('vxStrategyRules')
